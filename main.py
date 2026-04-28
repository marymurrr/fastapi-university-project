from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import httpx
import time

from database import engine, Base
from models_task import Task, User, Tag
from routers import tasks  
from auth.router import router as auth_router

app = FastAPI()

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Register API routers for tasks and authentication
app.include_router(tasks.router)
app.include_router(auth_router)

# Mount static files to serve the frontend application
# Note: StaticFiles should be mounted after routers to avoid path conflicts
app.mount("/", StaticFiles(directory="static", html=True), name="static")