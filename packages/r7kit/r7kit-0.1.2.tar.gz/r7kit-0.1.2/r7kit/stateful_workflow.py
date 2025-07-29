# === ПУТЬ К ФАЙЛУ: r7kit/stateful_workflow.py ===
from __future__ import annotations
from typing import Any, Optional
from datetime import timedelta

from .base_task_workflow import BaseTaskWorkflow

class StatefulWorkflow(BaseTaskWorkflow):
    """
    Расширенный воркфлоу, сохраняющий state в payload между активациями.
    """

    state: dict[str, Any]

    async def load_state(self, timeout: Optional[timedelta] = None) -> None:
        await self.ensure_task_loaded()
        self.state = self.payload or {}

    async def save_state(self, timeout: Optional[timedelta] = None) -> None:
        await self.patch_task({"payload": self.state}, timeout=timeout)

    async def update_state(self, updates: dict[str, Any], timeout: Optional[timedelta] = None) -> None:
        await self.load_state(timeout=timeout)
        self.state.update(updates)
        await self.save_state(timeout=timeout)
