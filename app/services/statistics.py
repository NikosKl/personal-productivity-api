from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.user import User
from app.schemas.stats import TaskStats

def get_task_stats(db: Session, user: User) -> TaskStats:
    id_validation = Task.user_id == user.id
    stmt = select(func.count(Task.id)).where(id_validation)
    total = db.scalar(stmt)
    stmt = select(func.count(Task.id)).where(id_validation, Task.status == 'pending')
    pending = db.scalar(stmt)
    stmt = select(func.count(Task.id)).where(id_validation, Task.status == 'completed')
    completed = db.scalar(stmt)

    completion_rate = round((completed / total) * 100, 2) if total > 0 else 0

    stats = TaskStats(
        total=total,
        pending=pending,
        completed=completed,
        completion_rate=completion_rate,
    )
    return stats

