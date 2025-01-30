"""
models.py - определение моделей данных для работы с БД.
"""

from tortoise import fields
from tortoise.models import Model
from datetime import datetime

class Task(Model):
    """
    Модель задачи (Task) для хранения данных в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор задачи (Primary Key).
        title (str): Название задачи (максимальная длина — 255 символов).
        description (str | None): Описание задачи (может быть пустым).
        status (str): Статус задачи (по умолчанию "to_do").
        created_at (datetime): Дата и время создания задачи (по умолчанию текущее время).
        updated_at (datetime): Дата и время последнего обновления задачи (автообновление при изменении).
        progress (int): Прогресс выполнения задачи (от 0 до 100, по умолчанию 0).

    Метаданные:
        table (str): Название таблицы в базе данных ("tasks_task").
    """

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=True)
    status = fields.CharField(max_length=20, default="to_do", null=False)
    created_at = fields.DatetimeField(default=datetime.utcnow, null=False)
    updated_at = fields.DatetimeField(default=datetime.utcnow, on_update=datetime.utcnow, null=False)
    progress = fields.IntField(default=0, null=False)

    class Meta:
        table = "tasks_task"
