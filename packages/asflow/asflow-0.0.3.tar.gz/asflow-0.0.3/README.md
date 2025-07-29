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

## Quick Guide

AsFlow allows you to define ETL workflows using regular `async` Python functions. All you have to do is decorate your functions with `@flow` and `@flow.task`. Everything else works just like standard Python.

Here’s a simple example:

```python
import asyncio
import duckdb
from asflow import flow

# Extract: simulate saving raw data
@flow.task(on="words/*.jsonl.gz")
async def extract(word):
    await asyncio.sleep(1)  # Simulate a slow operation
    flow.task.write({"word": word, "count": 1})

# Transform: run a SQL query on the raw data
@flow.task
def transform():
    return duckdb.sql("""
    SELECT * FROM read_json('words/*.jsonl.gz')
    """)

# Main workflow
@flow(verbose=True)
async def main():
    words = ["Hello", "World"]

    # Run extractions in parallel
    async with asyncio.TaskGroup() as tg:
        for word in words:
            tg.create_task(extract(word))

    print(transform())

if __name__ == "__main__":
    asyncio.run(main())
```

When you run this script:

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

### What’s Going On?

- The `extract()` function simulates downloading or generating raw data. It’s asynchronous, so multiple tasks can run in parallel.
- The `transform()` function uses DuckDB to run a SQL query on the saved data.
- The raw data is saved to files (e.g., `words/*.jsonl.gz`), so tasks won’t re-run if the data already exists—making your pipeline more stable and efficient.

## Documentation

- [Getting Started with AsFlow](https://asflow.readthedocs.io/en/latest/)
