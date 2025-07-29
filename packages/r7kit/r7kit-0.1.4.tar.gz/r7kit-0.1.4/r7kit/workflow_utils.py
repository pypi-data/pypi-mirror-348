# === ПУТЬ К ФАЙЛУ: workflow_utils.py ===
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

__all__ = [
    "default_retry_policy",
    "start_child",
    "call_child",
    "submit_workflow",
]

# --------------------------------------------------------------------
#                      helpers
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
    """Пытаемся импортировать `pkg.mod.Class`; при неудаче → None."""
    if "." not in wf_path:
        return None
    mod, cls = wf_path.rsplit(".", 1)
    try:
        return getattr(importlib.import_module(mod), cls)
    except Exception:  # noqa: BLE001
        return None


# --------------------------------------------------------------------
#          внутренний helper: нормализуем ссылку/очередь
# --------------------------------------------------------------------
@overload
async def _prepare(wf: str, queue: str | None) -> tuple[str, str, str]: ...
@overload
async def _prepare(wf: type, queue: str | None) -> tuple[type, str, str]: ...


async def _prepare(  # type: ignore[override]
    wf: Union[str, type],
    queue: str | None,
):
    """
    → (wf_ref, wf_name, task_queue)

    * `wf_ref` — либо сам класс, либо строка-имя.
    * Если `queue` не задан — автоматически `<wf_name>.lower()-queue`.
    """
    if isinstance(wf, str):
        cls      = _try_import(wf)
        wf_name  = cls.__name__ if cls else wf
        wf_ref   = cls or wf
    else:
        wf_ref   = wf
        wf_name  = wf.__name__

    task_queue = queue or f"{wf_name.lower()}-queue"
    return wf_ref, wf_name, task_queue


# --------------------------------------------------------------------
#                     child-workflow wrappers
# --------------------------------------------------------------------
async def start_child(
    wf: Union[str, type],
    *wf_args: Any,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_:   str | None = None,
) -> workflow.ChildWorkflowHandle:
    wf_ref, wf_name, tq = await _prepare(wf, queue)
    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))

    return await workflow.start_child_workflow(
        wf_ref,
        args=list(wf_args),
        id=id_ or f"{wf_name.lower()}-{workflow.info().run_id}",
        task_queue=tq,
        retry_policy=rp,
    )


async def call_child(
    wf: Union[str, type],
    *wf_args: Any,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_:   str | None = None,
):
    wf_ref, wf_name, tq = await _prepare(wf, queue)
    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))

    return await workflow.execute_child_workflow(
        wf_ref,
        args=list(wf_args),
        id=id_ or f"{wf_name.lower()}-{workflow.info().run_id}",
        task_queue=tq,
        retry_policy=rp,
    )

# --------------------------------------------------------------------
#                       top-level submit
# --------------------------------------------------------------------
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
    """
    • Если указан `payload` — будет создана Redis-задача
      (UUID = `task_uuid` или auto-UUID) и передана первым
      аргументом воркфлоу.

    • `wf` — класс, «pkg.mod.Class» **или** уже зарегистрированное имя.
    """
    # ——— normalise workflow reference ——————————————
    if isinstance(wf, str):
        cls      = _try_import(wf)
        wf_ref   = cls or wf
        wf_name  = cls.__name__ if cls else wf
    else:
        wf_ref   = wf
        wf_name  = wf.__name__

    # ——— args / memo ————————————————————————————————
    args   : list[Any]      = list(wf_args)
    memo   : dict[str, bytes] = {}
    kwargs : dict[str, Any]   = workflow_kwargs.copy() if workflow_kwargs else {}

    if payload is not None:
        task_id = task_uuid or str(_uuid.uuid4())
        await create_act(payload, status, cfg().stream_default, task_id)
        args.insert(0, task_id)

        size = await (await get_redis_client()).memory_usage(f"task:{task_id}") or 0
        memo["taskSize"] = str(size).encode()

    # ——— client ————————————————————————————————
    try:
        client = await get_temporal_client()
    except Exception as exc:  # pragma: no cover
        raise TemporalNotConnected(f"Cannot connect Temporal: {exc}") from exc

    rp = retry if isinstance(retry, RetryPolicy) else default_retry_policy(**(retry or {}))
    wf_id  = workflow_id or (args[0] if payload is not None else f"{wf_name.lower()}-{_uuid.uuid4()}")
    tq     = queue or f"{wf_name.lower()}-queue"

    return await client.start_workflow(
        wf_ref,
        *args,
        id=wf_id,
        task_queue=tq,
        retry_policy=rp,
        memo=memo or None,
        **kwargs,
    )
