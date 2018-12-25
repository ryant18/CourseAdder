from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import course_catalog as cc
import app as backend


# Main widget that is displayed in the window
class MainDisplayWindow(QMainWindow):
    def __init__(self):
        super(QWidget, self).__init__()
        self.app = backend.App()
        self.setWindowTitle("Course Adder")
        self.setMinimumSize(QSize(640, 480))
        self.termyears = cc.gettermyears()

        self.termyearcombobox = QComboBox()
        self.checkingtoggle = QPushButton("Start Check")
        self.delaylineedit = QLineEdit()
        self.crntable = QTableWidget()
        self.crntableinput = QLineEdit()

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
        self.settablefirstrow()

    def settablefirstrow(self):
        self.crntable.insertRow(0)
        self.crntableinput.setValidator(QIntValidator(0, 99999, self))
        self.crntable.setCellWidget(0, 0, self.crntableinput)
        for i in range(1, self.crntable.columnCount()):
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.crntable.setItem(0, i, item)

    def deletetablerows(self):
        while self.crntable.rowCount() > 1:
            self.crntable.removeRow(0)
        self.crntableinput.setText('')

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
        if self.app.settermyear(self.termyears[semester]):
            self.deletetablerows()

    def togglecrncheck(self, val):
        self.termyearcombobox.setDisabled(val)
        self.delaylineedit.setDisabled(val)
        self.crntable.setDisabled(val)
        if val:
            self.app.startcheck()
        else:
            self.app.endcheck()

    def crninputfromtable(self):
        newrowindex = self.crntable.rowCount()-1
        self.crntable.insertRow(newrowindex)
        crncourse = self.app.addcrn(int(self.crntableinput.text()))
        if crncourse is not None:
            self.inputcourseinfo(newrowindex, crncourse)
        else:
            deletebutton = QPushButton(self.crntableinput.text())
            deletebutton.setToolTip("Delete Course")
            erroritem = QTableWidgetItem("Not a valid crn")
            erroritem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            deletebutton.setStyleSheet('QPushButton { color: red }')
            erroritem.setForeground(QBrush(QColor(255, 0, 0)))
            self.crntable.setCellWidget(newrowindex, 0, deletebutton)
            deletebutton.clicked.connect(self.deleterow)
            self.crntable.setItem(newrowindex, 1, erroritem)
            for i in range(2, self.crntable.columnCount()):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.crntable.setItem(newrowindex, i, item)

        self.crntableinput.setText('')

    def inputcourseinfo(self, row, course):
        courseattributes = [course.crn, course.coursenumber, course.name, course.instructor,
                            course.days, course.starttime, course.endtime, course.location]
        deletebutton = QPushButton(courseattributes[0])
        deletebutton.setToolTip("Delete Course")
        deletebutton.clicked.connect(self.deleterow)
        self.crntable.setCellWidget(row, 0, deletebutton)
        for i in range(1, self.crntable.columnCount()):
            item = QTableWidgetItem(courseattributes[i])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.crntable.setItem(row, i, item)

    def deleterow(self):
        self.app.removecrn(int(self.sender().text()))
        row = self.crntable.indexAt(self.sender().pos()).row()
        self.crntable.removeRow(row)
        self.crntableinput.setFocus()

    def linkbuttons(self):
        self.termyearcombobox.activated[str].connect(self.changetermyear)
        self.checkingtoggle.toggled.connect(self.togglecrncheck)
        self.delaylineedit.textChanged.connect(self.changecheckdelay)
        self.crntableinput.editingFinished.connect(self.crninputfromtable)


if __name__ == "__main__":
    gui = QApplication([])
    gui.setStyle('Fusion')
    window = MainDisplayWindow()
    window.show()
    gui.exec_()
