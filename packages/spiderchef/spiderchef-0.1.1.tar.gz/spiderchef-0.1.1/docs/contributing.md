# Contributing to SpiderChef

Thank you for your interest in contributing to SpiderChef! This guide explains how to get started with contributing to the project.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/vonsteer/spiderchef.git
   cd spiderchef
   ```

3. Set up a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate
   ```

4. Install development dependencies:
   ```bash
   make dev
   ```

5. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

### Running Tests

SpiderChef uses pytest for testing:

```bash
# Run all tests + generate badges
make test
```

### Code Style

SpiderChef uses Ruff for code formatting and linting:

```bash
make style
```

### Type Checking

SpiderChef uses Pyright for type checking:

```bash
make typing
```

## Pull Request Guidelines

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with descriptive commit messages.

3. Update tests to cover your changes.

4. Update documentation if necessary.

5. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Open a pull request against the main repository.

## Adding New Features

### Adding a New Step Type

1. Create a new step class in the appropriate module under `spiderchef/steps/`.
2. Extend either `SyncStep` or `AsyncStep` depending on the nature of your step.
3. Implement the `_execute` method.
4. Register your step in `spiderchef/steps/__init__.py`.
5. Add tests for your new step.
6. Update documentation.

Example:

```python
from spiderchef import SyncStep, Recipe
from typing import Any

class MyNewStep(SyncStep):
    my_param: str
    optional_param: int = 10
    
    def _execute(self, recipe: Recipe, previous_output: Any = None) -> Any:
        # Implement step logic here
        return f"{self.my_param} processed with {self.optional_param}"
```

### Improving Existing Features

When improving existing features:

1. Maintain backward compatibility when possible.
2. Add tests for the new functionality.
3. Update documentation to reflect changes.

## Documentation

SpiderChef uses MkDocs with the Material theme for documentation:

1. Documentation source is in the `docs/` directory.
2. To build and preview documentation locally:
   ```bash
   make docs
   ```
3. Open http://127.0.0.1:8000/ in your browser to preview the docs.

## Release Process

1. Create a new release on GitHub
2. The CI pipeline will automatically publish to PyPI + bump the version

## Getting Help

If you need help or have questions about contributing:

1. Open an issue on GitHub
2. Refer to the existing documentation
3. Contact the maintainers

## Code of Conduct

Please be respectful and considerate of others when contributing to SpiderChef. We strive to maintain a welcoming and inclusive community.
