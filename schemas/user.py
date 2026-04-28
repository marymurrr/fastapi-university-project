from pydantic import BaseModel, EmailStr

# Schema for user registration data provided by the client
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Schema for public user data returned to the client (excludes sensitive information)
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        # Enables compatibility with SQLAlchemy models (ORM mode)
        from_attributes = True