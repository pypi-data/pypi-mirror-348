# === ПУТЬ К ФАЙЛУ: r7kit/serializer.py ===
import logging
from typing import Any, Final

import orjson

logger = logging.getLogger(__name__)

_PREFIX: Final[str] = "__r7kit__:v1__"


def _to_json(value: Any) -> str:
    try:
        payload = orjson.dumps(
            value,
            option=orjson.OPT_SERIALIZE_DATACLASS | orjson.OPT_NAIVE_UTC,
        )
    except orjson.JSONEncodeError as err:  # noqa: BLE001
        logger.exception("cannot serialize: %r", value)
        raise ValueError(f"Cannot serialize object of type {type(value)}") from err
    return _PREFIX + payload.decode()


def _from_json(value: str) -> Any:
    try:
        return orjson.loads(value[len(_PREFIX) :])
    except orjson.JSONDecodeError as err:  # noqa: BLE001
        logger.exception("broken payload: %s", value)
        raise ValueError("Corrupted serialized JSON") from err


# ── публичный API ────────────────────────────────────────────────────
def dumps(value: Any) -> str:
    """Бережная сериализация Python-объекта в str."""
    # строку тоже упакуем с префиксом для унификации
    return _to_json(value)


def loads(value: str) -> Any:  # noqa: ANN401
    """Обратная операция к dumps()."""
    if not isinstance(value, str) or not value.startswith(_PREFIX):
        # обратная совместимость: «сырые» строки без префикса
        return value
    return _from_json(value)
