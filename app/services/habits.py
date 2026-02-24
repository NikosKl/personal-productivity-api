from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.habit import Habits
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitUpdate


class HabitNotFoundError(Exception):
    """Raised when a habit is not found"""
    pass

class HabitAlreadyLoggedError(Exception):
    """Raised when a habit is already logged in"""
    pass

def create_habit(db: Session, user: User, habit_data: HabitCreate) -> Habits:
    habit = Habits(
        name=habit_data.name,
        frequency=habit_data.frequency,
        user_id=user.id
    )

    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit

def get_user_habits(db: Session, user: User) -> list[Habits]:
    stmt = select(Habits).where(Habits.user_id == user.id)

    habits = list(db.scalars(stmt))
    return habits

def update_habit(db: Session, user: User, habit_id: int, habit_data: HabitUpdate) -> Habits:
    stmt = select(Habits).where(Habits.id == habit_id, Habits.user_id == user.id)

    habit = db.scalar(stmt)

    if habit is None:
        raise HabitNotFoundError('Habit not found')

    for field, value in habit_data.model_dump(exclude_unset=True).items():
        setattr(habit, field, value)

    db.commit()
    db.refresh(habit)

    return habit

def delete_habit(db: Session, user: User, habit_id: int) -> None:
    stmt = select(Habits).where(Habits.id == habit_id, Habits.user_id == user.id)

    habit = db.scalar(stmt)

    if habit is None:
        raise HabitNotFoundError('Habit not found')

    db.delete(habit)
    db.commit()



