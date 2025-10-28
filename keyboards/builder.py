from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from misc.bot_setup import *
from .deps import back

class PayMenu:

    @staticmethod
    def main_keyboard():
        builder = InlineKeyboardBuilder()

        for text, callback_data in prices:
            builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))

        builder.add(back)
        builder.adjust(1)
        return builder.as_markup()

class SubMenu:

    @staticmethod
    def main_keyboard():
        builder = InlineKeyboardBuilder()

        for text, callback_data in sub_servs:
            builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))

        builder.add(back)
        builder.adjust(1)
        return builder.as_markup()

class InstructionMenu:

    @staticmethod
    def main_keyboard():
        builder = InlineKeyboardBuilder()

        for text, callback_data in platforms:
            builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))

        builder.add(back)
        builder.adjust(3)
        return builder.as_markup()