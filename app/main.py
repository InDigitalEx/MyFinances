import logging
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram.utils.exceptions import TelegramAPIError, ChatNotFound, BotBlocked

from app.filters import register_all_filters
from app.handlers import register_all_handlers
from app.keyboards import Keyboards
from app.middlewares import register_all_middlewares
from app.utils import Messages
from data import Env
from database import Database
from database.methods import UserMethods
from database.models import register_models


async def __on_startup(dp: Dispatcher) -> None:
    logging.info('Bot starts')

    register_all_filters(dp)
    register_all_handlers(dp)
    register_all_middlewares(dp)

    # Send messages to all users
    users = UserMethods.get_all_users()

    if not users:
        return

    counter = 0
    for user in users:
        with suppress(ChatNotFound, BotBlocked):
            await dp.bot.send_message(user.tg_id, Messages.BOT_START, reply_markup=Keyboards.reply.START)
            counter += 1

    logging.info(f'В базе данных {len(users)} аккаунт(а/ов). Совершено {counter} рассылок')


async def __on_shutdown(dp: Dispatcher) -> None:
    logging.info('Bot shutdown')

    users = UserMethods.get_all_users()

    if not users:
        return

    for user in users:
        with suppress(ChatNotFound, BotBlocked):
            await dp.bot.send_message(user.tg_id, Messages.BOT_STOP, reply_markup=ReplyKeyboardRemove())

    Database().engine.dispose()


def start_bot() -> None:
    # Register DB models
    register_models()

    # Start telegram bot
    try:
        bot = Bot(token=Env.TOKEN, parse_mode='HTML')
        dp = Dispatcher(bot, storage=MemoryStorage())
        executor.start_polling(dp, skip_updates=True, on_startup=__on_startup, on_shutdown=__on_shutdown)
    except TelegramAPIError as telegram_exception:
        logging.error(telegram_exception)
