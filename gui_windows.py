import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import _thread
import sys
import time

import code_helper as helper

class App(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setMinimumSize(QtCore.QSize(500, 180))
        self.setMaximumSize(QtCore.QSize(500, 180))

        self.title = 'MiniMenu for PiHole'
        self.tryPause = None
        
    def setTryPause(self, pause):
        self.tryPause = pause
        
    def initUI(self):
        self.setWindowTitle(self.title)

        try:
            self.data = helper.aprifile("data.txt")
        except Exception:
            self.data = ["pi.hole", ""]

        self.ip = self.data[0]
        self.key = self.data[1]

        # Create textbox
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(110, 10)
        self.textbox.resize(380, 30)
        self.textbox.setText(self.ip)

        # Create textbox
        self.textbox1 = QtWidgets.QLineEdit(self)
        self.textbox1.move(110, 50)
        self.textbox1.resize(380, 30)
        self.textbox1.setToolTip("Get it with: sudo cat /etc/pihole/setupVars.conf | grep PASSWORD")
        self.textbox1.setText(self.key)

        # Create textbox
        self.textbox2 = QtWidgets.QLineEdit(self)
        self.textbox2.move(110, 90)
        self.textbox2.resize(380, 30)
        self.textbox2.setToolTip("Indicate in second. Write 0 or leave it blank to permanently disable it")
        self.textbox2.setText("0")

        self.text = QtWidgets.QLabel('Pihole IP:', self)
        self.text.move(10, 10)
        self.text.resize(75, 30)

        self.text1 = QtWidgets.QLabel('Web password:', self)
        self.text1.move(10, 50)
        self.text1.resize(75, 30)
        self.text1.setToolTip("Get it with: sudo cat /etc/pihole/setupVars.conf | grep PASSWORD")

        self.text2 = QtWidgets.QLabel('ReEnable in:', self)
        self.text2.move(10, 90)
        self.text2.resize(75, 30)
        self.text2.setToolTip("Indicate in second. Write 0 or leave it blank to permanently disable it")

        # Create a button in the window
        self.button = QtWidgets.QPushButton('Disable', self)
        self.button.move(440, 125)
        self.button.resize(50, 30)
        self.button.setToolTip('Click to disable PiHole\nShortcut: Ctrl + d')
        self.button.clicked.connect(self.dis)
        self.button.setShortcut("Ctrl+d")

        self.button1 = QtWidgets.QPushButton('Enable', self)
        self.button1.move(10, 125)
        self.button1.resize(50, 30)
        self.button1.setToolTip('Click to enable PiHole\nShortcut: Ctrl + e')
        self.button1.clicked.connect(self.att)
        self.button1.setShortcut("Ctrl+e")

        self.statusBar().showMessage('Status: Searcing info')

        self.show()

        _thread.start_new_thread(self.updateBackground, ("http://" + self.ip + "/admin/api.php", ))

    def updateBackground(self, url):
        while True:
            self.risp(url)
            time.sleep(5)

    def dis(self):
        self.ip = self.textbox.text()
        self.key = self.textbox1.text()

        helper.scrivifile(self.ip + "\n" + self.key, "data.txt")

        temp = self.textbox2.text()

        url = "http://" + self.ip + "/admin/api.php?disable=" + temp + "&auth=" + self.key
        self.risp(url)

    def att(self):
        self.ip = self.textbox.text()
        self.key = self.textbox1.text()

        helper.scrivifile(self.ip + "\n" + self.key, "data.txt")

        url = "http://" + self.ip + "/admin/api.php?enable&auth=" + self.key
        self.risp(url)

    def risp(self, url):
        risp = helper.ricercainfo(url)

        if risp == True:
            self.statusBar().showMessage("Status: Active")
            if(self.tryPause != None):
                self.tryPause

        elif risp == False:
            self.statusBar().showMessage("Status: Disactive")
            if(self.tryPause != None):
                self.tryPause

    def closeEvent(self, event):
        self.hide()
        event.ignore()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())