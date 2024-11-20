from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс для загрузки конфигурационных настроек из .env файла.
    Использует pydantic для валидации и загрузки переменных окружения.
    """
    MONGO_URI: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    class Config:
        """
        Конфигурация для загрузки переменных окружения из файла .env.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
