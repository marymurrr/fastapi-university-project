from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import httpx
import time

from database import engine, Base
from models import Order
from routers import users, items, tasks
from auth.router import router as auth_router


app = FastAPI()


# static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML templates
templates = Jinja2Templates(directory="templates")


# create DB tables
Base.metadata.create_all(bind=engine)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AppError(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": exc.message,
            "path": str(request.url)
        }
    )


app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}


@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Moja strona FastAPI",
            "items": ["A", "B", "C"]
        }
    )


@app.get("/sync")
def sync_endpoint():
    time.sleep(2)
    return {"message": "Sync endpoint finished"}


@app.get("/async")
async def async_endpoint():
    async with httpx.AsyncClient() as client:
        await client.get("https://httpbin.org/get")
    return {"message": "Async endpoint finished"}


@app.get("/weather/{city}")
async def get_weather(city: str):

    async with httpx.AsyncClient() as client:

        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 52.52,
                "longitude": 13.41,
                "current_weather": True
            }
        )

        return response.json()


def send_email(email: str, message: str):

    time.sleep(3)

    print(f"Email to {email}: {message}")


@app.post("/register")
def register(email: str, background_tasks: BackgroundTasks):

    background_tasks.add_task(
        send_email,
        email,
        "Welcome!"
    )

    return {"message": "Registration completed"}


@app.get("/items/{item_id}")
def get_item(item_id: int):

    if item_id < 0:
        raise HTTPException(
            status_code=400,
            detail="ID musi być dodatnie"
        )

    if item_id > 1000:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {"id": item_id}


@app.get("/check")
def check():
    raise AppError("Coś poszło nie tak!", code=503)


@app.post("/orders")
def create_order(order: Order):
    city = order.shipping_address.city
    return {
        "city": city,
        "items_count": len(order.items)
    }