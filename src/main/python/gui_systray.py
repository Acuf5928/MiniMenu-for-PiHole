import _thread
import sys

import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import gui_windows, code_helper as helper
from appContext import AppContext


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, ctx):
        super(SystemTrayIcon, self).__init__()
        self.ctx = ctx
        self.menu = QtWidgets.QMenu()
        self.activated.connect(self.iconActivated)
        self.setIcon(QtGui.QIcon(ctx.icon()))
        self.updateKey()
        self.url = "http://" + self.ip + "/admin/api.php"
        self.setMenu()
        self.setPause()

    # Init sysTray
    def setMenu(self):
        self.menu.clear()

        self.status = self.menu.addAction("Status: Disactive")
        self.status.setEnabled(False)

        self.menu.addSeparator()

        self.switch = self.menu.addAction("Switch status")
        self.switch.triggered.connect(self.setPause)

        self.windows = self.menu.addAction("Windows")
        self.windows.triggered.connect(self.openWindows)

        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)

        self.setContextMenu(self.menu)

    # Set functions of all menu elements, from here:
    def setPause(self):
        self.updateInterface(self.url)

    def setUpdate(self):
        self.updateInterface("http://" + self.ip + "/admin/api.php")

    def openWindows(self):
        self.window = gui_windows.App(self.ctx)
        self.window.setSysTray(self)
        self.window.show()

    def exit(self):
        sys.exit()

    # To here

    # Override click on systray icon fun
    def iconActivated(self, reason):
        if reason == 1:
            super()
            _thread.start_new_thread(self.setUpdate, ())

    # View server status
    def setPersonalStatus(self, message):
        self.setToolTip(message)
        self.status.setText(message)

    # Read saved key
    def updateKey(self):
        self.ip, self.key = helper.readKey(self.ctx.get_resource("key/key"))

    # Send comand to PiHole server and update interface
    def updateInterface(self, url):
        self.updateKey()

        risp = helper.ricercaInfo(url)
        if risp:
            self.url = "http://" + self.ip + "/admin/api.php?disable=&auth=" + self.key
            self.setPersonalStatus("Status: Active")
        elif not risp:
            self.url = "http://" + self.ip + "/admin/api.php?enable=&auth=" + self.key
            self.setPersonalStatus("Status: Disactive")
        elif risp is None:
            self.setPersonalStatus("Status: Server not found")


# Start gui_sysTray
def main():
    appctxt = AppContext()
    trayIcon = SystemTrayIcon(appctxt)
    trayIcon.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
