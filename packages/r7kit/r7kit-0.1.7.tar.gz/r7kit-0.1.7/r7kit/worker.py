"""
Batteries-Included worker.

Запускает Temporal-worker, регистрируя:
 • стандартные r7kit-activities (create / get / patch / delete)
 • все workflow / activity, помеченные @taskflow или @activity,
   найденные в заданном **пакете или одиночном модуле**.
"""
from __future__ import annotations

import asyncio
import importlib
import logging
import pkgutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Iterable, List

from temporalio.worker import Worker

from .activities import create_act, delete_act, get_act, patch_act
from .config import configure
from .decorators import _ACTIVITY_ATTR, _TASKFLOW_ATTR
from .logging import setup as _setup_log
from .temporal_client import get_temporal_client

log = logging.getLogger("r7kit.worker")

# ------------------------------------------------------------------ #
#                         discovery helpers                          #
# ------------------------------------------------------------------ #
def _iter_modules(package: str) -> Iterable[ModuleType]:
    """
    Импортирует **сам** пакет/модуль и рекурсивно все его под-модули.

    Работает как для полноценного пакета (`pkg/__init__.py`),
    так и для одиночного файла-модуля `my_flow.py`.
    """
    root = importlib.import_module(package)
    yield root  # без него потеряем WF/ACT, объявленные в корне

    # если это не пакет – подпакетов нет
    search_locs = getattr(root.__spec__, "submodule_search_locations", None)
    if not search_locs:
        return

    for info in pkgutil.walk_packages(search_locs, prefix=f"{package}."):
        yield importlib.import_module(info.name)


def _discover(package: str) -> tuple[list[type], list]:
    """
    Возвращает два списка: (workflow-classes, activity-functions).
    Объекты определяются по «магическим» атрибутам,
    которые расставляют декораторы @taskflow / @activity.
    """
    workflows: List[type] = []
    activities: List = []

    for mod in _iter_modules(package):
        for obj in mod.__dict__.values():
            if hasattr(obj, _TASKFLOW_ATTR):
                workflows.append(obj)
            elif hasattr(obj, _ACTIVITY_ATTR):
                activities.append(obj)

    return workflows, activities

# ------------------------------------------------------------------ #
#                              Worker                                 #
# ------------------------------------------------------------------ #
class R7Worker:
    """
    Быстрый запуск worker-процесса.

    ```python
    from r7kit.worker import R7Worker

    if __name__ == "__main__":
        # «myflows» может быть пакетом ИЛИ одиночным .py-модулем
        R7Worker("myflows", queue="etl").start()
    ```
    """

    def __init__(
        self,
        package: str,
        *,
        queue: str = "default",
        redis_url: str | None = None,
        temporal_address: str | None = None,
    ):
        _setup_log()
        configure(redis_url=redis_url, temporal_address=temporal_address)

        self._package = package
        self._queue = queue

    # ---------------------- internal logic ------------------------ #
    async def _run_inner(self) -> None:
        user_wf, user_act = _discover(self._package)

        # + стандартные r7kit-activities
        activities = [*user_act, create_act, get_act, patch_act, delete_act]

        client = await get_temporal_client()
        worker = Worker(
            client,
            task_queue=self._queue,
            workflows=user_wf,
            activities=activities,
        )

        log.info(
            "R7Worker started (queue=%s, wf=%d, act=%d)",
            self._queue,
            len(user_wf),
            len(activities),
        )
        await worker.run()

    # ------------------------- public API ------------------------- #
    def start(self) -> None:
        """Блокирующий запуск (entry-point скрипта)."""
        try:
            asyncio.run(self._run_inner())
        except KeyboardInterrupt:
            log.info("worker stopped")
            sys.exit(0)

    async def run(self) -> None:
        """Асинхронный запуск — можно звать из уже работающего event-loop."""
        await self._run_inner()
