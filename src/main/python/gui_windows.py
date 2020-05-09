import _thread
import time

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import code_helper as helper


class App(QtWidgets.QMainWindow):

    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx

        self.setWindowIcon(QtGui.QIcon(ctx.icon()))
        self.setMinimumSize(QtCore.QSize(500, 180))
        self.setMaximumSize(QtCore.QSize(500, 180))

        self.title = 'MiniMenu for PiHole'
        self.initUI()

    # Init Ui
    def initUI(self):
        self.setWindowTitle(self.title)

        self.ip, self.key = helper.readKey(self.ctx.get_resource("key/key"))

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

        _thread.start_new_thread(self.updateBackground, ("http://" + self.ip + "/admin/api.php",))

    # Update in backgroud status bar info
    def updateBackground(self, url):
        while True:
            self.risp(url)
            time.sleep(5)

    # Functions for Disactive button
    def dis(self):
        self.saveNewData()

        url = "http://" + self.ip + "/admin/api.php?disable=" + self.textbox2.text() + "&auth=" + self.key
        self.risp(url)

    # Functions for Active button
    def att(self):
        self.saveNewData()

        url = "http://" + self.ip + "/admin/api.php?enable&auth=" + self.key
        self.risp(url)

    # Send comand to PiHole server and update interface
    def risp(self, url):
        risp = helper.ricercaInfo(url)

        if risp == True:
            self.statusBar().showMessage("Status: Active")

        elif risp == False:
            self.statusBar().showMessage("Status: Disactive")

        elif risp == None:
            self.statusBar().showMessage("Status: Server not found")

        self.sysTray.setUpdate()

    # Update saved info
    def saveNewData(self):
        ip = self.textbox.text()
        key = self.textbox1.text()

        if ip != self.ip or key != self.key:
            helper.saveKey(ip, key, self.ctx.get_resource("key/key"))

        self.ip = ip
        self.key = key

    # Set reference to sysTray
    def setSysTray(self, sysTray):
        self.sysTray = sysTray

    # Prevent program exit when clik on X button
    def closeEvent(self, event):
        self.hide()
        event.ignore()
