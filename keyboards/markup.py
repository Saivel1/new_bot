from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton

class MainKeyboard:
    
    @staticmethod
    def main_keyboard():

        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Оплатить", callback_data="pay_menu")],
            [InlineKeyboardButton(text="Подписка и ссылки", callback_data="subs")],
            [InlineKeyboardButton(text="Инструкция", callback_data="instruction")]
        ])

    @staticmethod
    def main_keyboard_with_trial():

        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Пробный период", callback_data="trial")],
            [InlineKeyboardButton(text="Оплатить", callback_data="pay_menu")],
            [InlineKeyboardButton(text="Подписка и ссылки", callback_data="subs")],
            [InlineKeyboardButton(text="Инструкция", callback_data="instruction")]
        ])
