from concurrent.futures import ThreadPoolExecutor
from time import sleep

from fastapi import FastAPI

app = FastAPI()

items = [
    {"id": 1, "name": "Item1", "address": "Address1"},
    {"id": 2, "name": "Item2", "address": "Address2"},
]

@app.get("/items/")
async def read_items():
    return items

i = 3
while True:

    #generate_points
    #generate_locations
    #generaate_objects
    sleep(10)
    items.append({"id": i, "name": f"Item{i}", "address": f"Address{i}"})
    i += 1