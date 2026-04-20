from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth.security import decode_token
from jose import JWTError
from sqlalchemy.orm import Session
from database import get_db
import models_task

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        # Извлекаем "sub" (subject) из токена
        user_identifier = payload.get("sub")
        
        if not user_identifier:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        # 1. Сначала пробуем найти по ID (если в токене число)
        user = db.query(models_task.User).filter(models_task.User.id == user_identifier).first()
        
        # 2. Если не нашли, пробуем по имени (если в токене строка)
        if not user:
            user = db.query(models_task.User).filter(models_task.User.username == user_identifier).first()
            
        if not user:
            print(f"DEBUG: User with identifier {user_identifier} not found in DB") # Это появится в терминале
            raise HTTPException(status_code=401, detail="User not found")
            
        return user
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")