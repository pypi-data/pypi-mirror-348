# === ПУТЬ К ФАЙЛУ: decorators.py ===
"""
@taskflow  – помечает класс Workflow   (+ .start()/ .run_async())  
@activity  – помечает функцию Activity (для auto-discovery)
"""

from __future__ import annotations

import asyncio
import functools
import inspect
import logging
from typing import Any, Callable, TypeVar

from temporalio import activity as _t_activity
from temporalio import workflow as _t_workflow

from .workflow_utils import submit_workflow

__all__ = ["taskflow", "activity"]

log = logging.getLogger("r7kit.decorators")

_TASKFLOW_ATTR = "__r7kit_taskflow__"
_ACTIVITY_ATTR = "__r7kit_activity__"

T = TypeVar("T")


# ------------------------------------------------------------------- #
#                              taskflow                                #
# ------------------------------------------------------------------- #
def _inject_start(cls, queue: str | None):
    """Добавляет `@classmethod start()` в workflow‐класс."""

    async def _start(
        _cls,
        *args: Any,
        payload: dict | None = None,
        uuid: str | None = None,
        **kwargs: Any,
    ):
        """
        Запускает workflow и (если есть payload) создаёт Redis-задачу.

        Возвращает tuple (WorkflowHandle, uuid|None).
        """
        handle = await submit_workflow(
            _cls,
            *args,
            payload=payload,
            task_uuid=uuid,
            queue=queue,  # один и тот же queue что и у worker
            workflow_kwargs=kwargs,
        )
        uid = uuid or (handle.args[0] if payload is not None else None)
        return handle, uid

    cls.start = classmethod(_start)  # type: ignore[attr-defined]


def taskflow(*, queue: str | None = None):  # decorator-factory
    def _decorator(cls: T) -> T:
        if not inspect.isclass(cls):
            raise TypeError("@taskflow применяется к классу Workflow")

        setattr(cls, _TASKFLOW_ATTR, True)
        _inject_start(cls, queue)

        # если автор забыл @workflow.defn – сделаем за него
        if not hasattr(cls, "__temporal_workflow_defn__"):
            cls = _t_workflow.defn()(cls)  # type: ignore[assignment]

        log.debug("registered taskflow %s", cls.__qualname__)
        return cls

    return _decorator


# ------------------------------------------------------------------- #
#                              activity                                #
# ------------------------------------------------------------------- #
def activity(fn: Callable[..., Any] | None = None, *, name: str | None = None):
    """
    Сахар над `@temporalio.activity.defn`: помечает функцию и
    удерживает имя (если нужно, иначе fn.__name__).
    """

    def _wrap(f: Callable[..., Any]):
        decorated = _t_activity.defn(name=name)(f)  # temporal-декоратор
        setattr(decorated, _ACTIVITY_ATTR, True)
        log.debug("registered activity %s", decorated.__qualname__)
        return decorated

    return _wrap(fn) if fn else _wrap
