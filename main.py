from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import httpx
import time

from database import engine, Base
from models_task import Task, User, Tag
from routers import tasks  # Проверь, что этот файл точно существует!
from auth.router import router as auth_router

app = FastAPI()

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Подключаем роутер ТАСКОВ (убедись, что эта строка ОДНА)
app.include_router(tasks.router)
app.include_router(auth_router)

#@app.get("/")
#def read_root():
    #return {"message": "Hello FastAPI"}

# Попробуй зайти по этой ссылке вручную: http://127.0.0.1:8000/tasks/admin/all

app.mount("/", StaticFiles(directory="static", html=True), name="static")  