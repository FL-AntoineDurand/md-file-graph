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

4. Test your changes manually:
   ```bash
   # Test graph generation
   md-file-graph graph ./example_docs -o ./test-output
   
   # Test HTML generation
   md-file-graph html ./example_docs \
       --output ./test-html \
       --base-url https://example.com
   ```

5. Commit your changes with clear, descriptive commit messages
6. Push to your fork and submit a pull request

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise

## Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting a PR
- Aim for good test coverage

## Project Structure

```
md-file-graph/
├── src/md_file_graph/
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # CLI commands (graph, html)
│   ├── parser.py           # Markdown parsing and link extraction
│   ├── graph.py            # Graph building and visualization
│   └── html_generator.py   # HTML generation with SEO
├── tests/                  # Test files
├── example_docs/           # Example documentation for testing
├── requirements.txt        # Python dependencies
├── requirements-dev.txt    # Development dependencies
├── pyproject.toml          # Package configuration
├── setup.py                # Setup script
├── README.md               # Main documentation
├── QUICKSTART.md           # Quick start guide
├── INSTALL.md              # Installation instructions
├── CHANGELOG.md            # Version history
└── CONTRIBUTING.md         # This file
```

## Adding New Features

### Graph Visualization Features

Edit `src/md_file_graph/graph.py`:
- Modify `GraphBuilder` class for new graph features
- Update DOT generation in `generate_dot()` method
- Add new options to CLI in `cli.py`

### HTML Generation Features

Edit `src/md_file_graph/html_generator.py`:
- Modify `HTMLGenerator` class for new HTML features
- Update template rendering in `generate_page()` method
- Add new metadata extraction in `extract_metadata()` method
- Update CLI options in `cli.py`

### Parser Features

Edit `src/md_file_graph/parser.py`:
- Modify `MarkdownParser` class
- Update link extraction in `extract_links()` method
- Add new exclusion patterns to `DEFAULT_EXCLUDE_DIRS`

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure all tests pass
- Test both `graph` and `html` commands if applicable
- Update documentation (README.md, QUICKSTART.md, etc.)
- Update documentation if needed

## Reporting Issues

- Use the GitHub issue tracker
- Provide a clear description of the problem
- Include steps to reproduce
- Mention your environment (OS, Python version, etc.)

## License

By contributing to md-file-graph, you agree that your contributions will be licensed under the GNU General Public License v3.0.

