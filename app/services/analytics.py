from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.habit import Habits
from app.models.habit_logs import HabitLogs
from app.models.user import User
from app.schemas.analytics import TaskSummary, HabitSummary, ProductivitySummary
from app.services.statistics import get_task_stats, get_habit_streak


def get_task_summary(db: Session, user: User) -> TaskSummary:
   task_stats = get_task_stats(db, user)

   stats = TaskSummary(
       total=task_stats.total,
       pending=task_stats.pending,
       completed=task_stats.completed,
       completion_rate=task_stats.completion_rate
   )
   return stats

def get_habit_summary(db: Session, user: User) -> HabitSummary:
    id_validation = Habits.user_id == user.id
    log_validation = HabitLogs.user_id == user.id
    stmt = select(func.count(Habits.id)).where(id_validation)
    total = db.scalar(stmt)
    stmt = select(func.count(Habits.id)).where(id_validation, Habits.is_active == True)
    active = db.scalar(stmt)
    stmt = select(func.count(HabitLogs.log_date)).where(log_validation)
    total_logs = db.scalar(stmt)
    longest_streak = get_max_habit_streak(db, user)

    return HabitSummary(
        total=total,
        active=active,
        total_logs=total_logs,
        longest_streak=longest_streak,
    )

def get_max_habit_streak(db: Session, user: User) -> int:
    id_validation = Habits.user_id == user.id
    stmt = select(Habits.id).where(id_validation)

    habit = db.scalars(stmt).all()

    max_streak = 0

    for habit_id in habit:
        streak = get_habit_streak(db, user, habit_id)
        max_streak = max(max_streak, streak)
    return max_streak

def get_productivity_summary(db: Session, user: User) -> ProductivitySummary:
    tasks = get_task_summary(db, user)
    habits = get_habit_summary(db, user)

    return ProductivitySummary(
        tasks=tasks,
        habits=habits
    )



