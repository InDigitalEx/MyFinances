from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from app.keyboards import Keyboards
from app.states import CreateGroupState
from app.utils import Buttons, Messages
from database.methods import Methods


# Create group handlers
async def __create_group(msg: Message) -> None:
    await CreateGroupState.NAME.set()
    await msg.answer(Messages.CREATE_GROUP, reply_markup=Keyboards.inline.CANCEL_CREATE_GROUP)


async def __create_group_name(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = msg.text

    await CreateGroupState.next()
    await msg.answer(Messages.CREATE_GROUP_PRIVATE,
                     reply_markup=Keyboards.reply.CREATE_GROUP_PRIVATE)


async def __create_group_name_invalid(msg: Message) -> None:
    await msg.answer(Messages.CREATE_GROUP_NAME_INVALID,
                     reply_markup=ReplyKeyboardRemove())


async def __create_group_private(msg: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        name = data['name']
        private = True if msg.text == Buttons.CREATE_GROUP_PRIVATE['private'] else False

        user = Methods(msg.from_user.id)
        group = user.create_group(name, private)
        user.active_group = group
        await msg.answer(Messages.CREATE_GROUP_DONE.format(group_name=name),
                         reply_markup=Keyboards.reply.START)
    await state.finish()


async def __create_group_private_invalid(msg: Message) -> None:
    await msg.answer(Messages.CREATE_GROUP_PRIVATE_INVALID,
                     reply_markup=Keyboards.reply.CREATE_GROUP_PRIVATE)


async def __cancel_create_group_callback(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.edit_reply_markup(None)
    await query.message.answer(Messages.CANCEL_CREATE_GROUP, reply_markup=Keyboards.reply.START)
    await state.finish()


def register_create_group_handlers(dp: Dispatcher) -> None:
    # region Messages

    dp.register_message_handler(__create_group, content_types=['text'], text=Buttons.START['create_group'])
    dp.register_message_handler(
        __create_group_name_invalid,
        lambda msg: msg.text in Buttons.START.values(),
        state=CreateGroupState.NAME
    )
    dp.register_message_handler(__create_group_name, content_types=['text'], state=CreateGroupState.NAME)

    dp.register_message_handler(
        __create_group_private_invalid,
        lambda msg: msg.text not in Buttons.CREATE_GROUP_PRIVATE.values(),
        state=CreateGroupState.PRIVATE
    )
    dp.register_message_handler(__create_group_private, content_types=['text'], state=CreateGroupState.PRIVATE)

    #endregion

    # region Callbacks

    dp.register_callback_query_handler(__cancel_create_group_callback,
                                       lambda c: c.data == "cancel_create_group",
                                       state=CreateGroupState)

    #endregion
