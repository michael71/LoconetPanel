from enum import Enum, IntEnum
from PyQt5 import QtCore as qtc


class State(IntEnum):
    CLOSED = 0
    THROWN = 1
    UNKNOWN = 2
    FREE = 3
    OCCUPIED = 4

MIN_SCALE = 0.7
MAX_SCALE = 3.0