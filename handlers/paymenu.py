from aiogram import F
from bot_instance import dp
from keyboards.builder import PayMenu
from keyboards.deps import BackButton
from aiogram.types import CallbackQuery
from logger_setup import logger
from yooka.payments import PaymentYoo
from yooka.mails import create_user_mailbox
from aiogram.types import InlineKeyboardButton
from db.db_models import PaymentData
from db.database import async_session
from repositories.base import BaseRepository
from marz.backend import marzban_client
from bot_instance import bot

async def create_order(amount: int, user_id):
    mail = await create_user_mailbox(user_id)
    logger.debug(mail)
    res = await PaymentYoo().create_payment(amount=amount, plan=str((amount/50)), email=mail) # type: ignore
    logger.debug(res)
    return res

PAY_MENU_TEXT = """
💳 <b>Оформление подписки</b>

🪞 <b>IV VPN</b> — ваш безопасный доступ к свободному интернету.

<b>Что входит в подписку:</b>
✓ Безлимитный трафик
✓ Высокая скорость
✓ Все серверы доступны
✓ Поддержка 24/7
✓ Полная конфиденциальность

Выберите тариф:
"""

ERROR_TEXT = """
🚧 <b>Упс! Что-то пошло не так</b>

Мы уже работаем над решением проблемы.
Попробуйте обновить через пару минут 🔄

Нужна помощь? → /help
"""


async def keyboard_buld(order_url: str):
    to_pay = [InlineKeyboardButton(
        text="💳 Перейти к оплате", 
        url=order_url
    )]
    
    keyboard = BackButton.back_pays()
    keyboard.inline_keyboard.insert(0, to_pay)
    return keyboard


@dp.callback_query(F.data == "pay_menu")
async def pay_menu(callback: CallbackQuery):
    user_id = callback.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Нажал на кнопку выбора платежа")

    health = await marzban_client.health_check()
    if not health:
        await callback.message.edit_text( #type: ignore
            text=ERROR_TEXT,
            reply_markup=BackButton.back_start(),
            parse_mode="HTML"
        )

        await bot.send_message(
            chat_id=482410857,
            text=f"❌ Панель недоступна"
        )

        return

    await callback.message.edit_text( #type:ignore
        text=PAY_MENU_TEXT,
        reply_markup=PayMenu.main_keyboard(),
        parse_mode="HTML"
    )


@dp.callback_query(F.data.startswith("pay_"))
async def payment_process(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    amount = int(callback.data.replace("pay_", "")) #type: ignore

    logger.info(f'Пользователь ID {user_id} Перещёл в оплату с суммой {amount}')
    order_url, order_id = await create_order(amount=amount, user_id=user_id) #type: ignore


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
