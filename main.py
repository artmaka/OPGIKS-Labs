import sys
import os

from PyQt5 import QtWidgets, QtGui, QtCore


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Labs №1")
        self.resize(600, 400)

        self.label = QtWidgets.QLabel("Press the button for image")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setMinimumSize(450, 250)

        self.label.setStyleSheet("""
            QLabel {
                border: 2px solid black;
                font-size: 18px;
            }
        """)

        self.button1 = QtWidgets.QPushButton("Default")
        self.button2 = QtWidgets.QPushButton("From PC")

        self.button1.clicked.connect(self.show_default_image)
        self.button2.clicked.connect(self.open_image)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.button1)
        buttons_layout.addWidget(self.button2)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def show_image(self, filename):

        pixmap = QtGui.QPixmap(filename)

        if pixmap.isNull():
            self.label.setText("Can't upload a image")
            return

        pixmap = pixmap.scaled(
            self.label.size(),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        )

        self.label.setText("")
        self.label.setPixmap(pixmap)

    def show_default_image(self):

        filename = "image.png"

        if os.path.exists(filename):
            self.show_image(filename)
        else:
            self.label.setText(
                "File image.png not found"
            )

    def open_image(self):

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Choose a image",
            "",
            "Image (*.png *.jpg *.jpeg *.bmp)"
        )

        if filename:
            self.show_image(filename)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())