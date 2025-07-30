# === ПУТЬ К ФАЙЛУ: r7kit/base_task_workflow.py ===
from __future__ import annotations
from datetime import timedelta
from typing import Any, Optional

from temporalio import workflow

from .base_workflow import BaseWorkflow
from .context import payload_state
from .models import TaskModel

_DEFAULT_TO = timedelta(seconds=30)


class BaseTaskWorkflow(BaseWorkflow):
    """
    После `await self.load_task()` доступны:
      • self.task     – TaskModel
      • self.payload  – dict | None

    Кроме того, есть:

        async with self.state(): ...
    """

    task: TaskModel
    payload: dict[str, Any] | None

    # ----------------------------------------------------------------
    async def load_task(self, timeout: Optional[timedelta] = None) -> None:
        """Повторяет несколько попыток: create_act мог ещё не отработать."""
        to = timeout or _DEFAULT_TO
        wait = 0.25
        for _ in range(4):
            t = await self.get_task(timeout=to)
            if t:
                self.task = t
                self.payload = t.payload or {}
                return
            await workflow.sleep(wait)
            wait *= 2
        raise ValueError(f"Task {self.task_id} not found in Redis")

    async def ensure_task_loaded(self) -> None:
        if not hasattr(self, "task"):
            await self.load_task()

    # ----------------------------------------------------------------
    def state(self, *, timeout: Optional[int] = None):
        """
        Асинхронный контекст-менеджер::

            async with self.state():
                self.payload["x"] = 1
        """
        return payload_state(self, timeout=timeout)
