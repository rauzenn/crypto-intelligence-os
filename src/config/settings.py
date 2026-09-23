from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import yaml

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/crypto_os"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    
    # Environment
    ENV: str = "development"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

def load_sources_config(file_path: str = "config/sources.yaml") -> dict:
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

sources_config = load_sources_config()
