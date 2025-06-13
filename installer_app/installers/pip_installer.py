from installer_app.core.insatller import Installer

class PipInstaller(Installer):
    def install(self):
        print("Installing package using pip...")

    def uninstall(self):
        print("Uninstalling package using pip...")

    def status(self):
        print("Checking status of package using pip...")
