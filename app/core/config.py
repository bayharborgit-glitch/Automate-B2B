from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    # These fields MATCH the keys in your .env file
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    CORS_ORIGINS: str = "*"  # Default fallback
    
    class Config:
        env_file = ".env"           # ← Tells Pydantic: "Load from .env"
        env_file_encoding = "utf-8"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS from string to list."""
        if not self.CORS_ORIGINS or self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

# Create a single global instance
settings = Settings()