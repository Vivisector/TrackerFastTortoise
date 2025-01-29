from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from tortoise.exceptions import DoesNotExist

async def create_task(task: TaskCreate):
    task_obj = await Task.create(**task.dict())
    return task_obj

async def get_task(task_id: int):
    try:
        task = await Task.get(id=task_id)
        return task
    except DoesNotExist:
        return None

async def get_tasks():
    tasks = await Task.all()
    return tasks

async def update_task(task_id: int, task: TaskUpdate):
    try:
        task_obj = await Task.get(id=task_id)
        task_obj.title = task.title
        task_obj.description = task.description
        task_obj.status = task.status
        task_obj.progress = task.progress
        await task_obj.save()
        return task_obj
    except DoesNotExist:
        return None

async def delete_task(task_id: int):
    try:
        task = await Task.get(id=task_id)
        await task.delete()
        return task
    except DoesNotExist:
        return None
