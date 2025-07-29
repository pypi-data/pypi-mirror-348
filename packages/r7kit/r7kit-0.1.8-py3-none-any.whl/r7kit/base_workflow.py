from __future__ import annotations

from datetime import timedelta
from typing import Any, Mapping, Optional, Union

from temporalio.common import RetryPolicy

from .child import child as _child_factory
from .models import TaskModel
from .tasks import delete_task, get_task, patch_task
from .workflow_utils import call_child, start_child

DEFAULT_TIMEOUT = timedelta(seconds=30)


class BaseWorkflow:
    """
    Базовый класс для всех workflow-агентов.

    Возможности:
    ------------
    • `self.task_id` – id Redis-задачи  
    • CRUD-методы: `get_task / patch_task / delete_task / exists`  
    • Сахар для дочерних WF:  
      `await self.child(OtherFlow).run(... )` / `.start(...)`
    """

    task_id: str

    # ---------------- infrastructure ---------------- #
    def __init__(self) -> None:
        self.task_id = ""

    async def _run_impl(self, task_id: str, *args: Any, **kwargs: Any) -> Any:
        if not task_id:
            raise ValueError("Первый аргумент run() должен быть непустым task_id")
        self.task_id = task_id
        return await self.handle(*args, **kwargs)

    async def handle(self, *args: Any, **kwargs: Any) -> Any:  # noqa: D401
        """Должен быть переопределён в наследнике."""
        raise NotImplementedError

    # ---------------- Task-helpers ------------------- #
    async def get_task(self, timeout: Optional[timedelta] = None) -> TaskModel | None:
        return await get_task(self.task_id, timeout=timeout or DEFAULT_TIMEOUT)

    async def patch_task(
        self,
        patch: dict[str, Any],
        *,
        timeout: Optional[timedelta] = None,
    ) -> None:
        if not patch:
            raise ValueError("patch должен быть непустым словарём")
        await patch_task(self.task_id, patch, timeout=timeout or DEFAULT_TIMEOUT)

    async def delete_task(self, timeout: Optional[timedelta] = None) -> None:
        await delete_task(self.task_id, timeout=timeout or DEFAULT_TIMEOUT)

    async def exists(self) -> bool:
        t = await self.get_task()
        return bool(t and t.exists)

    # ---------------- Child-workflow (raw) ----------- #
    async def call_child(
        self,
        wf: Union[str, type],
        *args: Any,
        queue: str | None = None,
        retry: RetryPolicy | Mapping[str, Any] | None = None,
        id_: str | None = None,
    ) -> Any:
        return await call_child(
            wf,
            self.task_id,
            *args,
            queue=queue,
            retry=retry,
            id_=id_,
        )

    async def start_child(
        self,
        wf: Union[str, type],
        *args: Any,
        queue: str | None = None,
        retry: RetryPolicy | Mapping[str, Any] | None = None,
        id_: str | None = None,
    ):
        return await start_child(
            wf,
            self.task_id,
            *args,
            queue=queue,
            retry=retry,
            id_=id_,
        )

    # ---------------- Fluent-helper ------------------ #
    def child(
        self,
        wf: Union[str, type],
        *,
        queue: str | None = None,
        retry: RetryPolicy | Mapping[str, Any] | None = None,
        id_: str | None = None,
    ):
        """
        Синтаксический сахар::

            await self.child(MyFlow).run(a, b)
            await self.child("Other", queue="q").start(x=1)
        """
        return _child_factory(wf, queue=queue, retry=retry, id_=id_)
