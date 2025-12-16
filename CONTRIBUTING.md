# Contributing to md-file-graph

Thank you for your interest in contributing to md-file-graph! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Development Workflow

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and write tests
3. Run the tests:
   ```bash
   pytest tests/
   ```

4. Commit your changes with clear, descriptive commit messages
5. Push to your fork and submit a pull request

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise

## Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting a PR
- Aim for good test coverage

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed

## Reporting Issues

- Use the GitHub issue tracker
- Provide a clear description of the problem
- Include steps to reproduce
- Mention your environment (OS, Python version, etc.)

## License

By contributing to md-file-graph, you agree that your contributions will be licensed under the GNU General Public License v3.0.

