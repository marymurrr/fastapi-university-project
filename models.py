
from pydantic import BaseModel, Field, EmailStr
from typing import List

#ITEM

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    description: str | None = None

#USER
class User(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(ge=18, le=120)
    bio: str = Field(default="", max_length=500)

#RESPONS MODELS
class UserCreate(BaseModel):
    username: str 
    password: str

class UserPublic(BaseModel):
    id: int
    username: str

#MODELS
class Address(BaseModel):
    street:str
    city: str
    postal_code: str

class Order(BaseModel):
    customer_name: str
    shipping_address: Address
    items: List[str]
    total: float

