# === ПУТЬ К ФАЙЛУ: r7kit/tasks.py ===
from __future__ import annotations

from datetime import timedelta
from typing import Any, Optional

from temporalio import workflow
from temporalio.common import RetryPolicy

from .activities import create_act, patch_act, get_act, delete_act
from .models import TaskModel
from .serializer import loads

_DEFAULT_TO = timedelta(seconds=30)

async def create_task(
    payload: dict[str, Any] | None = None,
    *,
    uuid: str | None = None,
    status: str = "new",
    stream: str | None = None,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> str:
    return await workflow.execute_activity(
        create_act,
        args=[payload, status, stream, uuid],
        start_to_close_timeout=timeout or _DEFAULT_TO,
        retry_policy=retry_policy,
    )

async def patch_task(
    task_id: str,
    patch: dict[str, Any],
    *,
    stream: str | None = None,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> None:
    await workflow.execute_activity(
        patch_act,
        args=[task_id, patch, stream],
        start_to_close_timeout=timeout or _DEFAULT_TO,
        retry_policy=retry_policy,
    )

async def get_task(
    task_id: str,
    *,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> TaskModel | None:
    raw = await workflow.execute_activity(
        get_act,
        args=[task_id],
        start_to_close_timeout=timeout or _DEFAULT_TO,
        retry_policy=retry_policy or RetryPolicy(maximum_attempts=1),
    )
    if not raw:
        return None
    parsed = {k: loads(v) for k, v in raw.items()}
    meta = {"uuid", "status", "created_at", "updated_at", "deleted_at", "ver"}
    business = {k: v for k, v in parsed.items() if k not in meta}
    return TaskModel.model_validate({
        "uuid":       parsed["uuid"],
        "status":     parsed["status"],
        "created_at": parsed["created_at"],
        "updated_at": parsed["updated_at"],
        "deleted_at": parsed.get("deleted_at"),
        "payload":    business or None,
    })

async def delete_task(
    task_id: str,
    *,
    stream: str | None = None,
    ttl: int | None = None,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> None:
    """
    Логическое удаление задачи.
    `ttl` — время в секундах до физического удаления (PEXPIRE).
    Если не указано, берётся из cfg().deleted_ttl.
    """
    await workflow.execute_activity(
        delete_act,
        args=[task_id, stream, ttl],
        start_to_close_timeout=timeout or _DEFAULT_TO,
        retry_policy=retry_policy,
    )

# mini-DSL для любых activity
from temporalio import workflow as _wf  # noqa: E402

async def act(
    name: str,
    *activity_args: Any,
    timeout: int | None = None,
    **activity_kwargs: Any,
) -> Any:
    to = timedelta(seconds=timeout) if timeout else _DEFAULT_TO
    return await _wf.execute_activity(
        name,
        *activity_args,
        **activity_kwargs,
        start_to_close_timeout=to,
    )
