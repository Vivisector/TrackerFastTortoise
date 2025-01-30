"""
database.py - управление подключением к базе данных
"""

from tortoise import Tortoise

DATABASE_URL = "sqlite://db.sqlite3"  # Используем SQLite для простоты

async def init_db():
    """
    Инициализирует подключение к базе данных и создает схемы, если их нет.
    """
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()

async def close_db():
    """
    Закрывает соединение с базой данных.
    """
    await Tortoise.close_connections()
