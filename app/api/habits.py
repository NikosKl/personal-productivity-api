from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.habit import HabitRead, HabitCreate, HabitUpdate, HabitLogRead, HabitLogCreate
from app.services.habits import create_habit, get_user_habits, update_habit, HabitNotFoundError, delete_habit, \
    log_habit, HabitAlreadyLoggedError

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.post("", response_model=HabitRead)
def create_habit_route(habit_data: HabitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = create_habit(db, current_user, habit_data)
    return habit

@router.get("", response_model=list[HabitRead])
def read_habit_route(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = get_user_habits(db, current_user)
    return habit

@router.put("/{habit_id}", response_model=HabitRead)
def update_habit_route(habit_id: int, habit_data: HabitUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        habit = update_habit(db, current_user, habit_id, habit_data)
        return habit
    except HabitNotFoundError:
        raise HTTPException(status_code=404, detail="Habit not found")

@router.delete("/{habit_id}", status_code=HTTP_204_NO_CONTENT)
def delete_habit_route(habit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        delete_habit(db, current_user, habit_id)
    except HabitNotFoundError:
        raise HTTPException(status_code=404, detail="Habit not found")

@router.post("/{habit_id}/log", response_model=HabitLogRead)
def log_habit_route(habit_id: int, log_data: HabitLogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        habit_log = log_habit(db, current_user, habit_id, log_data)
        return habit_log
    except HabitNotFoundError:
        raise HTTPException(status_code=404, detail="Habit not found")
    except HabitAlreadyLoggedError:
        raise HTTPException(status_code=400, detail="Habit already logged")