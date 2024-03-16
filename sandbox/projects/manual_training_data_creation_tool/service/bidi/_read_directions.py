from enum import Enum


class ReadDirection(Enum):
    RTL = -1
    AMBIGUOUS = 0
    LTR = 1
