from fastapi import APIRouter
from models import Item

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.get("/")
def get_items(skip: int = 0, limit: int = 10, search: str | None = None):
    return {"skip": skip, "limit": limit, "search": search}

@router.post("/")
def create_item(item: Item):
    return {
        "message": f"Dodano: {item.name}",
        "price_with_vat": item.price * 1.23,
        "in_stock": item.in_stock,
        "description": item.description
    }

@router.put("/{id}")
def update_item(id: int):
    return {"id": id, "status": "updated"}

@router.delete("/{id}")
def delete_item(id: int):
    return {"id": id, "status": "deleted"}