from enum import Enum
from enum import auto


class ProgramState(Enum):
    START = auto()
    IN_GAME = auto()
    GAME_OVER = auto()
    PAUSE = auto()
    EXIT = auto()
