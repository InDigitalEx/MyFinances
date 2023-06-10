from abc import ABC
from dataclasses import dataclass
from typing import Final

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.utils import Buttons


@dataclass
class ReplyKeyboards(ABC):
    START: Final = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие...'
    )
    for button in Buttons.START.values():
        START.insert(KeyboardButton(text=button))

    CREATE_GROUP_PRIVATE: Final = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True
    )
    for button in Buttons.CREATE_GROUP_PRIVATE.values():
        CREATE_GROUP_PRIVATE.insert(KeyboardButton(text=button))

    INVITE_TYPE: Final = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True
    )
    for button in Buttons.INVITE_TYPE.values():
        INVITE_TYPE.insert(KeyboardButton(text=button))