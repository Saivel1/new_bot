from aiogram import F
from bot_instance import dp
from keyboards.builder import InstructionMenu
from aiogram.types import CallbackQuery
from logger_setup import logger



@dp.callback_query(F.data == "instruction")
async def instriction_menu(callback: CallbackQuery):
    user_id = callback.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Нажал кнопку инстуркция")

    await callback.message.edit_text( #type:ignore
        text="Меню инструкций",
        reply_markup=InstructionMenu.main_keyboard()
    )