# AsFlow

**AsFlow** (short for "Async workflow") is a lightweight, asynchronous workflow runner built in pure Python. It's designed for ETL (Extract–Transform–Load) pipelines with a focus on minimal setup, fast iteration, and seamless integration with tools like [DuckDB](https://duckdb.org) and [Streamlit](https://streamlit.io).

![ScreenRecording](https://raw.githubusercontent.com/k24d/asflow/main/docs/assets/img/ScreenRecording.webp)

### Key Features

- 🐍 Pure Python, single-process — no external scheduler or services required
- ⚙️ Asynchronous by design — built on `asyncio` for parallel, non-blocking execution
- 📊 Rich console output — powered by [Rich](https://rich.readthedocs.io) for clean logs and progress bars
- 🔄 Built for data engineering — integrates naturally with [Daft](https://www.getdaft.io), [DuckDB](https://duckdb.org), and [Polars](https://pola.rs)

## Installation

```
% pip install asflow
```

## Quick Start

**AsFlow** lets you build ETL workflows using standard `async` Python functions. Just add the `@flow` and `@flow.task` decorators—everything else behaves like regular Python.

Here’s a minimal example:

```python
import asyncio
import duckdb
from asflow import Flow

flow = Flow(verbose=True)

# Extract: simulate saving raw data
@flow.task(on="words/*.jsonl.gz")
async def extract(word):
    await asyncio.sleep(1)  # Simulate I/O-bound operation
    flow.task.write({"word": word, "count": 1})

# Transform: read raw files into DuckDB
@flow.task
def transform():
    return duckdb.read_json("words/*.jsonl.gz")

# Define the workflow
@flow
async def main():
    words = ["Hello", "World"]

    # Run extractions concurrently
    async with asyncio.TaskGroup() as tg:
        for word in words:
            tg.create_task(extract(word))

    print(transform())

if __name__ == "__main__":
    asyncio.run(main())
```

Running this script produces output like:

```console
% python main.py
[12:34:56] Task extract('Hello') finished in 1.00s
           Task extract('World') finished in 1.01s
           Task transform() finished in 0.00s
┌─────────┬───────┐
│  word   │ count │
│ varchar │ int64 │
├─────────┼───────┤
│ Hello   │     1 │
│ World   │     1 │
└─────────┴───────┘
```

### What’s Happening?

- `extract()` simulates downloading or generating raw data. It’s async, so multiple calls run in parallel.
- `transform()` uses DuckDB to load the saved data into a queryable table.
- Results from `extract()` are written to disk (`words/*.jsonl.gz`), so they’re skipped on future runs if the file already exists—making your workflow faster and more reliable.

### Why Use AsFlow?
- ✅ Seamless support for **async and sync tasks**
- 🔁 Automatic **retry logic** for transient errors
- 🧵 Configurable **concurrency limits** for external APIs
- 📦 Easy **persistence** of intermediate results (e.g., JSON, CSV)
- 🗜️ Built-in **compression** support (`.gz`, `.zst`)
- 📊 **Rich-powered** logging with progress bars and status indicators

## Documentation

- [Getting Started with AsFlow](https://asflow.readthedocs.io/en/latest/)
