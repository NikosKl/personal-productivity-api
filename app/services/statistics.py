from datetime import timedelta
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.habit import Habits
from app.models.habit_logs import HabitLogs
from app.models.task import Task
from app.models.user import User
from app.schemas.stats import TaskStats
from app.services.habits import HabitNotFoundError


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

def get_habit_streak(db: Session, user: User, habit_id: int) -> int:

    stmt = select(Habits).where(Habits.id == habit_id, Habits.user_id == user.id)

    habit = db.scalar(stmt)

    if habit is None:
        raise HabitNotFoundError()

    stmt = select(HabitLogs.log_date).where(HabitLogs.habit_id == habit.id, HabitLogs.user_id == user.id).order_by(HabitLogs.log_date.desc())

    log_dates = db.scalars(stmt).all()

    if not log_dates:
        return 0

    streak = 0

    if habit.frequency == "daily":
        expected_date = log_dates[0]
        for day in log_dates:
            if day == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            else:
                break
        return streak

    if habit.frequency == "weekly":
        start_of_week = []

        for day in log_dates:
            week_start = day - timedelta(days=day.weekday())
            if week_start not in start_of_week:
                start_of_week.append(week_start)

        expected_week = start_of_week[0]
        for day in start_of_week:
            if day == expected_week:
                streak += 1
                expected_week -= timedelta(days=7)
            else:
                break
        return streak
    return 0