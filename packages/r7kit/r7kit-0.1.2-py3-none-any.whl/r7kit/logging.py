# === ПУТЬ К ФАЙЛУ: r7kit/logging.py ===
import logging
from logging.config import dictConfig

def setup(level: str | int = "INFO") -> None:
    """
    Устанавливает единый стиль логирования для r7kit и Temporal.
    Вызывать один раз в entry-point.
    """
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"}
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "standard"}
        },
        "root": {"handlers": ["console"], "level": level},
    })
