"""
Application Configuration
"""
import os
from datetime import datetime
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Table Order Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ADMIN_EXPIRY: int = 28800  # 8 hours in seconds
    JWT_TABLE_EXPIRY: int = 86400  # 24 hours in seconds
    
    # Database Configuration
    DB_FILE_PATH: str = "data/app.db"
    DB_POOL_MIN_SIZE: int = 10
    DB_POOL_MAX_SIZE: int = 20
    DB_CONNECTION_TIMEOUT: int = 30
    DB_IDLE_TIMEOUT: int = 300
    
    # Password Configuration
    BCRYPT_COST_FACTOR: int = 12
    
    # File Storage Configuration
    UPLOAD_DIR: str = "uploads/menu-images"
    MAX_FILE_SIZE: int = 5242880  # 5MB in bytes
    ALLOWED_MIME_TYPES: str = "image/*"
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "logs/app-{date}.log"
    LOG_RETENTION_DAYS: int = 30
    
    # Cache Configuration
    CACHE_TTL: int = 300  # 5 minutes in seconds
    
    # SSE Configuration
    SSE_HEARTBEAT_INTERVAL: int = 30  # seconds
    
    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:3000"
    
    @property
    def database_url(self) -> str:
        """Get SQLAlchemy database URL"""
        return f"sqlite:///{self.DB_FILE_PATH}"
    
    @property
    def log_file_path_today(self) -> str:
        """Get today's log file path"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.LOG_FILE_PATH.replace("{date}", today)
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Get CORS origins as list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
