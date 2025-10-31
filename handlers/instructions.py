from aiogram import F
from bot_instance import dp
from keyboards.builder import InstructionMenu
from aiogram.types import CallbackQuery
from logger_setup import logger
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from misc.utils import get_user_in_links



@dp.callback_query(F.data == "instruction")
async def instriction_menu(callback: CallbackQuery):
    user_id = callback.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Нажал кнопку инстуркция")

    user = await get_user_in_links(user_id=user_id)
    if not user:
        await callback.answer("Zalupa")
        return

    uuid = ""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📱 Инструкция по установке",
            web_app=WebAppInfo(url=f"https://webhook.ivvpn.world/vpn-guide/{uuid}")
        )]
    ])
    
    await callback.message.edit_text( #type:ignore
        "🪞 Нажмите на кнопку ниже для просмотра инструкции:",
        reply_markup=keyboard
    )