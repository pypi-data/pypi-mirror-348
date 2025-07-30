# === ПУТЬ К ФАЙЛУ: r7kit/redis_client.py ===
from __future__ import annotations

import asyncio
import logging
from typing import Optional, cast

import redis.asyncio as redis
from redis.exceptions import ConnectionError, TimeoutError

from .config import cfg

logger = logging.getLogger(__name__)

_POOL_LOCK = asyncio.Lock()
_POOL: Optional[redis.ConnectionPool] = None
_HEALTH_CHECK_INTERVAL = 30        # сек
_RETRIES = 3
_BACKOFF = 2.0                     # экспоненциальный коэффициент


async def _create_pool() -> redis.ConnectionPool:
    """
    Создание ConnectionPool с health-check и decode-responses.
    Отдельный объект — проще перевоссоздать при потере соединений.
    """
    return cast(
        redis.ConnectionPool,
        redis.ConnectionPool.from_url(
            str(cfg().redis_url),
            decode_responses=True,
            health_check_interval=_HEALTH_CHECK_INTERVAL,
            max_connections=20,
        ),
    )


async def get_redis_client() -> redis.Redis:
    """
    Singleton Redis-клиент с авто-reconnect и экспоненциальным бэк-оффом.
    """
    global _POOL
    attempt = 0
    sleep_for = 0.0

    while True:
        if _POOL is not None:
            return redis.Redis(connection_pool=_POOL)  # лёгкий wrapper

        if sleep_for:
            await asyncio.sleep(sleep_for)

        async with _POOL_LOCK:
            if _POOL is not None:            # мог появиться, пока ждали lock
                continue
            try:
                _POOL = await _create_pool()
                client = redis.Redis(connection_pool=_POOL)
                await client.ping()
                logger.info("Connected to Redis at %s", cfg().redis_url)
                return client
            except (ConnectionError, TimeoutError) as err:
                attempt += 1
                if attempt > _RETRIES:
                    raise
                sleep_for = _BACKOFF ** attempt
                logger.warning("Redis connect failed (%s), retry in %ss", err, sleep_for)


async def close_redis_client() -> None:
    global _POOL
    if _POOL is not None:
        await _POOL.disconnect(inuse_connections=True)
        _POOL = None
