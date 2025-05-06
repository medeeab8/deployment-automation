# deployment-automation

# Deployment Automation Tool

A flexible, extensible framework for packaging and deploying applications across different environments. This tool supports multiple programming languages, packaging methods, and deployment targets through a modular, configuration-driven architecture.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Packaging Methods](#packaging-methods)
- [Extending the Tool](#extending-the-tool)
- [Development](#development)
- [Testing](#testing)
- [Windows Usage](#windows-usage)
- [License](#license)

## Overview

The Deployment Automation Tool simplifies the process of packaging and deploying applications written in different programming languages to various environments. It handles the complexities of different packaging methods and environment configurations, providing a consistent interface for deployment operations.

**Current supported languages:**
- Python
- Perl

**Current supported packaging methods:**
- Tarballs (.tar.gz)
- Python wheels (.whl)
- Docker images

**Current supported environments:**
- Virtual machines (VM)

## Features

- **Language-agnostic design** - Extensible to support any programming language
- **Multiple packaging methods** - Choose the right packaging approach for each application
- **Environment abstraction** - Deploy to different environments using the same commands
- **Configuration-driven** - Easy to set up and customize through YAML files
- **Validation** - Pre-deployment validation ensures applications meet requirements
- **Test mode** - Preview deployment steps without making actual changes

## Architecture

The tool follows a modular architecture with clear separation of concerns:

```
                    ┌─────────────────┐
                    │ DeploymentManager│
                    └────────┬────────┘
                             │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
┌─────────▼───────┐ ┌───────▼─────┐ ┌─────────▼──────┐
│    Packager     │ │  Validator  │ │ EnvironmentManager│
└─────────────────┘ └─────────────┘ └──────────────────┘
```

- **Deployment Manager**: Orchestrates the overall deployment process
- **Packagers**: Handle language-specific packaging (Python, Perl)
- **Validators**: Verify applications meet requirements before deployment
- **Environment Manager**: Prepares and manages target environments

## Installation

### Prerequisites

- Python 3.6 or higher
- For wheel packaging: `wheel` package
- For Docker packaging: Docker installed and running

### From Source

Clone the repository and install:

```bash
git clone https://github.com/yourusername/deployment-automation.git
cd deployment-automation
pip install -e .
```

### With Optional Dependencies

For development with testing tools:
```bash
pip install -e ".[dev]"
```

For wheel packaging support:
```bash
pip install -e ".[wheel]"
```

## Configuration

The tool uses two YAML configuration files:

### apps.yaml

Define applications and their properties:

```yaml
python-app:
  name: python-app
  type: python
  source_dir: ./apps/python-app
  package_type: wheel  # Optional: tarball (default), wheel, docker
  
  # Optional Docker settings
  python_base_image: python:3.9-slim
  docker_commands:
    - RUN pip install -r requirements.txt
    - CMD ["python", "app.py"]

perl-app:
  name: perl-app
  type: perl
  source_dir: ./apps/perl-app
  
  # Optional Docker settings
  package_type: docker
  perl_base_image: perl:5.32-slim
  docker_commands:
    - CMD ["perl", "app.pl"]
```

### environments.yaml

Define deployment environments:

```yaml
development:
  type: vm
  hosts:
    - dev-server1.example.com
    - dev-server2.example.com

production:
  type: vm
  hosts:
    - prod-server1.example.com
    - prod-server2.example.com
```

## Usage

### Basic Command Format

```bash
python src/deployer.py <app-name> <environment> [--version VERSION] [--test]
```

### Examples

```bash
# Deploy python-app to development with auto-generated version
python src/deployer.py python-app development

# Deploy with specific version
python src/deployer.py python-app production --version 1.2.3

# Test mode (no actual deployment)
python src/deployer.py perl-app development --test
```

## Packaging Methods

### Tarballs

The default packaging method for both Python and Perl applications. Creates a `.tar.gz` file containing the application source code.

**Configuration:**
```yaml
python-app:
  name: python-app
  type: python
  source_dir: ./apps/python-app
  # No package_type specified defaults to tarball
```

### Python Wheels

For Python applications, creates a wheel package (`.whl`) that can be installed with pip.

**Requirements:**
- `wheel` package installed
- Valid `setup.py` in the application source directory

**Configuration:**
```yaml
python-app:
  name: python-app
  type: python
  source_dir: ./apps/python-app
  package_type: wheel
```

### Docker Images

Packages applications as Docker images that can be run in containerized environments.

**Requirements:**
- Docker installed and running

**Configuration:**
```yaml
python-app:
  name: python-app
  type: python
  source_dir: ./apps/python-app
  package_type: docker
  python_base_image: python:3.9-slim  # Base image for Python apps
  docker_commands:  # Additional Docker commands
    - RUN pip install -r requirements.txt
    - CMD ["python", "app.py"]
```

## Extending the Tool

### Adding a New Application Type

1. Create a new packager class in `app_packager.py`:
   ```python
   class NewAppTypePackager(BasePackager):
       def package(self, version):
           # Implementation here
           pass
   ```

2. Create a validator in `validators/`:
   ```python
   class NewAppTypeValidator:
       def __init__(self, app_config):
           self.app_config = app_config
           
       def validate(self):
           # Validation logic here
           pass
   ```

3. Update `deployer.py` to support the new type:
   ```python
   if self.app_config['type'] == 'new_app_type':
       self.packager = NewAppTypePackager(self.app_config)
       self.validator = NewAppTypeValidator(self.app_config)
   ```

### Adding a New Environment Type

1. Update `env_manager.py` to handle the new environment:
   ```python
   def prepare(self):
       if self.env_type == 'new_env_type':
           self._prepare_new_env_type()
           
   def _prepare_new_env_type(self):
       # Implementation here
       pass
   ```

## Development

### Project Structure

```
deployment-automation/
├── src/
│   ├── app_packager.py      # Application packaging functionality
│   ├── deployer.py          # Main deployment orchestration
│   ├── env_manager.py       # Environment management
│   └── validators/          # Application validators
│       ├── python_validator.py
│       └── perl_validator.py
├── tests/
│   ├── test_basic_deployment.py    # Basic functionality tests
│   └── test_docker_packaging.py    # Docker-specific tests
├── config/
│   ├── apps.yaml            # Application configurations
│   └── environments.yaml    # Environment configurations
├── setup.py                 # Package installation configuration
├── requirements.txt         # Dependencies
└── deploy.bat               # Windows wrapper script
```

### Development Workflow

1. Make your changes to the source code
2. Run tests to verify functionality
3. Update documentation if necessary
4. Submit a pull request

## Testing

The project includes several test modules:

```bash
# Run basic deployment tests
python tests/test_basic_deployment.py

# Run Docker packaging tests (requires Docker)
python tests/test_docker_packaging.py
```

## Windows Usage

On Windows systems, you can use the included batch file wrapper:

```
# Get help
deploy.bat --help

# Deploy an application
deploy.bat python-app development --test
```

The batch file handles path resolution and passes all arguments to the main Python script.
