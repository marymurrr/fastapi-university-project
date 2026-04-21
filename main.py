from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import httpx
import time

from database import engine, Base
from models_task import Task, User, Tag
from routers import users, items, tasks
from auth.router import router as auth_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Создаем таблицы
Base.metadata.create_all(bind=engine)

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
        content={"error": exc.message, "path": str(request.url)}
    )

# Подключаем роутеры
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

@app.get("/weather/{city}")
async def get_weather(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": 52.52, "longitude": 13.41, "current_weather": True}
        )
        return response.json()

@app.get("/check")
def check():
    raise AppError("Coś poszło nie tak!", code=503)