import functools
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    SECRET_KEY: str
    ALGORITHM: str
    # root_dir: Path = Path(__file__).resolve().parent.parent.parent
    # src_dir: Path = root_dir.joinpath("src")

    PROJECT_NAME: str = "websocket-chat-test"

    USE_CORS_MIDDLEWARE: bool = True

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    # SERVER_WORKERS_COUNT: int = 5

    ENVIRONMENT: str = "local"
    CORS_ALLOW_ORIGIN_LIST: str = "http://localhost:5173"

    POSTGRES_HOST: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "myapp_user"
    POSTGRES_PASSWORD: str = "myapp_password"
    POSTGRES_DB: str = "myapp_db"

    @functools.cached_property
    def postgres_dsn(self) -> str:
        postgres_host = (
            "localhost" if self.ENVIRONMENT == "local" else self.POSTGRES_HOST
        )
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{postgres_host}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@functools.lru_cache()
def settings() -> Settings:
    return Settings()


def get_auth_data():
    return {"secret_key": settings().SECRET_KEY, "algorithm": settings().ALGORITHM}
