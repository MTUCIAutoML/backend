from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_ADDR: str = '172.16.1.10'
    DB_PORT: int = 5432
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = 'password'
    DB_NAME: str = "automl"

    SERVER_ADDR: str = "localhost"
    SERVER_PORT: int = 8000
    SERVER_TEST: bool = True

    class Config:
        env_file = "../.env"


settings = Settings()
