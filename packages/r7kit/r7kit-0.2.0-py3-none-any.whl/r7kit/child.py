# === ПУТЬ К ФАЙЛУ: r7kit/child.py ===
from __future__ import annotations

import uuid as _uuid
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Union

from temporalio.common import RetryPolicy

from .tasks import create_task            # activity-обёртка
from .workflow_utils import call_child, start_child

# Атрибут из декоратора @taskflow
_TASKFLOW_QUEUE_ATTR = "__r7kit_queue__"


@dataclass(frozen=True, slots=True)
class _ChildHelper:
    wf:   Union[str, type]
    task_id: str
    queue:    str | None = None
    retry:    RetryPolicy | Mapping[str, Any] | None = None
    id_:      str | None = None

    async def run(self, *args: Any, **kwargs: Any):
        return await call_child(
            self.wf,
            self.task_id,
            *args,
            queue=self.queue,
            retry=self.retry,
            id_=self.id_,
            **kwargs,
        )

    async def start(
        self,
        *args: Any,
        payload: dict | None = None,
        uuid: str | None = None,
        **kwargs: Any,
    ):
        if payload is not None:
            task_id = await create_task(payload, uuid=uuid)
            wf_args = [task_id, *args]
        else:
            task_id = None
            wf_args = [self.task_id, *args]

        handle = await start_child(
            self.wf,
            *wf_args,
            queue=self.queue,
            retry=self.retry,
            id_=self.id_,
            **kwargs,
        )
        return (handle, task_id) if payload is not None else handle


def child(
    wf: Union[str, type],
    *,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_: str | None = None,
) -> Callable[[str], _ChildHelper]:
    """
    Фабрика, «привязанная» к task_id. Если queue не передали —
    пытаемся взять его из атрибута класса workflow.
    """
    def _factory(task_id: str) -> _ChildHelper:
        # получим default-queue из класса, если это класс
        if isinstance(wf, type) and hasattr(wf, _TASKFLOW_QUEUE_ATTR):
            default_q = getattr(wf, _TASKFLOW_QUEUE_ATTR)
        else:
            default_q = None
        return _ChildHelper(
            wf=wf,
            task_id=task_id,
            queue=queue or default_q,
            retry=retry,
            id_=id_,
        )
    return _factory
