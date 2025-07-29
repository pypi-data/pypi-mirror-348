# === ПУТЬ К ФАЙЛУ: r7kit/temporal_client.py ===
from __future__ import annotations

import asyncio
from typing import Optional

from temporalio.client import Client

from .config import cfg

_client: Optional[Client] = None
_lock = asyncio.Lock()


async def get_temporal_client() -> Client:
    """
    Singleton-клиент Temporal с lazy-connect и автоматическим
    пересозданием при обрыве.
    """
    global _client
    if _client is None or _client.closed:
        async with _lock:
            if _client is None or _client.closed:
                _client = await Client.connect(cfg().temporal_address)
    return _client  # type: ignore[arg-type]


async def close_temporal_client() -> None:
    global _client
    if _client is not None:
        try:
            await _client.close()
        finally:
            _client = None
