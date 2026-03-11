from fastapi import FastAPI
from database import engine, Base
from models import Order  # для заказов
from routers import users, items, tasks
from auth.router import router as auth_router  # JWT логин

app = FastAPI()

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Подключаем роутеры
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth_router)  # эндпоинт /auth/token

# Root
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Orders (оставляем здесь, т.к. все модели в models.py)
@app.post("/orders")
def create_order(order: Order):
    city = order.shipping_address.city
    return {"city": city, "items_count": len(order.items)}