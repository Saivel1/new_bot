from aiogram import F
from bot_instance import dp
from keyboards.builder import PayMenu
from keyboards.deps import BackButton
from aiogram.types import CallbackQuery
from logger_setup import logger
from yooka.payments import PaymentYoo
from yooka.mails import Anymessage
from aiogram.types import InlineKeyboardButton
from db.db_models import PaymentData
from db.database import async_session
from repositories.base import BaseRepository


async def create_order(amount: int):
    mail = await Anymessage().order_email()
    res = await PaymentYoo().create_payment(amount=amount, plan=str((amount/50)), email=mail) # type: ignore
    return res


async def keyboard_buld(order_url: str):
    to_pay = [InlineKeyboardButton(text="Оплатить", url=order_url)]
    keyboard = BackButton.back_pays()
    keyboard.inline_keyboard.insert(0, to_pay)
    return keyboard


@dp.callback_query(F.data == "pay_menu")
async def pay_menu(callback: CallbackQuery):
    user_id = callback.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Нажал на кнопку выбора платежа")

    await callback.message.edit_text( #type:ignore
        text="Меню покупки",
        reply_markup=PayMenu.main_keyboard()
    )


@dp.callback_query(F.data.startswith("pay_"))
async def payment_process(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    amount = int(callback.data.replace("pay_", "")) #type: ignore

    logger.info(f'Пользователь ID {user_id} Перещёл в оплату с суммой {amount}')
    order_url, order_id = await create_order(amount=amount) #type: ignore


    async with async_session() as session:
        repo = BaseRepository(session=session, model=PaymentData)
        await repo.create({
            "payment_id": order_id,
            "user_id": user_id,
            "amount": amount
        })

    reply_text = f"""
Ссылка для оплаты:

{order_url}
"""
    keyboard = await keyboard_buld(order_url=order_url) #type: ignore

    await callback.message.edit_text( # type: ignore
        text=reply_text,
        reply_markup=keyboard
    )
