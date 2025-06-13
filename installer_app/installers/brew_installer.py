from installer_app.core.installer import Installer
from typing import Dict, Any, Optional
from installer_app.core.logger import logger
import subprocess


class BrewInstaller(Installer):
    def __init__(
        self,
        package_name: str,
        config: Dict[str, Any],
        version: Optional[str] = "latest",
    ) -> None:
        super().__init__(package_name, config, version)
        logger.info(
            f"Initializing BrewInstaller for package: {self.package_name}, version: {self.version}"
        )

    def install(self) -> None:
        self._validate_package()
        logger.info(f"Installing {self.package_name} via brew")
        subprocess.run(["brew", "install", self.package_name], check=True)

    def uninstall(self) -> None:
        self._validate_package()
        logger.info(f"Uninstalling {self.package_name} via brew")
        subprocess.run(["brew", "uninstall", self.package_name], check=True)

    def status(self) -> bool:
        logger.info(f"Checking brew status for {self.package_name}")
        result = subprocess.run(
            ["brew", "list", self.package_name], capture_output=True, text=True
        )
        if result.returncode == 0:
            logger.info(f"Package {self.package_name} is installed.")
            logger.info(f"Package details:\n{result.stdout}")
            return True
        else:
            logger.warning(f"Package {self.package_name} is not installed.")
            return False
