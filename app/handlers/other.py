from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.exceptions import MessageNotModified

from app.utils import Messages


async def __message_not_modified() -> bool:
    return True


async def __unknown_message(msg: Message) -> None:
    await msg.answer(Messages.UNKNOWN_MESSAGE)


def register_other_handlers(dp: Dispatcher) -> None:
    # Message
    dp.register_message_handler(__unknown_message, content_types=['text'])

    # Exceptions
    dp.register_errors_handler(__message_not_modified, exception=MessageNotModified)
