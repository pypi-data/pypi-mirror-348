import sys
from collections.abc import Callable, Coroutine, Iterable, Mapping
from types import TracebackType
from typing import Any, Literal, overload

import anyio
import anyio.from_thread
import anyio.to_thread
import confluent_kafka
import confluent_kafka.admin

from ._utils import async_to_sync, make_kwargs, to_dict, to_list

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class Consumer:
    def __init__(self, config: Mapping[str, Any]) -> None:
        self._consumer = confluent_kafka.Consumer(to_dict(config))

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        with anyio.CancelScope(shield=True):
            await self.close()

    def assign(self, partitions: Iterable[confluent_kafka.TopicPartition]) -> None:
        self._consumer.assign(to_list(partitions))

    def assignment(self) -> list[confluent_kafka.TopicPartition]:
        return self._consumer.assignment()

    async def close(self) -> None:
        await anyio.to_thread.run_sync(self._consumer.close)

    @overload
    def commit(
        self,
        message: confluent_kafka.Message | None = None,
        offsets: Iterable[confluent_kafka.TopicPartition] | None = None,
        *,
        asynchronous: Literal[True] = True,
    ) -> None: ...

    @overload
    async def commit(
        self,
        message: confluent_kafka.Message | None = None,
        offsets: Iterable[confluent_kafka.TopicPartition] | None = None,
        *,
        asynchronous: Literal[False],
    ) -> list[confluent_kafka.TopicPartition]: ...

    def commit(
        self,
        message: confluent_kafka.Message | None = None,
        offsets: Iterable[confluent_kafka.TopicPartition] | None = None,
        *,
        asynchronous: bool = True,
    ) -> None | Coroutine[Any, Any, list[confluent_kafka.TopicPartition]]:
        offsets_list = to_list(offsets) if offsets is not None else None
        kwargs = make_kwargs(message=message, offsets=offsets_list)
        if asynchronous:
            return self._consumer.commit(**kwargs)

        return anyio.to_thread.run_sync(lambda: self._consumer.commit(asynchronous=False, **kwargs))

    async def committed(
        self, partitions: Iterable[confluent_kafka.TopicPartition], timeout: float | None = None
    ) -> list[confluent_kafka.TopicPartition]:
        return await anyio.to_thread.run_sync(
            lambda: self._consumer.committed(to_list(partitions), **make_kwargs(timeout=timeout))
        )

    async def consume(self, num_messages: int = 1, timeout: float | None = None) -> list[confluent_kafka.Message]:
        return await anyio.to_thread.run_sync(
            lambda: self._consumer.consume(num_messages, **make_kwargs(timeout=timeout))
        )

    def consumer_group_metadata(self) -> object:
        return self._consumer.consumer_group_metadata()

    @overload
    def get_watermark_offsets(
        self, partition: confluent_kafka.TopicPartition, *, cached: Literal[True]
    ) -> tuple[int, int]: ...

    @overload
    async def get_watermark_offsets(
        self, partition: confluent_kafka.TopicPartition, timeout: float | None = None, *, cached: Literal[False] = False
    ) -> tuple[int, int]: ...

    def get_watermark_offsets(
        self,
        partition: confluent_kafka.TopicPartition,
        timeout: float | None = None,
        cached: bool = False,
    ) -> tuple[int, int] | Coroutine[Any, Any, tuple[int, int]]:
        kwargs = make_kwargs(timeout=timeout)
        if cached:
            return self._consumer.get_watermark_offsets(partition, cached=True, **kwargs)
        return anyio.to_thread.run_sync(lambda: self._consumer.get_watermark_offsets(partition, cached=False, **kwargs))

    def incremental_assign(self, partitions: Iterable[confluent_kafka.TopicPartition]) -> None:
        self._consumer.incremental_assign(to_list(partitions))

    def incremental_unassign(self, partitions: Iterable[confluent_kafka.TopicPartition]) -> None:
        self._consumer.incremental_unassign(to_list(partitions))

    async def list_topics(
        self, topic: str | None = None, timeout: float | None = None
    ) -> confluent_kafka.admin.ClusterMetadata:
        return await anyio.to_thread.run_sync(lambda: self._consumer.list_topics(topic, **make_kwargs(timeout=timeout)))

    def memberid(self) -> str | None:
        return self._consumer.memberid()

    async def offsets_for_times(
        self, partitions: Iterable[confluent_kafka.TopicPartition], timeout: float | None = None
    ) -> list[confluent_kafka.TopicPartition]:
        return await anyio.to_thread.run_sync(
            lambda: self._consumer.offsets_for_times(to_list(partitions), **make_kwargs(timeout=timeout))
        )

    def pause(self, partitions: Iterable[confluent_kafka.TopicPartition]) -> None:
        self._consumer.pause(to_list(partitions))

    async def poll(self, timeout: float | None = None) -> confluent_kafka.Message | None:
        return await anyio.to_thread.run_sync(lambda: self._consumer.poll(**make_kwargs(timeout=timeout)))

    def position(self, partitions: Iterable[confluent_kafka.TopicPartition]) -> list[confluent_kafka.TopicPartition]:
        return self._consumer.position(to_list(partitions))

    def resume(self, partitions: Iterable[confluent_kafka.TopicPartition]) -> None:
        self._consumer.resume(to_list(partitions))

    def seek(self, partition: confluent_kafka.TopicPartition) -> None:
        self._consumer.seek(partition)

    def set_sasl_credentials(self, username: str, password: str) -> None:
        self._consumer.set_sasl_credentials(username, password)

    def store_offsets(
        self,
        message: confluent_kafka.Message | None = None,
        offsets: Iterable[confluent_kafka.TopicPartition] | None = None,
    ) -> None:
        kwargs = make_kwargs(
            message=message,
            offsets=to_list(offsets) if offsets is not None else None,
        )
        self._consumer.store_offsets(**kwargs)

    def subscribe(
        self,
        topics: Iterable[str],
        *,
        on_assign: (
            Callable[[confluent_kafka.Consumer, list[confluent_kafka.TopicPartition]], Coroutine[Any, Any, Any]] | None
        ) = None,
        on_revoke: (
            Callable[[confluent_kafka.Consumer, list[confluent_kafka.TopicPartition]], Coroutine[Any, Any, Any]] | None
        ) = None,
        on_lost: (
            Callable[[confluent_kafka.Consumer, list[confluent_kafka.TopicPartition]], Coroutine[Any, Any, Any]] | None
        ) = None,
    ) -> None:
        self._consumer.subscribe(
            to_list(topics),
            **make_kwargs(
                on_assign=async_to_sync(on_assign) if on_assign else None,
                on_revoke=async_to_sync(on_revoke) if on_revoke else None,
                on_lost=async_to_sync(on_lost) if on_lost else None,
            ),
        )

    def unassign(self) -> None:
        self._consumer.unassign()

    def unsubscribe(self) -> None:
        self._consumer.unsubscribe()
