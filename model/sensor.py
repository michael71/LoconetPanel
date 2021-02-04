from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .constants import State
from .track import Track


class Sensor(Track):

    @staticmethod
    def yellow_pen():
        pen = qtg.QPen(qtc.Qt.yellow, 4, qtc.Qt.CustomDashLine)
        pen.setDashPattern([3, 5, 3, 5])
        pen.setCapStyle(qtc.Qt.SquareCap)
        return pen

    @staticmethod
    def gray_pen():
        pen = qtg.QPen(qtc.Qt.lightGray, 4, qtc.Qt.CustomDashLine)
        pen.setDashPattern([3, 5, 3, 5])
        pen.setCapStyle(qtc.Qt.SquareCap)
        return pen

    @staticmethod
    def white_pen():
        pen = qtg.QPen(qtc.Qt.white, 4, qtc.Qt.CustomDashLine)
        pen.setDashPattern([3, 5, 3, 5])
        pen.setCapStyle(qtc.Qt.SquareCap)
        return pen

    @staticmethod
    def red_pen():
        pen = qtg.QPen(qtc.Qt.red, 4, qtc.Qt.CustomDashLine)
        pen.setDashPattern([3, 5, 3, 5])
        pen.setCapStyle(qtc.Qt.SquareCap)
        return pen

    def __init__(self, attr):
        super().__init__(attr)
        self.state = State.UNKNOWN
        addresses = str(attr['adr'].value).split(",")
        if (len(addresses) >= 1):
            self.adr = int(addresses[0])
        else:
            self.adr = -1
        if len(addresses) >= 2:
            self.adr2 = int(addresses[1])
        else:
            self.adr2 = -1

    def __repr__(self):
        return "Sensor adr={},{} at ({},{},{},{})".format(self.adr, self.adr2, self.x, self.x2, self.y, self.y2)

    def __str__(self):
        return "Sensor adr={},{} at ({},{},{},{})".format(self.adr, self.adr2, self.x, self.x2, self.y, self.y2)

    # draw Sensor
    def draw(self, qp, addr_flag):
        if self.state == State.UNKNOWN:
            qp.setPen(Sensor.gray_pen())
        elif self.state == State.FREE:
            qp.setPen(Sensor.white_pen())
        elif self.state == State.OCCUPIED:
            qp.setPen(Sensor.red_pen())
        qp.drawLine(self.x, self.y, self.x2, self.y2)
        qp.setPen(Sensor.red_pen())
        if addr_flag:
            qp.drawText((self.x + self.x2) / 2, self.y + 15, str(self.adr))

