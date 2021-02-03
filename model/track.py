# classes track, sensor, turnout to hold data of panel elements
#
# 04 Aug 2020 - (C) Michael Blank
#


from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .constants import State
import config


class Track:

    @staticmethod
    def track_pen():
        pen = qtg.QPen(qtc.Qt.black, 6, qtc.Qt.SolidLine)
        pen.setCapStyle(qtc.Qt.RoundCap)
        return pen

    def __init__(self, attr):
        self.x = int(attr['x'].value)
        self.x2 = int(attr['x2'].value)
        self.y = int(attr['y'].value)
        self.y2 = int(attr['y2'].value)

    def __repr__(self):
        return ("Track at ({},{},{},{})".format(self.x, self.x2, self.y, self.y2))

    def __str__(self):
        return ("Track at ({},{},{},{})".format(self.x, self.x2, self.y, self.y2))

    def draw(self, qp):
        qp.setPen(Track.track_pen())
        qp.drawLine(self.x, self.y, self.x2, self.y2)


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
    def redpen():
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
        if (len(addresses) >= 2):
            self.adr2 = int(addresses[1])
        else:
            self.adr2 = -1

    def __repr__(self):
        return ("Sensor adr={},{} at ({},{},{},{})".format(self.adr, self.adr2, self.x, self.x2, self.y, self.y2))

    def __str__(self):
        return ("Sensor adr={},{} at ({},{},{},{})".format(self.adr, self.adr2, self.x, self.x2, self.y, self.y2))

    # draw Sensor
    def draw(self, qp, addr_flag):
        if self.state == State.UNKNOWN:
            qp.setPen(Sensor.gray_pen())
        elif self.state == State.FREE:
            qp.setPen(Sensor.white_pen())
        elif self.state == State.OCCUPIED:
            qp.setPen(Sensor.redpen())
        qp.drawLine(self.x, self.y, self.x2, self.y2)
        qp.setPen(Sensor.redpen())
        if addr_flag:
            qp.drawText((self.x + self.x2) / 2, self.y + 15, str(self.adr))


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
        qp.drawEllipse(self.x-4, self.y-4,8,8)
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
