from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget, QPushButton,
)


class AboutBox(QWidget):
    """
    The AboutBox is a QWidget. It has no parent and
    will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        # TODO: make a nice HTML text window.
        self.setWindowTitle('About LoconetPanel')
        self.label = QLabel(
            '<p>With LoconetPanel you have graphical control over a model railroads</p>'
            '<p>turnouts and signals - all of them defined in an xml file.</p>'
            '<p>for creating the xml file see:</p>'
            '<p><a href="https://michael71.github.io/SX4Draw/">https://michael71.github.io/SX4Draw/</a></p>'
        )
        self.label.setOpenExternalLinks(True)
        layout.addWidget(self.label)
        button = QPushButton('OK', self)

        button.clicked.connect(self.close_about)
        layout.addWidget(button)
        self.setLayout(layout)

    def close_about(self):
        self.close()
