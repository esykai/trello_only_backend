from typing import Optional
from bson import ObjectId, errors
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.models import TaskInDB, Task


class TaskRepository:
    """
    Репозиторий для взаимодействия с коллекцией 'tasks' в MongoDB.
    Предоставляет методы для создания, чтения, обновления и удаления задач.
    """

    def __init__(self):
        """
        Инициализирует репозиторий задач с клиентом MongoDB и настраивает
        базу данных и коллекцию для работы с задачами.
        """
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client["tasks_db"]
        self.collection = self.db.tasks

    async def get_task_by_id(self, task_id: str) -> Optional[TaskInDB]:
        """
        Получает задачу по ее идентификатору.

        :param task_id: Идентификатор задачи в виде строки.
        :return: Задача в формате TaskInDB, если задача найдена, иначе None.
        """
        try:
            task = await self.collection.find_one({"_id": ObjectId(task_id)})
        except errors.InvalidId:
            return None

        if task:
            return TaskInDB(id=str(task["_id"]), **task)

        return None

    async def create_task(self, task: Task) -> TaskInDB:
        """
        Создает новую задачу.

        :param task: Объект задачи, который нужно создать.
        :return: Созданная задача в формате TaskInDB.
        """
        task_dict = task.model_dump(exclude_unset=True)
        result = await self.collection.insert_one(task_dict)
        task_in_db = TaskInDB(**task.model_dump(), id=str(result.inserted_id))

        return task_in_db

    async def update_task(self, task_id: str, task: Task) -> Optional[TaskInDB]:
        """
        Обновляет задачу по идентификатору.

        :param task_id: Идентификатор задачи, которую нужно обновить.
        :param task: Обновленные данные задачи в формате TaskInDB.
        :return: Обновленная задача в формате TaskInDB, если задача была обновлена, иначе None.
        """
        try:
            updated = await self.collection.update_one(
                {"_id": ObjectId(task_id)}, {"$set": task.model_dump(exclude_unset=True)}
            )
        except errors.InvalidId:
            return None

        if updated.modified_count:
            return await self.get_task_by_id(task_id)

        return None

    async def delete_task(self, task_id: str) -> bool:
        """
        Удаляет задачу по идентификатору.

        :param task_id: Идентификатор задачи, которую нужно удалить.
        :return: True, если задача была удалена, иначе False.
        """
        try:
            result = await self.collection.delete_one({"_id": ObjectId(task_id)})
        except errors.InvalidId:
            return False

        return result.deleted_count > 0
