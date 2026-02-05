from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.task import TaskRead, TaskCreate
from app.services.tasks import create_task, get_user_tasks

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskRead)
def create_tasks(task_data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = create_task(db, current_user, task_data)
    return task

@router.get("", response_model=list[TaskRead])
def read_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_tasks = get_user_tasks(db, current_user)
    return user_tasks