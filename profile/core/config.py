import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    PROJECT_NAME: str = "Education DB API"
    API_V1_STR: str = ""
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@postgres:5432/education_db"
    )

    class Config:
        env_file = ".env"


# Create global settings object
settings = Settings()