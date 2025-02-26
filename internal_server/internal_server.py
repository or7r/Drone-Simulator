import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

items = [
    {"id": 1, "name": "Item1", "address": "Address1"},
    {"id": 2, "name": "Item2", "address": "Address2"},
]


@asynccontextmanager
async def lifespan():
    """
    Asynchronous context manager for handling application startup and shutdown.
    This replaces the deprecated app.on_event("startup") and app.on_event("shutdown").
    """
    async def background_task():
        """
        A simple background task that appends to the `items` list every 10 seconds.
        """
        i = 3
        while True:
            await asyncio.sleep(10)  # Use asyncio.sleep for asynchronous delays
            items.append({"id": i, "name": f"Item{i}", "address": f"Address{i}"})
            i += 1

    task = asyncio.create_task(background_task())  # Start the background task

    yield  # This is where the app runs

    # --- Shutdown logic (if needed) ---
    # Optional:  If you need to perform cleanup tasks on shutdown, put them here
    # For example, you might want to cancel the background task:
    task.cancel()
    try:
        await task  # Wait for the task to cancel (or handle cancellation error)
    except asyncio.CancelledError:
        pass



app = FastAPI(lifespan=lifespan)  # Pass the lifespan function to the FastAPI app


@app.get("/items/")
async def read_items():
    return items


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
