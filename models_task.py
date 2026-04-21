from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# 1. ТАБЛИЦА-МОСТ (Association Table)
# Она не видна пользователю, в ней просто две колонки: 
# "какая задача" и "какой тег". Без неё связь "многие ко многим" не сработает.
task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id",  ForeignKey("tags.id"),  primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String(20), default="user") # Роль: admin или user

    tasks = relationship("Task", back_populates="author", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), default="")
    done = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="tasks")
    
    # 2. СВЯЗЬ С ТЕГАМИ
    # Мы говорим SQLAlchemy: "смотри в таблицу task_tags, чтобы найти теги для этой задачи"
    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # Обратная связь: чтобы по тегу можно было найти все задачи
    tasks = relationship("Task", secondary=task_tags, back_populates="tags")