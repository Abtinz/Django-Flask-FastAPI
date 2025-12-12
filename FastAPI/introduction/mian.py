from fastapi import FastAPI, HTTPException
from uvicorn import run
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    '''
    Docstring for Task
    '''
    text: str = None
    is_done: bool = False


@app.get("/")
async def root():
    return {"message": "Hello World"}

items = ["banana", "orange", "grape"]

@app.post("/items/")
async def create_item(item: str):
    items.append(item)
    return items

@app.get("/items/")
async def get_items():
    return items

@app.get("/items/{item_id}")
async def get_item(item_id: int) -> str:
    try:
        return items[item_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items", response_model=list[Task])
def list_items(limit: int = 10):
    return items[0:limit]


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)