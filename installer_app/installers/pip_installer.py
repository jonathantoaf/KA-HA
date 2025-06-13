from typing import List

from installer_app.installers.package_installer import PackageInstaller


class PipInstaller(PackageInstaller):
    def _get_installer_name(self) -> str:
        return "pip"

    def _get_install_command(self) -> List[str]:
        pkg = (
            f"{self.package_name}=={self.version}"
            if self.version != "latest"
            else self.package_name
        )
        return ["pip", "install", pkg]

    def _get_uninstall_command(self) -> List[str]:
        return ["pip", "uninstall", "-y", self.package_name]

    def _get_status_command(self) -> List[str]:
        return ["pip", "show", self.package_name]
