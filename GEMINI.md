# Gemini Code Assistant Workspace

This document provides context for the Gemini Code Assistant to work effectively within the `pyinterceptor` project.

## Project Overview

`PyInterceptor` is a Python library for intercepting and manipulating keyboard and mouse inputs on Windows systems. It provides a high-level interface for working with keyboard and mouse events, including hotkey management and input simulation. The core functionality is implemented in the `pyinterceptor` directory.

## Key Technologies

- **Language:** Python (>=3.7)
- **Build System:** `setuptools`
- **Packaging:** `pyproject.toml`

## Dependencies

- **Runtime:** The project requires the "Interception driver" to be installed on the user's Windows system. No other external Python packages are listed as runtime dependencies in `pyproject.toml`.
- **Build:** `build`, `twine` (for publishing)

## Commands

### Building the Project

To build the distributable package (`.whl` and `.tar.gz`):

```bash
python -m build
```
This command should be run from the project root directory. The output will be in the `dist/` directory.

### Running Tests

The project does not have a formal, automated test suite (e.g., using `pytest` or `unittest`). However, there is an example script that can be used for manual testing and demonstration.

To run the example:

```bash
python examples/test.py
```

### Building Documentation

The project uses [Sphinx](https://www.sphinx-doc.org/) to generate documentation.

To build the HTML documentation:

```bash
cd docs
make.bat html
```
The output will be generated in the `docs/_build/html/` directory.

## Code Style and Conventions

- **Typing:** The codebase uses Python's type hints extensively (e.g., `Set`, `Dict`, `Callable`, `Literal`). New code should also include type hints.
- **Docstrings:** Docstrings follow a style similar to Google's Python style guide, with `Args:` and `Returns:` sections.
- **Comments and Docstrings:** All comments and docstrings in the project must be written in English.
- **Key State Definition:** 'Key state' refers to the state recognized by the OS. Any key event sent to the OS via the Interception driver is considered a *software-level* event, even if initiated by a physical key press. This is a crucial concept for input handling in this project.
- **Structure:** The code is organized into classes and modules within the `pyinterceptor` package. It makes use of decorators, including a custom `@singleton` decorator.
- **Logging:** The standard `logging` module is used for logging messages.

## CI/CD

A GitHub Actions workflow is defined in `.github/workflows/publish.yml`. It automatically builds and publishes the package to PyPI whenever a new version tag (e.g., `v1.0.0`) is pushed to the `master` branch.

## Interaction Guidelines

- **Language:** All responses from the Gemini Code Assistant should be in Korean.