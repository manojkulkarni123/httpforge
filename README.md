# Httpforge

A production-grade async HTTP client library with automatic retries, exponential backoff, structured JSON logging, and a clean exception hierarchy.

Built as a learning project to understand production Python patterns — async/await, decorators, context managers, generators, and packaging.

---

## Features

- **Typed configuration** — immutable `ClientConfig` dataclass with sensible defaults
- **Async HTTP** — built on `httpx.AsyncClient` with proper session lifecycle management
- **Automatic retries** — exponential backoff decorator, only retries errors worth retrying
- **Context manager** — `async with` guarantees session cleanup even on exceptions
- **Pagination** — async generator that lazily fetches pages on demand
- **Custom exceptions** — clean exception hierarchy, no leaking of `httpx` internals
- **Structured logging** — JSON logs with timestamps via `structlog`

---

## Installation

```bash
git clone https://github.com/manojkulkarni123/httpforge
cd resilient-client
uv sync
```

Or install directly:

```bash
uv pip install -e .
```

---

## Quick Start

```python
import asyncio
from resilient_client import ResilientClient, ClientConfig

async def main():
    config = ClientConfig(
        base_url="https://httpbin.org",
        method="GET",
        timeout=30.0,
        max_retries=3,
        headers={"Authorization": "Bearer your-token"}
    )

    async with ResilientClient(config) as client:
        result = await client.request("/get")
        print(result)

asyncio.run(main())
```

---

## Configuration

`ClientConfig` is a frozen dataclass — set it once, it never mutates.

```python
from resilient_client import ClientConfig

config = ClientConfig(
    base_url="https://api.example.com",   # required — no default
    method="POST",                         # required — GET/POST/PUT/DELETE/PATCH
    timeout=30.0,                          # default 30.0 seconds
    max_retries=3,                         # default 3 retry attempts
    headers={"X-API-Key": "secret"}        # default empty dict
)
```

To create a modified config without mutating the original:

```python
client2 = client.update_headers({"X-Request-ID": "abc-123"})
# original client is unchanged
```

---

## Making Requests

```python
async with ResilientClient(config) as client:
    # GET request
    result = await client.request("/users")

    # POST request with body
    result = await client.request("/users", body={"name": "Manoj"})
```

Every request is automatically retried on `NetworkError`, `TimeoutError`, and `ServerError` with exponential backoff:

```
Attempt 1 fails → wait 1s → retry
Attempt 2 fails → wait 2s → retry
Attempt 3 fails → wait 4s → raise
```

---

## Pagination

Lazily fetches pages one at a time — never loads the full dataset into memory:

```python
async with ResilientClient(config) as client:
    async for page in client.paginate("/results"):
        for item in page:
            process(item)
```

Stops automatically when the response has no `next_page` field.

---

## Exception Handling

All exceptions inherit from `ResilientClientError` — no `httpx` internals leak out.

```
ResilientClientError          ← catch everything
    ├── NetworkError          ← connection or DNS failure
    ├── TimeoutError          ← request exceeded timeout
    ├── RateLimitError        ← 429 Too Many Requests
    ├── ServerError           ← 5xx server errors
    ├── ClientError           ← 4xx client errors
    └── PayloadError          ← malformed request body
```

```python
from resilient_client import ResilientClient, ClientConfig
from resilient_client.exceptions import (
    ResilientClientError,
    RateLimitError,
    TimeoutError,
    ServerError,
)

async with ResilientClient(config) as client:
    try:
        result = await client.request("/endpoint")
    except RateLimitError:
        print("Rate limited — back off and retry later")
    except TimeoutError:
        print("Request timed out")
    except ServerError as e:
        print(f"Server error: {e}")
    except ResilientClientError as e:
        print(f"Something went wrong: {e}")
```

---

## Structured Logging

Every request emits JSON logs automatically:

```json
{"endpoint": "/get", "method": "GET", "event": "request_started", "timestamp": "2026-05-18T09:43:43.317007Z", "level": "info"}
{"endpoint": "/get", "status": 200, "event": "request_success", "timestamp": "2026-05-18T09:43:45.894360Z", "level": "info"}
```

Pipe these into Datadog, Grafana, or CloudWatch for monitoring and alerting.

---

## Project Structure

```
resilient-client/
├── pyproject.toml                  — project metadata and dependencies
├── README.md
├── src/
│   └── resilient_client/
│       ├── __init__.py             — public API surface
│       ├── models.py               — ClientConfig dataclass
│       ├── client.py               — ResilientClient main class
│       ├── retry.py                — sync retry decorator
│       ├── async_retry.py          — async retry decorator with asyncio.sleep
│       ├── exceptions.py           — custom exception hierarchy
│       └── logger.py               — structlog JSON logger setup
└── tests/
    ├── client_test.py
    ├── retry_test.py
    └── log_test.py
```

---

## Concepts Demonstrated

| Concept | Where |
|---|---|
| Dataclasses + frozen immutability | `models.py` |
| Dunder methods (`__repr__`, `__call__`) | `client.py` |
| Decorators + closures + `functools.wraps` | `retry.py`, `async_retry.py` |
| `async/await` + `asyncio` event loop | `client.py`, `async_retry.py` |
| Context managers (`__aenter__`, `__aexit__`) | `client.py` |
| Async generators + `yield` | `client.py` — `paginate()` |
| Custom exception hierarchies | `exceptions.py` |
| Structured logging pipeline | `logger.py` |
| Python packaging with `uv` + `pyproject.toml` | `pyproject.toml` |