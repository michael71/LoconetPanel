from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .constants import State
from .track import Track



class Signal(Track):

    @staticmethod
    def black_pen():
        pen = qtg.QPen(qtc.Qt.black, 3, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    @staticmethod
    def red_pen():
        pen = qtg.QPen(qtc.Qt.red, 4, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    @staticmethod
    def green_pen():
        pen = qtg.QPen(qtc.Qt.green, 4, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    @staticmethod
    def gray_pen():
        pen = qtg.QPen(qtc.Qt.lightGray, 4, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    def __init__(self, attr):
        super().__init__(attr)
        try:
            self.adr = int(attr['adr'].value)
        except KeyError:
            # address missing in xml file
            self.adr = -1
        self.state = State.UNKNOWN

    def draw(self, qp, addr_flag):
        qp.setPen(Signal.black_pen())
        qp.drawEllipse(self.x-5, self.y-5,10,10)
        qp.drawLine(self.x, self.y, self.x2, self.y2)
        if self.state == State.CLOSED:
            qp.setPen(Signal.red_pen())
        elif self.state == State.THROWN:
            qp.setPen(Signal.green_pen())
        elif self.state == State.UNKNOWN:
            qp.setPen(Signal.gray_pen())
        qp.drawEllipse(self.x - 2, self.y - 2,4,4)
        qp.setPen(Signal.red_pen())
        if addr_flag:
            qp.drawText((self.x + self.x2) / 2, self.y + 15, str(self.adr))

    def touched(self, x, y):
        # distance of (x,y) to 'center' of turnout points
        dx = abs(self.x - x)
        dy = abs(self.y - y)
        if (dx * dx + dy * dy) < 300:
            return True
        else:
            return False

    def __repr__(self):
        return ("Signal adr={} at ({},{},{},{})".format(self.adr, self.x, self.x2,
                                                         self.y, self.y2))

    def __str__(self):
        return ("Signal adr={} at ({},{},{},{})".format(self.adr, self.x, self.x2,
                                                         self.y, self.y2))
