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
