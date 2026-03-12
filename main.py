from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from models import Order
from routers import users, items, tasks
from auth.router import router as auth_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


# Tworzymy aplikację FastAPI
app = FastAPI()

# Inicjalizujemy Jinja2 do renderowania szablonów HTML
templates = Jinja2Templates(directory="templates")

# Montujemy katalog "static" do serwowania plików statycznych (CSS, JS, obrazy)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Tworzymy tabele w bazie danych jeśli jeszcze nie istnieją
Base.metadata.create_all(bind=engine)

# Endpoint do renderowania strony HTML
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



# CORS pozwala frontendowi (np. React) komunikować się z backendem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # w development można używać "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Własny wyjątek aplikacji
class AppError(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code


# Handler który przechwytuje AppError i zwraca JSON
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": exc.message,
            "path": str(request.url)
        }
    )


# Podłączamy routery z innych plików
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth_router)  # router autoryzacji JWT


# Root endpoint do testu API
@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}


# Przykład standardowego błędu HTTP
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


# Endpoint pokazujący użycie własnego błędu
@app.get("/check")
def check():
    raise AppError("Coś poszło nie tak!", code=503)


# Endpoint do tworzenia zamówienia
@app.post("/orders")
def create_order(order: Order):
    city = order.shipping_address.city
    return {
        "city": city,
        "items_count": len(order.items)
    }