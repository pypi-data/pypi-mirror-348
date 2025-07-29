# === ПУТЬ К ФАЙЛУ: r7kit/redis_client.py ===
from __future__ import annotations

import asyncio
import logging
from typing import Optional, cast

import redis.asyncio as redis
from redis.exceptions import ConnectionError, TimeoutError

from .config import cfg

logger = logging.getLogger(__name__)

_redis_client: Optional[redis.Redis] = None
_lock = asyncio.Lock()
_HEALTH_CHECK_INTERVAL = 30        # сек
_RETRIES = 3
_BACKOFF = 2.0                     # кратность эксп.-бэк-оффа


async def _connect() -> redis.Redis:
    return cast(
        redis.Redis,
        redis.from_url(
            str(cfg().redis_url),
            decode_responses=True,
            health_check_interval=_HEALTH_CHECK_INTERVAL,
        ),
    )


async def get_redis_client() -> redis.Redis:
    """
    Singleton Redis-клиент с авто-reconnect и экспоненциальным бэк-оффом.
    """
    global _redis_client
    attempt = 0
    while True:
        if _redis_client is not None:
            return _redis_client
        async with _lock:
            if _redis_client is None:  # double-check
                try:
                    _redis_client = await _connect()
                    await _redis_client.ping()
                    logger.info("Connected to Redis at %s", cfg().redis_url)
                except (ConnectionError, TimeoutError) as err:
                    attempt += 1
                    if attempt > _RETRIES:
                        raise
                    wait = _BACKOFF ** attempt
                    logger.warning("Redis connect failed (%s), retry in %ss", err, wait)
                    await asyncio.sleep(wait)
                    continue
        # повторный проход цикла вернёт клиента


async def close_redis_client() -> None:
    global _redis_client
    if _redis_client is not None:
        try:
            await _redis_client.close()
        finally:
            _redis_client = None
