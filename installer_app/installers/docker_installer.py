from installer_app.core.installer import Installer
from typing import Dict, Any, Optional
from installer_app.core.logger import logger
from installer_app.constants import CommandResult
import subprocess


class DockerInstaller(Installer):
    def __init__(
        self,
        package_name: str,
        config: Dict[str, Any],
        version: Optional[str] = "latest",
    ) -> None:
        super().__init__(package_name, config, version)
        self.container_name = package_name
        logger.info(
            f"Initializing DockerInstaller for package: {self.package_name}, version: {self.version}"
        )

    def _get_docker_config(self) -> Dict[str, Any]:
        configurations = self.config.get("configurations", {})
        return configurations.get(
            self.package_name, {"image": self.package_name, "restart": "unless-stopped"}
        )

    def _image_exists_locally(self, image: str) -> bool:
        try:
            result = subprocess.run(
                ["docker", "images", "-q", image],
                capture_output=True,
                text=True,
                check=True,
            )
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError:
            return False

    def _pull_image_with_progress(self, image: str) -> None:
        if self._image_exists_locally(image):
            logger.info(f"✅ Image already exists locally: {image}")
            return

        logger.info(f"🔄 Pulling Docker image: {image}")
        logger.info("📥 This may take a few minutes...")

        try:
            process = subprocess.Popen(
                ["docker", "pull", image],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True,
            )

            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    if "Pulling from" in line:
                        logger.info(f"📦 {line}")
                    elif "Status:" in line:
                        logger.info(f"📋 {line}")

            if process.poll() == CommandResult.SUCCESS:
                logger.info(f"✅ Successfully pulled image: {image}")
            else:
                raise subprocess.CalledProcessError(
                    process.poll(), ["docker", "pull", image]
                )

        except subprocess.CalledProcessError:
            logger.error(f"❌ Failed to pull image: {image}")
            raise
        except KeyboardInterrupt:
            logger.warning("⚠️ Image pull interrupted by user")
            raise

    def _build_docker_command(self, config: Dict[str, Any], image: str) -> list:
        cmd = ["docker", "run", "-d", "--name", self.container_name]

        config_handlers = {
            "ports": lambda items: [
                f"-p{host}:{container}" for host, container in items.items()
            ],
            "environment": lambda items: [
                f"-e{key}={value}" for key, value in items.items()
            ],
            "volumes": lambda items: [
                f"-v{volume}:{mount}" for volume, mount in items.items()
            ],
            "restart": lambda value: [f"--restart={value}"],
        }

        for key, handler in config_handlers.items():
            if key in config:
                cmd.extend(handler(config[key]))

        cmd.append(image)
        return cmd

    def install(self) -> None:
        config = self._get_docker_config()
        image = f"{config['image']}:{self.version}"

        try:
            self._pull_image_with_progress(image)
        except (subprocess.CalledProcessError, KeyboardInterrupt):
            raise

        if self._container_exists():
            logger.info(f"🔄 Removing existing container: {self.container_name}")
            subprocess.run(["docker", "stop", self.container_name], capture_output=True)
            subprocess.run(["docker", "rm", self.container_name], capture_output=True)

        cmd = self._build_docker_command(config, image)

        logger.info(f"🚀 Starting Docker container: {self.container_name}")
        logger.info(f"Running command: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            container_id = result.stdout.strip()[:12]
            logger.info(f"✅ Container started successfully! ID: {container_id}")

            if "access_url" in config:
                logger.info(f"🌐 Access URL: {config['access_url']}")

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to start container: {e}")
            if e.stderr:
                logger.error(f"Error details: {e.stderr}")
            raise

    def _container_exists(self) -> bool:
        try:
            result = subprocess.run(
                ["docker", "ps", "-aq", "--filter", f"name=^{self.container_name}$"],
                capture_output=True,
                text=True,
                check=True,
            )
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError:
            return False

    def uninstall(self) -> None:
        logger.info(f"🛑 Uninstalling container: {self.container_name}")

        try:
            subprocess.run(
                ["docker", "stop", self.container_name],
                capture_output=True,
                text=True,
                check=True,
            )
            logger.info(f"✅ Stopped container: {self.container_name}")

            subprocess.run(
                ["docker", "rm", self.container_name],
                capture_output=True,
                text=True,
                check=True,
            )
            logger.info(f"✅ Removed container: {self.container_name}")

        except subprocess.CalledProcessError:
            logger.warning(
                f"⚠️ Container '{self.container_name}' not found or already removed"
            )

    def status(self) -> bool:
        logger.info(f"📊 Checking status of container: {self.container_name}")

        try:
            result = subprocess.run(
                [
                    "docker",
                    "ps",
                    "--filter",
                    f"name=^{self.container_name}$",
                    "--format",
                    "table {{.Names}}\t{{.Status}}\t{{.Ports}}",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            if self.container_name in result.stdout:
                logger.info(f"✅ Container '{self.container_name}' is running")
                logger.info(f"Details:\n{result.stdout}")

                config = self._get_docker_config()
                if "access_url" in config:
                    logger.info(f"🌐 Access URL: {config['access_url']}")
                return True
            else:
                all_result = subprocess.run(
                    [
                        "docker",
                        "ps",
                        "-a",
                        "--filter",
                        f"name=^{self.container_name}$",
                        "--format",
                        "table {{.Names}}\t{{.Status}}",
                    ],
                    capture_output=True,
                    text=True,
                )

                if self.container_name in all_result.stdout:
                    logger.warning(
                        f"⚠️ Container '{self.container_name}' exists but is not running"
                    )
                    logger.info(f"Details:\n{all_result.stdout}")
                else:
                    logger.warning(
                        f"❌ Container '{self.container_name}' does not exist"
                    )
                return False

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to check container status: {e}")
            raise
