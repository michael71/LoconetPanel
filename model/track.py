#
# 04 Aug 2020 - (C) Michael Blank
#

from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc


class Track:

    @staticmethod
    def track_pen():
        pen = qtg.QPen(qtc.Qt.GlobalColor.black, 6, qtc.Qt.PenStyle.SolidLine)
        pen.setCapStyle(qtc.Qt.PenCapStyle.RoundCap)
        return pen

    def __init__(self, attr):
        self.x = int(attr['x'].value)
        self.x2 = int(attr['x2'].value)
        self.y = int(attr['y'].value)
        self.y2 = int(attr['y2'].value)

    def __repr__(self):
        return "Track at ({},{},{},{})".format(self.x, self.x2, self.y, self.y2)

    def __str__(self):
        return "Track at ({},{},{},{})".format(self.x, self.x2, self.y, self.y2)

    def draw(self, qp, addr_flag):
        qp.setPen(Track.track_pen())
        qp.drawLine(self.x, self.y, self.x2, self.y2)

