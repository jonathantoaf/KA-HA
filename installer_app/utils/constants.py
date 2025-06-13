from enum import Enum, IntEnum
from typing import List, Tuple


class PackageType(str, Enum):
    """Package type enumeration."""

    PIP = "pip"
    BREW = "brew"
    DOCKER = "docker"


class Emoji:
    """Emoji constants for UI display."""

    SUCCESS = "✅"
    ERROR = "❌"
    INFO = "📊"
    SUMMARY = "📋"
    PIP = "📦"
    BREW = "🍺"
    DOCKER = "🐳"


class Config:
    """Configuration related constants."""

    FILENAME = "config.yaml"
    ALLOWED_PACKAGES_KEY = "allowed_packages"
    DEFAULT_VERSION = "latest"


class PackageInfo:
    """Package type display information."""

    @classmethod
    def get_all_types(cls) -> List[Tuple[PackageType, str, str]]:
        """Return all package types with their display info: (type, title, emoji)."""
        return [
            (PackageType.PIP, f"{Emoji.PIP} PIP Packages:", Emoji.PIP),
            (PackageType.BREW, f"{Emoji.BREW} BREW Packages:", Emoji.BREW),
            (PackageType.DOCKER, f"{Emoji.DOCKER} DOCKER Packages:", Emoji.DOCKER),
        ]

    @classmethod
    def get_type_title(cls, package_type: str) -> str:
        """Get the display title for a package type."""
        type_map = {
            PackageType.PIP: f"{Emoji.PIP} PIP Packages:",
            PackageType.BREW: f"{Emoji.BREW} BREW Packages:",
            PackageType.DOCKER: f"{Emoji.DOCKER} DOCKER Packages:",
        }
        return type_map.get(package_type, f"Unknown Package Type: {package_type}")


class CommandResult(IntEnum):
    """Command execution result codes."""

    SUCCESS = 0
    FAILURE = 1
    NOT_FOUND = 127
    PERMISSION_DENIED = 126
    TIMEOUT = 124
