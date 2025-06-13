from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class Installer(ABC):
    def __init__(
        self, package_name: str, config: dict, version: Optional[str] = "latest"
    ) -> None:
        self.package_name = package_name
        self.version = version
        self.config = config
        self.allowed_packages: Dict[str, List[str]] = self.config.get(
            "allowed_packages", {}
        )

    def _validate_package(self) -> None:
        if self.package_name not in self.allowed_packages:
            raise ValueError(
                f"Package '{self.package_name}' is not allowed. "
                f"Allowed packages are: {list(self.allowed_packages.keys())}"
            )
        if self.version not in self.allowed_packages[self.package_name]:
            raise ValueError(
                f"Version '{self.version}' of package '{self.package_name}' is not allowed. "
                f"Allowed versions are: {self.allowed_packages[self.package_name]}"
            )

    @abstractmethod
    def install(self) -> None:
        pass

    @abstractmethod
    def uninstall(self) -> None:
        pass

    @abstractmethod
    def status(self) -> bool:
        pass
