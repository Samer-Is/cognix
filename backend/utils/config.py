"""
Configuration management using Pydantic Settings
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    environment: str = "development"
    debug: bool = True
    secret_key: str = "your-secret-key-change-in-production"
    
    # API Keys
    anthropic_api_key: str
    openai_api_key: str
    google_api_key: str
    
    # AWS
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "us-east-1"
    s3_bucket_data: str = "cognix-data"
    s3_bucket_uploads: str = "cognix-uploads"
    dynamodb_table_users: str = "cognix-users"
    dynamodb_table_activity: str = "cognix-activity"
    dynamodb_table_memory: str = "cognix-agent-memory"
    
    # Database
    database_url: str
    
    # JWT
    jwt_secret: str = "your-jwt-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # API Configuration
    max_requests_per_minute: int = 100
    
    # URLs
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()
