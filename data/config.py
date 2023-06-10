from abc import ABC
from dataclasses import dataclass
from typing import Final


@dataclass
class Config(ABC):
    PAGE_LENGHT: Final = 10
