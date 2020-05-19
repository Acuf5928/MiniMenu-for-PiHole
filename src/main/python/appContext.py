from fbs_runtime.application_context.PyQt5 import ApplicationContext
import os


class AppContext(ApplicationContext):
    def run(self):
        return self.app.exec_()

    def icon(self):
        return self.get_resource("images/icon.png")

    def appName(self):
        return "MiniMenu"

    def keyPath(self):
        return os.getenv('USERPROFILE') + "/." + self.appName()
