import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN")


DEFAULT_COMMANDS: tuple = (
    ('new_bot', "Новый бот"),
    ('helper', "Инструкция")
)
