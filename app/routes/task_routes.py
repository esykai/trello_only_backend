from fastapi import APIRouter, HTTPException

from app.models import Task, TaskInDB
from app.services.task_service import TaskService

router = APIRouter()

task_service = TaskService()


@router.post("/tasks/", response_model=TaskInDB)
async def create_task(task: Task):
    """
    Создание новой задачи.

    :param task: Объект задачи, который будет создан.
    :return: Созданная задача.
    """
    return await task_service.create_task(task)

@router.get("/tasks/{task_id}", response_model=TaskInDB)
async def get_task(task_id: str):
    """
    Получение задачи по идентификатору.

    :param task_id: Идентификатор задачи.
    :return: Задача, если найдена, иначе ошибка 404.
    """
    task = await task_service.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.put("/tasks/{task_id}", response_model=TaskInDB)
async def update_task(task_id: str, task: Task):
    """
    Обновление задачи по идентификатору.

    :param task_id: Идентификатор задачи для обновления.
    :param task: Обновленные данные задачи.
    :return: Обновленная задача, если обновление успешно, иначе ошибка 404.
    """
    updated_task = await task_service.update_task(task_id, task)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task

@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """
    Удаление задачи по идентификатору.

    :param task_id: Идентификатор задачи для удаления.
    :return: Статус 204, если задача была удалена, иначе ошибка 404.
    """
    if not await task_service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
