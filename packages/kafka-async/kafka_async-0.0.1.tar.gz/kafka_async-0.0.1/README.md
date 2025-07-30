# kafka-async

[![PyPI - Status](https://img.shields.io/pypi/status/kafka-async)](https://pypi.org/project/kafka-async)
[![PyPI](https://img.shields.io/pypi/v/kafka-async)](https://pypi.org/project/kafka-async)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kafka-async)](https://pypi.org/project/kafka-async)
[![PyPI - License](https://img.shields.io/pypi/l/kafka-async)](https://pypi.org/project/kafka-async)
[![CI Status](https://github.com/tkukushkin/kafka-async/actions/workflows/check.yml/badge.svg)](https://github.com/tkukushkin/kafka-async/actions/workflows/check.yml)
[![codecov](https://codecov.io/gh/tkukushkin/kafka-async/graph/badge.svg?token=376OQ1J9YH)](https://codecov.io/gh/tkukushkin/kafka-async)
[![docs](https://readthedocs.org/projects/kafka-async/badge/?version=latest)](https://kafka-async.readthedocs.io/stable/)

Thin async wrapper for [Confluent Kafka Python Client](https://pypi.org/project/confluent-kafka/).

## Installation

```bash
pip install kafka-async
```

## Usage

At the moment, only `Producer`, `Consumer`, and `AdminClient` are supported.

API is similar to the original `confluent-kafka` library, but with async/await syntax.

## License

This project is licensed under the MIT License – see the LICENSE file for details.
