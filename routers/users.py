from fastapi import APIRouter
from models import UserCreate, UserPublic

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
def list_users():
    return [{"id": 1, "name": "Anna"}]

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}

@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate):
    # пароль здесь не возвращаем, только публичная информация
    return {"id": 1, "username": user.username}