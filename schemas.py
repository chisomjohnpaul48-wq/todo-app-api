from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

class TodoUpdate(BaseModel):
    title: str
    description: str
    completed: bool = False