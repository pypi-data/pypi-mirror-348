# === ПУТЬ К ФАЙЛУ: r7kit/models.py ===
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field

class TaskModel(BaseModel):
    uuid: str
    status: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = Field(
        None,
        description="If set — timestamp of logical deletion"
    )
    payload: Dict[str, Any] | None = None

    @property
    def exists(self) -> bool:
        return self.deleted_at is None

    class Config:
        extra = "allow"
