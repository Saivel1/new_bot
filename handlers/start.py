from aiogram import F, types
from aiogram.filters import Command
from bot_instance import dp
from keyboards.markup import MainKeyboard
from aiogram.types import CallbackQuery
from logger_setup import logger
from misc.utils import get_user, create_user



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Ввёл команду /start")

    user = await get_user(user_id)
    if not user:
        await create_user(user_id=user_id, username=message.from_user.username) #type: ignore
        await message.answer(f"Привет! Твой ID: {message.from_user.id}", # type: ignore
                             reply_markup=MainKeyboard.main_keyboard_with_trial()) 
    elif user.trial_used == False:    
        await message.answer(f"Привет! Твой ID: {message.from_user.id}", # type: ignore
                             reply_markup=MainKeyboard.main_keyboard_with_trial())
    else:
        await message.answer(f"Привет! Твой ID: {message.from_user.id}", # type: ignore
                             reply_markup=MainKeyboard.main_keyboard()) 


@dp.callback_query(F.data == "start_menu")
async def call_start(callback: CallbackQuery):
    user_id = callback.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Нажал старт меню")
    user = await get_user(user_id)
    if user is None:
        await callback.message.edit_text(text="Возникла ошибка")# type: ignore
    elif user.trial_used == False:    
        await callback.message.edit_text(f"Привет! Твой ID: {callback.from_user.id}", # type: ignore
                             reply_markup=MainKeyboard.main_keyboard_with_trial())
    else:
        await callback.message.edit_text(f"Привет! Твой ID: {callback.from_user.id}", # type: ignore
                             reply_markup=MainKeyboard.main_keyboard())



@dp.message(Command("id"))
async def cmd_id(message: types.Message):
    user_id = message.from_user.id #type: ignore
    logger.info(f"ID : {user_id} | Ввёл команду /id")
    await message.answer(f"Привет! Твой ID: {message.from_user.id}") # type: ignore
