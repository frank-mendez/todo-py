from pydantic_settings import BaseSettings
from pydantic import EmailStr, field_validator, computed_field
from typing import Optional, Dict, Any, Union, List
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Todo API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A FastAPI-based Todo application"

    # Security Settings
    SECRET_KEY: str = "your-secret-key-here"  # Change in production!
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_ALGORITHM: str = "HS256"

    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database Settings
    DATABASE_TYPE: str = "postgresql"
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_NAME: str = "todo"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from settings."""
        if self.DATABASE_TYPE == "sqlite":
            return f"sqlite:///./todo.db"
        return (
            f"{self.DATABASE_TYPE}://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

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

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

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
