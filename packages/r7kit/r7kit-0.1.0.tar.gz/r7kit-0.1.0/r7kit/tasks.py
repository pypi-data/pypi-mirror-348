# === ПУТЬ К ФАЙЛУ: r7kit/tasks.py ===
from __future__ import annotations
from datetime import timedelta
from typing import Any, Optional

from temporalio import workflow
from temporalio.common import RetryPolicy

from .activities import create_act, patch_act, get_act, delete_act
from .models import TaskModel
from .serializer import loads

DEFAULT_ACTIVITY_TIMEOUT = timedelta(seconds=30)

async def create_task(
    payload: dict[str, Any] | None = None,
    *,
    status: str = "new",
    stream: str | None = None,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> str:
    return await workflow.execute_activity(
        create_act,
        args=[payload, status, stream],
        start_to_close_timeout=timeout or DEFAULT_ACTIVITY_TIMEOUT,
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
        start_to_close_timeout=timeout or DEFAULT_ACTIVITY_TIMEOUT,
        retry_policy=retry_policy,
    )

async def get_task(
    task_id: str,
    *,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> TaskModel | None:
    """
    Получить задачу. Активность get_act выполнится **один раз**,
    любые TaskNotFoundError пробросятся без повторов.
    """
    raw = await workflow.execute_activity(
        get_act,
        args=[task_id],
        start_to_close_timeout=timeout or DEFAULT_ACTIVITY_TIMEOUT,
        retry_policy=RetryPolicy(maximum_attempts=1),
    )
    if raw is None:
        return None
    parsed = {k: loads(v) for k, v in raw.items()}

    meta = {"uuid", "status", "created_at", "updated_at", "deleted_at"}
    payload = {k: v for k, v in parsed.items() if k not in meta}
    model_data = {
        "uuid": parsed["uuid"],
        "status": parsed["status"],
        "created_at": parsed["created_at"],
        "updated_at": parsed["updated_at"],
        "deleted_at": parsed.get("deleted_at"),
        "payload": payload or None,
    }
    return TaskModel.model_validate(model_data)  # type: ignore

async def delete_task(
    task_id: str,
    *,
    stream: str | None = None,
    timeout: Optional[timedelta] = None,
    retry_policy: RetryPolicy | None = None,
) -> None:
    await workflow.execute_activity(
        delete_act,
        args=[task_id, stream],
        start_to_close_timeout=timeout or DEFAULT_ACTIVITY_TIMEOUT,
        retry_policy=retry_policy,
    )
