from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.models.task import Task, CreateOrUpdateTask
from app.schemas.task import TasksRepository
from app.dependencies import catch_task_repository

# Definição do router
router = APIRouter(
    prefix="/tasks"
)

# Rota de listagem geral das tarefas
@router.get("/", response_model=list[Task])
async def list_tasks(task_repository: Annotated[TasksRepository,
                                                Depends(catch_task_repository)]):
    return await task_repository.list_tasks()

# Rota de pesquisa de uma tarefa em especifico com base no id da tarefa
@router.get("/{task_id}", response_model=Task | None)
async def search_task(task_id: int,
                      task_repository: Annotated[TasksRepository,
                                                 Depends(catch_task_repository)]):
    
    task = await task_repository.search_task(task_id=task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

# Rota de Criação de tarefa
@router.post("/", response_model=Task, status_code=201)
async def add_task(task_repository: Annotated[TasksRepository,
                                              Depends(catch_task_repository)],
                    task: CreateOrUpdateTask):

    return await task_repository.add_task(task=task)

# Rota de Atualizar uma tarefa em especifico através do ID
@router.put("/{task_id}", response_model=Task | None)
async def update_task(task_repository: Annotated[TasksRepository,
                                              Depends(catch_task_repository)],
                      task_id: int,
                      task: CreateOrUpdateTask):
    
    task = await task_repository.update_task(task_id, task)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

# Rota de deletar uma tarefa em especifico através do ID
@router.delete("/{task_id}", status_code=204)
async def delete_task(task_repository: Annotated[TasksRepository,
                                              Depends(catch_task_repository)],
                      task_id: int):
    task = await task_repository.delete_task(task_id=task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task