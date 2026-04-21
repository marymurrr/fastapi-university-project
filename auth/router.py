from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models_task import User  # Импортируем твою модель пользователя
from auth.security import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/auth", tags=["auth"])

# Эндпоинт для РЕГИСТРАЦИИ
@router.post("/register", status_code=201)
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # 1. Проверяем, нет ли уже такого пользователя в базе
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Создаем нового пользователя
    new_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password), # Хешируем пароль перед сохранением!
        role="admin"
    )
    
    # 3. Сохраняем в базу данных
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

# Эндпоинт для ЛОГИНА (получения токена)
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Ищем пользователя в реальной базе, а не в списке fake_users
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем JWT токен
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}