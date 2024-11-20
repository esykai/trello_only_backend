from app.repositories.task_repository import TaskRepository
from app.models import Task
from app.decorators.cache_decorator import cache_task

class TaskService:
    """
    Сервис для работы с задачами.
    Предоставляет методы для получения, создания, обновления и удаления задач,
    с кэшированием для метода получения задачи.
    """
    def __init__(self):
        """
        Инициализация сервиса с репозиторием задач.
        """
        self.repo = TaskRepository()

    @cache_task
    async def get_task(self, task_id: str):
        """
        Получает задачу по идентификатору.
        Кэширует результат с использованием декоратора cache_task.

        :param task_id: Идентификатор задачи.
        :return: Задача, если найдена, или сообщение об ошибке, если задача не найдена.
        """
        task = await self.repo.get_task_by_id(task_id)

        if task:
            return task

        return None

    async def create_task(self, task: Task):
        """
        Создает новую задачу.

        :param task: Объект задачи, который нужно создать.
        :return: Созданная задача.
        """
        return await self.repo.create_task(task)

    async def update_task(self, task_id: str, task: Task):
        """
        Обновляет существующую задачу.

        :param task_id: Идентификатор задачи для обновления.
        :param task: Обновленные данные задачи.
        :return: Обновленная задача, если обновление успешно, иначе None.
        """
        return await self.repo.update_task(task_id, task)

    async def delete_task(self, task_id: str):
        """
        Удаляет задачу по идентификатору.

        :param task_id: Идентификатор задачи для удаления.
        :return: True, если задача была удалена, иначе False.
        """
        return await self.repo.delete_task(task_id)
