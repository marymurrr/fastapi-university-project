from pydantic import BaseModel

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    id: int
    # Это нужно, чтобы Pydantic умел читать данные из базы SQLAlchemy
    class Config:
        from_attributes = True