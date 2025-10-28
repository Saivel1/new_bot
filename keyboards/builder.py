from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from misc.bot_setup import prices

class PayMenu:

    @staticmethod
    def main_keyboard():
        builder = InlineKeyboardBuilder()

        for text, callback_data in prices:
            builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))

        builder.adjust(1)
        return builder.as_markup()