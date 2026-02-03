from datetime import datetime
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=3)

class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    priority: int
    status: str
    created_at: datetime

    model_config = {
        'from_attributes': True}