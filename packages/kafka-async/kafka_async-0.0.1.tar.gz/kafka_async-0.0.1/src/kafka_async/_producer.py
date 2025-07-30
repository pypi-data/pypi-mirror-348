import sys
from collections.abc import Callable, Coroutine, Iterable, Mapping, Sequence
from datetime import datetime
from types import TracebackType
from typing import Any

import anyio
import anyio.from_thread
import anyio.to_thread
import confluent_kafka
import confluent_kafka.admin

from kafka_async._utils import make_kwargs, to_dict, to_list

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class Producer:
    def __init__(self, config: Mapping[str, Any]) -> None:
        self._producer = confluent_kafka.Producer(to_dict(config))

    def __len__(self) -> int:
        return len(self._producer)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        with anyio.CancelScope(shield=True):
            await self.flush()

    async def abort_transaction(self, timeout: float | None = None) -> None:
        await anyio.to_thread.run_sync(lambda: self._producer.abort_transaction(**make_kwargs(timeout=timeout)))

    def begin_transaction(self) -> None:
        self._producer.begin_transaction()

    async def commit_transaction(self, timeout: float | None = None) -> None:
        await anyio.to_thread.run_sync(lambda: self._producer.commit_transaction(**make_kwargs(timeout=timeout)))

    async def flush(self, timeout: float | None = None) -> None:
        await anyio.to_thread.run_sync(lambda: self._producer.flush(**make_kwargs(timeout=timeout)))

    async def init_transactions(self, timeout: float | None = None) -> None:
        await anyio.to_thread.run_sync(lambda: self._producer.init_transactions(**make_kwargs(timeout=timeout)))

    async def list_topics(
        self, topic: str | None = None, timeout: float | None = None
    ) -> confluent_kafka.admin.ClusterMetadata:
        return await anyio.to_thread.run_sync(lambda: self._producer.list_topics(topic, **make_kwargs(timeout=timeout)))

    async def poll(self, timeout: float | None = None) -> int:
        return await anyio.to_thread.run_sync(lambda: self._producer.poll(**make_kwargs(timeout=timeout)))

    def produce(
        self,
        topic: str,
        value: str | bytes | None = None,
        *,
        key: str | bytes | None = None,
        partition: int | None = None,
        on_delivery: (
            Callable[[confluent_kafka.KafkaError | None, confluent_kafka.Message], Coroutine[Any, Any, Any]] | None
        ) = None,
        timestamp: int | datetime | None = None,
        headers: Mapping[str, str | bytes | None] | Sequence[tuple[str, str | bytes | None]] | None = None,
    ) -> None:
        self._producer.produce(
            topic=topic,
            key=key,
            value=value,
            on_delivery=lambda err, msg: anyio.from_thread.run(on_delivery, err, msg) if on_delivery else None,
            headers=(
                [(k, v) for k, v in headers.items()]
                if isinstance(headers, Mapping)
                else to_list(headers)
                if isinstance(headers, Sequence)
                else None
            ),
            **make_kwargs(
                timestamp=int(timestamp.timestamp() * 1000) if isinstance(timestamp, datetime) else timestamp,
                partition=partition,
            ),
        )

    async def purge(self, in_queue: bool = True, in_flight: bool = True, blocking: bool = True) -> None:
        await anyio.to_thread.run_sync(self._producer.purge, in_queue, in_flight, blocking)

    async def send_offsets_to_transaction(
        self, positions: Iterable[confluent_kafka.TopicPartition], group_metadata: object, timeout: float | None = None
    ) -> None:
        await anyio.to_thread.run_sync(
            lambda: self._producer.send_offsets_to_transaction(
                to_list(positions), group_metadata, **make_kwargs(timeout=timeout)
            ),
        )

    def set_sasl_credentials(self, username: str, password: str) -> None:
        self._producer.set_sasl_credentials(username, password)
