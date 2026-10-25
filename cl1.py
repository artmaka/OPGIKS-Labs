from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class CelsiusConverter(QObject):
    fahrenheit_changed = pyqtSignal(float)
    kelvin_changed = pyqtSignal(float)

    @pyqtSlot(float)
    def convert(self, celsius):
        fahrenheit = celsius * 9 / 5 + 32
        kelvin = celsius + 273.15

        self.fahrenheit_changed.emit(fahrenheit)
        self.kelvin_changed.emit(kelvin)
