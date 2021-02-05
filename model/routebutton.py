from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .constants import State


class Routebutton():

    @staticmethod
    def gray_pen():
        pen = qtg.QPen(qtc.Qt.lightGray, 12, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    @staticmethod
    def white_pen():
        pen = qtg.QPen(qtc.Qt.white, 12, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    @staticmethod
    def red_pen():
        pen = qtg.QPen(qtc.Qt.red, 6, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    def __init__(self, attr):
        self.state = State.UNKNOWN
        self.adr = attr['adr'].value
        self.x = int(attr['x'].value)
        self.y = int(attr['y'].value)

    def __repr__(self):
        return "Routebutton adr={},{} at ({},{})".format(self.adr, self.x, self.y)

    def __str__(self):
        return "Routebutton adr={},{} at ({},{})".format(self.adr, self.x, self.y)

    def touched(self, x, y):
        # distance of (x,y) to 'center' of route button
        dx = abs(self.x - x)
        dy = abs(self.y - y)
        if (dx * dx + dy * dy) < 300:
            return True
        else:
            return False

    # draw Route Btn
    def draw(self, qp, addr_flag):
        if self.state == State.UNKNOWN:
            qp.setPen(Routebutton.gray_pen())
        elif self.state == State.CLOSED:
            qp.setPen(Routebutton.gray_pen())
        elif self.state == State.THROWN:
            qp.setPen(Routebutton.white_pen())
        qp.drawEllipse(self.x-6, self.y-6, 12,12)
        qp.setPen(Routebutton.red_pen())
        if addr_flag:
            qp.drawText(self.x, self.y + 15, str(self.adr))

