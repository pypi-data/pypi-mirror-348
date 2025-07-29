"""
Batteries-Included worker.

• Поднимает Temporal-worker на указанной очереди.
• Регистрирует стандартные r7kit-activities и ВСЕ workflow /
  activity, найденные в заданном пакете (или одиночном модуле).

Workflow обнаруживаются по одному из признаков
------------------------------------------------
1. Есть «магический» атрибут __temporal_workflow_defn__
   (его добавляет @temporalio.workflow.defn).
2. Присутствует наш собственный маркёр _TASKFLOW_ATTR
   (ставится декоратором @taskflow).
"""
from __future__ import annotations

import asyncio
import importlib
import inspect
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
#                       helpers (module walk)                        #
# ------------------------------------------------------------------ #
def _iter_modules(package: str) -> Iterable[ModuleType]:
    """Импортирует сам пакет/модуль и рекурсивно все подпакеты."""
    root = importlib.import_module(package)
    yield root

    sub_locs = getattr(root.__spec__, "submodule_search_locations", None)
    if not sub_locs:                     # одиночный .py-модуль
        return

    for info in pkgutil.walk_packages(sub_locs, prefix=f"{package}."):
        yield importlib.import_module(info.name)


def _discover(package: str) -> tuple[list[type], list]:
    """
    Возвращает кортеж (workflow_classes, activity_functions).
    Workflow-класс попадает в список, если выполняется хотя бы одно:

    • hasattr(obj, "__temporal_workflow_defn__")          → обычный @workflow.defn
    • hasattr(obj, _TASKFLOW_ATTR)                        → наш @taskflow
    """
    workflows: List[type] = []
    activities: List = []

    for mod in _iter_modules(package):
        for obj in mod.__dict__.values():
            # --- workflow --------------------------------------------------
            if inspect.isclass(obj) and (
                hasattr(obj, "__temporal_workflow_defn__") or
                hasattr(obj, _TASKFLOW_ATTR)
            ):
                workflows.append(obj)
            # --- activity --------------------------------------------------
            elif callable(obj) and hasattr(obj, _ACTIVITY_ATTR):
                activities.append(obj)

    return workflows, activities

# ------------------------------------------------------------------ #
#                            R7Worker                                #
# ------------------------------------------------------------------ #
class R7Worker:
    """
    Быстрый запуск worker-процесса.

    ```python
    from r7kit.worker import R7Worker

    if __name__ == "__main__":
        # «myflows» может быть пакетом ИЛИ одиночным .py-файлом
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

    # ------------------------ internals ---------------------------- #
    async def _run_inner(self) -> None:
        user_wf, user_act = _discover(self._package)

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

    # ------------------------- public ------------------------------ #
    def start(self) -> None:
        """Блокирует текущий поток (удобно для entry-point скрипта)."""
        try:
            asyncio.run(self._run_inner())
        except KeyboardInterrupt:
            log.info("worker stopped")
            sys.exit(0)

    async def run(self) -> None:
        """Асинхронный запуск из уже работающего event-loop."""
        await self._run_inner()
