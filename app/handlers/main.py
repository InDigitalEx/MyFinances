from aiogram import Dispatcher

from app.handlers.admin import register_admin_handlers
from app.handlers.other import register_other_handlers
from app.handlers.user import register_user_handlers


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_user_handlers,
        register_admin_handlers,
        register_other_handlers
    )
    for handler in handlers:
        handler(dp)
