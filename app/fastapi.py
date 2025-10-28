from fastapi import FastAPI, Request
import json
from aiogram import Dispatcher, types, Bot
from main import dp, bot
from config_data.config import settings as s

app = FastAPI() # type: ignore

@app.on_envent("startup")
async def on_startup():
    await bot.set_webhook(s.WEBHOOK_URL)


@app.post("/webhook")
async def web_hook(request: Request): # type: ignore
    data = await request.json() # type: ignore
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}