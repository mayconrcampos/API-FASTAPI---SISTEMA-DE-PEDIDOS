"""
    Configuração da API
"""
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = os.getenv("DB_URL")
    DB_URL_TESTS: str = os.getenv("DB_URL_TESTS")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60 * 24 # 1 dia

    class Config:
        case_sensitive = True
        env_file = ".env"

settings: Settings = Settings()
