from aiogram import types
from aiogram.filters import Command
from bot_instance import dp

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет! Твой ID: {message.from_user.id}")
