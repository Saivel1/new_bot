from fastapi import FastAPI, Request
from aiogram import types
from bot_instance import bot, dp
from config_data.config import settings


# Импортируем handlers для регистрации
import handlers.start

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(
        url=settings.WEBHOOK_URL,
        drop_pending_updates=True
    )
    print(f"Webhook установлен: {settings.WEBHOOK_URL}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "running"}

@app.get("/health")
async def health():
    return {"status": "ok"}
