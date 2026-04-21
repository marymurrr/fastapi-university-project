from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from database import get_db
from models_task import Task, User, Tag
from auth.deps import get_current_user, require_admin

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

# --- СХЕМЫ (Pydantic) ---
# Сначала TagOut, чтобы TaskOut мог его использовать
class TagOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    tags: list[str] = []  # Список имен тегов, например ["work", "urgent"]

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    done: bool
    tags: list[TagOut] = []  # Теперь теги будут видны в ответе!

    class Config:
        from_attributes = True

# --- ЭНДПОИНТЫ ---

# 1. Получение своих задач (с поиском и пагинацией)
@router.get("/", response_model=list[TaskOut])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    search: str | None = Query(None),
    done: bool | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, le=100)
):
    # .options(joinedload(Task.tags)) подтягивает теги из базы одним запросом
    query = db.query(Task).options(joinedload(Task.tags)).filter(Task.author_id == current_user.id)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))
    if done is not None:
        query = query.filter(Task.done == done)

    skip = (page - 1) * per_page
    return query.offset(skip).limit(per_page).all()

# 2. Создание задачи с тегами
@router.post("/", response_model=TaskOut, status_code=201)
def create_task(
    data: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(
        title=data.title, 
        description=data.description, 
        author_id=current_user.id
    )

    # Логика тегов: ищем существующий или создаем новый
    for tag_name in data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
        new_task.tags.append(tag)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# 3. Обновление задачи
@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int, 
    data: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id, Task.author_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = data.title
    task.description = data.description
    
    # Синхронизация тегов
    task.tags = []
    for tag_name in data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
        task.tags.append(tag)

    db.commit()
    db.refresh(task)
    return task

# 4. Удаление задачи
@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id, Task.author_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None

# 5. АДМИНКА: Все задачи всех пользователей
@router.get("/admin/all", response_model=list[TaskOut])
def get_all_tasks_for_admin(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    # Админ видит всё, включая теги каждой задачи
    return db.query(Task).options(joinedload(Task.tags)).all()