from typing import Optional

import typer

from installer_app.utils.constants import (
    Config,
    Emoji,
    PackageInfo,
    PackageType,
    CommandResult,
)
from installer_app.utils.exceptions import PackageInstallerError
from installer_app.core.config import load_config
from installer_app.core.factory import InstallerFactory
from installer_app.core.logger import logger


app = typer.Typer(
    help="Generic Python-based CLI installer that automates package installation"
)


@app.command()
def install(
    installer_type: PackageType = typer.Argument(..., help="Type of installer to use"),
    package: str = typer.Argument(..., help="Name of the package to install"),
    version: Optional[str] = typer.Option(
        Config.DEFAULT_VERSION,
        "--version",
        "-v",
        help=f"Version to install (default: {Config.DEFAULT_VERSION})",
    ),
):
    logger.info(
        f"Installing {package} (version: {version}) using {installer_type.value}"
    )

    try:
        installer = InstallerFactory.create_installer(
            installer_type.value, package, version
        )
        installer.install()
        typer.echo(
            f"{Emoji.SUCCESS} Successfully installed {package} using {installer_type.value}"
        )
    except PackageInstallerError as e:
        typer.echo(f"{Emoji.ERROR} Installation failed: {e}", err=True)
        raise typer.Exit(CommandResult.FAILURE)
    except ValueError as e:
        typer.echo(f"{Emoji.ERROR} Error: {e}", err=True)
        raise typer.Exit(CommandResult.FAILURE)
    except Exception as e:
        typer.echo(f"{Emoji.ERROR} Unexpected error: {e}", err=True)
        raise typer.Exit(CommandResult.FAILURE)


@app.command()
def uninstall(
    installer_type: PackageType = typer.Argument(..., help="Type of installer to use"),
    package: str = typer.Argument(..., help="Name of the package to uninstall"),
):
    logger.info(f"Uninstalling {package} using {installer_type.value}")

    try:
        installer = InstallerFactory.create_installer(installer_type.value, package)
        installer.uninstall()
        typer.echo(
            f"{Emoji.SUCCESS} Successfully uninstalled {package} using {installer_type.value}"
        )
    except PackageInstallerError as e:
        typer.echo(f"{Emoji.ERROR} Uninstallation failed: {e}", err=True)
        raise typer.Exit(CommandResult.FAILURE)
    except ValueError as e:
        typer.echo(f"{Emoji.ERROR} Error: {e}", err=True)
        raise typer.Exit(CommandResult.FAILURE)
    except Exception as e:
        typer.echo(f"{Emoji.ERROR} Unexpected error: {e}", err=True)
        raise typer.Exit(CommandResult.FAILURE)


@app.command()
def status(
    installer_type: PackageType = typer.Argument(..., help="Type of installer to use"),
    package: str = typer.Argument(..., help="Name of the package to check"),
):
    logger.info(f"Checking status of {package} using {installer_type.value}")

    try:
        installer = InstallerFactory.create_installer(installer_type.value, package)
        is_installed = installer.status()
        if is_installed:
            typer.echo(
                f"{Emoji.SUCCESS} {package} is installed using {installer_type.value}"
            )
        else:
            typer.echo(
                f"{Emoji.ERROR} {package} is not installed using {installer_type.value}"
            )
        typer.echo(f"{Emoji.INFO} Status check completed for {package}")
    except ValueError as e:
        typer.echo(f"{Emoji.ERROR} Error: {e}", err=True)
        raise typer.Exit(CommandResult.FAILURE)
    except Exception as e:
        typer.echo(f"{Emoji.ERROR} Status check failed: {e}", err=True)
        raise typer.Exit(CommandResult.FAILURE)


@app.command("list")
def list_packages():
    logger.info("Listing allowed packages and versions from config")

    try:
        config = load_config()

        total_counts = []
        has_packages = False

        for pkg_type, title, _ in PackageInfo.get_all_types():
            pkg_config = config.get(pkg_type.value, {})
            packages = pkg_config.get(Config.ALLOWED_PACKAGES_KEY, {})
            if packages:
                has_packages = True
                typer.echo(f"\n{title}")
                for pkg, versions in packages.items():
                    typer.echo(f"  • {pkg}: allowed versions = {versions}")
                total_counts.append(f"{len(packages)} {pkg_type.value}")

        if not has_packages:
            typer.echo(f"{Emoji.ERROR} No allowed packages configured")
        else:
            typer.echo(f"\n{Emoji.SUMMARY} Total packages: {', '.join(total_counts)}")

    except FileNotFoundError:
        typer.echo(
            f"{Emoji.ERROR} Configuration file '{Config.FILENAME}' not found", err=True
        )
        raise typer.Exit(CommandResult.FAILURE)
    except Exception as e:
        typer.echo(f"{Emoji.ERROR} Failed to load configuration: {e}", err=True)
        raise typer.Exit(CommandResult.FAILURE)


if __name__ == "__main__":
    app()