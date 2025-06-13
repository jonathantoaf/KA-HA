import subprocess
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from installer_app.utils.constants import CommandResult
from installer_app.utils.exceptions import PackageInstallerError
from installer_app.core.installer import Installer
from installer_app.core.logger import logger


class PackageInstaller(Installer, ABC):
    def __init__(
        self,
        package_name: str,
        config: Dict[str, Any],
        version: Optional[str] = "latest",
    ) -> None:
        super().__init__(package_name, config, version)
        self.installer_name = self._get_installer_name()
        logger.info(
            f"Initializing {self.installer_name} for package: {self.package_name}, version: {self.version}"
        )

    @abstractmethod
    def _get_installer_name(self) -> str:
        pass

    @abstractmethod
    def _get_install_command(self) -> List[str]:
        pass

    @abstractmethod
    def _get_uninstall_command(self) -> List[str]:
        pass

    @abstractmethod
    def _get_status_command(self) -> List[str]:
        pass

    def _run_command(
        self, command: List[str], operation: str, raise_on_error: bool = True
    ) -> subprocess.CompletedProcess:
        try:
            logger.info(f"Running {operation} command: {' '.join(command)}")
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == CommandResult.SUCCESS:
                logger.info(
                    f"{self.installer_name} {operation} completed successfully for {self.package_name}"
                )
                if result.stdout:
                    logger.debug(f"Command output:\n{result.stdout}")
            elif raise_on_error:
                error_msg = (
                    f"{self.installer_name} {operation} failed for {self.package_name}"
                )
                if result.stderr:
                    error_msg += f"\nError: {result.stderr.strip()}"
                if result.stdout:
                    error_msg += f"\nOutput: {result.stdout.strip()}"

                logger.error(error_msg)
                raise PackageInstallerError(error_msg)
            else:
                logger.info(
                    f"{self.installer_name} {operation} returned code {result.returncode} for {self.package_name}"
                )

            return result

        except subprocess.TimeoutExpired as e:
            error_msg = f"{self.installer_name} {operation} timed out for {self.package_name} after {e.timeout} seconds"
            logger.error(error_msg)
            raise PackageInstallerError(error_msg) from e
        except FileNotFoundError as e:
            error_msg = f"{self.installer_name} command not found. Is {self.installer_name} installed?"
            logger.error(error_msg)
            raise PackageInstallerError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error during {self.installer_name} {operation} for {self.package_name}: {e}"
            logger.error(error_msg)
            raise PackageInstallerError(error_msg) from e

    def install(self) -> None:
        command = self._get_install_command()
        self._run_command(command, "install")

    def uninstall(self) -> None:
        command = self._get_uninstall_command()
        self._run_command(command, "uninstall")

    def status(self) -> bool:
        try:
            command = self._get_status_command()
            result = self._run_command(command, "status", raise_on_error=False)

            if result.returncode == CommandResult.SUCCESS:
                logger.info(
                    f"Package {self.package_name} is installed via {self.installer_name}"
                )
                if result.stdout:
                    logger.debug(f"Package details:\n{result.stdout}")
                return True
            else:
                logger.info(
                    f"Package {self.package_name} is not installed via {self.installer_name}"
                )
                return False

        except PackageInstallerError:
            logger.warning(
                f"Status check failed for {self.package_name} via {self.installer_name}"
            )
            return False
