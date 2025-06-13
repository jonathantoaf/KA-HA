from installer_app.core.insatller import Installer

class BrewInstaller(Installer):
    def install(self):
        print("Installing package using brew...")

    def uninstall(self):
        print("Uninstalling package using brew...")

    def status(self):
        print("Checking status of package using brew...")