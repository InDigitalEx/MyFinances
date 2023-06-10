from abc import ABC
from dataclasses import dataclass

from aiogram.utils.callback_data import CallbackData


@dataclass
class Callbacks(ABC):
    CHANGE_GROUPS = CallbackData('change_groups', 'group_id')
    CANCEL_EXPENSE = CallbackData('cancel_expense', 'group_name', 'expense_id')
    CANCEL_INCOME = CallbackData('cancel_income', 'group_name', 'income_id')
    ACCEPT_INVITE = CallbackData('accept_invite', 'group_id', 'inviter_id')
    DECLINE_INVITE = CallbackData('decline_invite', 'group_id', 'inviter_id')
    STATISTICS = CallbackData('statistics', 'type', 'period', 'page')
