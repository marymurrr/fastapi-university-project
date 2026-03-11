from fastapi import FastAPI
from routers import users, items, auth
from models import Order  # нужен для orders
from database import engine, Base
from routers import tasks
import models_task




app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(tasks.router)


# Подключаем роутеры
app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth.router)

# Root
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Orders (оставляем здесь, т.к. все модели в models.py)
@app.post("/orders")
def create_order(order: Order):
    city = order.shipping_address.city
    return {"city": city, "items_count": len(order.items)}