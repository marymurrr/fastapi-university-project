from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models_task import Task
from auth.deps import get_current_user

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
def list_tasks(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # Проверяем, кто спрашивает
):
    # Фильтруем по твоему ID
    return db.query(Task).filter(Task.author_id == current_user.id).all()


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.post("/", response_model=TaskOut, status_code=201)
def create_task(
    data: TaskCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # 1. Проверяем токен
):
    # 2. Распаковываем данные и ДОБАВЛЯЕМ автора
    task = Task(**data.model_dump(), author_id=current_user.id) 

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskCreate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = data.title
    task.description = data.description

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # Проверяем, кто пришел
):
    # Ищем задачу, которая принадлежит ИМЕННО этому пользователю
    task = db.query(Task).filter(Task.id == task_id, Task.author_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or access denied")

    db.delete(task)
    db.commit()