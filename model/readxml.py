# readxml.py   (xml read with "minidom" parser)
#
# MB, 02 Feb 2021
#
# see: https://stackoverflow.com/questions/1912434/how-do-i-parse-xml-in-python

from xml.dom import minidom

import config
from .track import Track
from .turnout import Turnout
from .sensor import Sensor
from .signal import Signal
from .routebutton import Routebutton
from .route import Route


class PanelData:

    def __init__(self):
        pass

    def readXML(self, filename, printFlag):
        xmldoc = minidom.parse(filename)
        print('reading xml-file: '+filename)

        config.trks = []
        config.turn = []
        config.sens = []
        config.signals = []
        config.rtBtns = []
        config.routes = []

        track_list = xmldoc.getElementsByTagName('track')
        for t in track_list:
            config.trks.append(Track(t.attributes))

        turnout_list = xmldoc.getElementsByTagName('turnout')
        for t in turnout_list:
            config.turn.append(Turnout(t.attributes))

        sensor_list = xmldoc.getElementsByTagName('sensor')
        for t in sensor_list:
            config.sens.append(Sensor(t.attributes))

        signal_list = xmldoc.getElementsByTagName('signal')
        for t in signal_list:
            config.signals.append(Signal(t.attributes))

        rtbtns_list = xmldoc.getElementsByTagName('routebutton')
        for t in rtbtns_list:
            config.rtBtns.append(Routebutton(t.attributes))

        routes_list = xmldoc.getElementsByTagName('route')
        for t in routes_list:
            config.routes.append(Route(t.attributes))

        if printFlag:
            print(str(len(config.trks)) + " tracks:")
            for tr in config.trks:
                print(tr)

            print(str(len(config.turn)) + " turnouts:")
            for tu in config.turn:
                print(tu)

            print(str(len(config.sens)) + " sensors:")
            for se in config.sens:
                print(se)

            print(str(len(config.signals)) + " signals:")
            for si in config.signals:
                print(si)

            print(str(len(config.rtBtns)) + " route buttons:")
            for rb in config.rtBtns:
                print(rb)

            print(str(len(config.routes)) + " routes:")
            for ro in config.routes:
                print(ro)

        # determine place needed for panel
        panel_w = 0
        panel_h = 0
        for tr in config.trks:
            if tr.x > panel_w:
                panel_w = tr.x
            if (tr.x2 > panel_w):
                panel_w = tr.x2
            if (tr.y > panel_h):
                panel_h = tr.y
            if (tr.y2 > panel_h):
                panel_h = tr.y2

        return panel_w, panel_h
