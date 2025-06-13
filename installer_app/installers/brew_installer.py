from typing import List

from installer_app.installers.package_installer import PackageInstaller


class BrewInstaller(PackageInstaller):
    def _get_installer_name(self) -> str:
        return "brew"

    def _get_install_command(self) -> List[str]:
        return ["brew", "install", self.package_name]

    def _get_uninstall_command(self) -> List[str]:
        return ["brew", "uninstall", self.package_name]

    def _get_status_command(self) -> List[str]:
        return ["brew", "list", self.package_name]
