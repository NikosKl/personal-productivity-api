from datetime import datetime, date
from typing import Literal
from pydantic import BaseModel

class HabitCreate(BaseModel):
    name: str
    frequency: Literal['daily', 'weekly']

class HabitUpdate(BaseModel):
    name: str | None = None
    frequency: Literal['daily', 'weekly'] | None = None
    is_active: bool | None = None

class HabitRead(BaseModel):
    id: int
    name: str
    frequency: Literal['daily', 'weekly']
    is_active: bool
    created_at: datetime

    model_config = {'from_attributes': True}

class HabitLogCreate(BaseModel):
    log_date: date | None = None

class HabitLogRead(BaseModel):
    id: int
    habit_id: int
    log_date: date
    created_at: datetime

    model_config = {'from_attributes': True}