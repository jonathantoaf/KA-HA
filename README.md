# KA-HA Package Installer

**KA-HA** (Kayhut Home Assignment) is a generic Python-based CLI installer that automates package installation across multiple package managers (pip, brew, docker) using a unified configuration file.

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#️-usage)
- [Configuration](#️-configuration)
- [Examples](#-examples-in-action)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)


## 🚀 Features

- **Multi-platform support**: pip, brew, and Docker installers
- **Configuration-driven**: Define allowed packages and versions in YAML
- **Unified CLI**: Single command interface for all package managers
- **Real-time feedback**: Progress indicators for Docker image pulls
- **Status monitoring**: Check installation status of packages
- **Safe operations**: Validates packages against whitelist before installation

## 📦 Installation

### Prerequisites

KA-HA assumes you have the following tools already installed on your system:

- **Python 3.12+** with pip
- **Docker** - For container management
- **Homebrew** - For macOS/Linux package management (if using brew installer)

### From Source
```bash
git clone https://github.com/jonathantoaf/KA-HA.git
cd KA-HA

# Install using Poetry (recommended)
poetry install
poetry run installer --help

# Or install with pip
pip install -e .
installer --help
```

### Using the CLI directly
```bash
python main.py --help
```

### As installed package
```bash
# After installation
installer --help
```

## 🛠️ Usage

### Basic Commands

```bash
# List all available packages
installer list

# Install a package
installer install <installer_type> <package_name> [--version VERSION]

# Check package status
installer status <installer_type> <package_name>

# Uninstall a package
installer uninstall <installer_type> <package_name>
```

### Examples

#### PIP Packages
```bash
# Install latest version
installer install pip requests

# Install specific version
installer install pip requests --version 2.28.0

# Check status
installer status pip requests

# Uninstall
installer uninstall pip requests
```

#### Homebrew Packages
```bash
# Install htop using Homebrew
installer install brew htop

# Check status
installer status brew htop

# Uninstall
installer uninstall brew htop
```

#### Docker Containers
```bash
# Install nginx container
installer install docker nginx

# Install OpenWebUI with custom configuration
installer install docker openwebui

# Check container status
installer status docker nginx

# Stop and remove container
installer uninstall docker nginx
```

## ⚙️ Configuration

Create a `config.yaml` file in your project root:

```yaml
logging:
  version: 1
  formatters:
    formatter:
      (): coloredlogs.ColoredFormatter
      format: "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
  handlers:
    console:
      class: "logging.StreamHandler"
      level: "DEBUG"
      formatter: "formatter"
      stream: "ext://sys.stdout"
  root:
    level: "DEBUG"
    handlers: ["console"]

pip:
  allowed_packages:
    requests: ["2.28.0", "latest"]
    numpy: ["1.24.0", "latest"]
    pandas: ["1.5.0", "latest"]

brew:
  allowed_packages:
    htop: ["latest"]  
    bat: ["latest"]

docker:
  allowed_packages:
    nginx: ["latest", "1.25", "1.24"]
    openwebui: ["latest", "0.1.124"]
  configurations:
    nginx:
      image: "nginx"
      ports:
        "80": "80"
      restart: "always"
      access_url: "http://localhost:80"
    openwebui:
      image: "ghcr.io/open-webui/open-webui"
      ports:
        "3000": "8080"
      environment:
        OLLAMA_BASE_URL: "https://api.openai.com/v1"
      volumes:
        "open-webui": "/app/backend/data"
      restart: "always"
      access_url: "http://localhost:3000"
```

## 📝 Examples in Action

### Complete workflow example:
```bash
# 1. List available packages
installer list

# 2. Install a Python package
installer install pip requests --version latest

# 3. Install a system package
installer install brew htop

# 4. Run a Docker container
installer install docker nginx

# 5. Check all statuses
installer status pip requests
installer status brew htop
installer status docker nginx

# 6. Clean up
installer uninstall pip requests
installer uninstall brew htop
installer uninstall docker nginx
```

## 👨‍💻 Development

### Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/jonathantoaf/KA-HA.git
cd KA-HA
```

2. **Install Poetry** (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. **Install dependencies using Poetry:**
```bash
# Install all dependencies including dev dependencies
poetry install

# Activate the virtual environment
poetry shell
```

4. **Verify installation:**
```bash
# Test the CLI
poetry run installer --help
# or if shell is activated
installer --help
```

### Development Workflow

#### Running the project:
```bash
# Method 1: Using Poetry
poetry run installer list

# Method 2: Direct execution
python main.py list

# Method 3: Module execution
python -m installer_app.cli_app list
```

#### Installing dependencies:
```bash
# Add a new dependency
poetry add <package_name>

# Add a development dependency
poetry add --group dev <package_name>

# Update dependencies
poetry update

# Show dependency tree
poetry show --tree
```

#### Code formatting and linting:
```bash
# Run ruff linter
poetry run ruff check .

# Fix auto-fixable issues
poetry run ruff check --fix .

# Format code
poetry run ruff format .
```

#### Testing:
```bash
# Note: Unit tests are not implemented yet
# Currently testing is done manually by running the CLI commands

# Test installation
poetry run installer list

# Test specific commands
poetry run installer install docker nginx
poetry run installer status docker nginx
poetry run installer uninstall docker nginx
```

### Project Structure
```
KA-HA/
├── installer_app/
│   ├── __init__.py
│   ├── cli_app.py              # Main CLI application
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration loader
│   │   ├── factory.py          # Installer factory
│   │   ├── installer.py        # Base installer class
│   │   └── logger.py           # Logging configuration
│   └── installers/
│       ├── __init__.py
│       ├── pip_installer.py    # PIP installer
│       ├── brew_installer.py   # Homebrew installer
│       └── docker_installer.py # Docker installer
├── config.yaml                 # Configuration file
├── main.py                     # Entry point
├── pyproject.toml              # Poetry configuration
├── poetry.lock                 # Poetry lock file
└── README.md                   # This file
```


## 🔧 Troubleshooting

### Prerequisites Check
Verify that all required tools are installed:

```bash
# Check Python
python --version  # Should be 3.12+

# Check Docker
docker --version

# Check Homebrew (macOS)
brew --version

# Check Poetry
poetry --version
```

If any of these commands fail, install the missing tools:
- **Python**: Download from [python.org](https://python.org)
- **Docker**: Download from [docker.com](https://docker.com)
- **Homebrew**: Install from [brew.sh](https://brew.sh)
- **Poetry**: Install from [python-poetry.org](https://python-poetry.org)



### Development Guidelines
- Use Poetry for dependency management
- Follow the existing code structure
- Add type hints for all functions
- Use the logging system instead of print statements




