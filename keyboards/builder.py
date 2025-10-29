from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, CopyTextButton
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

    @staticmethod
    def links_keyboard(links: list):
        builder = InlineKeyboardBuilder()

        for text, link in links:
            builder.add(InlineKeyboardButton(text=text, copy_text=CopyTextButton(text=link)))

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