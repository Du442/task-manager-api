from app.models.task import Task, CreateOrUpdateTask
from app.db_local.db import DBLocal

class TasksRepository:
    def __init__(self, db: DBLocal):
        self.db = db

    async def list_tasks(self) -> list[Task]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            tasks = [
                Task(id_=row[0],
                     task_name=row[1],
                     description=row[2],
                     date=row[3],
                     is_active=row[4])
                     for row in rows
            ]
            return tasks

    async def search_task(self, task_id: int) -> Task | None:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row:
                return Task(id_=row[0], task_name=row[1], description=row[2], date=row[3], is_active=row[4])
            return None

    async def add_task(self, task: CreateOrUpdateTask) -> Task:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task_name, description, date, is_active) VALUES (?,?,?,?)", (task.task_name, task.description, task.date, task.is_active,))
            task_id = cursor.lastrowid
            return Task(id_=task_id, task_name=task.task_name, description=task.description, date=task.date, is_active=task.is_active)

    async def update_task(self, task_id:int, task: CreateOrUpdateTask) -> Task | None:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET task_name = ?, description = ?, date = ?, is_active = ?", (task.task_name, task.description, task.date, task.is_active,))
            if cursor.rowcount == 0:
                return None
            return Task(id_=task_id, task_name=task.task_name, description=task.description, date=task.date, is_active=task.is_active)


    async def delete_task(self, task_id: int) -> bool | None:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            if cursor.rowcount < 0:
                return None
            return cursor.rowcount > 0