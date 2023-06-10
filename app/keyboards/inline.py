from abc import ABC
from dataclasses import dataclass
from typing import Final

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.filters import Callbacks
from app.utils import Buttons
from .util import get_user_groups_dict


@dataclass
class InlineKeyboards(ABC):
    SETTINGS: Final = InlineKeyboardMarkup(row_width=2)
    for key, value in Buttons.SETTINGS.items():
        SETTINGS.insert(InlineKeyboardButton(text=value, callback_data=key))

    AUTHOR: Final = InlineKeyboardMarkup(1).add(
        InlineKeyboardButton(text='VK', url='https://vk.com/in_dgtl'),
        InlineKeyboardButton(text='GitHub', url='https://github.com/InDigitalEx')
    )

    CANCEL_CREATE_GROUP: Final = InlineKeyboardMarkup(1).add(
        InlineKeyboardButton(text='Отмена', callback_data='cancel_create_group')
    )

    CANCEL_INVITE: Final = InlineKeyboardMarkup(1).add(
        InlineKeyboardButton(text='Отменить', callback_data='cancel_invite')
    )


    @staticmethod
    def change_groups(user_id: int) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)
        groups = get_user_groups_dict(user_id)

        for (index, text) in groups.items():
            keyboard.insert(InlineKeyboardButton(
                text=text,
                callback_data=Callbacks.CHANGE_GROUPS.new(group_id=index))
            )
        return keyboard

    @staticmethod
    def cancel_expense(group_name: str, expense_id: int) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(1).add(
            InlineKeyboardButton(
                text='Отменить',
                callback_data=Callbacks.CANCEL_EXPENSE.new(group_name=group_name, expense_id=expense_id))
        )
        return keyboard

    @staticmethod
    def cancel_income(group_name: str, income_id: int) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(1).add(
            InlineKeyboardButton(
                text='Отменить',
                callback_data=Callbacks.CANCEL_INCOME.new(group_name=group_name, income_id=income_id))
        )
        return keyboard

    @staticmethod
    def invite(group_id: int, inviter_id: int) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(
                text=Buttons.INVITE['accept'],
                callback_data=Callbacks.ACCEPT_INVITE.new(group_id=group_id, inviter_id=inviter_id)),
            InlineKeyboardButton(
                text=Buttons.INVITE['decline'],
                callback_data=Callbacks.DECLINE_INVITE.new(group_id=group_id, inviter_id=inviter_id))
        )
        return keyboard

    @staticmethod
    def statistics(type_: str, period: str, was_trimmed: bool = False, page: int = 0) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=3)

        # Prev page
        if page > 0:
            keyboard.insert(InlineKeyboardButton(
                text='⬅️',
                callback_data=Callbacks.STATISTICS.new(
                    type=type_, period=period, page=page-1
                )
            ))

        # Change type
        new_type = 'incomes' if type_ == 'expenses' else 'expenses'
        keyboard.insert(InlineKeyboardButton(
            text=Buttons.STAT_TYPE[type_],
            callback_data=Callbacks.STATISTICS.new(
                type=new_type, period=period, page=0
            )
        ))

        # Next page
        if was_trimmed:
            keyboard.insert(InlineKeyboardButton(
                text='➡️',
                callback_data=Callbacks.STATISTICS.new(
                    type=type_, period=period, page=page+1
                )
            ))

        # Period buttons
        keyboard.row()
        for name, text in Buttons.STAT_PERIOD.items():
            if name == period:
                continue

            keyboard.insert(InlineKeyboardButton(
                text=text,
                callback_data=Callbacks.STATISTICS.new(
                    type=type_, period=name, page=0
                )
            ))
        return keyboard
