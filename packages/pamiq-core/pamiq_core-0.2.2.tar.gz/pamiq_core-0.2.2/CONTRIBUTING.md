# Contributing

Thank you for your interest in contributing to PAMIQ Core. This guide explains how to set up your development environment.

## 📋 Prerequisites

Please install the following tools in advance:

### Required Tools

- 🐳 **Docker (Docker Compose)**

    - Docker Desktop: <https://www.docker.com/get-started/>
    - Docker Engine (Linux only): <https://docs.docker.com/engine/install/>
    - Verification command:
        ```sh
        docker version && docker compose version
        ```

- 🔨 **make**

    - Windows: Install via [`scoop`](https://scoop.sh) or [`chocolatey`](https://chocolatey.org)
    - macOS: Pre-installed
    - Linux: Use your distribution's package manager (e.g., for Ubuntu: `sudo apt install make`)
    - Verification command:
        ```sh
        make -v
        ```

- 🌲 **git**

    - Download: <https://git-scm.com/downloads>
    - Verification command:
        ```sh
        git -v
        ```

## 🚀 Setting Up the Development Environment

1. Repository Setup

    First, fork the repository by clicking the "Fork" button:

    [![Fork Repository](https://img.shields.io/badge/Fork%20Repository-2ea44f?style=for-the-badge)](https://github.com/MLShukai/pamiq-core/fork)

    After fork, clone your repository:

    ```sh
    git clone https://github.com/your-name/pamiq-core.git
    cd pamiq-core
    ```

2. Building the Docker Environment

    ```sh
    # Build the image
    make docker-build

    # Start the container
    make docker-up

    # Connect to the container
    make docker-attach
    ```

3. Git Initial Configuration

    ```sh
    git config user.name <your GitHub username>
    git config user.email <your GitHub email>
    ```

## 💻 Development Environment Configuration

### Development with VSCode

You can develop by attaching to the container from your preferred editor (VSCode recommended).

📚 Reference: [Attach with VSCode Dev Containers extension](https://code.visualstudio.com/docs/devcontainers/attach-container)

The development container includes the following environment:

- Package manager ([**uv**](https://docs.astral.sh/uv/))
- Git for version control
- Development dependency packages

## 🔄 Development Workflow

Use the following commands for development:

```sh
# Set up Python virtual environment
make venv

# Format code and run pre-commit hooks
make format

# Run tests
make test

# Run type checking
make type

# Run the entire workflow (format, test, type)
make run
```

## ⚙️ Environment Management

### Stopping the Container

```sh
make docker-down
```

### Cleaning Up the Development Environment

```sh
make clean
```

### ⚠️ Complete Deletion (Use Caution)

```sh
# Warning: All work data will be deleted!
make docker-down-volume
```

## 🤝 Contribution Flow

1. Create a new branch for feature additions or bug fixes
2. Make your changes
3. Write tests for new features
4. Run the entire workflow before sending a PR:
    ```shell
    make run
    ```
5. Submit a Pull Request with a clear explanation of your changes

If you have questions or issues, please create an Issue in the GitHub repository.

## 🪮 Coding Conventions

Checkout to [**CODING_CONVENTIONS.md**](./CODING_CONVENTIONS.md)
