from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    id_: int
    task_name: str
    description: str
    date: datetime
    is_active: bool
    priority: int

class CreateOrUpdateTask(BaseModel):
    task_name: str
    description: str
    date: datetime
    is_active: bool
    priority: int

# -- Modelos das tarefas com Pydantic --