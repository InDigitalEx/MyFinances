from typing import List, Dict, AnyStr, Tuple

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from app.filters import Callbacks
from app.keyboards import Keyboards
from app.utils import Buttons, Messages, DateGroupsSorter
from database.methods import Methods


def _get_items_str(items: Dict | List, indent: int=0) -> AnyStr:
    result = ''
    for key, value in items.items():
        result += f"{'  '*indent}<b>{key}</b>\n"

        if isinstance(value, Dict):
            result += _get_items_str(value, indent+1)
        else:
            for item in value:
                result += '  ' * (indent + 1) + Messages.STATISTICS_ITEM.format(
                amount=item.amount, text=item.text
            )
    if not result:
        result += Messages.STATISTICS_MISSING
    return result

def _get_message_str(
        items: List,
        group_name: str,
        type_: str = 'expenses',
        period: str='month',
        page: int=0
) -> Tuple[AnyStr, bool]:
    items, was_trimmed = DateGroupsSorter(items).get_by_name(period, page)
    items_str = _get_items_str(items)
    type_str = Messages.EXPENSES if type_ == 'expenses' else Messages.INCOMES
    return Messages.STATISTICS.format(group_name=group_name, type=type_str, items=items_str), was_trimmed


async def __statistics(msg: Message) -> None:
    user = Methods(msg.from_user.id)
    active_group = user.active_group
    expenses = active_group.expenses

    message, was_trimmed = _get_message_str(expenses, active_group.name)
    await msg.answer(message,
                     reply_markup=Keyboards.inline.statistics('expenses', 'month', was_trimmed))


async def __statistics_callback(query: CallbackQuery, callback_data: dict) -> None:
    type_ = callback_data["type"]
    period = callback_data["period"]
    page = int(callback_data["page"])

    user = Methods(query.from_user.id)
    active_group = user.active_group
    items = active_group.expenses if type_ == 'expenses' else active_group.incomes

    message, was_trimmed = _get_message_str(items, active_group.name, type_, period, page)
    await query.message.edit_text(
        text=message,
        reply_markup=Keyboards.inline.statistics(type_, period, was_trimmed, page)
    )


def register_statistics_handlers(dp: Dispatcher) -> None:
    # Messages
    dp.register_message_handler(__statistics, content_types=['text'], text=Buttons.START['statistics'])

    # Callbacks
    dp.register_callback_query_handler(__statistics_callback, Callbacks.STATISTICS.filter())
