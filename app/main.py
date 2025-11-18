from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from aiogram import types
from bot_instance import bot, dp
from config_data.config import settings
from contextlib import asynccontextmanager
from logger_setup import logger
from db.database import engine, async_session
from db.db_models import Base, PaymentData
from repositories.base import BaseRepository
from keyboards.deps import BackButton
from misc.utils import modify_user, calculate_expire, get_user, new_date, get_links_of_panels
import aiohttp, asyncio
from fastapi.templating import Jinja2Templates


# Импортируем handlers для регистрации
import handlers.start
import handlers.instructions
import handlers.paymenu
import handlers.subsmenu
import handlers.trial
import handlers.others


templates = Jinja2Templates(directory="app/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(
        url=settings.WEBHOOK_URL,
        drop_pending_updates=False
    )
    print(f"Webhook установлен: {settings.WEBHOOK_URL}")
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)
    
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


@app.post("/marzban")
async def webhook_marz(request: Request):
    data = await request.json()
    logger.info(data)
    return {"ok": True}


@app.post("/pay")
async def yoo_kassa(request: Request):
    data = await request.json()
    event = data.get('event')
    order_id = data.get('object', {}).get("id")
    
    if not order_id:
        logger.warning(f'Missing order_id. Response: {data}')
        return {"status": "error", "message": "missing order_id"}
    
    logger.info(f"Webhook received: order={order_id}, event={event}")
    
    # Обновляем статус
    obj = await change_status(order_id=order_id, status=event)
    
    if obj is False:  # Canceled
        logger.info(f"Order {order_id} was canceled")
        return {"status": "canceled"}
    
    if obj is None:  # waiting_for_capture
        logger.info(f"Order {order_id} waiting for capture")
        return {"status": "waiting"}
    
    # Проверка на повторную обработку
    if obj.status == "succeeded":
        logger.info(f"Order {order_id} already processed")
        return {"status": "already_processed"}
    
    # Получаем данные платежа
    obj_data = data.get("object", {})
    pay_id = obj_data.get('id')
    pay_am = obj_data.get('amount', {})
    
    logger.info(f"Processing payment: id={pay_id}, amount={pay_am}, user={obj.user_id}")
    
    try:
        # Получаем пользователя из БД
        user = await get_user(user_id=obj.user_id)
        if not user:
            raise Exception(f"User {obj.user_id} not found in DB")
        
        # Вычисляем новую дату
        expire = calculate_expire(old_expire=user.subscription_end)
        new_expire = new_date(expire=expire, amount=pay_am.get('value', '0'))
        
        logger.info(f"User {obj.user_id}: old_expire={user.subscription_end}, new_expire={new_expire}")
        
        # Обновляем подписку
        result = await modify_user(username=obj.user_id, expire=new_expire)
        
        if not result:
            raise Exception("Failed to modify user")
        
        # Уведомления
        logger.info(f"Payment processed successfully for user {obj.user_id}")
        
        await bot.send_message(
            chat_id=obj.user_id,
            text=f"Оплата прошла успешно на сумму: {obj.amount}",
            reply_markup=BackButton.back_start()
        )
        
        await bot.send_message(
            chat_id=482410857,
            text=f"Пользователь {obj.user_id} заплатил {obj.amount}"
        )
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing payment {order_id}: {e}", exc_info=True)
        
        # Уведомляем пользователя
        try:
            await bot.send_message(
                text="Возникла ошибка при обработке платежа. Напиши в поддержку /help",
                chat_id=obj.user_id
            )
        except:
            pass
        
        # Уведомляем админа
        await bot.send_message(
            chat_id=482410857,
            text=f"❌ Ошибка обработки платежа {order_id} для {obj.user_id}: {e}"
        )
        
        return {"status": "error", "message": str(e)}


@app.get("/sub/{uuid}")
async def process_sub(request: Request, uuid: str):
    """Проверяем все панели параллельно"""
    
    links = await get_links_of_panels(uuid=uuid)
    
    if not links:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    async def check_panel(link: str) -> tuple[bool, str]:
        """Проверить доступность панели"""
        try:
            timeout = aiohttp.ClientTimeout(total=3.0)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                response = await session.get(url=link)
                return (response.status in (200, 201), link)
        except Exception:
            return (False, link)
    
    # Проверяем все панели параллельно
    results = await asyncio.gather(*[check_panel(link) for link in links])
    
    # Выбираем первую рабочую
    for is_available, link in results:
        if is_available:
            logger.info(f"Подписка отдана: {link}")
            return RedirectResponse(url=link, status_code=302)
    
    # Все недоступны
    raise HTTPException(status_code=503, detail="All panels unavailable")


@app.get("/vpn-guide/{user_id}")
async def vpn_guide(request: Request, user_id: str):
    # Получаем данные пользователя (например, из БД)
    user_data = {
        "subscription_link": f"{settings.IN_SUB_LINK}{user_id}"
    }
    
    return templates.TemplateResponse(
        "guide.html",
        {"request": request, "user_data": user_data}
    )


@app.get("/")
async def root():
    return {"status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}
