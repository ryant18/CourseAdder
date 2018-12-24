from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import course_catalog as cc
import app


# Main widget that is displayed in the window
class MainDisplayWindow(QMainWindow):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setWindowTitle("Combobox example")
        self.setMinimumSize(QSize(831, 480))
        self.termyears = cc.gettermyears()

        self.termyearcombobox = QComboBox()
        self.checkingtoggle = QPushButton("Start Check")
        self.delaylineedit = QLineEdit()
        self.crntable = QTableWidget(3, 8)

        self.termdelaybottomleft = QVBoxLayout()
        self.bottomrow = QHBoxLayout()
        self.mainlayout = QVBoxLayout()

        self.setupbuttons()
        self.setuplayout()
        self.linkbuttons()
        self.changetermyear(self.termyearcombobox.currentText())

        mainwidget = QWidget()
        mainwidget.setLayout(self.mainlayout)
        self.setCentralWidget(mainwidget)

        self.app = app.App()

    def setupbuttons(self):
        # Selector for registration year
        self.termyearcombobox.setGeometry(QRect(30, 430, 110, 25))
        self.termyearcombobox.addItems(self.termyears.keys())
        # Button for starting course checking
        self.checkingtoggle.setCheckable(True)

        # Delay set box
        self.delaylineedit.setText('30')
        self.delaylineedit.setValidator(QIntValidator(0, 3600, self))

        # Table for holding and displaying crns
        self.crntable.setColumnCount(8)
        self.crntable.setHorizontalHeaderLabels(['Crn', 'Course Number', 'Name', 'Instructor',
                                                 'Days', 'Begin', 'End', 'Location'])
        for i in range(10):
            for j in range(10):
                item = QTableWidgetItem(str(i * j))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.crntable.setItem(i, j, item)

    def setuplayout(self):
        self.termdelaybottomleft.addWidget(self.termyearcombobox)
        self.termdelaybottomleft.addWidget(self.delaylineedit)

        self.bottomrow.addLayout(self.termdelaybottomleft)
        self.bottomrow.addStretch(1)
        self.bottomrow.addWidget(self.checkingtoggle)
        self.bottomrow.addStretch(1)

        self.mainlayout.addWidget(self.crntable)
        self.mainlayout.addLayout(self.bottomrow)

    def changecheckdelay(self, delay):
        if delay != '':
            self.app.setdelaytime(int(delay))

    def changetermyear(self, semester):
        print(self.termyears[semester])

    def togglecrncheck(self, val):
        self.termyearcombobox.setDisabled(val)
        self.delaylineedit.setDisabled(val)
        if val:
            pass
        else:
            pass

    def linkbuttons(self):
        self.termyearcombobox.activated[str].connect(self.changetermyear)
        self.checkingtoggle.toggled.connect(self.togglecrncheck)
        self.delaylineedit.textChanged.connect(self.changecheckdelay)


if __name__ == "__main__":
    gui = QApplication([])
    gui.setStyle('Fusion')
    window = MainDisplayWindow()
    window.show()
    gui.exec_()

'''
add delete buttom from table
add ability to input crn
link up to backend
'''
