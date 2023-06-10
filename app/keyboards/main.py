from abc import ABC
from dataclasses import dataclass
from typing import Final

from .inline import InlineKeyboards
from .reply import ReplyKeyboards


@dataclass
class Keyboards(ABC):
    inline: Final = InlineKeyboards
    reply: Final = ReplyKeyboards
