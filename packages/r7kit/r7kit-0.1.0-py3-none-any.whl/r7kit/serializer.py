# === ПУТЬ К ФАЙЛУ: r7kit/serializer.py ===
import logging
from typing import Any

import orjson

logger = logging.getLogger(__name__)

_SERIALIZATION_PREFIX = "__r7kit__:v1__"


class SafeSerializer:
    """
    Надёжная сериализация payload-данных
    (любые типы → str; JSON — с версионированным префиксом).
    """

    @classmethod
    def dumps(cls, value: Any) -> str:
        # строку тоже упаковываем с префиксом,
        # иначе при смене схемы непонятно, сериализовано оно или нет
        try:
            payload = orjson.dumps(
                value,
                option=orjson.OPT_SERIALIZE_DATACLASS | orjson.OPT_NAIVE_UTC,
            )
        except orjson.JSONEncodeError as err:  # noqa: BLE001
            logger.exception("cannot serialize: %r", value)
            raise ValueError(f"Cannot serialize object of type {type(value)}") from err
        return _SERIALIZATION_PREFIX + payload.decode()

    @classmethod
    def loads(cls, value: str) -> Any:
        if not isinstance(value, str) or not value.startswith(_SERIALIZATION_PREFIX):
            # обратная совместимость: «сырые» строки без префикса
            return value
        try:
            return orjson.loads(value[len(_SERIALIZATION_PREFIX) :])
        except orjson.JSONDecodeError as err:  # noqa: BLE001
            logger.exception("broken payload: %s", value)
            raise ValueError("Corrupted serialized JSON") from err

    @classmethod
    def is_serialized(cls, value: str) -> bool:
        return isinstance(value, str) and value.startswith(_SERIALIZATION_PREFIX)


# ── алиасы для прежнего публичного API ──────────────────────────────
dumps = SafeSerializer.dumps
loads = SafeSerializer.loads
