import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import sys
import _thread

import gui_windows
import code_helper as helper

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtWidgets.QMenu(parent)   
        self.activated.connect(self.iconActivated) 
        self.icon = icon
        self.updateKey()
        self.url = "http://" + self.ip + "/admin/api.php"
        self.setMenu()
        self.setPause()

#Init sysTray
    def setMenu(self):
        self.menu.clear()

        self.status = self.menu.addAction("Status: Disactive")
        self.status.setEnabled(False)

        self.menu.addSeparator()
        
        self.switch = self.menu.addAction("Switch status")
        self.switch.triggered.connect(self.setPause)

        self.update = self.menu.addAction("Update status")
        self.update.triggered.connect(self.setUpdate)
        
        self.windows = self.menu.addAction("Windows")
        self.windows.triggered.connect(self.openWindows)

        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)
        
        self.setContextMenu(self.menu)


#Set functions of all menu elements, from here:
    def setPause(self):
        self.updateInterface(self.url)
    
    def setUpdate(self):
        self.updateInterface("http://" + self.ip + "/admin/api.php")

    def openWindows(self):
        self.window = gui_windows.App()
        self.window.setSysTray(self)
        self.window.show()
    
    def exit(self):
        sys.exit()
#To here

#Override Right click fun
    def iconActivated(self, reason):
        if reason == 1:
            super()
            _thread.start_new_thread(self.setUpdate, ())

#View server status
    def setPersonalStatus(self, message):
        self.setToolTip(message)
        self.status.setText(message)

#Read saved key
    def updateKey(self):
        self.ip, self.key = helper.readKey()

#Send comand to PiHole server and update interface
    def updateInterface(self, url):
        self.updateKey()

        risp = helper.ricercaInfo(url)
        if risp == True:
            self.url = "http://" + self.ip + "/admin/api.php?disable=&auth=" + self.key
            self.setPersonalStatus("Status: Active")
        elif risp == False:
            self.url = "http://" + self.ip + "/admin/api.php?enable=&auth=" + self.key
            self.setPersonalStatus("Status: Disactive")
        elif risp == None:
            self.setPersonalStatus("Status: Server not found")

#Start gui_sysTray
def main(image):
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.show()
    sys.exit(app.exec_())
