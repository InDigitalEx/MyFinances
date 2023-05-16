import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.utils.exceptions import TelegramAPIError

from app.filters import register_all_filters
from app.handlers import register_all_handlers
from app.middlewares import register_all_middlewares
from data import Env
from database.models import register_models


async def __on_startup(dp: Dispatcher) -> None:
    logging.info('Bot starts')

    register_all_filters(dp)
    register_all_handlers(dp)
    register_all_middlewares(dp)


async def __on_shutdown(dp: Dispatcher) -> None:
    logging.info('Bot shutdown')


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
