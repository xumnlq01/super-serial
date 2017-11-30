"""
Copyright Justin Watson 2017

References
* http://pyqt.sourceforge.net/Docs/PyQt5/modules.html#ref-module-index

"""

import argparse
import ctypes
import os.path as osp
import sys

from PyQt5 import QtCore, QtWidgets, QtSerialPort, QtGui
from PyQt5.Qt import QDesktopServices, QUrl

# http://pyqt.sourceforge.net/Docs/PyQt5/gotchas.html#crashes-on-exit
app = None
app_icon = None

_super_serial_version = 'v0.1.0'

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Super Serial")

        script_dir = osp.dirname(osp.realpath(__file__))
        app_icon = QtGui.QIcon(script_dir + osp.sep + 'super_serial_64x64.ico')

        self.setWindowIcon(app_icon)

        #self.setGeometry(200, 200, 800, 480)
        self.resize(800, 480)

        self.super_serial_menu = QtWidgets.QMenu('&Super Serial', self)
        self.menuBar().addMenu(self.super_serial_menu)

        self.super_serial_menu.addAction('&Connect to Device', self.connect,
            QtCore.Qt.CTRL + QtCore.Qt.Key_P)

        # The function addAction returns a QAction object.
        discconect_action = self.super_serial_menu.addAction('&Disconnect', self.disconnect,
            QtCore.Qt.CTRL + QtCore.Qt.Key_D)
        discconect_action.setEnabled(False)

        self.super_serial_menu.addAction('&Set Title', self.setTitle)

        self.super_serial_menu.addAction('&Exit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.super_serial_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&Documentation', self.documentation,
            QtCore.Qt.Key_F1)
        self.help_menu.addAction('&Super Serial Webpage', self.webpage)
        self.help_menu.addAction('&About Super Serial', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Nothing here yet.", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, 'Super Serial',
            'Super Serial\r\nVersion: {}'.format(_super_serial_version))

    def webpage(self):
        url = QUrl('http://superserial.io')
        QDesktopServices.openUrl(url)

    def documentation(self):
        url = QUrl('http://docs.superserial.io/en/latest/')
        QDesktopServices.openUrl(url)

    def connect(self):
        dialog = SerialConfigDialog()
        dialog.setModal(True)
        dialog.show()
        dialog.exec_()

    def disconnect(self):
        pass

    def setTitle(self):
        dialog = SetTitleDialog()
        dialog.setModal(True)
        dialog.show()
        dialog.exec_()

        new_title = dialog.getTitle()
        if new_title != '':
            self.setWindowTitle(new_title)


class SetTitleDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SetTitleDialog, self).__init__(parent)

        self.setWindowTitle("Set Window Title")

        self._title = ''

        self.titleLineEdit = QtWidgets.QLineEdit()
        self.setTitleButton = QtWidgets.QPushButton("Set Title")
        self.cancelButton = QtWidgets.QPushButton("Cancel")

        self.setTitleButton.clicked.connect(self.setTitle)
        self.cancelButton.clicked.connect(self.cancel)

        # http://www.bogotobogo.com/Qt/Qt5_GridLayout.php
        layout = QtWidgets.QGridLayout()
        #layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(0, 200)
        layout.setColumnMinimumWidth(1, 100)

        # row, column, rowspan, colspan
        layout.addWidget(self.titleLineEdit, 0, 0, 1, 2)
        layout.addWidget(self.setTitleButton, 1, 0, 1, 1)
        layout.addWidget(self.cancelButton, 1, 1, 1, 1)

        self.setLayout(layout)

    def cancel(self):
        self._title = ''
        self.close()

    def setTitle(self):
        self._title = self.titleLineEdit.text()
        self.close()

    def getTitle(self):
        return self._title


class SerialConfigDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SerialConfigDialog, self).__init__(parent)

        self.setWindowTitle('Set Window Title')
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.MSWindowsFixedSizeDialogHint)

        self.portLabel = QtWidgets.QLabel('Serial Port')

        self.portComboBox = QtWidgets.QComboBox()
        self.portComboBox.addItem("COM4")
        self.portComboBox.addItem("COM5")
        self.portComboBox.addItem("COM6")

        self.scanComsButton = QtWidgets.QPushButton('Scan COMs')

        self.baudrateLabel = QtWidgets.QLabel('Baudrate')

        self.baudrateEdit = QtWidgets.QLineEdit()

        self.databitsLabel = QtWidgets.QLabel('Databits')

        self.databitsComboBox = QtWidgets.QComboBox()
        self.databitsComboBox.addItem('5')
        self.databitsComboBox.addItem('6')
        self.databitsComboBox.addItem('7')
        self.databitsComboBox.addItem('8')

        self.stopbitsLabel = QtWidgets.QLabel('Stopbits')

        self.stopbitsComboBox = QtWidgets.QComboBox()
        self.stopbitsComboBox.addItem('1')
        self.stopbitsComboBox.addItem('1.5')
        self.stopbitsComboBox.addItem('2')

        self.parityLabel = QtWidgets.QLabel('Parity')

        self.parityComboBox = QtWidgets.QComboBox()
        self.parityComboBox.addItem('NONE')
        self.parityComboBox.addItem('ODD')
        self.parityComboBox.addItem('EVEN')
        self.parityComboBox.addItem('SPACE')
        self.parityComboBox.addItem('MARK')

        self.flowControlLabel = QtWidgets.QLabel('Flow Control')

        self.flowControlComboBox = QtWidgets.QComboBox()
        self.flowControlComboBox.addItem('NONE')
        self.flowControlComboBox.addItem('XON/XOFF')
        self.flowControlComboBox.addItem('RTS/CTS')
        self.flowControlComboBox.addItem('DSR/DTR')

        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.connectButton = QtWidgets.QPushButton('Connect')
        self.saveButton = QtWidgets.QPushButton('Save')
        self.loadButton = QtWidgets.QPushButton('Load')

        self.cancelButton.clicked.connect(self.cancel)

        # http://www.bogotobogo.com/Qt/Qt5_GridLayout.php
        layout = QtWidgets.QGridLayout()
        #layout.setColumnStretch(1, 1)
        # layout.setColumnMinimumWidth(0, 200)
        # layout.setColumnMinimumWidth(1, 100)

        # row, column, rowspan, colspan
        layout.addWidget(self.portLabel, 0, 0, 1, 2)
        layout.addWidget(self.portComboBox, 0, 2, 1, 1)
        layout.addWidget(self.scanComsButton, 0, 3, 1, 1)

        layout.addWidget(self.baudrateLabel, 1, 0, 1, 2)
        layout.addWidget(self.baudrateEdit, 1, 2, 1, 2)

        layout.addWidget(self.databitsLabel, 2, 0, 1, 2)
        layout.addWidget(self.databitsComboBox, 2, 2, 1, 2)

        layout.addWidget(self.stopbitsLabel, 3, 0, 1, 2)
        layout.addWidget(self.stopbitsComboBox, 3, 2, 1, 2)

        layout.addWidget(self.parityLabel, 4, 0, 1, 2)
        layout.addWidget(self.parityComboBox, 4, 2, 1, 2)

        layout.addWidget(self.flowControlLabel, 5, 0, 1, 2)
        layout.addWidget(self.flowControlComboBox, 5, 2, 1, 2)

        layout.addWidget(self.cancelButton, 6, 0, 1, 1)
        layout.addWidget(self.connectButton, 6, 1, 1, 1)
        layout.addWidget(self.saveButton, 6, 2, 1, 1)
        layout.addWidget(self.loadButton, 6, 3, 1, 1)

        self.setLayout(layout)

    def cancel(self):
        self.close()


def main():
    global app

    app = QtWidgets.QApplication(sys.argv)

    script_dir = osp.dirname(osp.realpath(__file__))
    app_icon = QtGui.QIcon(script_dir + osp.sep + 'super_serial_64x64.ico')
    app.setWindowIcon(app_icon)

    aw = ApplicationWindow()
    aw.show()

    app.exec()


if __name__ == '__main__':
    main()