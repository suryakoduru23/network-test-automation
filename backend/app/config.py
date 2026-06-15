"""Application Configuration"""
from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application Settings"""
    
    # App Config
    APP_NAME: str = "Network Test Automation Framework"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    PYTHON_ENV: str = Field(default="development", env="PYTHON_ENV")
    
    # Server
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./test.db", env="DATABASE_URL")
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key", env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="CORS_ORIGINS"
    )
    
    # Email
    SMTP_SERVER: str = Field(default="smtp.gmail.com", env="SMTP_SERVER")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: str = Field(default="", env="SMTP_USER")
    SMTP_PASSWORD: str = Field(default="", env="SMTP_PASSWORD")
    SMTP_FROM: str = Field(default="noreply@network-test-automation.com", env="SMTP_FROM")
    
    # SSH
    SSH_TIMEOUT: int = Field(default=30, env="SSH_TIMEOUT")
    SSH_PORT: int = Field(default=22, env="SSH_PORT")
    
    # Scheduler
    SCHEDULER_ENABLED: bool = Field(default=True, env="SCHEDULER_ENABLED")
    SCHEDULER_INTERVAL_MINUTES: int = Field(default=60, env="SCHEDULER_INTERVAL_MINUTES")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
