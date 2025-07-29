# === ПУТЬ К ФАЙЛУ: r7kit/base_workflow.py ===
from __future__ import annotations
from typing import Any, Mapping, Optional, Union
from datetime import timedelta

from temporalio.common import RetryPolicy

from .tasks import get_task, patch_task, delete_task
from .models import TaskModel
from .workflow_utils import call_child, start_child, default_retry_policy

DEFAULT_TIMEOUT = timedelta(seconds=30)

class BaseWorkflow:
    """
    Базовый класс без декораторов. Содержит:
      - _run_impl — устанавливает self.task_id и вызывает handle()
      - abstract handle() — переопределяется агентами
      - хелперы: get_task, patch_task, delete_task, exists
      - call_child, start_child с автопередачей task_id
    """

    task_id: str

    def __init__(self):
        # Temporal создаёт экземпляр без аргументов
        self.task_id = ""

    async def _run_impl(self, task_id: str, *args: Any, **kwargs: Any) -> Any:
        if not isinstance(task_id, str) or not task_id:
            raise ValueError("Первый аргумент run() должен быть непустым task_id")
        self.task_id = task_id
        return await self.handle(*args, **kwargs)

    async def handle(self, *args: Any, **kwargs: Any) -> Any:
        """
        Этот метод должны реализовать дочерние классы вместо run().
        """
        raise NotImplementedError("handle() должен быть реализован в дочернем классе")

    # ————— Работа с R7kit-задачей —————

    async def get_task(self, timeout: Optional[timedelta] = None) -> TaskModel | None:
        return await get_task(self.task_id, timeout=timeout or DEFAULT_TIMEOUT)

    async def patch_task(
        self,
        patch: dict[str, Any],
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

    # ————— Вызов дочерних воркфлоу —————

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
