# request states

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtNetwork as qtn
from PyQt5 import QtCore as qtc

from .constants import State


class RequestStates(qtc.QObject):

    def __init__(self):
        super().__init__()

    def buildLNRequestCommand(self, adr):
        if (adr > 127) or (adr < 1):  # TODO extend to higher addresses
            return
        # example BC 0F 00 4C (request turnout 16 state)
        cmd = [0xBC, (adr-1), 0x00, 0x00]
        # calc checksum
        chk = cmd[0] ^ cmd[1] ^ cmd[2]
        cmd[3] = chk ^ 0xFF
        cmdStr = " ".join(format(b, "02x") for b in cmd)
        return(cmdStr.upper())
