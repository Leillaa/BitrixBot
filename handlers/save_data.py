from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from keyboards.reply_kb import kb_reply_cancel, kb_yn
from states import FSMSave
from keyboards.inline_kb import inline_keyboard_default
from handlers.func import delete_message, cancel_handler
from loguru import logger
from loader import bot
from typing import Union
from create_bot import create_bot


async def start(message: Union[Message, CallbackQuery]) -> None:
    """
    Отправляет сообщение приветствия и функции при получении команды /start
    :param message:
    :return:
    """
    await delete_message(message)
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "start"')
    await bot.send_message(message.from_user.id, "Здравствуйте! Я помогу вам сделать бота-навигатора для вашего сайта:"
                                                 "\n", parse_mode='html',
                           reply_markup=inline_keyboard_default())


async def helper(message: Union[Message, CallbackQuery]) -> None:
    """
    Инструкция по работе с ботом
    :parm message:
    :return:
    """
    await delete_message(message)
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) в функциии "helper"')
    await bot.send_message(
        message.from_user.id,
        "Это конструктор ботов для навигации по сайту написаному на Bitrix. "
        "Чтобы создать такого бот и выложить его к вам на сервер вам понадабятся некоторые данные!\n"
        "1.URL сайта\n"
        "2.Логин и пароль bitrix\n"
        "3.Логин и пароль от сервера на котором будет бот\n"
        "4.Имя пользователя и пароль баы данных сайта"
    )


async def new_bot(message: Union[Message, CallbackQuery]) -> None:
    """
    Инструкции для получения токена бота
    :param message:
    :return:
    """
    await delete_message(message)
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) в функциии "new_bot"')
    await bot.send_message(
        message.from_user.id,
        '1. Перейдите в чат с этим ботом - https://t.me/BotFather ,\n '
        '2. Напишите ему сообщение с текстом /newbot, \n '
        '3. Задайте ему имя и ник по инструкции, \n '
        '4. Отправьте сюда HTTP API который получите от бота'
    )
    await FSMSave.step_1.set()


async def save_token(message: types.Message, state: FSMContext) -> None:
    """
    Сохранение токена и запрос url
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Save_data Пользователь {message.from_user.full_name}({message.from_user.id}) в функции save_token!')
    res = message.text != '' and all(char.isalpha() or char.isspace() for char in message.text)
    if res:
        async with state.proxy() as data:
            data['token'] = message.text
        await bot.send_message(
            message.from_user.id,
            "Отлично! Теперь мне нужна ссылка на ваш сайт для которого вы делаете бота")
        await FSMSave.next()
    else:
        await bot.send_message(
            message.from_user.id,
            'Пожалуйста, введите токен, который вы получили от BotFather, повторите ввод или наберите "отмена"',
            reply_markup=kb_reply_cancel)
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) - Ошибка ввода токена')


async def save_url(message: types.Message, state: FSMContext) -> None:
    """
    Сохранение url и запрос данных Bitrix
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Save_data Пользователь {message.from_user.full_name}({message.from_user.id}) в функции save_url!')
    async with state.proxy() as data:
        data['url'] = message.text
    await bot.send_message(
        message.from_user.id,
        "Теперь отправьте пожалуйста логин и пароль от Bitrix для вашего сайта, через пробел без запятых, "
        "в формате 'login password' (Если вы не знаете уочните у разработчиков)"
    )
    await FSMSave.next()


async def save_lp_bitrix(message: types.Message, state: FSMContext) -> None:
    """
    Сохранение данных Bitrix и запрос данных сервера
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Save_data Пользователь {message.from_user.full_name}({message.from_user.id}) '
                f'в функции save_lp_bitrix!'
                )
    if len(message.text.split()) == 2:
        async with state.proxy() as data:
            text = message.text.split(" ")
            data['login_bitrix'] = text[0]
            data['password_bitrix'] = text[1]
        await bot.send_message(
            message.from_user.id,
            "Отправьте пожалуйста ip-адресс, логин и пароль от сервера на котором будет расположен ваш бот, "
            "через пробел без запятых, в формате '127.0.0.1 login passwor'"
        )
        await FSMSave.next()
    else:
        await bot.send_message(
            message.from_user.id,
            'Пожалуйста, введите логин и пароль от Bitrix для вашего сайта, через пробел без запятых, '
            'в формате "login password", повторите ввод или наберите "отмена"',
            reply_markup=kb_reply_cancel)
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) '
                     f'- Ошибка ввода логина и пароля битрикса')


async def save_lp_server(message: types.Message, state: FSMContext) -> None:
    """
    Сохранение данных сервера и запрос данных БД Bitrix
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Save_data Пользователь {message.from_user.full_name}({message.from_user.id}) '
                f'в функции save_lp_server!')
    if len(message.text.split(" ")) == 3:
        async with state.proxy() as data:
            text = message.text.split(" ")
            data['host'] = text[0]
            data['login_server'] = text[1]
            data['password_server'] = text[2]
        await bot.send_message(
            message.from_user.id,
            "Отлично!\n Последний шаг)\n Отправьте пожалуйста имя пользователя и пароль от базы данных в Bitrix. "
            "Через пробел без запятых, в формате 'login password'"
        )
        await FSMSave.next()
    else:
        await bot.send_message(
            message.from_user.id,
            'Пожалуйста, введите логин и пароль от Bitrix для вашего сайта, через пробел без запятых, '
            'в формате "login password", повторите ввод или наберите "отмена"',
            reply_markup=kb_reply_cancel)
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) '
                     f'- Ошибка ввода логина и пароля битрикса')


