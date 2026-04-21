from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from database import get_db
from models_task import Task, User
from auth.deps import get_current_user, require_admin

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

class TaskCreate(BaseModel):
    title: str
    description: str = ""

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    done: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=list[TaskOut])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    search: str | None = Query(None, description="Поиск по названию"),
    done: bool | None = Query(None, description="Фильтр по статусу"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, le=100)
):
    query = db.query(Task).options(joinedload(Task.tags)).filter(Task.author_id == current_user.id)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    if done is not None:
        query = query.filter(Task.done == done)

    skip = (page - 1) * per_page
    return query.offset(skip).limit(per_page).all()

@router.post("/", response_model=TaskOut, status_code=201)
def create_task(
    data: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = Task(**data.model_dump(), author_id=current_user.id) 
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int, 
    data: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id, Task.author_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")

    task.title = data.title
    task.description = data.description
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id, Task.author_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")
    db.delete(task)
    db.commit()

@router.get("/admin/all")
def get_all_tasks_for_admin(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin) 
):
    return db.query(Task).all()