from fastapi import FastAPI, Request
from aiogram import types
from bot_instance import bot, dp
from config_data.config import settings
from contextlib import asynccontextmanager
from logger_setup import logger
from db.database import engine, async_session
from db.db_models import Base, PaymentData
from repositories.base import BaseRepository
from keyboards.deps import BackButton
from misc.utils import modify_user, calculate_expire, get_user, new_date


# Импортируем handlers для регистрации
import handlers.start
import handlers.instructions
import handlers.paymenu
import handlers.subsmenu
import handlers.trial


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(
        url=settings.WEBHOOK_URL,
        drop_pending_updates=True
    )
    print(f"Webhook установлен: {settings.WEBHOOK_URL}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    await bot.delete_webhook()
    await bot.session.close()
    print("Бот остановлен")


# Создаём приложение с lifespan
app = FastAPI(lifespan=lifespan)


async def change_status(order_id: str, status: str):
    st = status.split(".")[1]
    async with async_session() as session:
        repo = BaseRepository(session=session, model=PaymentData)
        res = await repo.update_one({
            "status": st
        }, payment_id=order_id)
        if st == 'canceled':
            await repo.delete_where(payment_id=order_id)
            return False
        if st == 'waiting_for_capture':
            return None
        return res


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
    

    obj = await change_status(order_id=order_id, status=event)
    if not obj:
        logger.info(f"Order: {order_id} was canceled or TimeOut")
        return {"response": "Order was canceled"}
    

    obj_data = data.get("object", {})
    pay_id, pay_am = obj_data.get('id'), obj_data.get('amount')

    logger.info(f'{pay_id} | {pay_am}')
    user = await get_user(user_id=obj.user_id)
    expire =  calculate_expire(old_expire=user.subscription_end) #type: ignore
    new_expire = new_date(expire=expire, amount=pay_am['value'])


    try:
        await modify_user(username=obj.user_id, expire=new_expire)
        logger.info(f"Для пользователя {obj.user_id} оплата и обработка прошли успешно.")

        await bot.send_message(
        chat_id=obj.user_id, #type: ignore
        text=f"Оплата прошла успешно на сумму: {obj.amount}", #type: ignore
        reply_markup=BackButton.back_start()
        )
    except Exception as e:
        logger.warning(e)
        await bot.send_message(
            text="Возникла ошибка, напиши в поддержку /help",
             chat_id=obj.user_id
        )

    return {"ok": True}


@app.get("/")
async def root():
    return {"status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}
