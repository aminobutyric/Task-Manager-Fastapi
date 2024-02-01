from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskDB(TaskBase):
    id: int

    class Config:
        from_attributes = True

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: datetime
    completed: bool

    class Config:
        from_attributes = True