from fastapi import FastAPI
from app.routes import tasks

# Definição de aplicação
app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="Tasks CRUD"
)

# Incluindo o router de tasks na aplicação
app.include_router(tasks.router)

# Health check para verificação se o app está funcionante
@app.get("/")
async def health_check():
    return {"message": "OK"}