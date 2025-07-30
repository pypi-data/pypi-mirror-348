# === ПУТЬ К ФАЙЛУ: r7kit/activities.py ===
from __future__ import annotations

import logging
import uuid as _uuid
from datetime import datetime, timezone
from typing import Any, Iterable, Final

from redis.exceptions import ResponseError
from temporalio import activity
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import cfg
from .exceptions import TaskAlreadyExistsError, TaskNotFoundError
from .redis_client import get_redis_client
from .serializer import dumps

logger = logging.getLogger(__name__)

_TASK_HASH: Final[str] = "task:"
_DEFAULT_TTL: Final[int] = 7 * 24 * 3600        # 7 дней для create/patch
_STREAM_FIELD_LIMIT: Final[int] = 50            # макс-полей в XADD
_DELETED_TTL: Final[int] = 24 * 3600            # дефолтный ttl для delete (1 день)

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def _flatten(src: dict[str, str]) -> list[str]:
    out: list[str] = []
    for k in sorted(src):
        out.extend((k, src[k]))
    return out

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.2, max=1.0))
async def _lua(script: str, keys: Iterable[str], *args: Any) -> None:
    cli = await get_redis_client()
    await cli.eval(script, len(list(keys)), *keys, *args)

# ──────────────────── Lua-скрипты ─────────────────────────────────
_LUA_CREATE = r"""
if redis.call('EXISTS', KEYS[1]) == 1 then
  return redis.error_reply('EEXISTS')
end
redis.call('HSET', KEYS[1], unpack(ARGV, 5, 4 + ARGV[3]*2))
redis.call('HSET', KEYS[1], 'ver', 1)
redis.call('PEXPIRE', KEYS[1], ARGV[1] * 1000)
local x_start = 5 + ARGV[3]*2
redis.call('XADD', KEYS[2], '*', 'event', ARGV[2],
            unpack(ARGV, x_start, x_start + ARGV[4]*2 - 1))
return 'OK'
"""

_LUA_PATCH = r"""
local cur = redis.call('HGET', KEYS[1], 'ver')
if not cur then return redis.error_reply('ENOENT') end
if cur ~= ARGV[1] then return redis.error_reply('ECONFLICT') end
redis.call('HSET', KEYS[1], unpack(ARGV, 6, 5 + ARGV[3]*2))
redis.call('HINCRBY', KEYS[1], 'ver', 1)
redis.call('PEXPIRE', KEYS[1], ARGV[2] * 1000)
local x_start = 6 + ARGV[3]*2
redis.call('XADD', KEYS[2], '*', 'event', ARGV[5],
            unpack(ARGV, x_start, x_start + ARGV[4]*2 - 1))
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

# ───────────────────── Activities ──────────────────────────────────

@activity.defn(name="r7kit.create")
async def create_act(
    payload: dict[str, Any] | None,
    status: str,
    stream_name: str | None = None,
    task_id: str | None = None,
) -> str:
    stream = stream_name or cfg().stream_default
    task_id = task_id or str(_uuid.uuid4())
    key = f"{_TASK_HASH}{task_id}"
    record: dict[str, str] = {
        "uuid":       task_id,
        "status":     status,
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
            _DEFAULT_TTL,
            "created",
            len(h_args)//2,
            len(x_args)//2,
            *h_args,
            *x_args,
        )
    except ResponseError as exc:
        if "EEXISTS" in str(exc):
            raise TaskAlreadyExistsError(task_id)
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
    cur_ver = await cli.hget(key, "ver")
    if cur_ver is None:
        raise TaskNotFoundError(task_id)
    record = {k: dumps(v) for k, v in patch.items()}
    record["updated_at"] = _now_iso()
    h_args = _flatten(record)
    x_args = h_args[: _STREAM_FIELD_LIMIT * 2]
    try:
        await _lua(
            _LUA_PATCH,
            [key, stream],
            cur_ver,
            _DEFAULT_TTL,
            len(h_args)//2,
            len(x_args)//2,
            "patched",
            *h_args,
            *x_args,
        )
    except ResponseError as exc:
        msg = str(exc)
        if "ENOENT" in msg or "EDELETED" in msg:
            raise TaskNotFoundError(task_id)
        if "ECONFLICT" in msg:
            raise RuntimeError(f"Version conflict for task {task_id}")
        raise

@activity.defn(name="r7kit.get")
async def get_act(task_id: str) -> dict[str, str] | None:
    cli = await get_redis_client()
    return await cli.hgetall(f"{_TASK_HASH}{task_id}") or None

@activity.defn(name="r7kit.delete")
async def delete_act(
    task_id: str,
    stream_name: str | None = None,
    ttl: int | None = None,
) -> None:
    stream = stream_name or cfg().stream_default
    key = f"{_TASK_HASH}{task_id}"
    expire = ttl if ttl is not None else cfg().deleted_ttl
    try:
        await _lua(_LUA_DELETE, [key, stream], _now_iso(), expire)
    except ResponseError as exc:
        msg = str(exc)
        if "EDELETED" in msg or "ENOENT" in msg:
            raise TaskNotFoundError(task_id)
        raise
