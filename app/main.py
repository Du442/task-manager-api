from fastapi import FastAPI
from app.routes.router import api_router

# Definição de aplicação
app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="Tasks CRUD"
)

# Incluindo o router de tasks na aplicação
app.include_router(api_router, prefix="/api/v1")

# Health check para verificação se o app está funcionante
@app.get("/")
async def health_check():
    return {"message": "OK"}