import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.deep_linking import get_start_link

from app.keyboards import Keyboards
from app.states import InviteState
from app.utils import Buttons, Messages
from app.utils.util import user_active_group_answer, get_full_name_by_tg_id
from database.methods import Methods

# Constants
INVITE_LINK_REGEX = re.compile(r'^gid-(\d+)uid-(\d+)$')


async def __invite_link(msg: Message, state: FSMContext) -> None:
    user = Methods(msg.from_user.id)

    group = user.active_group
    link = await get_start_link(f'gid-{group.id}uid-{msg.from_user.id}', encode=True)

    await msg.answer(
        Messages.INVITE_LINK.format(group_name=group.name, link=link),
        reply_markup=Keyboards.reply.START
    )
    await state.finish()


async def __invite_link_join(msg: Message, deep_link: re.Match) -> None:
    group_id = int(deep_link[1])
    inviter_id = int(deep_link[2])

    # if the user is the inviter
    if msg.from_user.id == inviter_id:
        await msg.answer(
            Messages.INVITE_LINK_USER_IS_INVITER,
            reply_markup=Keyboards.reply.START
        )
        return None

    # is user already in group
    user = Methods(msg.from_user.id)

    if user.is_in_group(group_id):
        await msg.answer(
            Messages.INVITE_LINK_USER_IN_GROUP,
            reply_markup=Keyboards.reply.START
        )
        return None

    # Add user to group
    group = user.add_to_group(group_id)
    user.active_group = group

    # Send messages to active user group
    inviter_name = await get_full_name_by_tg_id(msg.bot, inviter_id)
    user_message = Messages.INVITE_LINK_JOIN.format(
        name=inviter_name,
        group_name=group.name
    )
    other_message = Messages.INVITE_LINK_JOIN_TO_USERS.format(
        name=msg.from_user.full_name,
        group_name=group.name
    )
    await user_active_group_answer(
        msg=msg,
        methods=user,
        user_message=user_message,
        user_markup=Keyboards.reply.START,
        other_message=other_message
    )


def register_invite_link_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        __invite_link,
        content_types=['text'],
        text=Buttons.INVITE_TYPE['link'],
        state=InviteState.TYPE
    )
    dp.register_message_handler(
        __invite_link_join,
        CommandStart(INVITE_LINK_REGEX, encoded=True)
    )
