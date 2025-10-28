from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config_data.config import settings as s


bot = Bot(token=s.BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет! Твой ID: {message.from_user.id}") # type: ignore

