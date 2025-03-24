from typing import Any, Dict, Optional, List, Union
from pydantic import PostgresDsn, EmailStr, Field, model_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

class Settings(BaseSettings):
    # API
    SECRET_KEY: str = Field(default=os.getenv("SECRET_KEY"))
    PROJECT_NAME: str = "Todo API"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A FastAPI-based Todo application"

    # Security Settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_ALGORITHM: str = "HS256"

    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database
    POSTGRES_SERVER: str = Field(default=os.getenv("DATABASE_HOST", "localhost"))
    POSTGRES_USER: str = Field(default=os.getenv("DATABASE_USER", "postgres"))
    POSTGRES_PASSWORD: str = Field(default=os.getenv("DATABASE_PASSWORD", "postgres"))
    POSTGRES_PORT: str = Field(default=os.getenv("DATABASE_PORT", "5432"))
    POSTGRES_DB: str = Field(default=os.getenv("DATABASE_NAME", "todo"))

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Email Settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_FILE: Path = Path("logs/todo-app.log")

    # Debug Mode
    DEBUG: bool = False

    # Server Settings
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
    SERVER_RELOAD: bool = True

    @model_validator(mode='before')
    @classmethod
    def validate_cors_origins(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(values.get('BACKEND_CORS_ORIGINS'), str):
            values['BACKEND_CORS_ORIGINS'] = [i.strip() for i in values['BACKEND_CORS_ORIGINS'].split(",")]
        return values

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Create global settings instance
settings = Settings()

# Production configuration overrides
def get_production_config() -> Dict[str, Any]:
    return {
        "DEBUG": False,
        "LOG_LEVEL": "WARNING",
        "BACKEND_CORS_ORIGINS": [],  # Set production origins
        "DATABASE_URL": "postgresql://user:password@localhost/dbname",  # Set production DB
    }

# Development configuration overrides
def get_development_config() -> Dict[str, Any]:
    return {
        "DEBUG": True,
        "LOG_LEVEL": "DEBUG",
        "SECRET_KEY": "development-key",
    }
