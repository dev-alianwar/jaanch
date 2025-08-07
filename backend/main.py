from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="React Native + FastAPI Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory storage (use a database in production)
items_db = []
next_id = 1

@app.get("/")
async def root():
    return {"message": "Welcome to React Native + FastAPI Backend"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/items", response_model=List[ItemResponse])
async def get_items():
    return items_db

@app.post("/api/items", response_model=ItemResponse)
async def create_item(item: Item):
    global next_id
    new_item = ItemResponse(
        id=next_id,
        name=item.name,
        description=item.description
    )
    items_db.append(new_item.dict())
    next_id += 1
    return new_item

@app.get("/api/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

@app.delete("/api/items/{item_id}")
async def delete_item(item_id: int):
    global items_db
    items_db = [item for item in items_db if item["id"] != item_id]
    return {"message": "Item deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)