from aiogram import F
from bot_instance import dp
from keyboards.builder import PayMenu
from aiogram.types import CallbackQuery
from logger_setup import logger

@dp.callback_query(F.data == "pay_menu")
async def pay_menu(callback: CallbackQuery):
    user_id = callback.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Нажал на кнопку выбора платежа")

    await callback.message.edit_text( #type:ignore
        text="Меню покупки",
        reply_markup=PayMenu.main_keyboard()
    )