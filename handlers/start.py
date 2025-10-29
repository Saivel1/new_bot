from aiogram import F, types
from aiogram.filters import Command
from bot_instance import dp
from keyboards.markup import MainKeyboard
from aiogram.types import CallbackQuery
from logger_setup import logger
from db.db_models import UserOrm
from db.database import async_session
from repositories.base import BaseRepository


async def get_user(user_id: str):
    async with async_session() as session:
        user_repo = BaseRepository(session=session, model=UserOrm)
        res = await user_repo.get_one(user_id=user_id)
        return res


async def create_user(user_id: str, username: str | None = None):
    async with async_session() as session:
        user_repo = BaseRepository(session=session, model=UserOrm)
        data = {
            "user_id": user_id
        }
        if username:
            data["username"] = username

        res = await user_repo.create(data)
        return res


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id #type: ignore
    user_id = str(user_id)
    logger.info(f"ID : {user_id} | Ввёл команду /start")
    user = await get_user(user_id)
    if not user:
        await create_user(user_id=user_id, username=message.from_user.username) #type: ignore
        await message.answer(f"Привет! Твой ID: {message.from_user.id}", reply_markup=MainKeyboard.main_keyboard()) # type: ignore
    else:    
        await message.answer(f"Привет! Твой ID: {message.from_user.id}", reply_markup=MainKeyboard.main_keyboard()) # type: ignore


@dp.callback_query(F.data == "start_menu")
async def call_start(callback: CallbackQuery):
    user_id = callback.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Нажал Назад")
    await callback.message.edit_text(f"Привет! Твой ID: {callback.from_user.id}", reply_markup=MainKeyboard.main_keyboard()) # type: ignore


@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    user_id = message.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Ввёл команду /id")
    await message.answer(f"Привет! Твой ID: {message.from_user.id}") # type: ignore
