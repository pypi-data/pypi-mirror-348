# Tutorial: Data Engineering with AsFlow

In this tutorial, we’ll walk through a step-by-step data engineering workflow using AsFlow.

As a practical example, we’ll collect data from the YouTube channel [@MrBeast](https://www.youtube.com/@MrBeast) and build a data dashboard using [Streamlit](https://streamlit.io).

You can find the complete source code for this tutorial in the repository: [asflow-tutorial](...)

## Installation

Assuming you already have [uv](https://docs.astral.sh/uv/) installed for Python package management, let's start by creating a new project:

```console
% mkdir asflow-tutorial
% cd asflow-tutorial
% uv init
Initialized project `asflow-tutorial`
```

Install the necessary dependencies:

```console
% uv add asflow zstandard
Using CPython 3.13.3
Creating virtual environment at: .venv
Resolved 6 packages in 3ms
Installed 5 packages in 8ms
 + asflow==0.0.2
 + markdown-it-py==3.0.0
 + mdurl==0.1.2
 + pygments==2.19.1
 + rich==14.0.0
 + zstandard==0.23.0
```

## Raw Data 1: YouTube Playlist

To begin, we’ll fetch a list of videos from a YouTube channel using `yt-dlp`.

Install `yt-dlp`:

```console
% uv add yt-dlp
Resolved 7 packages in 2ms
Installed 1 package in 9ms
 + yt-dlp==2025.4.30
```

You can use the following command to get the playlist data. The output will be in JSON Lines format:

```console
% uv run yt-dlp --dump-json --flat-playlist https://www.youtube.com/@MrBeast
{"_type": "url", "ie_key": "Youtube", "id": "-4GmbBoYQjE", ...}
...
```

Instead of running `yt-dlp` manually, let’s write an AsFlow task to run it as a subprocess and save the output to disk. Since the output is in JSON Lines format, we’ll save it as a Zstandard-compressed `.jsonl.zst` file.

```python
# flows/playlist.py

import asyncio
from asflow import flow

@flow.task(on="data/playlist.jsonl.zst")
async def extract(channel_url):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp", "--dump-json", "--flat-playlist", channel_url,
        stdout=asyncio.subprocess.PIPE,
    )
    async for line in proc.stdout:
        flow.task.write(line)

@flow
async def playlist():
    await extract("https://www.youtube.com/@MrBeast")

if __name__ == "__main__":
    asyncio.run(playlist())
```

Run the script:

```console
% uv run -m flows.playlist
@flow playlist() ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% -:--:--
 @task extract() ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% -:--:--
```

Once finished, the raw playlist data will be saved to `data/playlist.jsonl.zst`.

### Transformation

Before diving deeper, it’s a good idea to explore the structure of the raw data. Since the data is in a semi-structured JSON Lines format, tools like [Daft](https://www.getdaft.io), [DuckDB](https://duckdb.org), and [Polars](https://pola.rs) are ideal for quick inspection and transformation.

Among these, it’s generally recommended to load the raw data as a dataframe, which gives you powerful, flexible ways to manipulate and analyze it.

Here’s a simple example using Polars to read a `.jsonl.zst` file:

```python
import polars as pl

@flow.task
def transform():
    return pl.read_ndjson("data/playlist.jsonl.zst")
```

As your application evolves, you’ll likely need to modify and enrich this data — for example, by adding new columns or unpacking nested structures. The `transform()` function may grow to look like this:

```python
import polars as pl

@flow.task
def transform():
    df = pl.read_ndjson(
        "data/playlist.jsonl.zst",
        # Override schema if automatic inference fails
        schema_overrides={
            "release_timestamp": pl.Int64,
        },
    )

    # Add a column by extracting values from an existing one
    df = df.with_columns(
        playlist_type=pl.col("playlist").str.split(by=" - ").list.get(1)
    )

    # Unpack a struct column into separate columns
    df = df.unnest("_version")

    return df
```

During development, it’s important to verify the output of your transformation. You can do this by printing the result at the end of your workflow file.

To go a step further, you can use tools like [skimpy](https://github.com/aeturrell/skimpy) to get a high-level summary of the dataframe:

```python
from skimpy import skim

@flow
async def playlist():
    await extract("https://www.youtube.com/@MrBeast")
    return transform()

if __name__ == "__main__":
    df = asyncio.run(playlist())
    skim(df)
```

```console
% uv add polars skimpy
% uv run -m flows.playlist
╭─────────────────────────────── skimpy summary ───────────────────────────────╮
│          Data Summary                Data Types                              │
│ ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓ ┏━━━━━━━━━━━━━┳━━━━━━━┓                       │
│ ┃ Dataframe         ┃ Values ┃ ┃ Column Type ┃ Count ┃                       │
│ ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩ ┡━━━━━━━━━━━━━╇━━━━━━━┩                       │
│ │ Number of rows    │ 870    │ │ string      │ 21    │                       │
│ │ Number of columns │ 42     │ │ object      │ 12    │                       │
│ └───────────────────┴────────┘ │ int64       │ 7     │                       │
│                                │ float64     │ 1     │                       │
│                                │ bool        │ 1     │                       │
│                                └─────────────┴───────┘                       │
│                                  All null                                    │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓  │
│ ┃ column                                      ┃ NA         ┃ NA %         ┃  │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩  │
│ │ release_timestamp                           │        870 │          100 │  │
│ │ uploader_url                                │        870 │          100 │  │
│ │ release_year                                │        870 │          100 │  │
│ ...                                                                          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

By inspecting and refining the output early, you’ll build more robust pipelines as your data application grows.

### Application Structure

We’ll use **Streamlit** to build an interactive dashboard for exploring the data. Here’s a recommended project layout:

```bash
asflow-tutorial/
  app.py                   # Main Streamlit app entrypoint
  pages/
    playlist.py            # Streamlit page for playlist summary
    ...
  flows/
    playlist.py            # AsFlow workflow script
    ...
  data/
    playlist.jsonl.zst     # Raw extracted data
    ...
```

- `flows/` contains your workflow definitions. It’s a good practice to keep one file per data source. You can run these workflows independently with commands like `uv run -m flows.playlist`.
- `pages/` holds Streamlit UI pages. Each page corresponds to a flow and typically summarizes a specific dataset.
- `data/` stores raw or intermediate data generated by your workflows.

### Embedding Workflows in Streamlit

You can easily embed your workflows into Streamlit apps like this:

```python
# app.py

import asyncio
import streamlit as st

import flows.playlist

st.title("Dashboard")

# Run the workflow to get a dataframe
playlist_df = asyncio.run(flows.playlist.playlist())

# Run SQL against the dataframe and show results
result = playlist_df.sql("""
SELECT playlist, count(*) count
FROM self
GROUP BY 1
""")
st.dataframe(result)
```

To start the Streamlit app:

```console
% uv add streamlit watchdog
% uv run streamlit run app.py

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.200:8501
```

Streamlit watches for file changes and reloads the app automatically. Every time you modify and save a flow script, Streamlit reruns the workflow from scratch—helpful for rapid iteration during development.

!!! note

    For small-to-medium datasets, this full re-execution model is usually fast enough that you won’t notice delays.

### Improving Performance with Caching

If your data takes time to load or transform, caching can help speed up iteration and improve responsiveness. Here are several options:

#### 1. Streamlit’s In-Memory Cache

For UI-level caching, use `@st.cache_data` to reuse workflow results across reruns:

```python
import streamlit as st

@st.cache_data
def playlist():
    return asyncio.run(flows.playlist.playlist())
```

Use this when:
- The computation is relatively fast.
- The results are used primarily in the frontend.
- You’re OK with cache reset when the app restarts.

#### 2. Disk-Based Caching with Joblib

To persist results across app reloads or system restarts, use [Joblib](https://joblib.readthedocs.io/) with a cache directory:

```python
from joblib import Memory

memory = Memory(".cache")

@flow.task
@memory.cache
def transform():
    return pl.read_ndjson("data/playlist.jsonl.zst")
```

Joblib tracks changes to function code and parameters, automatically invalidating outdated results.

Use this for:
- Repeated, expensive data transformations.
- Development workflows where inputs are stable but logic changes often.

#### 3. Exporting to Parquet

AsFlow doesn’t provide native Parquet output, but you can write to `.parquet` manually at the end of a flow:

```
@flow
async def playlist():
    await extract("https://www.youtube.com/@MrBeast")
    df = transform()
    df.write_parquet("playlist.parquet")
```

Use this for:
- Long-term storage.
- Fast reloads across sessions.
- Sharing data between tools or pipelines.

### Comparing Persistence Methods

| Method | File Path | Compression | Lifespan | Bast Use Case |
| --- | --- | --- | --- | --- |
| `@flow.task(on=...)` | Custom path | `.gz`, `.zst` | Until file is deleted | Raw data extractions |
| Manual `.parquet` write | Custom path | Snappy | until file is deleted | Long-term persistence & sharing |
| Joblib `@memory.cache` | Cache directory | None | Until code or parameters change | Data transformations |
| Streamlit `@st.cache_data` | In-memory | None | Until app restart or input changes | Repeated UI results |
