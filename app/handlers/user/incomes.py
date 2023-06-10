from re import Match

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from app.filters import Callbacks
from app.keyboards import Keyboards
from app.utils import Messages
from app.utils.util import user_active_group_answer
from database.methods import Methods


async def __add_income_to_active_group(msg: Message, regexp: Match) -> None:
    amount: int = regexp[2]
    text: str = regexp[3]

    user = Methods(msg.from_user.id)
    group_name = user.active_group.name
    income_id = user.create_income(amount=amount, text=text).id

    # Messages
    user_markup = Keyboards.inline.cancel_income(group_name, income_id)
    user_message = Messages.INCOME_CREATE_TO_CREATOR.format(
        group_name=group_name, amount=amount, text=text)
    other_message = Messages.INCOME_CREATE_TO_USERS.format(
        group_name=group_name, name=msg.from_user.full_name, amount=amount, text=text)

    await user_active_group_answer(msg, user, user_message, user_markup, other_message)


async def __cancel_income_callback(query: CallbackQuery, callback_data: dict) -> None:
    group_name = callback_data['group_name']
    income_id = callback_data['income_id']

    user = Methods(query.from_user.id)
    income = user.get_income(income_id)

    # Message
    user_message = Messages.INCOME_DELETE_TO_CREATOR.format(
        group_name=group_name, amount=income.amount, text=income.text)
    other_message = Messages.INCOME_DELETE_TO_USERS.format(
        group_name=group_name, name=query.from_user.full_name,
        amount=income.amount, text=income.text
    )

    user.delete_income_by_id(income_id)
    await query.message.delete()
    await user_active_group_answer(query.message, user, user_message=user_message, other_message=other_message)


def register_incomes_handlers(dp: Dispatcher) -> None:
    # Расход amount name
    dp.register_message_handler(__add_income_to_active_group,
                                regexp=r'^(добавить|доход)\s([0-9]+)\s*([^#\+]{0,32})$')

    # Callbacks
    dp.register_callback_query_handler(__cancel_income_callback, Callbacks.CANCEL_INCOME.filter())
