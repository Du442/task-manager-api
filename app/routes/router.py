from fastapi import APIRouter
from app.routes.v1.endpoints import tasks

api_router = APIRouter()

# Registra o endpoint de tarefas sob a URL /tasks
api_router.include_router(
    tasks.router, 
    prefix="/tasks", 
    tags=["Tasks"]
)