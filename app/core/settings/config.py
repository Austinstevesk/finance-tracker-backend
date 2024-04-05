import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_URL:str = os.getenv("DB_URL")
    ACCESS_TOKEN_EXPIRE_MINUTES:int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    ACCESS_TOKEN_SECRET_KEY: str = os.getenv("ACCESS_TOKEN_SECRET_KEY")
    REFRESH_TOKEN_SECRET_KEY: str = os.getenv("REFRESH_TOKEN_SECRET_KEY")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    # ENVIRONMENT: str = os.getenv("environment", "dev")
    # DB_ADMIN: str = os.getenv("dashboard_admin")
    # DB_PWD: str = os.getenv("dashboard_pwd")
    # DB_HOST: str = os.getenv("dashboard_host")
    # DB_PORT: str = os.getenv("dashboard_port")
    # DATABASE_NAME: str = os.getenv("dashboard_name", "test")


@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()