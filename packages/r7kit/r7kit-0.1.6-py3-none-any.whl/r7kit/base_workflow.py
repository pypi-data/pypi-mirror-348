from __future__ import annotations
from datetime import timedelta
from typing import Any, Mapping, Optional, Union

from temporalio.common import RetryPolicy

from .child import child as _child_factory
from .models import TaskModel
from .tasks import delete_task, get_task, patch_task
from .workflow_utils import call_child, default_retry_policy, start_child

DEFAULT_TIMEOUT = timedelta(seconds=30)


class BaseWorkflow:
    """
    Общая логика для всех Workflow-классов.
    """

    task_id: str

    def __init__(self) -> None:
        self.task_id = ""

    # -------- основной запуск ---------- #

    async def _run_impl(self, task_id: str, *args: Any, **kwargs: Any) -> Any:
        if not task_id:
            raise ValueError("первый аргумент run() – непустой task_id")
        self.task_id = task_id
        return await self.handle(*args, **kwargs)

    async def handle(self, *args: Any, **kwargs: Any) -> Any:  # noqa: D401
        raise NotImplementedError

    # -------- R7kit-задача -------------- #

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

    # -------- дочерние воркфлоу -------- #

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

    # -------- «fluent» helper ----------- #

    def child(
        self,
        wf: Union[str, type],
        *,
        queue: str | None = None,
        retry: RetryPolicy | Mapping[str, Any] | None = None,
        id_: str | None = None,
    ):
        """
        Возвращает объект-хелпер:

            res = await self.child(MyFlow).run(1, 2)
            h   = await self.child("Other").start(x=1)
        """
        return _child_factory(wf, queue=queue, retry=retry, id_=id_)
