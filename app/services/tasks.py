from sqlalchemy import select
from typing import cast
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate

class TaskNotFoundError(Exception):
    """Raised when a task is not found"""
    pass

def create_task(db: Session, user: User, task_data: TaskCreate) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        status='pending',
        user_id = user.id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_user_tasks(db: Session, user: User) -> list[Task]:
    stmt = select(Task).where(Task.user_id == user.id)

    tasks = cast(list[Task], db.scalars(stmt).all())
    return tasks

def update_task(db: Session, user: User, task_id: int, task_data: TaskUpdate) -> Task:

    stmt = select(Task).where(
        Task.id == task_id,
        Task.user_id == user.id,
    )

    task = db.scalar(stmt)

    if task is None:
        raise TaskNotFoundError('Task not found')

    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task

def delete_task(db: Session, user: User, task_id: int) -> None:
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user.id)

    task = db.scalar(stmt)

    if task is None:
        raise TaskNotFoundError('Task not found')

    db.delete(task)
    db.commit()
