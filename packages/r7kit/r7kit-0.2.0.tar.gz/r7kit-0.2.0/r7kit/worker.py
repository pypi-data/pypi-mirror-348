# === ПУТЬ К ФАЙЛУ: r7kit/worker.py ===
"""
Batteries-Included worker.

• Поднимает Temporal-worker на указанной очереди.
• Регистрирует стандартные r7kit-activities и ВСЕ workflow / activity,
  найденные в заданном пакете (или одиночном модуле).

Workflow попадает в регистрацию, если выполнено хотя бы одно:
----------------------------------------------------------------
1. Класс имеет атрибут __temporal_workflow_defn__
   (добавляется декоратором @temporalio.workflow.defn).

2. На классе стоит наш собственный маркёр _TASKFLOW_ATTR
   (его задаёт декоратор @taskflow – даёт .start() и пр.).
"""
from __future__ import annotations

import asyncio
import importlib
import inspect
import logging
import pkgutil
import sys
from types import ModuleType
from typing import Iterable, List, Set

from temporalio.worker import Worker

from .activities import create_act, delete_act, get_act, patch_act
from .config import configure
from .decorators import _ACTIVITY_ATTR, _TASKFLOW_ATTR
from .logging import setup as _setup_log
from .temporal_client import get_temporal_client

log = logging.getLogger("r7kit.worker")

# --------------------------------------------------------------------- #
#                     helpers: рекурсивный import                       #
# --------------------------------------------------------------------- #
def _iter_modules(package: str) -> Iterable[ModuleType]:
    """
    Импортирует сам пакет/модуль **и** рекурсивно все подпакеты.

    Работает как для «настоящего» пакета с __init__.py,
    так и для одиночного файла-модуля.
    """
    root = importlib.import_module(package)
    yield root

    search = getattr(root.__spec__, "submodule_search_locations", None)
    if not search:                      # одиночный .py
        return

    for info in pkgutil.walk_packages(search, prefix=f"{package}."):
        yield importlib.import_module(info.name)


def _discover(package: str) -> tuple[list[type], list]:
    """
    Собирает workflow-классы и activity-функции из всех модулей,
    удаляя дубликаты (один и тот же объект может «всплывать»
    несколько раз из-за реэкспортов в __init__.py).
    """
    workflows: List[type] = []
    activities: List = []

    seen_wf: Set[int] = set()
    seen_act: Set[int] = set()

    for mod in _iter_modules(package):
        for obj in mod.__dict__.values():
            # ---- workflow -------------------------------------------------
            if inspect.isclass(obj) and (
                hasattr(obj, "__temporal_workflow_defn__")
                or hasattr(obj, _TASKFLOW_ATTR)
            ):
                if id(obj) not in seen_wf:
                    workflows.append(obj)
                    seen_wf.add(id(obj))

            # ---- activity -------------------------------------------------
            elif callable(obj) and hasattr(obj, _ACTIVITY_ATTR):
                if id(obj) not in seen_act:
                    activities.append(obj)
                    seen_act.add(id(obj))

    return workflows, activities

# --------------------------------------------------------------------- #
#                                Worker                                 #
# --------------------------------------------------------------------- #
class R7Worker:
    """
    Быстрый entry-point worker-процесса.

    Example
    -------
    ```python
    if __name__ == "__main__":
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

    # ------------------------ internal ------------------------------ #
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
            self._queue, len(user_wf), len(activities),
        )
        await worker.run()

    # ------------------------- public ------------------------------- #
    def start(self) -> None:
        """Блокирующий запуск (удобен для __main__)."""
        try:
            asyncio.run(self._run_inner())
        except KeyboardInterrupt:
            log.info("worker stopped")
            sys.exit(0)

    async def run(self) -> None:
        """Асинхронный запуск, если loop уже работает."""
        await self._run_inner()
