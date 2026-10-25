from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class OtherScalesConverter(QObject):
    celsius_changed = pyqtSignal(float)
    fahrenheit_changed = pyqtSignal(float)
    kelvin_changed = pyqtSignal(float)

    @pyqtSlot(float)
    def from_fahrenheit(self, fahrenheit):
        celsius = (fahrenheit - 32) * 5 / 9
        kelvin = celsius + 273.15

        self.celsius_changed.emit(celsius)
        self.kelvin_changed.emit(kelvin)

    @pyqtSlot(float)
    def from_kelvin(self, kelvin):
        celsius = kelvin - 273.15
        fahrenheit = celsius * 9 / 5 + 32

        self.celsius_changed.emit(celsius)
        self.fahrenheit_changed.emit(fahrenheit)
