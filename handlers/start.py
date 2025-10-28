from aiogram import F, types
from aiogram.filters import Command
from bot_instance import dp
from keyboards.markup import MainKeyboard
from keyboards.builder import PayMenu, SubMenu, InstructionMenu
from aiogram.types import CallbackQuery
from logger_setup import logger

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Ввёл команду /start")
    await message.answer(f"Привет! Твой ID: {message.from_user.id}", reply_markup=MainKeyboard.main_keyboard()) # type: ignore


@dp.callback_query(F.data == "start_menu")
async def call_start(callback: CallbackQuery):
    user_id = callback.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Нажал Назад")
    await callback.message.edit_text(f"Привет! Твой ID: {callback.from_user.id}", reply_markup=MainKeyboard.main_keyboard()) # type: ignore
