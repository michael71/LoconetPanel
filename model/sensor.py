from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

import config
from .constants import State, SensorRouteState
from .track import Track


def set_sensors_route_state(s_list_str, state):
    a_list = s_list_str.split(',')
    map_object = map(int, a_list)
    list_of_integers = list(map_object)
    for s_adr in list_of_integers:
        for s in config.sens:
            if s_adr == s.adr:
                s.route_state = state


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
        self.route_state = SensorRouteState.NOT_IN_ROUTE
        addresses = str(attr['adr'].value).split(",")
        if len(addresses) >= 1:
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
        if self.route_state == SensorRouteState.NOT_IN_ROUTE:
            if self.state == State.UNKNOWN:
                qp.setPen(Sensor.gray_pen())
            elif self.state == State.FREE:
                qp.setPen(Sensor.white_pen())
            elif self.state == State.OCCUPIED:
                qp.setPen(Sensor.red_pen())
        else:
            if self.state == State.UNKNOWN or self.state == State.FREE:
                qp.setPen(Sensor.yellow_pen())
            else:
                qp.setPen(Sensor.red_pen())

        qp.drawLine(self.x, self.y, self.x2, self.y2)
        qp.setPen(Sensor.red_pen())
        if addr_flag:
            qp.drawText((self.x + self.x2) / 2, self.y - 5, str(self.adr))

