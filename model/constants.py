from enum import Enum, IntEnum
from PyQt5 import QtCore as qtc


class State(IntEnum):
    CLOSED = 0  # also Hp0
    THROWN = 1  # also Hp1
    UNKNOWN = 2
    FREE = 3
    OCCUPIED = 4
    # HP2 = 3
    # SH1 = 4


class BtnState(IntEnum):
    NOT_SEL = 0      # button not selected
    FIRST_SEL = 1    # button is first selected button
    SECOND_SEL = 2      # button is second selected button


class RouteState(IntEnum):
    NOT_ACTIVE = 0
    ACTIVE = 1


MIN_SCALE = 0.7
MAX_SCALE = 3.0
