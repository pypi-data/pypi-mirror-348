# === ПУТЬ К ФАЙЛУ: r7kit/decorators.py ===
from __future__ import annotations
import inspect
import logging
import sys
import types
import uuid as _uuid
from typing import Any, Callable, TypeVar

from temporalio import activity as _t_activity
from temporalio import workflow as _t_workflow

from .workflow_utils import submit_workflow

__all__ = ["taskflow", "activity"]

log = logging.getLogger("r7kit.decorators")

_TASKFLOW_ATTR = "__r7kit_taskflow__"
_ACTIVITY_ATTR = "__r7kit_activity__"
# тут храним default-queue в классе
_TASKFLOW_QUEUE_ATTR = "__r7kit_queue__"
T = TypeVar("T")


def _create_run_method(cls) -> Callable:
    async def _run(self, task_id, *args, **kwargs):  # noqa: ANN001
        return await self._run_impl(task_id, *args, **kwargs)

    mod = sys.modules[cls.__module__]
    fn = types.FunctionType(
        _run.__code__,
        mod.__dict__,
        name="run",
        argdefs=_run.__defaults__,
        closure=_run.__closure__,
    )
    fn.__module__ = cls.__module__
    fn.__qualname__ = f"{cls.__qualname__}.run"
    fn = _t_workflow.run(fn)
    return fn


def _inject_run(cls) -> None:
    if "run" not in cls.__dict__:
        cls.run = _create_run_method(cls)  # type: ignore[attr-defined]


def _inject_start(cls, default_queue: str | None) -> None:
    async def _start(
        _cls,
        *args: Any,
        payload: dict | None = None,
        uuid: str | None = None,
        **kwargs: Any,
    ):
        runtime_queue = kwargs.pop("queue", None)
        task_uuid = uuid or (str(_uuid.uuid4()) if payload else None)
        # передаём реальный queue в submit
        q = runtime_queue or getattr(cls, _TASKFLOW_QUEUE_ATTR, default_queue)
        handle = await submit_workflow(
            _cls,
            *args,
            payload=payload,
            task_uuid=task_uuid,
            queue=q,
            workflow_kwargs=kwargs,
        )
        return handle, task_uuid

    cls.start = classmethod(_start)  # type: ignore[attr-defined]


def taskflow(*, queue: str | None = None):
    """
    Декоратор @taskflow(queue="…"):
      • кладёт default-queue в класс
      • генерирует .run() и .start()
      • сам делает @workflow.defn
    """
    def _decorator(cls: T) -> T:
        if not inspect.isclass(cls):
            raise TypeError("@taskflow применяется только к классу")
        # помечаем класс и сохраняем queue
        setattr(cls, _TASKFLOW_ATTR, True)
        setattr(cls, _TASKFLOW_QUEUE_ATTR, queue)
        _inject_run(cls)
        _inject_start(cls, queue)
        if not hasattr(cls, "__temporal_workflow_defn__"):
            cls = _t_workflow.defn()(cls)  # type: ignore[assignment]
        log.debug("registered taskflow %s (queue=%s)", cls.__qualname__, queue)
        return cls
    return _decorator


def activity(
    fn: Callable[..., Any] | None = None,
    *,
    name: str | None = None,
):
    """Синоним @temporalio.activity.defn с авторегистрацией."""
    def _wrap(f: Callable[..., Any]):
        decorated = _t_activity.defn(name=name)(f)
        setattr(decorated, _ACTIVITY_ATTR, True)
        log.debug("registered activity %s", decorated.__qualname__)
        return decorated
    return _wrap(fn) if fn else _wrap
