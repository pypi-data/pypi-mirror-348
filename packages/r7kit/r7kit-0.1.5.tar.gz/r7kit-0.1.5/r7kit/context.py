"""
Асинхронный контекст-менеджер, упрощающий работу с self.payload
(редактируем словарь – он автоматически сохраняется в Redis).
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, Optional

from .base_task_workflow import BaseTaskWorkflow


@asynccontextmanager
async def payload_state(
    wf: BaseTaskWorkflow,
    *,
    timeout: Optional[int] = None,
) -> AsyncIterator[Dict[str, Any]]:
    """
    async def handle(self):
        async with payload_state(self) as p:
            p["foo"] = 1
            p.setdefault("bar", []).append(2)
    """
    await wf.ensure_task_loaded()

    # если payload ещё None – превращаем в пустой dict, чтобы можно было писать
    if wf.payload is None:
        wf.payload = {}

    try:
        yield wf.payload       # <- тот же объект, что и внутри wf
    finally:
        # even if ничего не изменилось – patch_task «дёшево»
        await wf.patch_task({"payload": wf.payload}, timeout=timeout)
