# === ПУТЬ К ФАЙЛУ: r7kit/workflow_utils.py ===
from __future__ import annotations

import importlib
import uuid
from datetime import timedelta
from typing import Any, Mapping, Union

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
    """
    Упрощённый конструктор RetryPolicy с типичным back-off.
    """
    return RetryPolicy(
        initial_interval=timedelta(seconds=initial_interval),
        backoff_coefficient=backoff,
        maximum_interval=(
            timedelta(seconds=maximum_interval) if maximum_interval else None
        ),
        maximum_attempts=maximum_attempts or 1,
    )


def _resolve_wf(wf: Union[str, type]) -> type:
    """
    Принимает либо сам класс воркфлоу, либо строку «pkg.module.Class».
    """
    if isinstance(wf, str):
        module_name, cls_name = wf.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, cls_name)
    return wf  # type: ignore[arg-type]

# --------------------------------------------------------------------
#                child-workflow helpers
# --------------------------------------------------------------------
async def start_child(
    wf: Union[str, type],
    *wf_args: Any,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_: str | None = None,
) -> workflow.ChildWorkflowHandle:
    """
    Fire-and-forget запуск дочернего воркфлоу.
    """
    wf_cls = _resolve_wf(wf)
    info = workflow.info()
    task_queue = queue or info.task_queue
    child_id = id_ or f"{wf_cls.__name__.lower()}-{info.run_id}"

    rp = (
        retry
        if isinstance(retry, RetryPolicy)
        else default_retry_policy(**(retry or {}))
    )
    return await workflow.start_child_workflow(
        wf_cls.__name__,
        args=list(wf_args),
        id=child_id,
        task_queue=task_queue,
        retry_policy=rp,
    )


async def call_child(
    wf: Union[str, type],
    *wf_args: Any,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_: str | None = None,
) -> Any:
    """
    Синхронный (await) вызов дочернего воркфлоу.
    """
    wf_cls = _resolve_wf(wf)
    info = workflow.info()
    task_queue = queue or info.task_queue
    call_id = id_ or f"{wf_cls.__name__.lower()}-{info.run_id}"

    rp = (
        retry
        if isinstance(retry, RetryPolicy)
        else default_retry_policy(**(retry or {}))
    )
    return await workflow.execute_child_workflow(
        wf_cls.__name__,
        args=list(wf_args),
        id=call_id,
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
    Создаёт task (если нужен) и запускает новый воркфлоу в Temporal Cloud / Cluster.

    * Если указан `payload`, библиотека сама вызовет activity **create_act**
      и подставит сгенерированный `task_id` как *первый* позиционный аргумент
      в новый workflow.
    * В SearchAttributes/Memo автоматически добавляется `taskSize`
      (байты Redis-hash) — удобно фильтровать в Temporal-Web.

    Возвращается `WorkflowHandle`.
    """
    wf_cls = _resolve_wf(wf)

    memo: dict[str, bytes] = {}
    args: list[Any] = list(wf_args)
    kwargs: dict[str, Any] = workflow_kwargs.copy() if workflow_kwargs else {}

    # ─── создаём Redis-task, если пришёл payload ────────────────────
    if payload is not None:
        task_id = await create_act(payload, status, cfg().stream_default)
        args.insert(0, task_id)

        redis_cli = await get_redis_client()
        size = await redis_cli.memory_usage(f"task:{task_id}") or 0
        memo["taskSize"] = str(size).encode()

    # ─── Temporal-client singleton ──────────────────────────────────
    try:
        client = await get_temporal_client()
    except Exception as exc:  # pragma: no cover
        raise TemporalNotConnected(f"Cannot connect Temporal: {exc}") from exc

    rp = (
        retry
        if isinstance(retry, RetryPolicy)
        else default_retry_policy(**(retry or {}))
    )
    wf_id = workflow_id or f"{wf_cls.__name__.lower()}-{uuid.uuid4()}"
    task_queue_name = queue or f"{wf_cls.__name__.lower()}-queue"

    return await client.start_workflow(
        wf_cls,
        *args,
        id=wf_id,
        task_queue=task_queue_name,
        retry_policy=rp,
        memo=memo or None,
        **kwargs,
    )
