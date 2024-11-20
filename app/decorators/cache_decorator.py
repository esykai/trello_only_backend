import json
import logging

from functools import wraps
from typing import Callable

from app.models import TaskInDB
from app.repositories.redis_cache import RedisCache

logging.basicConfig(level=logging.INFO)


def cache_task(func: Callable):
    @wraps(func)
    async def wrapper(self, task_id: str):
        redis_cache = RedisCache()

        cached = await redis_cache.get_cache(task_id)
        if cached:
            logging.info(f"Кэширование сработало: Задача {task_id} извлечена из кэша.")
            return TaskInDB(**json.loads(cached))

        result = await func(self, task_id)

        if result:
            result_json = json.dumps(result.dict())
            await redis_cache.set_cache(task_id, result_json)
            logging.info(f"Кэширование сработало: Задача {task_id} сохранена в кэш.")

        return result

    return wrapper