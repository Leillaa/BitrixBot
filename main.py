from aiogram.utils import executor
from loader import dp, shutdown, log_func, setup_bot_commands
from loging import log_func
from handlers.save_data import register_default_handlers


def main():
    log_func()
    register_default_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands, on_shutdown=shutdown)


if __name__ == '__main__':
    main()
