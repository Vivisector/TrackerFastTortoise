"""
main.py - основной файл FastAPI-приложения.
Определяет маршруты API и рендеринг HTML-страниц.
"""

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from app.schemas import TaskCreate, TaskUpdate, TaskInDB
from app.crud import create_task, get_task, get_tasks, update_task, delete_task
from app.database import init_db, close_db
from app.models import Task

app = FastAPI()

# Указываем папку, где будут храниться HTML-шаблоны
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
async def on_startup():
    """Инициализирует подключение к базе данных при старте приложения."""
    await init_db()


@app.on_event("shutdown")
async def on_shutdown():
    """Закрывает соединение с базой данных при завершении работы приложения."""
    await close_db()


@app.get("/", response_class=HTMLResponse)
@app.get("/tasks/", response_class=HTMLResponse)
async def tasks_html(request: Request, page: int = 1, limit: int = 5):
    total_tasks = await Task.all().count()  # Общее количество задач
    total_pages = (total_tasks + limit - 1) // limit  # Округление вверх

    tasks = await Task.all().offset((page - 1) * limit).limit(limit)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tasks": tasks,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "has_previous": page > 1,
            "has_next": page < total_pages,
            "previous_page": page - 1 if page > 1 else None,
            "next_page": page + 1 if page < total_pages else None,
        }
    )

# async def tasks_html(request: Request):
#     """
#     Отображает главную страницу со списком задач в формате HTML.
#
#     :param request: Объект запроса.
#     :return: HTML-страница со списком задач.
#     """
#     tasks = await get_tasks()
#     return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})


@app.get("/tasks/{task_id}/edit", response_class=HTMLResponse, name="edit_task")
async def edit_task(task_id: int, request: Request):
    """
    Отображает страницу редактирования задачи.

    :param task_id: Идентификатор задачи.
    :param request: Объект запроса.
    :return: HTML-страница редактирования задачи.
    """
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("edit_task.html", {"request": request, "task": task})


@app.post("/tasks/{task_id}/complete", name="complete_task")
async def complete_task(task_id: int):
    """
    Помечает задачу как завершенную (устанавливает статус 'done' и прогресс 100%).

    :param task_id: Идентификатор задачи.
    :return: Перенаправление на страницу со списком задач.
    """
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = 'done'
    task.progress = 100
    await task.save()

    return RedirectResponse(url=app.url_path_for("tasks_html"), status_code=303)


@app.post("/tasks/{task_id}/edit", response_class=HTMLResponse, name="update_task")
async def update_task_view(
        request: Request,
        task_id: int,
        title: str = Form(...),
        description: str = Form(...),
        progress: int = Form(...)
):
    """
    Обрабатывает форму редактирования задачи и обновляет ее в базе данных.

    :param request: Объект запроса.
    :param task_id: Идентификатор задачи.
    :param title: Новое название задачи.
    :param description: Новое описание задачи.
    :param progress: Новый прогресс выполнения задачи.
    :return: Перенаправление на страницу со списком задач.
    """
    updated_task = await update_task(task_id, TaskUpdate(title=title, description=description, progress=progress))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return RedirectResponse(url=app.url_path_for("tasks_html"), status_code=303)


@app.get("/tasks/new", response_class=HTMLResponse)
async def create_task_form(request: Request):
    """
    Отображает страницу создания новой задачи.

    :param request: Объект запроса.
    :return: HTML-страница формы создания задачи.
    """
    return templates.TemplateResponse("create_task.html", {"request": request})


@app.post("/tasks/new", response_class=HTMLResponse)
async def create_task_form_post(request: Request):
    """
    Обрабатывает форму создания новой задачи и сохраняет ее в базе данных.

    :param request: Объект запроса.
    :return: Перенаправление на страницу со списком задач.
    """
    form_data = await request.form()
    title = form_data.get("title")
    description = form_data.get("description")

    task_data = TaskCreate(title=title, description=description)
    await create_task(task_data)

    return RedirectResponse(url=app.url_path_for("tasks_html"), status_code=303)


@app.get("/api/tasks/{task_id}", response_model=TaskInDB)
async def read_task(task_id: int):
    """
    Возвращает данные конкретной задачи в формате JSON.

    :param task_id: Идентификатор задачи.
    :return: Объект задачи в формате JSON.
    """
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/api/tasks/", response_model=TaskInDB)
async def create_new_task(task: TaskCreate):
    """
    Создает новую задачу через API.

    :param task: Данные новой задачи.
    :return: Объект созданной задачи в формате JSON.
    """
    return await create_task(task)


@app.put("/api/tasks/{task_id}", response_model=TaskInDB)
async def update_existing_task(task_id: int, task: TaskUpdate):
    """
    Обновляет существующую задачу через API.

    :param task_id: Идентификатор задачи.
    :param task: Данные для обновления.
    :return: Обновленный объект задачи в формате JSON.
    """
    updated_task = await update_task(task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@app.delete("/api/tasks/{task_id}", response_model=TaskInDB)
async def delete_existing_task(task_id: int):
    """
    Удаляет задачу через API.

    :param task_id: Идентификатор задачи.
    :return: Удаленный объект задачи в формате JSON.
    """
    deleted_task = await delete_task(task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
