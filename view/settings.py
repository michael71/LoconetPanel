from PyQt6 import QtWidgets as qtw
from PyQt6 import QtGui as qtg
from PyQt6 import QtCore as qtc

from model import constants
from model.routebutton import reset_rtbtns


class SettingsDialog(qtw.QDialog):
    """Dialog for selecting and storing settings values"""

    def __init__(self, settings, parent=None):
        super().__init__(parent, modal=False)
        form = qtw.QFormLayout()
        form.setContentsMargins(20,20,20,20)
        form.setVerticalSpacing(20)
        self.setLayout(form)
        self.setWindowTitle('Settings')
        self.settings = settings
        self.layout().addRow(
            qtw.QLabel('<h4>LbServer Settings</h4>'),
        )

        self.hostname_text = qtw.QLineEdit()
        hn = self.settings.value("hostname")
        if hn:
            self.hostname_text.setText(hn)
        else:
            self.hostname_text.setText('localhost')
        self.layout().addRow("Hostname",self.hostname_text)

        self.port_text = qtw.QLineEdit()
        self.onlyInt = qtg.QIntValidator(1000,65535)
        self.port_text.setValidator(self.onlyInt)
        p = self.settings.value("port")
        if p:
            self.port_text.setText(p)
        else:
            self.port_text.setText("1234")
        self.layout().addRow("Port", self.port_text)

        self.simulation_cb = qtw.QCheckBox(
            checked = settings.value('simulation_on', type=bool)
        )
        self.layout().addRow("Only simulation", self.simulation_cb)

        self.routing_cb = qtw.QCheckBox(checked = settings.value('routing_enabled', type=bool))
        self.layout().addRow("Enable routing", self.routing_cb)

        self.layout().addRow(" ", None)
        self.layout().addRow(qtw.QLabel('<H4>Panel Settings</H4>'))

        self.disp_addr_cb = qtw.QCheckBox(checked = settings.value('disp_dcc_addresses', type=bool))
        self.layout().addRow("Display DCC Addresses", self.disp_addr_cb)

        self.disp_loco_msg_cb = qtw.QCheckBox(checked = settings.value('disp_loco_messages', type=bool))
        self.layout().addRow("Display Loco Messages", self.disp_loco_msg_cb)

        self.disp_sensor_msg_cb = qtw.QCheckBox(checked = settings.value('disp_sensor_messages', type=bool))
        self.layout().addRow("Display Sensor Messages", self.disp_sensor_msg_cb)

        self.scale_text = qtw.QLineEdit()
        self.onlyDouble = qtg.QDoubleValidator(constants.MIN_SCALE,constants.MAX_SCALE,2)
        self.scale_text.setValidator(self.onlyDouble)
        p = self.settings.value("scale")
        if p:
            self.scale_text.setText(str(p))
        else:
            self.scale_text.setText("1.0")
        sc_text = f"Scale ({constants.MIN_SCALE}..{constants.MAX_SCALE})"
        self.layout().addRow(sc_text, self.scale_text)
        self.layout().addRow(" ", None)

        self.accept_btn = qtw.QPushButton('Ok', clicked=self.accept)
        self.cancel_btn = qtw.QPushButton('Cancel', clicked=self.reject)
        self.layout().addRow(self.accept_btn, self.cancel_btn)

    # prevents window closing when hitting ENTER in QLineEdit box
    def keyPressEvent(self, event):
        if event.key() == qtc.Qt.Key_Enter:
            print("enter key pressed.")
        event.accept()

    def accept(self):
        self.settings.setValue('hostname', self.hostname_text.text())
        self.settings.setValue('port',self.port_text.text())
        self.settings.setValue(
            'simulation_on',
            self.simulation_cb.isChecked()
        )
        self.settings.setValue(
            'disp_dcc_addresses',
            self.disp_addr_cb.isChecked()
        )
        self.settings.setValue(
            'routing_enabled',
            self.routing_cb.isChecked()
        )
        if not self.settings.value('routing_enabled'):
            reset_rtbtns()

        self.settings.setValue(
            'disp_loco_messages',
            self.disp_loco_msg_cb.isChecked()
        )

        self.settings.setValue(
            'disp_sensor_messages',
            self.disp_sensor_msg_cb.isChecked()
        )

        # debug output
        print("hostname=" + self.settings.value('hostname'))
        print("port=" + self.settings.value('port'))
        print("simulation:" + str(self.settings.value('simulation_on')))
        print("routing:" + str(self.settings.value('routing_enabled')))
        print("ddc-addr:" + str(self.settings.value('disp_dcc_addresses')))
        print("loco-msg:" + str(self.settings.value('disp_loco_messages')))
        print("sensor-msg:" + str(self.settings.value('disp_sensor_messages')))

        scale_value = float(self.scale_text.text())
        if scale_value < constants.MIN_SCALE:
            scale_value = constants.MIN_SCALE
        if scale_value > constants.MAX_SCALE:
            scale_value = constants.MAX_SCALE
        self.settings.setValue('scale', scale_value)
        print("scale=" + str(self.settings.value('scale')))

        super().accept()
