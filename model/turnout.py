from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .constants import State
from .track import Track


class Turnout(Track):

    @staticmethod
    def black_pen():
        pen = qtg.QPen(qtc.Qt.black, 6, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    @staticmethod
    def background_pen():
        pen = qtg.QPen(qtc.Qt.lightGray, 6, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    @staticmethod
    def red_pen():
        pen = qtg.QPen(qtc.Qt.red, 6, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    @staticmethod
    def green_pen():
        pen = qtg.QPen(qtc.Qt.green, 6, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    def __init__(self, attr):
        super().__init__(attr)
        self.xt = int(attr['xt'].value)
        self.yt = int(attr['yt'].value)
        try:
            self.adr = int(attr['adr'].value)
        except KeyError:
            # address missing in xml file
            self.adr = -1
        self.state = State.UNKNOWN

    def draw(self, qp, addr_flag):
        if self.state == State.UNKNOWN:
            qp.setPen(Turnout.green_pen())
            qp.drawLine(self.x, self.y, self.x2, self.y2)
            qp.setPen(Turnout.red_pen())
            qp.drawLine(self.x, self.y, self.xt, self.yt)
        elif self.state == State.CLOSED:
            qp.setPen(Turnout.background_pen())
            qp.drawLine(self.x, self.y, self.xt, self.yt)
            qp.setPen(Turnout.black_pen())
            qp.drawLine(self.x, self.y, self.x2, self.y2)
        elif self.state == State.THROWN:
            qp.setPen(Turnout.background_pen())
            qp.drawLine(self.x, self.y, self.x2, self.y2)
            qp.setPen(Turnout.black_pen())
            qp.drawLine(self.x, self.y, self.xt, self.yt)
        qp.setPen(Turnout.red_pen())
        if addr_flag:
            qp.drawText((self.x + self.x2) / 2, self.y + 15, str(self.adr))

    def touched(self, x, y):
        # distance of (x,y) to 'center' of turnout points
        dx = abs((self.x + self.x2 + self.xt) / 3 - x)
        dy = abs((self.y + self.y2 + self.yt) / 3 - y)
        if (dx * dx + dy * dy) < 300:
            return True
        else:
            return False

    def __repr__(self):
        return ("Turnout adr={} at ({},{},{},{})".format(self.adr, self.x, self.x2,
                                                         self.y, self.y2))

    def __str__(self):
        return ("Turnout adr={} at ({},{},{},{})".format(self.adr, self.x, self.x2,
                                                         self.y, self.y2))

