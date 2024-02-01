from fastapi import FastAPI
from app.routers import task
from app.db import engine

app = FastAPI()

# Include the task router
app.include_router(task.router, prefix="/v1")
