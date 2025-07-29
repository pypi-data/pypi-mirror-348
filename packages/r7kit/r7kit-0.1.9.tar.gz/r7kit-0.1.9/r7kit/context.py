# === ПУТЬ К ФАЙЛУ: context.py ===
"""
Асинхронный контекст-менеджер для безопасной работы с self.payload.

Пример
------
async def handle(self):
    async with self.state():        # ← alias в BaseTaskWorkflow
        self.payload["foo"] = 42    # patch сохранится автоматически
"""
from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Optional

if TYPE_CHECKING:                  # импорт только для проверок типов
    from .base_task_workflow import BaseTaskWorkflow


@contextlib.asynccontextmanager
async def payload_state(
    wf: "BaseTaskWorkflow",         # строковая аннотация – не вызывает импорт
    *,
    timeout: Optional[int] = None,
) -> AsyncIterator[Dict[str, Any]]:
    """
    Контекст-менеджер, возвращающий текущий payload (dict).
    При выходе автоматически делает `patch_task({'payload': …})`.
    """
    # гарантируем, что задача и payload загружены
    await wf.ensure_task_loaded()

    try:
        yield wf.payload or {}      # mypy знает, что это Dict[str, Any]
    finally:
        await wf.patch_task({"payload": wf.payload}, timeout=timeout)
