from installer_app.installers.pip_installer import PipInstaller
from installer_app.installers.brew_installer import BrewInstaller
from installer_app.core.installer import Installer
from installer_app.core.config import load_config
from typing import Optional


class InstallerFactory:
    installers = {"pip": PipInstaller, "brew": BrewInstaller}

    @staticmethod
    def create_installer(
        installer_type: str, package_name: str, version: Optional[str] = "latest"
    ) -> Installer:
        installer_class = InstallerFactory.installers.get(installer_type)
        if not installer_class:
            raise ValueError(f"Unknown installer type: {installer_type}")

        config = load_config()
        installer_config = config.get(installer_type, {})

        return installer_class(package_name, installer_config, version)
