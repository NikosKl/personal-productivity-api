from pydantic import BaseModel

class TaskSummary(BaseModel):
    total: int
    completed: int
    pending: int
    completion_rate: float

class HabitSummary(BaseModel):
    total: int
    active: int
    total_logs: int
    longest_streak: int

class ProductivitySummary(BaseModel):
    tasks: TaskSummary
    habits: HabitSummary