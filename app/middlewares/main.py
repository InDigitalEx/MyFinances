from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware


def register_all_middlewares(dp: Dispatcher) -> None:
    dp.middleware.setup(LoggingMiddleware())
