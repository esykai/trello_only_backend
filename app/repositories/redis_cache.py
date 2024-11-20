import redis.asyncio as redis

from typing import Optional

from app.config import settings


class RedisCache:
    """
    Класс для работы с кэшем Redis.
    Предоставляет асинхронные методы для получения и установки значений в Redis.
    """
    def __init__(self):
        """
        Инициализирует клиент Redis с параметрами подключения из настроек.
        """
        self.client = None

    async def connect(self):
        """
        Устанавливает соединение с Redis.
        """
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )

    async def get_cache(self, key: str) -> Optional[str]:
        """
        Получает значение из кэша по ключу.

        :param key: Ключ для поиска значения в кэше.
        :return: Значение в виде строки, если ключ найден, иначе None.
        """
        if self.client is None:
            await self.connect()

        if key is None:
            return None

        value = await self.client.get(key)

        if value is None:
            return None

        return value.decode("utf-8")

    async def set_cache(self, key: str, value: str):
        """
        Устанавливает значение в кэш по ключу.

        :param key: Ключ для установки значения.
        :param value: Значение, которое нужно установить в кэш.
        """
        if self.client is None:
            await self.connect()

        if key is None or value is None:
            return

        await self.client.set(key, value)
