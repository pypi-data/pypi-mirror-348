import time
from collections.abc import Mapping
from types import MappingProxyType
from typing import Any
from uuid import uuid1

import confluent_kafka.admin
import pytest
from lovely.pytest.docker.compose import Services

import kafka_async


@pytest.fixture(scope='session', autouse=True)
def anyio_backend() -> str:
    return 'asyncio'


@pytest.fixture(scope='session')
def kafka_addr() -> str:
    return '127.0.0.1:9092'


@pytest.fixture(scope='session')
def default_config(kafka_addr) -> Mapping[str, Any]:
    return MappingProxyType({'bootstrap.servers': kafka_addr, 'topic.metadata.refresh.interval.ms': 1000})


@pytest.fixture(scope='session', autouse=True)
def _start_kafka(default_config: Mapping[str, Any], docker_services: Services) -> None:
    docker_services.start('kafka')
    exception = None
    for _ in range(50):
        try:
            confluent_kafka.admin.AdminClient(dict(default_config)).list_topics(timeout=10)
        except confluent_kafka.KafkaException as exc:
            time.sleep(0.3)
            exception = exc
        else:
            return
    raise TimeoutError from exception


@pytest.fixture
async def producer(default_config):
    async with kafka_async.Producer(default_config) as producer:
        yield producer


@pytest.fixture
async def admin_client(default_config) -> kafka_async.AdminClient:
    return kafka_async.AdminClient(default_config)


@pytest.fixture
async def consumer(default_config):
    async with kafka_async.Consumer(
        {**default_config, 'group.id': str(uuid1()), 'auto.offset.reset': 'earliest'}
    ) as consumer:
        yield consumer


@pytest.fixture
def topic() -> str:
    return str(uuid1())
