from __future__ import annotations

import importlib
import uuid
from datetime import timedelta
from typing import Any, Mapping, Union, overload

from temporalio import workflow
from temporalio.common import RetryPolicy

from .activities import create_act
from .config import cfg
from .exceptions import TemporalNotConnected
from .redis_client import get_redis_client
from .temporal_client import get_temporal_client

__all__ = [
    "default_retry_policy",
    "start_child",
    "call_child",
    "submit_workflow",
]

# --------------------------------------------------------------------
#                     helpers
# --------------------------------------------------------------------
def default_retry_policy(
    *,
    initial_interval: int = 1,
    backoff: float = 2.0,
    maximum_interval: int | None = None,
    maximum_attempts: int | None = None,
) -> RetryPolicy:
    """Упрощённый конструктор RetryPolicy."""
    return RetryPolicy(
        initial_interval=timedelta(seconds=initial_interval),
        backoff_coefficient=backoff,
        maximum_interval=(
            timedelta(seconds=maximum_interval) if maximum_interval else None
        ),
        maximum_attempts=maximum_attempts or 1,
    )


def _try_import(wf_path: str) -> type | None:
    """Пробует импортировать `pkg.mod.Class`, иначе возвращает None."""
    if "." not in wf_path:
        return None
    module_name, cls_name = wf_path.rsplit(".", 1)
    try:
        module = importlib.import_module(module_name)
        return getattr(module, cls_name)
    except Exception:  # noqa: BLE001
        return None


# --------------------------------------------------------------------
#               child-workflow helpers (имя или класс)
# --------------------------------------------------------------------
@overload
async def _prepare(
    wf: str, id_prefix: str, queue: str | None
) -> tuple[str, str, str]: ...
@overload
async def _prepare(
    wf: type, id_prefix: str, queue: str | None
) -> tuple[type, str, str]: ...


async def _prepare(  # type: ignore[override]
    wf: Union[str, type],
    id_prefix: str,
    queue: str | None,
):
    """
    Возвращает tuple: (wf_ref, wf_name_for_id, task_queue)

    wf_ref  – либо сам класс, либо строка-имя воркфлоу
    """
    info = workflow.info()
    task_queue = queue or info.task_queue

    if isinstance(wf, str):
        cls = _try_import(wf)
        if cls is not None:
            return cls, cls.__name__, task_queue
        # обычное «сырое» имя
        return wf, wf, task_queue

    # wf – уже класс
    return wf, wf.__name__, task_queue


async def start_child(
    wf: Union[str, type],
    *wf_args: Any,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_: str | None = None,
) -> workflow.ChildWorkflowHandle:
    wf_ref, wf_name, task_queue = await _prepare(wf, "start", queue)
    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))

    return await workflow.start_child_workflow(
        wf_ref,
        args=list(wf_args),
        id=id_ or f"{wf_name.lower()}-{workflow.info().run_id}",
        task_queue=task_queue,
        retry_policy=rp,
    )


async def call_child(
    wf: Union[str, type],
    *wf_args: Any,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_: str | None = None,
):
    wf_ref, wf_name, task_queue = await _prepare(wf, "call", queue)
    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))

    return await workflow.execute_child_workflow(
        wf_ref,
        args=list(wf_args),
        id=id_ or f"{wf_name.lower()}-{workflow.info().run_id}",
        task_queue=task_queue,
        retry_policy=rp,
    )

# --------------------------------------------------------------------
#                   public: submit_workflow
# --------------------------------------------------------------------
async def submit_workflow(
    wf: Union[str, type],
    *wf_args: Any,
    payload: dict[str, Any] | None = None,
    status: str = "new",
    workflow_id: str | None = None,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    workflow_kwargs: dict[str, Any] | None = None,
):
    """
    Создаёт task (если нужен) и стартует новый воркфлоу в Temporal.

    wf — может быть классом, путём "pkg.mod.Class" **или просто именем**
          уже зарегистрированного воркфлоу (без импорта).
    """
    # ─── resolve wf_ref / wf_name ───────────────────────────────────
    if isinstance(wf, str):
        wf_cls = _try_import(wf)
        wf_ref = wf_cls or wf           # если импорт не вышел — строка-имя
        wf_name = wf_cls.__name__ if wf_cls else wf
    else:
        wf_ref = wf
        wf_name = wf.__name__

    # ─── args / memo ────────────────────────────────────────────────
    memo: dict[str, bytes] = {}
    args: list[Any] = list(wf_args)
    kwargs: dict[str, Any] = workflow_kwargs.copy() if workflow_kwargs else {}

    if payload is not None:
        task_id = await create_act(payload, status, cfg().stream_default)
        args.insert(0, task_id)

        redis_cli = await get_redis_client()
        size = await redis_cli.memory_usage(f"task:{task_id}") or 0
        memo["taskSize"] = str(size).encode()

    # ─── Temporal client ────────────────────────────────────────────
    try:
        client = await get_temporal_client()
    except Exception as exc:  # pragma: no cover
        raise TemporalNotConnected(f"Cannot connect Temporal: {exc}") from exc

    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))
    wf_id = workflow_id or f"{wf_name.lower()}-{uuid.uuid4()}"
    task_queue_name = queue or f"{wf_name.lower()}-queue"

    return await client.start_workflow(
        wf_ref,
        *args,
        id=wf_id,
        task_queue=task_queue_name,
        retry_policy=rp,
        memo=memo or None,
        **kwargs,
    )
