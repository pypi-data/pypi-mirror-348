# === ПУТЬ К ФАЙЛУ: worker.py ===
"""
Batteries-Included worker: разворачивает Redis/Temporal,
регистрирует стандартные r7kit-activities и автоматически
находит ваши @taskflow / @activity классы в указанном пакете.
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

from .activities import (
    create_act,
    get_act,
    patch_act,
    delete_act,
)  # always в worker
from .config import configure, cfg
from .decorators import _TASKFLOW_ATTR, _ACTIVITY_ATTR
from .logging import setup as _setup_log
from .temporal_client import get_temporal_client

log = logging.getLogger("r7kit.worker")


def _iter_modules(package: str) -> Iterable[ModuleType]:
    """Рекурсивно импортирует все *.py в пакете."""
    mod = importlib.import_module(package)
    pkg_path = Path(mod.__file__).parent
    for info in pkgutil.walk_packages([str(pkg_path)], prefix=f"{package}."):
        yield importlib.import_module(info.name)


def _discover(package: str):
    """Обходит модули и собирает классы с «магическими» атрибутами."""
    workflows: List[type] = []
    activities: List = []
    for mod in _iter_modules(package):
        for obj in mod.__dict__.values():
            if hasattr(obj, _TASKFLOW_ATTR):
                workflows.append(obj)
            elif hasattr(obj, _ACTIVITY_ATTR):
                activities.append(obj)
    return workflows, activities


class R7Worker:
    """
    Пример использования::

        # worker.py
        from r7kit.worker import R7Worker

        if __name__ == "__main__":
            R7Worker("my_app.workflows", queue="etl").start()
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

    async def _run(self) -> None:
        workflows, activities = _discover(self._package)

        # std r7kit activities + пользовательские
        activities.extend([create_act, get_act, patch_act, delete_act])

        client = await get_temporal_client()
        worker = Worker(
            client,
            task_queue=self._queue,
            workflows=workflows,
            activities=activities,
        )
        log.info(
            "R7Worker started (queue=%s, wf=%d, act=%d)",
            self._queue,
            len(workflows),
            len(activities),
        )
        await worker.run()

    # public -------------
    def start(self) -> None:  # блокирует текущий поток
        try:
            asyncio.run(self._run())
        except KeyboardInterrupt:
            log.info("worker stopped")
            sys.exit(0)
