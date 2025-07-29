# === ПУТЬ К ФАЙЛУ: r7kit/base_task_workflow.py ===
from __future__ import annotations
from typing import Any, Optional
from datetime import timedelta

from temporalio import workflow

from .base_workflow import BaseWorkflow
from .models import TaskModel

DEFAULT_TIMEOUT = timedelta(seconds=30)

class BaseTaskWorkflow(BaseWorkflow):
    """
    Базовый класс для воркфлоу, автоматически подгружающий задачу и её payload.
    Дочерние классы переопределяют handle().
    """

    task: TaskModel
    payload: dict[str, Any] | None

    async def load_task(self, timeout: Optional[timedelta] = None) -> None:
        task = await self.get_task(timeout=timeout or DEFAULT_TIMEOUT)
        if not task:
            raise ValueError(f"Task {self.task_id} не найдена")
        self.task = task
        self.payload = task.payload or {}

    async def ensure_task_loaded(self) -> None:
        if not hasattr(self, "task"):
            await self.load_task()
