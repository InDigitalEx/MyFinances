from re import Match

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from app.filters import Callbacks
from app.keyboards import Keyboards
from app.utils import Messages
from app.utils.util import user_active_group_answer
from database.methods import Methods


async def __add_expense_to_active_group(msg: Message, regexp: Match) -> None:
    amount: int = regexp[1]
    text: str = regexp[2]

    user = Methods(msg.from_user.id)
    group_name = user.active_group.name
    expense_id = user.create_expense(amount=amount, text=text).id

    # Messages
    user_markup = Keyboards.inline.cancel_expense(group_name, expense_id)
    user_message = Messages.EXPENSE_CREATE_TO_CREATOR.format(
        group_name=group_name, amount=amount, text=text)
    other_message = Messages.EXPENSE_CREATE_TO_USERS.format(
        group_name=group_name, name=msg.from_user.full_name, amount=amount, text=text)

    await user_active_group_answer(msg, user, user_message, user_markup, other_message)


async def __cancel_expense_callback(query: CallbackQuery, callback_data: dict) -> None:
    group_name = callback_data['group_name']
    expense_id = callback_data['expense_id']

    user = Methods(query.from_user.id)
    expense = user.get_expense(expense_id)

    # Message
    user_message = Messages.EXPENSE_DELETE_TO_CREATOR.format(
        group_name=group_name, amount=expense.amount, text=expense.text)
    other_message = Messages.EXPENSE_DELETE_TO_USERS.format(
        group_name=group_name, name=query.from_user.full_name,
        amount=expense.amount, text=expense.text
    )

    user.delete_expense_by_id(expense_id)
    await query.message.delete()
    await user_active_group_answer(query.message, user, user_message=user_message, other_message=other_message)


def register_expenses_handlers(dp: Dispatcher) -> None:
    # regexp: amount name
    dp.register_message_handler(__add_expense_to_active_group, regexp=r'^([0-9]+)\s*([^#\+]{0,32})$')

    # Callbacks
    dp.register_callback_query_handler(__cancel_expense_callback, Callbacks.CANCEL_EXPENSE.filter())
