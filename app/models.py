from tortoise import fields
from tortoise.models import Model
from datetime import datetime

class Task(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=True)
    status = fields.CharField(max_length=20, default="to_do", null=False)
    created_at = fields.DatetimeField(default=datetime.utcnow, null=False)
    updated_at = fields.DatetimeField(default=datetime.utcnow, on_update=datetime.utcnow, null=False)
    progress = fields.IntField(default=0, null=False)

    class Meta:
        table = "tasks_task"
