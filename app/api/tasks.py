from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.task import TaskRead, TaskCreate, TaskUpdate
from app.services.tasks import create_task, get_user_tasks, TaskNotFoundError, update_task, delete_task

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskRead)
def create_task_route(task_data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = create_task(db, current_user, task_data)
    return task

@router.get("", response_model=list[TaskRead])
def read_task_route(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_tasks = get_user_tasks(db, current_user)
    return user_tasks

@router.put("/{task_id}", response_model=TaskRead)
def update_task_route(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        task = update_task(db, current_user, task_id, task_data)
        return task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_route(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        delete_task(db, current_user, task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

