from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from app.keyboards import Keyboards
from app.states import InviteState
from app.utils import Buttons, Messages
from database.methods import Methods
from .link import register_invite_link_handlers
from .personal import register_invite_personal_handlers


async def __invite(msg: Message) -> None:
    group_name = Methods(msg.from_user.id).group_name

    await msg.answer(
        Messages.INVITE.format(group_name=group_name),
        reply_markup=Keyboards.reply.INVITE_TYPE)

    await InviteState.TYPE.set()


async def __invite_type_invalid(msg: Message) -> None:
    await msg.answer(Messages.INVITE_TYPE_INVALID, reply_markup=Keyboards.reply.INVITE_TYPE)


async def __cancel_invite_callback(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_reply_markup(None)
    await query.message.answer(Messages.CANCEL_INVITE, reply_markup=Keyboards.reply.START)
    await state.finish()


def register_invite_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(
        __invite,
        content_types=['text'],
        text=Buttons.START['invite']
    )
    dp.register_message_handler(
        __invite_type_invalid,
        lambda msg: msg.text not in Buttons.INVITE_TYPE.values(),
        state=InviteState.TYPE
    )

    # Callbacks
    dp.register_callback_query_handler(
        __cancel_invite_callback,
        lambda c: c.data == 'cancel_invite',
        state=InviteState
    )

    # Other handlers
    register_invite_link_handlers(dp)
    register_invite_personal_handlers(dp)
