from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.schemas import TaskCreate, TaskUpdate, TaskInDB
from app.crud import create_task, get_task, get_tasks, update_task, delete_task
from app.database import init_db, close_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.on_event("shutdown")
async def on_shutdown():
    await close_db()

@app.get("/")
@app.get("/tasks/", response_model=list[TaskInDB])
async def read_tasks():
    return await get_tasks()

@app.post("/tasks/", response_model=TaskInDB)
async def create_new_task(task: TaskCreate):
    return await create_task(task)

@app.get("/tasks/", response_model=list[TaskInDB])
async def read_tasks():
    return await get_tasks()

@app.get("/tasks/{task_id}", response_model=TaskInDB)
async def read_task(task_id: int):
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskInDB)
async def update_existing_task(task_id: int, task: TaskUpdate):
    updated_task = await update_task(task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}", response_model=TaskInDB)
async def delete_existing_task(task_id: int):
    deleted_task = await delete_task(task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
