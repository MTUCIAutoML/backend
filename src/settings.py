from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_ADDR: str = "postgres"
    DB_PORT: int = 5432
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str
    DB_NAME: str

    AWS_HOST: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: Optional[str] = None
    AWS_BUCKET: str

    SERVER_ADDR: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    SERVER_TEST: bool = True

    class Config:
        env_file = "../.env"


settings = Settings()
