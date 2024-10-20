import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN")
URL: str = os.getenv("URL")
LOGIN_BITRIX: str = os.getenv("LOGIN_BITRIX")
PASSWORD_BITRIX: str = os.getenv("PASSWORD_BITRIX")
HOST_SERVER: str = os.getenv("HOST_SERVER")
LOGIN_SERVER: str = os.getenv("LOGIN_SERVER")
PASSWORD_SERVER: str = os.getenv("PASSWORD_SERVER")
LOGIN_DB: str = os.getenv("LOGIN_DB")
PASSWORD_DB: str = os.getenv("PASSWORD_DB")
