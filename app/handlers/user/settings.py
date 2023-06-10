from aiogram import Dispatcher
from aiogram.types import Message

from app.keyboards import Keyboards
from app.utils import Buttons
from app.utils import Messages


async def __settings(msg: Message) -> None:
    await msg.answer(Messages.SETTINGS, reply_markup=Keyboards.inline.SETTINGS)


def register_settings_handlers(dp: Dispatcher) -> None:
    # Messages
    dp.register_message_handler(__settings, content_types=['text'], text=Buttons.START['settings'])

    # Callbacks
