from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Клавистура отмены
kb_cancel = KeyboardButton('Отмена')
kb_reply_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(kb_cancel)

# Клавиатура Да/Нет
kb_yn = ReplyKeyboardMarkup(resize_keyboard=True)
kb_1_1 = KeyboardButton('Да')
kb_1_2 = KeyboardButton('Нет')
kb_yn.row(kb_1_1, kb_1_2, kb_cancel)
