from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate

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
    return db.query(Task).filter(Task.user_id == user.id).all()

