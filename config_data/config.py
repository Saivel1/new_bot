from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Bot
    BOT_TOKEN: str
    WEBHOOK_URL: str
    
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding='utf-8', 
        extra='ignore',
    )


settings = Settings() #type:ignore