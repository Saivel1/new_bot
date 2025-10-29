from fastapi import FastAPI, Request
from aiogram import types
from bot_instance import bot, dp
from config_data.config import settings
from contextlib import asynccontextmanager
from logger_setup import logger
from db.database import engine, async_session
from db.db_models import Base, PaymentData
from repositories.base import BaseRepository


# Импортируем handlers для регистрации
import handlers.start
import handlers.instructions
import handlers.paymenu
import handlers.subsmenu


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await bot.set_webhook(
        url=settings.WEBHOOK_URL,
        drop_pending_updates=True
    )
    print(f"Webhook установлен: {settings.WEBHOOK_URL}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # Приложение работает
    
    # Shutdown
    await bot.delete_webhook()
    await bot.session.close()
    print("Бот остановлен")


# Создаём приложение с lifespan
app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}


@app.post("/pay")
async def yoo_kassa(request: Request):
    data = await request.json()
    event = data.get('event')
    order_id = data.get('object', {}).get("id", {})

    if order_id == {}:
        logger.warning(f'{order_id} Response: {data}')
        return {"status": "ne-ok"}
    
    async with async_session() as session:
        repo = BaseRepository(session=session, model=PaymentData)
        if event == 'payment.succeeded':
            await repo.update_one(
                {"status": "succeeded"},
                payment_id=order_id
            )
        elif event == "payment.canceled":
            await repo.update_one(
                {"status": "succeeded"},
                payment_id=order_id
            )

    pay_id = data.get("object", {}).get("id")
    pay_am = data.get("object", {}).get("amount")
    logger.info(f'{pay_id} | {pay_am}')
    return {"ok": True}


@app.get("/")
async def root():
    return {"status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}
