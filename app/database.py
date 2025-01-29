from tortoise import Tortoise

DATABASE_URL = "sqlite://db.sqlite3"  # Используем SQLite для простоты

async def init_db():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()
