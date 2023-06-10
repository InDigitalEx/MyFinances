from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from app.filters import Callbacks
from app.keyboards import Keyboards
from app.utils import Messages, Buttons
from database.methods import Methods


async def __change_groups(msg: Message) -> None:
    user = Methods(msg.from_user.id)
    group_name = user.active_group.name
    keyboard = Keyboards.inline.change_groups(msg.from_user.id)

    await msg.answer(Messages.CHANGE_GROUPS.format(group_name=group_name),
                     reply_markup=keyboard)


async def __change_groups_callback(query: CallbackQuery, callback_data: dict) -> None:
    user = Methods(query.from_user.id)
    group_id = int(callback_data['group_id'])

    if user.active_group_id == group_id:
        await query.bot.answer_callback_query(query.id, Messages.ALREADY_IN_GROUP, cache_time=0)
    else:
        user.active_group_id = group_id

    group_name = user.active_group.name
    keyboard = Keyboards.inline.change_groups(query.from_user.id)
    await query.bot.edit_message_text(Messages.CHANGE_GROUPS.format(
        group_name=group_name),
        query.from_user.id,
        query.message.message_id,
        reply_markup=keyboard
    )


def register_groups_handlers(dp: Dispatcher) -> None:
    # Messages
    dp.register_message_handler(__change_groups, content_types=['text'], text=Buttons.START['groups'])

    # Callbacks
    dp.register_callback_query_handler(__change_groups_callback, Callbacks.CHANGE_GROUPS.filter())
