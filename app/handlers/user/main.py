from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.keyboards import Keyboards
from app.utils import Buttons
from app.utils import Messages
from database.methods import Methods
from .create_group import register_create_group_handlers
from .expenses import register_expenses_handlers
from .groups import register_groups_handlers
from .incomes import register_incomes_handlers
from .invite import register_invite_handlers
from .settings import register_settings_handlers
from .statistics import register_statistics_handlers


async def __start(msg: Message) -> None:
    user = Methods(msg.from_user.id)
    group_name = user.active_group.name

    await msg.answer(Messages.START.format(
        name=msg.from_user.first_name, group=group_name),
        reply_markup=Keyboards.reply.START
    )


async def __help(msg: Message) -> None:
    await msg.answer(Messages.HELP)


async def __author(msg: Message) -> None:
    await msg.answer(Messages.AUTHOR, reply_markup=Keyboards.inline.AUTHOR)


def register_user_handlers(dp: Dispatcher) -> None:
    # region Messages

    dp.register_message_handler(__start, CommandStart(''))
    dp.register_message_handler(__help, content_types=['text'], text=Buttons.START['help'])
    dp.register_message_handler(__author, content_types=['text'], text=Buttons.START['author'])

    #endregion

    # region handlers

    register_create_group_handlers(dp)
    register_expenses_handlers(dp)
    register_groups_handlers(dp)
    register_incomes_handlers(dp)
    register_invite_handlers(dp)
    register_settings_handlers(dp)
    register_statistics_handlers(dp)

    #endregion
