from aiogram import F, types
from aiogram.filters import Command
from bot_instance import dp
from keyboards.markup import MainKeyboard
from keyboards.builder import PayMenu, SubMenu, InstructionMenu
from aiogram.types import CallbackQuery

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет! Твой ID: {message.from_user.id}", reply_markup=MainKeyboard.main_keyboard()) # type: ignore


@dp.callback_query(F.data == "start_menu")
async def call_start(callback: CallbackQuery):
    await callback.message.edit_text(f"Привет! Твой ID: {callback.from_user.id}", reply_markup=MainKeyboard.main_keyboard()) # type: ignore


@dp.callback_query(F.data == "pay_menu")
async def pay_menu(callback: CallbackQuery):
    await callback.message.edit_text( #type:ignore
        text="Меню покупки",
        reply_markup=PayMenu.main_keyboard()
    )


@dp.callback_query(F.data == "subs")
async def subs_menu(callback: CallbackQuery):
    await callback.message.edit_text( #type:ignore
        text="Меню подписок",
        reply_markup=SubMenu.main_keyboard()
    )


@dp.callback_query(F.data == "instruction")
async def instriction_menu(callback: CallbackQuery):
    await callback.message.edit_text( #type:ignore
        text="Меню инструкций",
        reply_markup=InstructionMenu.main_keyboard()
    )