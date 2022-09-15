from enum import Enum, auto


class EntryType(Enum):
    ENTRY = auto()
    DATE = auto()
    TIME = auto()
    DATETIME = auto()