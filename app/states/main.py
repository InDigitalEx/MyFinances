from typing import Final

from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateGroupState(StatesGroup):
    NAME: Final = State()
    PRIVATE: Final = State()


class InviteState(StatesGroup):
    TYPE: Final = State()
    PERSONAL: Final = State()
