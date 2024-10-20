from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """
    Отправляет сообщение приветствия и функции при получении команды /start
    :param update:
    :param context:
    :return:
    """
    keyboard = [
        [
            InlineKeyboardButton("Меню сайта", callback_data='/menu'),
            InlineKeyboardButton("Помощь в поиске страницы", callback_data='/help'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        'Здравствуйте! Я бот навигатор по сайту. Вот что я могу вам показать:',
        reply_markup=reply_markup
    )


def menu(update: Update, context: CallbackContext) -> None:
    """
    Выводит меню сайта
    :param update:
    :param context:
    :return:
    """


def button(update: Update, context: CallbackContext) -> None:
    """

    :param update:
    :param context:
    :return:
    """
    query = update.callback_query
    selected_name = query.data
    query.edit_message_text(text=f"Вы выбрали: {selected_name}")