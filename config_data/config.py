from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Bot
    BOT_TOKEN: str
    WEBHOOK_URL: str

    #Marzban
    M_DIGITAL_URL: str
    M_DIGITAL_U: str
    M_DIGITAL_P: str

    #Anymessage
    ANY_TOKEN: str
    ANY_SITE: str
    ANY_DOMAIN: str
        
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding='utf-8', 
        extra='ignore',
    )


settings = Settings() #type:ignore