"""
crud.py - функции для работы с базой данных (CRUD: Create, Read, Update, Delete)
"""

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from tortoise.exceptions import DoesNotExist

async def create_task(task: TaskCreate):
    """
    Создает новую задачу в базе данных.

    :param task: Объект TaskCreate с данными новой задачи.
    :return: Созданный объект задачи.
    """
    task_obj = await Task.create(**task.dict())
    return task_obj

async def get_task(task_id: int):
    """
    Получает задачу по ID.

    :param task_id: Идентификатор задачи.
    :return: Объект задачи или None, если задача не найдена.
    """
    try:
        return await Task.get(id=task_id)
    except DoesNotExist:
        return None

async def get_tasks():
    """
    Получает список всех задач.

    :return: Список объектов задач.
    """
    return await Task.all()

async def update_task(task_id: int, task: TaskUpdate):
    """
    Обновляет существующую задачу по ID.

    :param task_id: Идентификатор задачи.
    :param task: Объект TaskUpdate с обновленными данными.
    :return: Обновленный объект задачи или None, если задача не найдена.
    """
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
    """
    Удаляет задачу по ID.

    :param task_id: Идентификатор задачи.
    :return: Удаленный объект задачи или None, если задача не найдена.
    """
    try:
        task = await Task.get(id=task_id)
        await task.delete()
        return task
    except DoesNotExist:
        return None
