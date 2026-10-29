from app.schemas.task import Task, CreateOrUpdateTask
from app.db_local.db import DBLocal

# Classe na qual será utilizado nas rotas para fazer consultas / adição / atualização / deleção diretamente do banco de dados.
class TasksRepository:
    def __init__(self, db: DBLocal):
        self.db = db

    # Responsavel por listar todas as tarefas através do select * from tasks
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
                     is_active=row[4],
                     priority=row[5])
                     for row in rows
            ]
            return tasks

    # Responsavel pela pesquisa de uma tarefa em especifico através do ID direto por código em sql
    async def search_task(self, task_id: int) -> Task | None:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row:
                return Task(id_=row[0], task_name=row[1], description=row[2], date=row[3], is_active=row[4], priority=row[5])
            return None

    # Responsavel por filtrar as tarefas a partir das prioridades delas
    async def search_task_by_priority(self, task_priority: int) -> list[Task]:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE priority = ?", (task_priority,))
            rows = cursor.fetchall()
 
            tasks = [
                Task(id_=row[0],
                        task_name=row[1],
                        description=row[2],
                        date=row[3],
                        is_active=row[4],
                        priority=row[5])
                        for row in rows
            ]

            return tasks

    # Responsavel por filtrar as tarefas a partir de seus status
    async def search_task_by_status(self, task_status: bool) -> list[Task] | None:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE is_active = ?", (task_status,))
            rows = cursor.fetchall()
            tasks = [
                Task(id_=row[0],
                        task_name=row[1],
                        description=row[2],
                        date=row[3],
                        is_active=row[4],
                        priority=row[5])
                        for row in rows
            ]
            if tasks:
                return tasks
            return None

    # Responsavel por adicionar uma tarefa no banco de dados.
    async def add_task(self, task: CreateOrUpdateTask) -> Task:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task_name, description, date, is_active, priority) VALUES (?,?,?,?, ?)", (task.task_name, task.description, task.date, task.is_active, task.priority,))
            task_id = cursor.lastrowid
            return Task(id_=task_id, task_name=task.task_name, description=task.description, date=task.date, is_active=task.is_active, priority=task.priority)

    # Responsavel por atualizar uma tarefa em espeficifico através do ID de uma tarefa
    async def update_task(self, task_id:int, task: CreateOrUpdateTask) -> Task | None:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET task_name = ?, description = ?, date = ?, is_active = ?, priority = ? WHERE id = ?", (task.task_name, task.description, task.date, task.is_active, task.priority, task_id,))
            if cursor.rowcount == 0:
                return None
            return Task(id_=task_id, task_name=task.task_name, description=task.description, date=task.date, is_active=task.is_active, priority=task.priority)

    # Responsável por deletar uma tarefa em especifico através do ID de uma tarefa
    async def delete_task(self, task_id: int) -> bool | None:
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            if cursor.rowcount < 0:
                return None
            return cursor.rowcount > 0