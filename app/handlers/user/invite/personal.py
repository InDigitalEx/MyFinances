from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from app.filters import Callbacks
from app.keyboards import Keyboards
from app.states import InviteState
from app.utils import Buttons, Messages
from app.utils.util import user_active_group_answer
from database.methods import Methods


async def __invite_personal(msg: Message) -> None:
    await msg.answer(Messages.INVITE_PERSONAL, reply_markup=Keyboards.inline.CANCEL_INVITE)
    await InviteState.PERSONAL.set()


async def __invite_personal_contact(msg: Message, state: FSMContext) -> None:
    contact_id = msg.contact.user_id

    if contact_id == msg.from_user.id:
        await msg.answer(Messages.INVITE_PERSONAL_SENDER_CONTACT)
        return None

    if not Methods.is_user_exists(contact_id):
        await msg.answer(Messages.INVITE_PERSONAL_CONTACT_NOT_EXISTS,
                         reply_markup=Keyboards.reply.START)
        await state.finish()
        return None

    user = Methods(msg.from_user.id)
    group = user.active_group
    if Methods(contact_id).is_in_group(group.id):
        await msg.answer(Messages.INVITE_PERSONAL_CONTACT_IN_GROUP,
                         reply_markup=Keyboards.reply.START)
        await state.finish()
        return None

    await msg.bot.send_message(contact_id, Messages.INVITE_PERSONAL_SEND.format(
            group_name=group.name, inviter=msg.from_user.full_name),
                               reply_markup=Keyboards.inline.invite(group.id, msg.from_user.id))

    contact_name = msg.contact.full_name
    await user_active_group_answer(
        msg=msg,
        methods=user,
        user_message=Messages.INVITE_PERSONAL_SEND_TO_INVITER.format(
            name=contact_name, group_name=group.name),
        other_message=Messages.INVITE_PERSONAL_SEND_TO_USERS.format(
            group_name=group.name, inviter=msg.from_user.full_name, name=contact_name),
        user_markup=Keyboards.reply.START,
        other_markup=None
    )
    await state.finish()


async def __invite_personal_contact_invalid(msg: Message) -> None:
    await msg.answer(Messages.INVITE_PERSONAL_CONTACT_INVALID)


async def __invite_accept(query: CallbackQuery, callback_data: dict) -> None:
    group_id = int(callback_data['group_id'])
    inviter_id = int(callback_data['inviter_id'])

    user = Methods(query.from_user.id)
    group = user.add_to_group(group_id)

    user_message = Messages.INVITE_PERSONAL_ACCEPT.format(
        group_name=group.name
    )
    other_message = Messages.INVITE_PERSONAL_ACCEPT_TO_USERS.format(
        group_name=group.name, name=query.from_user.full_name
    )

    await user_active_group_answer(
        msg=query.message,
        methods=user,
        user_message=user_message,
        other_message=other_message
    )
    await query.message.delete()


async def __invite_decline(query: CallbackQuery, callback_data: dict) -> None:
    group_id = int(callback_data['group_id'])
    inviter_id = int(callback_data['inviter_id'])

    await query.message.answer(Messages.INVITE_PERSONAL_DECLINE)
    await query.message.delete()
    await query.bot.send_message(
        inviter_id,
        Messages.INVITE_PERSONAL_DECLINE_TO_INVITER.format(
            name=query.from_user.full_name,
            group_name=Methods.get_group_by_id(group_id).name
        )
    )


def register_invite_personal_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        __invite_personal,
        content_types=['text'],
        text=Buttons.INVITE_TYPE['personal'],
        state=InviteState.TYPE
    )


    dp.register_message_handler(__invite_personal_contact, content_types=['contact'], state=InviteState.PERSONAL)
    dp.register_message_handler(__invite_personal_contact_invalid, state=InviteState.PERSONAL)

    # Callbacks
    dp.register_callback_query_handler(__invite_accept, Callbacks.ACCEPT_INVITE.filter())
    dp.register_callback_query_handler(__invite_decline, Callbacks.DECLINE_INVITE.filter())
