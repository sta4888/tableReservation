from pydantic import BaseModel, BaseSettings, Field, PostgresDsn


class Project(BaseModel):
    """
    Описание проекта.
    """

    #: название проекта
    title: str = "table reservation Service"
    #: описание проекта
    description: str = "Сервис для сохранения любимых мест."
    #: версия релиза
    release_version: str = Field(default="0.1.0")


class Settings(BaseSettings):
    """
    Настройки проекта.
    """

    #: режим отладки
    debug: bool = Field(default=False)
    #: уровень логирования
    log_level: str = Field(default="INFO")
    #: описание проекта
    project: Project = Project()
    #: базовый адрес приложения
    base_url: str = Field(default="http://0.0.0.0:8010")
    #: строка подключения к БД
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://table_reservation_user:secret@db/table_reservation"
    )

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


# инициализация настроек приложения
settings = Settings()
