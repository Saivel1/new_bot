from aiogram import F, types
from aiogram.filters import Command
from bot_instance import dp
from keyboards.markup import MainKeyboard
from keyboards.builder import PayMenu
from aiogram.types import CallbackQuery

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет! Твой ID: {message.from_user.id}", reply_markup=MainKeyboard.main_keyboard()) # type: ignore


@dp.callback_query(F.data == "pay_menu")
async def pay_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Меню покупки",
        reply_markup=PayMenu.main_keyboard()
    )