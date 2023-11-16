from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_ADDR: str = 'postgres'
    DB_PORT: int = 5432
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str
    DB_NAME: str = "AutoML"

    SERVER_ADDR: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    SERVER_TEST: bool = False


settings = Settings()
