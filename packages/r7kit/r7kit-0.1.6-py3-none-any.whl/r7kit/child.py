"""
await self.child(OtherFlow).run(arg1, …)  или  .start(...)
"""
from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Mapping, Union

from temporalio.common import RetryPolicy

from .workflow_utils import call_child, start_child


class _ChildHelper(SimpleNamespace):
    _wf: Union[str, type]
    _q: str | None
    _r: RetryPolicy | Mapping[str, Any] | None
    _id: str | None

    async def run(self, *args: Any, **kwargs: Any):
        return await call_child(
            self._wf, *args, **kwargs, queue=self._q, retry=self._r, id_=self._id
        )

    async def start(self, *args: Any, **kwargs: Any):
        return await start_child(
            self._wf, *args, **kwargs, queue=self._q, retry=self._r, id_=self._id
        )


def child(
    wf: Union[str, type],
    *,
    queue: str | None = None,
    retry: RetryPolicy | Mapping[str, Any] | None = None,
    id_: str | None = None,
) -> _ChildHelper:
    """Фабрика хелпера c .run() / .start()."""
    return _ChildHelper(_wf=wf, _q=queue, _r=retry, _id=id_)
