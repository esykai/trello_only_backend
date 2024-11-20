from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    in_progress = "in_progress"

class Task(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    status: TaskStatus = Field(default=TaskStatus.pending)

    class Config:
        use_enum_values = True


class TaskInDB(Task):
    id: str
