from fastapi import FastAPI
from models import Item, UserCreate, UserPublic, Address, Order

app = FastAPI()


# Root
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Items
@app.get("/items")
def get_items(skip: int = 0, limit: int = 10, search: str | None = None):
    # Можно расширить для работы с базой/списком
    return {"skip": skip, "limit": limit, "search": search}

@app.post("/items")
def create_item(item: Item):
    return {
        "message": f"Dodano: {item.name}",
        "price_with_vat": item.price * 1.23,
        "in_stock": item.in_stock,
        "description": item.description
    }

@app.put("/items/{id}")
def update_item(id: int):
    return {"id": id, "status": "updated"}

@app.delete("/items/{id}")
def delete_item(id: int):
    return {"id": id, "status": "deleted"}


# Users
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "Anna"}

@app.post("/users", response_model=UserPublic)
def create_user(user: UserCreate):
   return {"id": 1, "username": user.username}

# Orders
@app.post("/orders")
def create_order(order: Order):
    city = order.shipping_address.city
    return {"city": city, "items_count": len(order.items)}

