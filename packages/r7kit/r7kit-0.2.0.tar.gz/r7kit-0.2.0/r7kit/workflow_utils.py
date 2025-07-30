# === ПУТЬ К ФАЙЛУ: r7kit/workflow_utils.py ===
from __future__ import annotations

import importlib
import uuid as _uuid
from datetime import timedelta
from typing import Any, Mapping, Union, overload

from temporalio import workflow
from temporalio.common import RetryPolicy

from .activities import create_act
from .config import cfg
from .exceptions import TemporalNotConnected
from .redis_client import get_redis_client
from .temporal_client import get_temporal_client

# Синхронизация с атрибутом в декораторе
_TASKFLOW_QUEUE_ATTR = "__r7kit_queue__"

__all__ = [
    "default_retry_policy",
    "start_child",
    "call_child",
    "submit_workflow",
]

def default_retry_policy(
    *,
    initial_interval: float = 1.0,
    backoff: float = 2.0,
    maximum_interval: float | None = None,
    maximum_attempts: int | None = None,
) -> RetryPolicy:
    return RetryPolicy(
        initial_interval=timedelta(seconds=initial_interval),
        backoff_coefficient=backoff,
        maximum_interval=(
            timedelta(seconds=maximum_interval) if maximum_interval else None
        ),
        maximum_attempts=maximum_attempts or 1,
    )


def _try_import(path: str) -> type | None:
    if "." not in path:
        return None
    mod, cls = path.rsplit(".", 1)
    try:
        return getattr(importlib.import_module(mod), cls)
    except Exception:
        return None


@overload
async def _prepare(wf: str, queue: str | None) -> tuple[str, str, Union[type,str]]: ...
@overload
async def _prepare(wf: type, queue: str | None) -> tuple[type, str, str]: ...

async def _prepare(wf, queue):
    # Разрешаем строковый путь
    if isinstance(wf, str):
        cls = _try_import(wf)
        wf_ref = cls or wf
        wf_name = cls.__name__ if cls else wf
    else:
        wf_ref = wf
        wf_name = wf.__name__

    # Если класс помечен @taskflow, возьмём оттуда queue
    if isinstance(wf_ref, type) and hasattr(wf_ref, _TASKFLOW_QUEUE_ATTR):
        default_queue = getattr(wf_ref, _TASKFLOW_QUEUE_ATTR)
    else:
        default_queue = f"{wf_name.lower()}-queue"

    task_queue = queue or default_queue
    return wf_ref, wf_name, task_queue


async def start_child(
    wf: Union[str, type],
    *wf_args: Any,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_: str | None = None,
) -> workflow.ChildWorkflowHandle:
    wf_ref, wf_name, tq = await _prepare(wf, queue)
    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))
    return await workflow.start_child_workflow(
        wf_ref,
        id=id_ or f"{wf_name.lower()}-{workflow.info().run_id}",
        task_queue=tq,
        retry_policy=rp,
        args=list(wf_args) if wf_args else None,
    )


async def call_child(
    wf: Union[str, type],
    *wf_args: Any,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_: str | None = None,
):
    wf_ref, wf_name, tq = await _prepare(wf, queue)
    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))
    return await workflow.execute_child_workflow(
        wf_ref,
        id=id_ or f"{wf_name.lower()}-{workflow.info().run_id}",
        task_queue=tq,
        retry_policy=rp,
        args=list(wf_args) if wf_args else None,
    )


async def submit_workflow(
    wf: Union[str, type],
    *wf_args: Any,
    payload: dict[str, Any] | None = None,
    status: str = "new",
    task_uuid: str | None = None,
    workflow_id: str | None = None,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    workflow_kwargs: dict[str, Any] | None = None,
):
    # Разрешаем путь и default-queue из класса
    if isinstance(wf, str):
        cls = _try_import(wf)
        wf_ref = cls or wf
        wf_name = cls.__name__ if cls else wf
    else:
        wf_ref = wf
        wf_name = wf.__name__

    if isinstance(wf_ref, type) and hasattr(wf_ref, _TASKFLOW_QUEUE_ATTR):
        default_queue = getattr(wf_ref, _TASKFLOW_QUEUE_ATTR)
    else:
        default_queue = f"{wf_name.lower()}-queue"

    args = list(wf_args)
    memo: dict[str, bytes] = {}

    if payload is not None:
        tid = task_uuid or str(_uuid.uuid4())
        await create_act(payload, status, cfg().stream_default, tid)
        args.insert(0, tid)
        size = await (await get_redis_client()).memory_usage(f"task:{tid}") or 0
        memo["taskSize"] = str(size).encode()

    try:
        client = await get_temporal_client()
    except Exception as exc:
        raise TemporalNotConnected(f"Cannot connect Temporal: {exc}") from exc

    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))
    wf_id = workflow_id or (args[0] if payload is not None else f"{wf_name.lower()}-{_uuid.uuid4()}")
    tq = queue or default_queue

    kw = (workflow_kwargs or {}).copy()
    kw.pop("queue", None)

    return await client.start_workflow(
        wf_ref,
        id=wf_id,
        task_queue=tq,
        retry_policy=rp,
        memo=memo or None,
        args=args if args else None,
        **kw,
    )
