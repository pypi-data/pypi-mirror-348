"""
Batteries-included worker.

*   Настраивает r7kit (Redis / Temporal URL)
*   Регистрирует стандартные r7kit-activities (`create / get / patch / delete`)
*   Рекурсивно ищет ваши `@taskflow`-классы и `@activity`-функции
    в указанном пакете и добавляет их в Temporal-worker.
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
from .config import configure, cfg
from .decorators import _ACTIVITY_ATTR, _TASKFLOW_ATTR
from .logging import setup as _setup_log
from .temporal_client import get_temporal_client

log = logging.getLogger("r7kit.worker")


# --------------------------------------------------------------------------- #
#                              helpers                                         #
# --------------------------------------------------------------------------- #
def _iter_modules(package: str) -> Iterable[ModuleType]:
    """Импортирует **все** `.py` внутри `package` рекурсивно."""
    root = importlib.import_module(package)
    root_path = Path(root.__file__).parent
    for info in pkgutil.walk_packages([str(root_path)], prefix=f"{package}."):
        yield importlib.import_module(info.name)


def _discover(package: str):
    """Находит классы/функции, помеченные «магическими» атрибутами."""
    workflows: List[type] = []
    activities: List = []
    for mod in _iter_modules(package):
        for obj in mod.__dict__.values():
            if hasattr(obj, _TASKFLOW_ATTR):
                workflows.append(obj)
            elif hasattr(obj, _ACTIVITY_ATTR):
                activities.append(obj)
    return workflows, activities


# --------------------------------------------------------------------------- #
#                               public API                                    #
# --------------------------------------------------------------------------- #
class R7Worker:
    """
    Быстрый запуск worker-процесса::

        from r7kit.worker import R7Worker

        # блокирует поток (удобно в скриптах)
        R7Worker("my_app.workflows", queue="etl").start()

        # либо из уже работающего event-loop
        worker = R7Worker("my_app.workflows", queue="etl")
        await worker.run()
    """

    # ------------------------------------------------------------------ #
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

    # ------------------------------------------------------------------ #
    async def _run_inner(self) -> None:
        user_wf, user_act = _discover(self._package)

        # r7kit-core activities добавляем всегда
        activities = user_act + [create_act, get_act, patch_act, delete_act]

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

    # ------------------------------------------------------------------ #
    async def run(self) -> None:
        """
        Асинхронный запуск – ждать внутри **уже** работающего event-loop.

        ```python
        worker = R7Worker("pkg")
        await worker.run()
        ```
        """
        await self._run_inner()

    # ------------------------------------------------------------------ #
    def start(self) -> None:
        """
        Синхронный запуск: сам поднимает event-loop и блокирует поток.

        Нельзя вызывать из уже работающего цикла (`asyncio.run()` внутри
        другого `asyncio.run()` вызовет ошибку) – используйте `await run()`.
        """
        try:
            # если loop уже существует и активен – советуем пользоваться run()
            loop = asyncio.get_running_loop()
            if loop.is_running():  # внутри корутины
                raise RuntimeError(
                    "R7Worker.start() нельзя вызывать из работающего event-loop; "
                    "используйте `await worker.run()`"
                )
        except RuntimeError:
            # loop отсутствует – всё нормально
            pass

        try:
            asyncio.run(self._run_inner())
        except KeyboardInterrupt:
            log.info("worker stopped")
            sys.exit(0)
