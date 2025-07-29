# === ПУТЬ К ФАЙЛУ: r7kit/config.py ===
from __future__ import annotations
import os
from functools import lru_cache
from pydantic import BaseModel, Field

class Settings(BaseModel):
    """Конфигурация r7kit."""
    redis_url: str = Field("redis://localhost:6379", description="Redis URI")
    temporal_address: str = Field("localhost:7233", description="Temporal address")
    stream_default: str = Field("tasks_events", description="Redis Stream name")

    class Config:
        extra = "ignore"
        frozen = True

@lru_cache()
def cfg() -> Settings:
    """Читает настройки из окружения один раз."""
    return Settings(
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
        temporal_address=os.getenv("TEMPORAL_ADDRESS", "localhost:7233"),
        stream_default=os.getenv("R7KIT_STREAM", "tasks_events"),
    )

def configure(
    *,
    redis_url: str | None = None,
    temporal_address: str | None = None,
    stream_default: str | None = None,
) -> None:
    """
    Переопределение настроек до первого вызова cfg().
    """
    if cfg.cache_info().currsize:
        raise RuntimeError("r7kit уже инициализирован; configure() нужно вызвать раньше")
    if redis_url:
        os.environ["REDIS_URL"] = redis_url
    if temporal_address:
        os.environ["TEMPORAL_ADDRESS"] = temporal_address
    if stream_default:
        os.environ["R7KIT_STREAM"] = stream_default
