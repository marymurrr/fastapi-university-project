from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.security import decode_token
from jose import JWTError
from sqlalchemy.orm import Session
from database import get_db
import models_task

# Configuration for extracting the Bearer token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency that validates the JWT token and returns the current authenticated user.
    """
    try:
        payload = decode_token(token)
        # Extract the subject (sub) identifier from the JWT payload
        user_identifier = payload.get("sub")
        
        if not user_identifier:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        # 1. Primary lookup: Attempt to find user by unique ID
        user = db.query(models_task.User).filter(models_task.User.id == user_identifier).first()
        
        # 2. Fallback lookup: Attempt to find user by username
        if not user:
            user = db.query(models_task.User).filter(models_task.User.username == user_identifier).first()
            
        if not user:
            # Internal debugging for failed identity resolution
            print(f"DEBUG: User with identifier {user_identifier} not found in DB")
            raise HTTPException(status_code=401, detail="User not found")
            
        return user
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")

# Role-Based Access Control (RBAC) factory
def require_role(required_role: str):
    """
    Factory function to create dependency checkers for specific user roles.
    """
    def role_checker(current_user: models_task.User = Depends(get_current_user)) -> models_task.User:
        # Validate that the authenticated user possesses the required permission level
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied! Required role: {required_role}"
            )
        return current_user
    return role_checker

# Pre-defined dependency for administrative access
require_admin = require_role("admin")