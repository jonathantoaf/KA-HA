from enum import Enum
from typing import Optional

import typer

from installer_app.core.config import load_config
from installer_app.core.factory import InstallerFactory
from installer_app.core.logger import logger


class InstallerType(str, Enum):
    pip = "pip"
    brew = "brew"
    docker = "docker"


app = typer.Typer(
    help="Generic Python-based CLI installer that automates package installation"
)


@app.command()
def install(
    installer_type: InstallerType = typer.Argument(
        ..., help="Type of installer to use"
    ),
    package: str = typer.Argument(..., help="Name of the package to install"),
    version: Optional[str] = typer.Option(
        "latest", "--version", "-v", help="Version to install (default: latest)"
    ),
):
    """Install a package using the specified installer type."""
    logger.info(
        f"Installing {package} (version: {version}) using {installer_type.value}"
    )

    try:
        installer = InstallerFactory.create_installer(
            installer_type.value, package, version
        )
        installer.install()
        typer.echo(f"✅ Successfully installed {package} using {installer_type.value}")
    except ValueError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Installation failed: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def uninstall(
    installer_type: InstallerType = typer.Argument(
        ..., help="Type of installer to use"
    ),
    package: str = typer.Argument(..., help="Name of the package to uninstall"),
):
    """Uninstall a package using the specified installer type."""
    logger.info(f"Uninstalling {package} using {installer_type.value}")

    try:
        installer = InstallerFactory.create_installer(installer_type.value, package)
        installer.uninstall()
        typer.echo(
            f"✅ Successfully uninstalled {package} using {installer_type.value}"
        )
    except ValueError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Uninstallation failed: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def status(
    installer_type: InstallerType = typer.Argument(
        ..., help="Type of installer to use"
    ),
    package: str = typer.Argument(..., help="Name of the package to check"),
):
    """Check the installation status of a package."""
    logger.info(f"Checking status of {package} using {installer_type.value}")

    try:
        installer = InstallerFactory.create_installer(installer_type.value, package)
        is_installed = installer.status()
        if is_installed:
            typer.echo(f"✅ {package} is installed using {installer_type.value}")
        else:
            typer.echo(f"❌ {package} is not installed using {installer_type.value}")
        typer.echo(f"📊 Status check completed for {package}")
    except ValueError as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Status check failed: {e}", err=True)
        raise typer.Exit(1)


@app.command("list")
def list_packages():
    """List all allowed packages and their versions from the configuration."""
    logger.info("Listing allowed packages and versions from config")

    try:
        config = load_config()

        pip_config = config.get("pip", {})
        pip_packages = pip_config.get("allowed_packages", {})

        if pip_packages:
            typer.echo("\n📦 PIP Packages:")
            for pkg, versions in pip_packages.items():
                typer.echo(f"  • {pkg}: allowed versions = {versions}")

        brew_config = config.get("brew", {})
        brew_packages = brew_config.get("allowed_packages", {})

        if brew_packages:
            typer.echo("\n🍺 BREW Packages:")
            for pkg, versions in brew_packages.items():
                typer.echo(f"  • {pkg}: allowed versions = {versions}")

        # Display Docker packages
        docker_config = config.get("docker", {})
        docker_packages = docker_config.get("allowed_packages", {})

        if docker_packages:
            typer.echo("\n🐳 DOCKER Packages:")
            for pkg, versions in docker_packages.items():
                typer.echo(f"  • {pkg}: allowed versions = {versions}")

        if not pip_packages and not brew_packages and not docker_packages:
            typer.echo("❌ No allowed packages configured")
        else:
            typer.echo(
                f"\n📋 Total packages: {len(pip_packages)} pip, {len(brew_packages)} brew, {len(docker_packages)} docker"
            )

    except FileNotFoundError:
        typer.echo("❌ Configuration file 'config.yaml' not found", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"❌ Failed to load configuration: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
