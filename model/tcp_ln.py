# tcp_ln.py
# connects to LbServer and receives and send LN messages
# over TCP
#
# MB, 04 Aug 2020
# receive and send basically work

# import sys
from PyQt5 import QtNetwork as qtn
from PyQt5 import QtCore as qtc

from .constants import State


def get_acc_adr(ba):
    """calculate LocoNet ACCESSORY address from command
       bytes 1 and 2 code address"""
    adr = 1 + ba[1] & 0x7F  # A6...A0
    adr += (ba[2] & 0x0F) * 128
    return adr


def get_sens_adr(ba):  #
    """calculate LocoNet SENSOR address from command
       bytes 1 and 2 code address"""
    adr = ba[1] & 0x7F  # A7...A1 for sensors ONLY !
    adr += (ba[2] & 0x0F) * 128
    adr = adr << 1   # in case of sensor we will add the least significant bit
    adr += 1       # add 1 as always
    adr += (ba[2] & 0x20) >> 5   # add the least significant bit A0
    return adr


class TcpLNClient(qtc.QObject):
    """Network interface for loconet messages."""
    error = qtc.pyqtSignal(str)               # error msg
    rec_state = qtc.pyqtSignal(int, int)      # turnout(or signal)-address, state
    rec_sens_state = qtc.pyqtSignal(int, int)  # sensor-address, state
    error_to_gui = qtc.pyqtSignal(str)        # error msg

    def __init__(self, main_win):

        super().__init__()
        self.tcpSocket = qtn.QTcpSocket(self)
        self.blockSize = 0
        self.settings = main_win.settings

        self.port = self.get_port()           # 'safe' settings
        self.hostname = self.get_hostname()   # defaults to localhost
        self.tcpSocket.connectToHost(
            self.hostname, self.port, qtc.QIODevice.ReadWrite)

        self.tcpSocket.readyRead.connect(self.receive)
        self.tcpSocket.error.connect(self.display_error)

        self.last_adr = -1  # used in lack responses

        self.mw = main_win

    def get_port(self):
        port_string = self.settings.value('port')
        if port_string:
            try:
                port = int(port_string)
            except (TypeError, ValueError):
                port = 1234
        else:
            port = 1234
        return port

    def get_hostname(self):
        host = self.settings.value('hostname')
        if not host:
            host = 'localhost'
        return host

    def reconnect(self):
        self.port = self.get_port()  # 'safe' settings
        self.hostname = self.get_hostname()  # defaults to localhost
        self.tcpSocket.connectToHost(
            self.hostname, self.port, qtc.QIODevice.ReadWrite)

    def receive(self):
        input_string = str(self.tcpSocket.readAll(), 'utf-8')
        input_string = input_string.replace('\r', '')
        # TODO wait for the newline to appear until decoding the loconet string
        commands = input_string.split('\n')  # can be multiple commands in 1 input string
        for cmd in commands:
            # handle loconet server message
            if 'RECEIVE' in cmd:
                cmd = cmd.replace('RECEIVE ', '')
                self.handle_received_cmd(cmd)
            # nothing done currently with the following commands
            # if 'VERSION' in cmd:
            #    break
            # elif 'ERROR' in cmd:
            #    break
            # elif 'SENT OK' in cmd:
            #    break

    def handle_received_cmd(self, cmd):
        if len(cmd) < 11:  # 4byte commands checked only
            return
        print('rec: '+cmd)
        try:
            ba = bytearray.fromhex(cmd[:11])  # split into 4 bytes (throw away byte#5ff.)
        except ValueError:
            print("error in str to hex conversion "+"#"+cmd[:11]+"#")
            return
        if ba[0] == 0xA0:
            if self.settings.value('disp_loco_messages', type=bool):
                print("loco speed", end=" ")
                print(list(ba))
        elif ba[0] == 0xBC:     # example BC 0F 00 4C (request turnout state)
            #    ==> B4 3C 30 47 (=closed) or B4 3C 50 27 (=thrown)
            self.last_adr = get_acc_adr(ba)
            print("requesting T{}".format(self.last_adr))
        elif (ba[0] == 0xB4) and (ba[1] == 0x3C):
            # lack response to request turnout/signal state
            if (ba[2] & 0x30) == 0x30:
                print("T{} closed".format(self.last_adr))
                self.rec_state.emit(self.last_adr, State.CLOSED)
            else:
                print("T{} thrown".format(self.last_adr))
                self.rec_state.emit(self.last_adr, State.THROWN)
        elif ba[0] == 0xB0:  # set accessory (turnout or signal
            adr = get_acc_adr(ba)
            if (ba[2] & 0x20) == 0x20:    # 0x30 or 0x20
                print("T{} closed".format(adr))
                self.rec_state.emit(adr, State.CLOSED)
            else:  # 0x10 or 0x00
                print("T{} thrown".format(adr))
                self.rec_state.emit(adr, State.THROWN)
        elif ba[0] == 0xB2:  # sensor state
            adr = get_sens_adr(ba)
            # least significant bit of address is bit6 of ba[2]
            s_flag = self.settings.value('disp_sensor_messages', type=bool)
            if (ba[2] & 0x10) >> 4:
                if s_flag:
                    print("S{} occ".format(adr))
                self.rec_sens_state.emit(adr, State.OCCUPIED)
            else:
                if s_flag:
                    print("S{} free".format(adr))
                self.rec_sens_state.emit(adr, State.FREE)

    def display_error(self, socket_error):
        if socket_error == qtn.QAbstractSocket.RemoteHostClosedError:
            pass
        else:
            print("Error: %s." %
                  self.tcpSocket.errorString())
            self.error_to_gui.emit("Error: "+self.tcpSocket.errorString())

    def send_message(self, message):
        """Prepare and send a message"""
        msg = 'SEND ' + message + '\r\n'
        if self.tcpSocket.state() != qtn.QAbstractSocket.ConnectedState:
            # self.tcpSocket.connectToHost('localhost', self.port)
            self.reconnect()

        if self.tcpSocket.state() == qtn.QAbstractSocket.ConnectedState:
            print("sending: "+msg, end=" ")
            self.tcpSocket.write(msg.encode())
