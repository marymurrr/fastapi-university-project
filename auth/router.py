from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models_task import User  
from auth.security import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/auth", tags=["auth"])

# User Registration Endpoint
@router.post("/register", status_code=201)
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # 1. Verify if the email address is already in use
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Initialize new user instance with hashed password for security
    new_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role="admin"
    )
    
    # 3. Persist the user record to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

# Authentication Endpoint: Generates JWT Access Token
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Query user credentials from the database by username
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # Validate user existence and password hash integrity
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate and return a signed JWT access token
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}