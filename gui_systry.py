import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import sys

import gui_windows
import code_helper as helper

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtWidgets.QMenu(parent)    
        self.icon = icon
        self.updateKey()
        self.url = "http://" + self.ip + "/admin/api.php"
        self.setMenu()
        self.setPause()

#Init sysTray

    def setMenu(self):
        self.menu.clear()

        self.pause = self.menu.addAction("Disactive")
        self.pause.triggered.connect(self.setPause)
        
        self.windows = self.menu.addAction("Windows")
        self.windows.triggered.connect(self.openWindows)

        self.update = self.menu.addAction("Update")
        self.update.triggered.connect(self.setUpdate)

        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)
        
        self.setContextMenu(self.menu)

#Set functions of all menu elements, from here:

    def setPause(self):
        self.updateInterface(self.url)

    def openWindows(self):
        self.window = gui_windows.App()
    
    def setUpdate(self):
        self.updateInterface("http://" + self.ip + "/admin/api.php")
    
    def exit(self):
        sys.exit()

#To here

#Read saved key

    def updateKey(self):
        self.ip, self.key = helper.readKey()

#Send comand to PiHole server and update interface

    def updateInterface(self, url):
        self.updateKey()

        risp = helper.ricercaInfo(url)
        if risp == True:
            self.url = "http://" + self.ip + "/admin/api.php?disable=&auth=" + self.key
            self.pause.setText("Active")
        elif risp == False:
            self.url = "http://" + self.ip + "/admin/api.php?enable=&auth=" + self.key
            self.pause.setText("Disactive")

def main(image):
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.show()
    sys.exit(app.exec_())
