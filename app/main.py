from fastapi import FastAPI

from app.routes.task import router as task_router

app = FastAPI()

app.include_router(task_router)
