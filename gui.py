from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import course_catalog as cc


def settermyear():
    pass


if __name__ == "__main__":
    gui = QApplication([])
    gui.setStyle('Fusion')
    window = QMainWindow()

    window.setFixedSize(QSize(640, 480))
    window.setWindowTitle("Combobox example")

    termyearcombobox = QWidget()
    combobox = QComboBox(termyearcombobox)
    combobox.setGeometry(QRect(30, 430, 110, 25))
    for term in list(cc.gettermyears().keys()):
        combobox.addItem(term)

    window.setCentralWidget(termyearcombobox)

    window.show()
    gui.exec_()
