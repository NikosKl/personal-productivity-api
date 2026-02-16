from typing import Literal, Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from starlette import status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.stats import TaskStats
from app.schemas.task import TaskRead, TaskCreate, TaskUpdate
from app.services.statistics import get_task_stats
from app.services.tasks import create_task, get_user_tasks, TaskNotFoundError, update_task, delete_task, complete_task, \
    InvalidTaskStateError, reset_task

router = APIRouter(prefix="/tasks", tags=["Tasks"])

TaskStatusParam = Annotated[Literal['pending', 'completed'] | None, Query(None, description="Filter by status: pending or completed")]

@router.post("", response_model=TaskRead)
def create_task_route(task_data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = create_task(db, current_user, task_data)
    return task

@router.get("", response_model=list[TaskRead])
def read_task_route(
        limit: int = Query(10, gt = 0),
        offset: int = Query(0, ge = 0),
        task_status: TaskStatusParam | None = None,
        order: Literal['asc', 'desc'] = 'desc',
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):

    tasks = get_user_tasks(db, current_user, limit, offset, task_status, order)
    return tasks

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

@router.patch('/{task_id}/complete', response_model=TaskRead)
def complete_task_route(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        task = complete_task(db, current_user, task_id)
        return task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    except InvalidTaskStateError:
        raise HTTPException(status_code=400, detail="Invalid state transition")

@router.patch('/{task_id}/reset', response_model=TaskRead)
def reset_task_route(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        task = reset_task(db, current_user, task_id)
        return task
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    except InvalidTaskStateError:
        raise HTTPException(status_code=400, detail="Invalid state transition")

@router.get('/stats', response_model=TaskStats)
def task_stats_route(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
        task_stats = get_task_stats(db, user)
        return task_stats
