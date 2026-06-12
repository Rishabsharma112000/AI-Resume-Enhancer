"""Configuration settings for the application"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_TITLE: str = "ResumeBoost AI"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./resume_enhance.db"
    DATABASE_ECHO: bool = False

    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # OpenAI Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    # File Upload Configuration
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: list = ["pdf", "docx", "doc"]

    # CORS Configuration
    # Allow all origins (useful during development). For production, restrict this.
    CORS_ORIGINS: list = ["*"]


    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
