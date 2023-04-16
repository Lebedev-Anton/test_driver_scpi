from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    PROJECT_NAME: str = 'Test project'
    APP_HOST: str = '127.0.0.1'
    APP_PORT: int = 8000


settings = Settings()
