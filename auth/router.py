from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

fake_users = {
    "anna": {"username": "anna", "hashed_password": "$2b$12$..."}  # bcrypt hash
}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}