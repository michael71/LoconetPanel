'''
loconet_panel main program
04 Aug 2020 - by MB
'''

#  TODO scale touch() method

import sys
import os
from pathlib import Path

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from model import constants as const
from model.readxml import PanelData

from model.tcp_ln import TcpLNClient
from view.settings import SettingsDialog
import model.ln_command as ln_command

import config


# print statistical info about panel data
def print_statistics():
    print("main, #trks=" + str(len(config.trks)))
    print("main, #sens=" + str(len(config.sens)))
    print("main, #turn=" + str(len(config.turn)))
    print("main, #signals=" + str(len(config.signals)))
    print("main, #rt-buttons=" + str(len(config.rtBtns)))
    # print("main, adr of first sensor="+str(config.sens[0].adr))

class MainWindow(qtw.QMainWindow):
    """application main window
    """


    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here

        self.settings = qtc.QSettings('blank-edv', 'loconet_panel')
        self.counter = 0

        self.graphics = qtw.QWidget()
        self.setCentralWidget(self.graphics)

        self.setWindowTitle('LN Panel')

        # start Loconet communication
        self.interface = TcpLNClient(self)
#        self.submitted.connect(self.interface.send_message)
#        self.interface.received.connect(self.received_message)    NOT USED
        self.interface.rec_state.connect(self.rec_accessory_state_change)
        self.interface.rec_sens_state.connect(self.rec_sensor_state_change)
        self.interface.error_to_gui.connect(
            #            lambda x: qtw.QMessageBox.critical(None, 'Error', x))
            self.status_msg)

        # Setup the menu
        self.build_menu()
        self.simulationIsOn = True

        panel_file = self.settings.value('panel_file')
        if not panel_file or not os.path.isfile(panel_file):
            print("from settings: filename=None")
            self.select_file()  #includes read_data_file()
        else:
            print("from settings: filename=" + panel_file)
            self.read_data_file(panel_file)

        self.timer = qtc.QTimer()
        self.timer.setInterval(400)   # every 400 millis
        self.timer.timeout.connect(self.timer_interval)
        self.tu_it = iter(config.turn)
        self.timer.start()

        self.panel_w = 600
        self.panel_h = 400

        # End main UI code
        self.show()

    def timer_interval(self):
        self.counter += 1
        if self.counter <= 10:
            return
        if self.counter >= (10 + len(config.turn)):
            self.timer.stop()
        try:
            adr = next(self.tu_it).adr
            lnstring = ln_command.request_state(adr)
            if lnstring:
                self.interface.send_message(lnstring)
        except StopIteration:
            print("end of iteration")

    def build_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu('File')
        file_menu.addAction('Open Panel File', self.select_file)
        file_menu.addAction('Settings', self.show_settings)
        file_menu.addSeparator()
        file_menu.addAction('Exit', self.close)

        edit_menu = menu.addMenu('Help')
        edit_menu.addAction('About', self.showAboutBox)

    def show_settings(self):
        old_port = self.settings.value('port')
        old_hostname = self.settings.value('hostname')
        settings_dialog = SettingsDialog(self.settings, self)
        settings_dialog.exec()
        self.update()  # display settings may have changed
        # if network settings have been changed
        if (old_port != self.settings.value('port')) or (old_hostname != self.settings.value('hostname')):
            self.interface.reconnect()

    def status_msg(self, msg):
        self.statusBar().showMessage(msg,10000) # display only for 10 seconds

    # read panel data from xml-file, set title and geometry
    def read_data_file(self, file_name):
        pd = PanelData()
        (self.panel_w, self.panel_h) = pd.readXML(file_name, False)
        print_statistics()
        self.setWindowTitle('LN Panel     -     ' + Path(file_name).stem)
        scale = self.get_scale()
        self.setGeometry(200, 200, int((self.panel_w + 20) * scale), int((self.panel_h + 20) * scale))

    # select XML file, then read it
    def select_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName(
            self,
            'Select an XML panel file to open…',
            qtc.QDir.homePath(),
            'XML Files (*.xml) ;; All Files (*)'
        )
        if filename:
            print("file: "+filename)
            self.settings.setValue('panel_file',filename)
            self.read_data_file(filename)
        else:
            print("no filename selected")

    def paintEvent(self, e):
        qp = qtg.QPainter(self)
        scale = self.get_scale()
        qp.scale(scale,scale)
        self.draw(qp)

    def get_scale(self):  # avoid runtime errors
        scale_string = self.settings.value('scale')
        if scale_string:   # there is already a scale value
            try:
                scale = float(scale_string)
            except (ValueError, TypeError) as e:
                scale = 1.0
                self.settings.value('scale', 1.0)
        else:  # string is None
            scale = 1.0
            self.settings.value('scale', 1.0)
        if scale < const.MIN_SCALE:
            scale = const.MIN_SCALE
        if scale > const.MAX_SCALE:
            scale = const.MAX_SCALE
        return scale

    def mousePressEvent(self, e):
        if e.button() == qtc.Qt.LeftButton:
            sc = self.get_scale()
            x = e.x()/sc
            y = e.y()/sc
            # print("mouse pressed (left)"+str(x)+"/"+str(y))
            list_active_pes = config.turn + config.signals + config.rtBtns # all active panel elements
            for pe in list_active_pes:
                if pe.touched(x, y):
                    # print("hit adr="+str(pe.adr)+" st="+str(pe.state))
                    if pe.state == const.State.CLOSED:  # toggle state
                        st = const.State.THROWN
                    else:
                        st = const.State.CLOSED
                    if self.settings.value('simulation_on', type=bool):
                        pe.state = st
                        self.update()
                    else:
                        print("changing to: st=" + str(st))
                        lnstring = ln_command.set_accessory(pe.adr,st)
                        if lnstring:
                            self.interface.send_message(lnstring)
                    break
            e.accept()
        # right button not yet implemented

    def draw(self, qp):
        size = self.size()   # size of Main-window !!

        # draw raster
        qp.setPen(qtg.QPen(qtc.Qt.black))
        for x in range(0, size.width(), 20):   # TODO must size_width be scaled with scaling factor ??
            for y in range(0, size.height(), 20):  # TODO size.height??
                qp.drawPoint(x, y)

        addr_flag = self.settings.value('disp_dcc_addresses', type=bool)
        route_flag = True    # self.settings.value('routes_enabled', type=bool)

        # draw Tracks
        for t in config.trks:
            t.draw(qp, addr_flag)

        # draw Sensors
        for t in config.sens:
            t.draw(qp, addr_flag)

        # draw Turnouts (depend on t.state)
        for t in config.turn:
            t.draw(qp, addr_flag)

        # draw signals (depend on t.state)
        for t in config.signals:
            t.draw(qp, addr_flag)

        if route_flag:
            # draw route buttons
            for t in config.rtBtns:
                t.draw(qp, addr_flag)


    def showAboutBox(self):
        print("About: not yet implemented.")

#    def received_message(self, msg):   NOT USED
#        print("rec: "+msg)

    def rec_accessory_state_change(self, adr, st):
        if config.turn:   # this callback function can be called before a panel is read
            for t in config.turn:
                if t.adr == adr:
                    t.state = st
                    self.update()

    def rec_sensor_state_change(self, adr, st):
        if config.sens:    # this callback function can be called before a panel is read
            for s in config.sens:
                if s.adr == adr:
                    s.state = st
                    self.update()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
