from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    redis_host: str
    redis_port: str
    redis_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

from dotenv import load_dotenv
from pydantic import BaseSettings
import os

load_dotenv()

class Settings(BaseSettings):
    database_hostname: str = os.environ.get("DATABASE_HOSTNAME")
    database_port: int = os.environ.get("DATABASE_PORT")
    database_password: str = os.environ.get("DATABASE_PASSWORD")
    database_name: str = os.environ.get("DATABASE_NAME")
    database_username: str = os.environ.get("DATABASE_USERNAME")
    redis_host: str = os.environ.get("REDIS_HOST")
    redis_port: int = os.environ.get("REDIS_PORT")
    redis_password: str = os.environ.get("REDIS_PASSWORD")
    secret_key: str = os.environ.get("SECRET_KEY")
    algorithm: str = os.environ.get("ALGORITHM")
    access_token_expire_minutes: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"


settings = Settings()
