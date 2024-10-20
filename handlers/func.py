from typing import Union
from keyboards.inline_kb import inline_keyboard_default
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from loguru import logger


async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Выход из машины состояний (FSM)
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) отменил ввод!')
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Ввод отменен!', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Здравствуйте! Я помогу вам сделать бота-навигатора для вашего сайта:\n', reply_markup=inline_keyboard_default())


async def delete_message(call: Union[Message, CallbackQuery]):
    if type(call) == CallbackQuery:
        await call.answer(cache_time=60)
        await call.message.delete()
    else:
        await call.delete()
