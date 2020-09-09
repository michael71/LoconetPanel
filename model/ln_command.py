# ln_command.py
# build LN commands from addresses, states ...

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtNetwork as qtn
from PyQt5 import QtCore as qtc

from .constants import State


def request_state(adr):
    if (adr > 127) or (adr < 1):  # TODO extend to higher addresses
        return
    # example BC 0F 00 4C (request turnout 16 state)
    cmd = [0xBC, (adr - 1), 0x00, 0x00]
    # calc checksum
    chk = cmd[0] ^ cmd[1] ^ cmd[2]
    cmd[3] = chk ^ 0xFF
    cmd_str = " ".join(format(b, "02x") for b in cmd)
    return cmd_str.upper()


# B0 00 10 5F   1 => Abzweig, danach B0 00 00 4F (vermutlich "magnetantrieb aus")
# B0 03 30 7C   adr 4 => gerade, danach B0 03 20 6C
def set_accessory(adr, st):
    if (adr > 127) or (adr < 1):  # TODO extend to higher addresses
        return
    if st == 1:
        cmd = [0xB0, (adr - 1), 0x30, 0x00]
    else:
        cmd = [0xB0, (adr - 1), 0x10, 0x00]
    # calc checksum
    chk = cmd[0] ^ cmd[1] ^ cmd[2]
    cmd[3] = chk ^ 0xFF
    cmd_str = " ".join(format(b, "02x") for b in cmd)
    return cmd_str.upper()


