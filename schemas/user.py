from pydantic import BaseModel, EmailStr

# Это то, что нам присылает юзер
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Это то, что мы показываем юзеру (без пароля!)
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True