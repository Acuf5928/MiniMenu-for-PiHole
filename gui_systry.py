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

    def updateKey(self):
        self.ip, self.key = helper.update_info()

    def setMenu(self):
        self.menu.clear()

        self.pause = self.menu.addAction("Disactive")
        self.pause.triggered.connect(self.setPause)
        
        self.windows = self.menu.addAction("Windows")
        self.windows.triggered.connect(self.openWindows)

        self.update = self.menu.addAction("Update")
        self.update.triggered.connect(self.updateInterface)

        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)
        
        self.setContextMenu(self.menu)

    def openWindows(self):
        self.window = gui_windows.App()
        self.window.setTryPause(self.updateInterface())
        self.window.initUI()
        self.window.show()

    def updateInterface(self):
        self.updateKey()

        risp = helper.ricercainfo("http://" + self.ip + "/admin/api.php")
        if risp == True:
            self.pause.setText("Active")
        elif risp == False:
            self.pause.setText("Disactive")

    def setPause(self):
        risp = helper.ricercainfo(self.url)

        if risp == True:
            self.url = "http://" + self.ip + "/admin/api.php?disable=&auth=" + self.key
            self.pause.setText("Active")

        elif risp == False:
            self.url = "http://" + self.ip + "/admin/api.php?enable=&auth=" + self.key
            self.pause.setText("Disactive")
        
    def exit(self):
        sys.exit()

def main(image):
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main("icon.png")