from enum import Enum, auto


class EntryType(Enum):
    ENTRY = auto()
    DATE = auto()
    DATETIME = auto()
    DROPDOWN = auto()
    RANGE = auto()
    TIME = auto()