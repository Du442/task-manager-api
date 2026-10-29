from fastapi import Depends
from typing import Annotated

from app.db_local.db import DBLocal
from app.repositories.task import TasksRepository

db = DBLocal()

def catch_db() -> DBLocal:
    return db

def catch_task_repository(
        db_local: Annotated[DBLocal,
                           Depends(catch_db)]
) -> TasksRepository:
    return TasksRepository(db_local)

# -- repositório centralizado para funções e classes de injeção de dependência --