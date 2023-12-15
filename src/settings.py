from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_ADDR: str = 'db'
    DB_PORT: int = 5432
    DB_USERNAME: str = 'postgres'
    DB_PASSWORD: str
    DB_NAME: str

    SERVER_ADDR: str = '0.0.0.0'
    SERVER_PORT: int = 8000
    SERVER_TEST: bool = True

    class Config:
        env_file = "../.env"


settings = Settings()
