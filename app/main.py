from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from app.schemas import TaskCreate, TaskUpdate, TaskInDB
from app.crud import create_task, get_task, get_tasks, update_task, delete_task
from app.database import init_db, close_db

app = FastAPI()

# Указываем папку, где будут храниться HTML-шаблоны
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.on_event("shutdown")
async def on_shutdown():
    await close_db()


# 📌 Главная страница с HTML-списком задач
# @app.get("/", response_class=HTMLResponse, name="index")
@app.get("/", response_class=HTMLResponse)
@app.get("/tasks/", response_class=HTMLResponse)
async def tasks_html(request: Request):
    tasks = await get_tasks()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})


# 📌 API-версия получения всех задач (JSON)
# @app.get("/api/tasks/", response_model=list[TaskInDB])
# async def read_tasks():
#     return await get_tasks()

# 📌 Страница редактирования задачи
@app.get("/tasks/{task_id}/edit", response_class=HTMLResponse, name="edit_task")
async def edit_task(task_id: int, request: Request):
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("edit_task.html", {"request": request, "task": task})


# 📌 Обновление задачи через HTML-форму
@app.post("/tasks/{task_id}/edit", response_class=HTMLResponse, name="update_task")
async def update_task_view(
        request: Request,
        task_id: int,
        title: str = Form(...),
        description: str = Form(...),
        progress: int = Form(...)
):
    updated_task = await update_task(task_id, TaskUpdate(title=title, description=description, progress=progress))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return RedirectResponse(url=app.url_path_for("tasks_html"), status_code=303)


# 📌 API-версия получения одной задачи (JSON)
@app.get("/api/tasks/{task_id}", response_model=TaskInDB)
async def read_task(task_id: int):
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# 📌 API-добавление новой задачи
@app.post("/api/tasks/", response_model=TaskInDB)
async def create_new_task(task: TaskCreate):
    return await create_task(task)


# 📌 API-обновление задачи
@app.put("/api/tasks/{task_id}", response_model=TaskInDB)
async def update_existing_task(task_id: int, task: TaskUpdate):
    updated_task = await update_task(task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


# 📌 API-удаление задачи
@app.delete("/api/tasks/{task_id}", response_model=TaskInDB)
async def delete_existing_task(task_id: int):
    deleted_task = await delete_task(task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
