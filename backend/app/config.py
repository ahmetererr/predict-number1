from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Digit Recognition API"
    
    # Model Settings
    MODEL_PATH: str = "app/models/saved_model"
    INPUT_SHAPE: tuple = (28, 28)
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 