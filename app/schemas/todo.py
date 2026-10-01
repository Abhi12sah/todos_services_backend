from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.enums import TodoStatus, TodoPriority


class TodoBase(BaseModel):
    title: str
    description: str | None = None
    status: TodoStatus = TodoStatus.PENDING
    priority: TodoPriority = TodoPriority.MEDIUM
    due_date: datetime | None = None


class TodoCreate(TodoBase):
    user_id: int


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TodoStatus | None = None
    priority: TodoPriority | None = None
    due_date: datetime | None = None


class TodoOut(TodoBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)