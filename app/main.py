from fastapi import FastAPI
from app.routes import tasks

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="Tasks CRUD"
)

app.include_router(tasks.router)

@app.get("/")
async def health_check():
    return {"message": "OK"}