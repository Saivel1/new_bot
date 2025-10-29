from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config_data.config import settings
from db.db_models import *
import asyncio
from pathlib import Path
from sqlalchemy import select
from logger_setup import logger
from sqlalchemy.ext.asyncio import AsyncSession


from repositories.base import BaseRepository


engine = create_async_engine(
    url=settings.DATABASE_URL_aiosqlite
    )

async_session = async_sessionmaker(
    bind=engine
)