async def save_lp_db(message: types.Message, state: FSMContext) -> None:
    """
    Сохранени е данных БД Bitrix
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Save_data Пользователь {message.from_user.full_name}({message.from_user.id}) '
                f'в функции save_lp_db!')
    if len(message.text.split(" ")) == 2:
        async with state.proxy() as data:
            text = message.text.split(" ")
            data['login_db'] = text[0]
            data['password_db'] = text[1]
        await bot.send_message(message.from_user.id, "Все данные записаны")
        await check(message, state)
    else:
        await bot.send_message(
            message.from_user.id,
            'Пожалуйста, введите логин и пароль от Bitrix для вашего сайта, через пробел без запятых, '
            'в формате "login password", повторите ввод или наберите "отмена"',
            reply_markup=kb_reply_cancel)
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) - '
                     f'Ошибка ввода логина и пароля базы двнных битрикса')


async def check(message: types.Message, state: FSMContext) -> None:
    """
    Проверка введённых пользователем данных
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Save_data Пользователь {message.from_user.full_name}({message.from_user.id}) '
                f'в функции check!')
    async with state.proxy() as data:
        await message.answer(
            f"Ваши данные:\n "
            f"Токен бота: {data['token']}\n"
            f"URL сайта: {data['url']}\n"
            f"Логин и пароль от Bitrix: {data['login_bitrix']}, {data['password_bitrix']}\n"
            f"IP-адресс сервера: {data['host']}\n"
            f"Логин и пароль от сервера: {data['login_server']}, {data['password_server']}\n"
            f"Логин и пароль от базы данных Bitrix: {data['login_db']}, {data['password_db']}\n"
            "Все верно?",
            reply_markup=kb_yn
        )
        await FSMSave.next()


async def end(message: types.Message, state: FSMContext) -> None:
    """
    Создание бота
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Save_data Пользователь {message.from_user.full_name}({message.from_user.id}) '
                f'в функции end!')
    if message.text.lower() in ["да", "нет", "yes", "no"]:
        async with state.proxy() as data:
            if message.text.lower() in ['да', 'yes']:
                token = data['token']
                url = data['url']
                log_bit = data['login_bitrix']
                pass_bit = data['password_bitrix']
                host = data['host']
                log_serv = data['login_server']
                pass_serv = data['password_server']
                log_db = data['login_db']
                pass_db = data['password_db']
                await bot.send_message(message.from_user.id, "Бот создается. Пожалуйста подождите...")
                create_bot(token, url, log_bit, pass_bit, host, log_serv, pass_serv, log_db, pass_db)
    else:
        logger.debug(
            f'Пользователь {message.from_user.full_name}({message.from_user.id}) - '
            f'Ошибка в ведении данных пользователем')
        await bot.send_message(message.from_user.id, "Пожалуйста вернитесь в начало и заполните данные заного",
                               reply_markup=kb_reply_cancel)


def register_default_handlers(disp: Dispatcher) -> None:
    """
    Регистрация хэндлеров
    :parm disp:
    :return:
    """
    disp.register_message_handler(start, commands=['start'])
    disp.register_callback_query_handler(start, text='/start')
    disp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    disp.register_callback_query_handler(new_bot, text='/new_bot')
    disp.register_message_handler(new_bot, commands=['new_bot'])
    disp.register_callback_query_handler(helper, text='/helper')
    disp.register_message_handler(helper, commands=['helper'])
    disp.register_message_handler(save_token, state=FSMSave.step_1)
    disp.register_message_handler(save_url, state=FSMSave.step_2)
    disp.register_message_handler(save_lp_bitrix, state=FSMSave.step_3)
    disp.register_message_handler(save_lp_server, state=FSMSave.step_4)
    disp.register_message_handler(save_lp_db, state=FSMSave.step_5)
    disp.register_message_handler(end, state=FSMSave.step_6)
