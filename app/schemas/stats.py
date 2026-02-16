from pydantic import BaseModel

class TaskStats(BaseModel):
    total: int
    completed: int
    pending: int
    completion_rate: float