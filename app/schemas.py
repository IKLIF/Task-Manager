from pydantic import BaseModel, ConfigDict

class Task(BaseModel):
    name: str
    description: str
    status: str

class TaskFilter(BaseModel):
    id: str

class TaskUpdate(BaseModel):
    id: str
    name: str | None = None
    status: str | None = None
    description: str | None = None
