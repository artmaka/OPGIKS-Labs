import sys

from PyQt5 import QtCore, QtWidgets

import cl1
import cl2


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Labs №2 — Signals and Slots")
        self.resize(520, 250)

        self.celsius_converter = cl1.CelsiusConverter()
        self.other_converter = cl2.OtherScalesConverter()

        self.updating = False

        title = QtWidgets.QLabel("Temperature converter")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        description = QtWidgets.QLabel(
            "Change any value — the other fields will update automatically."
        )
        description.setAlignment(QtCore.Qt.AlignCenter)

        self.celsius_input = self.create_spinbox(-273.15, 10000.0, 0.0, " °C")
        self.fahrenheit_input = self.create_spinbox(-459.67, 18032.0, 32.0, " °F")
        self.kelvin_input = self.create_spinbox(0.0, 10273.15, 273.15, " K")

        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(12)
        form_layout.addRow("Celsius:", self.celsius_input)
        form_layout.addRow("Fahrenheit:", self.fahrenheit_input)
        form_layout.addRow("Kelvin:", self.kelvin_input)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.addWidget(title)
        main_layout.addWidget(description)
        main_layout.addSpacing(10)
        main_layout.addLayout(form_layout)

        self.setLayout(main_layout)

        self.celsius_input.valueChanged.connect(self.on_celsius_changed)
        self.fahrenheit_input.valueChanged.connect(self.on_fahrenheit_changed)
        self.kelvin_input.valueChanged.connect(self.on_kelvin_changed)

        self.celsius_converter.fahrenheit_changed.connect(
            lambda value: self.update_spinbox(self.fahrenheit_input, value)
        )
        self.celsius_converter.kelvin_changed.connect(
            lambda value: self.update_spinbox(self.kelvin_input, value)
        )

        self.other_converter.celsius_changed.connect(
            lambda value: self.update_spinbox(self.celsius_input, value)
        )
        self.other_converter.fahrenheit_changed.connect(
            lambda value: self.update_spinbox(self.fahrenheit_input, value)
        )
        self.other_converter.kelvin_changed.connect(
            lambda value: self.update_spinbox(self.kelvin_input, value)
        )

    def create_spinbox(self, minimum, maximum, value, suffix):
        spinbox = QtWidgets.QDoubleSpinBox()
        spinbox.setRange(minimum, maximum)
        spinbox.setDecimals(2)
        spinbox.setSingleStep(1.0)
        spinbox.setValue(value)
        spinbox.setSuffix(suffix)
        spinbox.setMinimumHeight(32)
        return spinbox

    def update_spinbox(self, spinbox, value):
        self.updating = True
        spinbox.setValue(round(value, 2))
        self.updating = False

    def on_celsius_changed(self, value):
        if not self.updating:
            self.celsius_converter.convert(value)

    def on_fahrenheit_changed(self, value):
        if not self.updating:
            self.other_converter.from_fahrenheit(value)

    def on_kelvin_changed(self, value):
        if not self.updating:
            self.other_converter.from_kelvin(value)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
