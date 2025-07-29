# === ПУТЬ К ФАЙЛУ: r7kit/activities.py ===
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Iterable

from redis.exceptions import ResponseError
from temporalio import activity

from .config import cfg
from .exceptions import TaskAlreadyExistsError, TaskNotFoundError
from .redis_client import get_redis_client
from .serializer import dumps

logger = logging.getLogger(__name__)

_TASK_HASH = "task:"
_DEFAULT_TTL = 7 * 24 * 3600          # 7 дней
_DELETED_TTL = 24 * 3600              # ключ хранится сутки после delete
_STREAM_FIELD_LIMIT = 50              # макс-число полей, пишущихся в XADD

# ─────────────────────────  Lua-скрипты  ────────────────────────────
_LUA_CREATE = r"""
if redis.call('EXISTS', KEYS[1]) == 1 then
  return redis.error_reply('EEXISTS')
end
redis.call('HSET', KEYS[1], unpack(ARGV, 4, 3 + ARGV[3]*2))
redis.call('HSET', KEYS[1], 'ver', 1)
redis.call('PEXPIRE', KEYS[1], ARGV[1] * 1000)
redis.call('XADD', KEYS[2], '*', 'event', ARGV[2], unpack(ARGV, 4, 3 + ARGV[4]*2))
return 'OK'
"""

_LUA_PATCH = r"""
local cur = redis.call('HGET', KEYS[1], 'ver')
if not cur then return redis.error_reply('ENOENT') end
if cur ~= ARGV[1] then return redis.error_reply('ECONFLICT') end
redis.call('HSET', KEYS[1], unpack(ARGV, 4, 3 + ARGV[3]*2))
redis.call('HINCRBY', KEYS[1], 'ver', 1)
redis.call('PEXPIRE', KEYS[1], ARGV[2] * 1000)
redis.call('XADD', KEYS[2], '*', 'event', ARGV[4], unpack(ARGV, 4, 3 + ARGV[4]*2))
return 'OK'
"""

_LUA_DELETE = r"""
if redis.call('HEXISTS', KEYS[1], 'deleted_at') == 1 then
  return redis.error_reply('EDELETED')
end
redis.call('HSET', KEYS[1], 'deleted_at', ARGV[1])
redis.call('HINCRBY', KEYS[1], 'ver', 1)
redis.call('PEXPIRE', KEYS[1], ARGV[2] * 1000)
redis.call('XADD', KEYS[2], '*', 'event', 'deleted', 'deleted_at', ARGV[1])
return 'OK'
"""

# ─────────────────────────  helpers  ────────────────────────────────
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _flatten(d: dict[str, str]) -> list[str]:
    """dict → flat list, ключи сортируются для детерминированного порядка."""
    out: list[str] = []
    for k in sorted(d.keys()):
        out.extend((k, d[k]))
    return out


async def _lua(
    script: str,
    keys: Iterable[str],
    args: Iterable[str | int],
):
    keys_list = list(keys)
    cli = await get_redis_client()
    try:
        return await cli.eval(script, len(keys_list), *[*keys_list, *args])
    except ResponseError as exc:
        raise exc


# ─────────────────────────  Activities  ─────────────────────────────
@activity.defn(name="r7kit.create")
async def create_act(
    payload: dict[str, Any] | None,
    status: str,
    stream_name: str | None = None,
) -> str:
    stream = stream_name or cfg().stream_default
    task_id = str(uuid.uuid4())
    key = f"{_TASK_HASH}{task_id}"

    record: dict[str, str] = {
        "uuid": task_id,
        "status": status,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    if payload:
        record.update({k: dumps(v) for k, v in payload.items()})

    h_args = _flatten(record)
    x_args = h_args[: _STREAM_FIELD_LIMIT * 2]

    try:
        await _lua(
            _LUA_CREATE,
            [key, stream],
            [
                _DEFAULT_TTL,          # ARGV1
                "created",             # ARGV2
                len(h_args) // 2,      # ARGV3 nh
                len(x_args) // 2,      # ARGV4 nx
                *h_args,
                *x_args,
            ],
        )
    except ResponseError as exc:
        if "EEXISTS" in str(exc):
            raise TaskAlreadyExistsError(task_id) from None
        raise
    return task_id


@activity.defn(name="r7kit.patch")
async def patch_act(
    task_id: str,
    patch: dict[str, Any],
    stream_name: str | None = None,
) -> None:
    stream = stream_name or cfg().stream_default
    key = f"{_TASK_HASH}{task_id}"

    cli = await get_redis_client()
    current_ver = await cli.hget(key, "ver")
    if current_ver is None:
        raise TaskNotFoundError(task_id)

    record = {k: dumps(v) for k, v in patch.items()}
    record["updated_at"] = _now_iso()

    h_args = _flatten(record)
    x_args = h_args[: _STREAM_FIELD_LIMIT * 2]

    try:
        await _lua(
            _LUA_PATCH,
            [key, stream],
            [
                current_ver,           # ARGV1 expected_ver
                _DEFAULT_TTL,          # ARGV2 renew TTL
                len(h_args) // 2,      # ARGV3 nh
                len(x_args) // 2,      # ARGV4 nx
                *h_args,
                *x_args,
            ],
        )
    except ResponseError as exc:
        msg = str(exc)
        if "ENOENT" in msg or "EDELETED" in msg:
            raise TaskNotFoundError(task_id) from None
        if "ECONFLICT" in msg:
            raise RuntimeError(f"Version conflict for task {task_id}") from None
        raise


@activity.defn(name="r7kit.get")
async def get_act(task_id: str) -> dict[str, str] | None:
    cli = await get_redis_client()
    return await cli.hgetall(f"{_TASK_HASH}{task_id}") or None


@activity.defn(name="r7kit.delete")
async def delete_act(
    task_id: str,
    stream_name: str | None = None,
) -> None:
    stream = stream_name or cfg().stream_default
    key = f"{_TASK_HASH}{task_id}"
    try:
        await _lua(
            _LUA_DELETE,
            [key, stream],
            [_now_iso(), _DELETED_TTL],
        )
    except ResponseError as exc:
        if "EDELETED" in str(exc) or "ENOENT" in str(exc):
            raise TaskNotFoundError(task_id) from None
        raise
