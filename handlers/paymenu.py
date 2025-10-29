from aiogram import F
from bot_instance import dp
from keyboards.builder import PayMenu
from keyboards.deps import BackButton
from aiogram.types import CallbackQuery
from logger_setup import logger
from yooka.payments import PaymentYoo
from yooka.mails import Anymessage
from aiogram.types import InlineKeyboardButton




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

    mail = await Anymessage().order_email()
    order_url = await PaymentYoo().create_payment(amount=amount, plan=str((amount/50)), email=mail) # type: ignore

    reply_text = f"""
Ссылка для оплаты:

{order_url}
"""
    to_pay = [InlineKeyboardButton(text="Оплатить", url=order_url)]

    await callback.message.edit_text( # type: ignore
        text=reply_text,
        reply_markup=BackButton.back_pays().inline_keyboard.append(to_pay)
    )
