from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config_data.config import DEFAULT_COMMANDS


# Клавиатура начальных команд
def inline_keyboard_default() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup()
    for item in DEFAULT_COMMANDS:
        inline_kb.add(InlineKeyboardButton(text=item[1], callback_data="/" + item[0]))
    return inline_kb



