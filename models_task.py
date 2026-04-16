from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# 1. ТАБЛИЦА-ПОСРЕДНИК (Сваха)
# Она нужна, чтобы связать Посты и Теги. В базе это будет отдельная таблица.
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id",  ForeignKey("tags.id"),  primary_key=True),
)

# 2. ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String(20), default="user")

    # Тропинка к постам: "Один пользователь -> Много постов"
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

# 3. ТАБЛИЦА ПОСТОВ
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    
    # Бирка с номером автора
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Тропинка к автору: "Пост -> Один автор"
    author = relationship("User", back_populates="posts")
    
    # Тропинка к тегам через "сваху" (secondary)
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")

# 4. ТАБЛИЦА ТЕГОВ
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # Тропинка к постам через ту же "сваху"
    posts = relationship("Post", secondary=post_tags, back_populates="tags")

# 5. ТВОЙ СТАРЫЙ TASK (Задачи)
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), default="")
    done = Column(Boolean, default=False)