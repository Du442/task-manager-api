from fastapi import FastAPI

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="Tasks CRUD"
)

@app.get("/")
async def health_check():
    return {"message": "OK"}