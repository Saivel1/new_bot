from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Bot
    BOT_TOKEN: str
    WEBHOOK_URL: str
    TRIAL_DAYS: int

    #Marzban
    M_DIGITAL_URL: str
    M_DIGITAL_U: str
    M_DIGITAL_P: str

    #Anymessage
    ANY_TOKEN: str
    ANY_SITE: str
    ANY_DOMAIN: str

    #DB SetUp
    DB_NAME: str

    #YooKassa
    ACCOUNT_ID: int
    SECRET_KEY: str

    IN_SUB_LINK: str 

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        """Асинхронный URL для asyncpg"""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def DATABASE_URL_aiosqlite(self):
        return f"sqlite+aiosqlite:///{self.DB_NAME}"
        
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding='utf-8', 
        extra='ignore',
    )


settings = Settings() #type:ignore