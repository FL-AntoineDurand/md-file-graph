# Installation Guide

Complete installation instructions for `md-file-graph`.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Feature-Specific Dependencies](#feature-specific-dependencies)
- [Verifying Installation](#verifying-installation)
- [Troubleshooting](#troubleshooting)
- [Upgrading](#upgrading)

## Prerequisites

### Required

1. **Python 3.8 or higher**
   ```bash
   python3 --version
   ```
   
   If not installed:
   - **Ubuntu/Debian:** `sudo apt-get install python3 python3-pip`
   - **macOS:** `brew install python3`
   - **Windows:** Download from https://www.python.org/downloads/

2. **pip** (Python package manager)
   ```bash
   pip3 --version
   ```

### Optional (Feature-Specific)

3. **GraphViz** (for graph visualization)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install graphviz
   ```
   
   **macOS:**
   ```bash
   brew install graphviz
   ```
   
   **Windows:**
   - Download from: https://graphviz.org/download/
   - Add GraphViz bin directory to your PATH
   - Restart terminal after installation

   **Verify:**
   ```bash
   dot -V
   ```

## Installation Methods

### Method 1: Install with pip (Recommended)

This installs all dependencies including HTML generation support:

```bash
# Clone or navigate to the repository
cd /path/to/md-file-graph

# Install in editable/development mode
pip3 install -e .
```

**Advantages:**
- ✅ Installs all dependencies automatically
- ✅ Command `md-file-graph` available globally
- ✅ Easy to update and develop

### Method 2: Using Virtual Environment (Best Practice)

Isolate dependencies in a virtual environment:

```bash
# Navigate to md-file-graph directory
cd /path/to/md-file-graph

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
# On Windows: venv\Scripts\activate

# Install the package
pip install -e .

# Verify
md-file-graph --help
```

**Advantages:**
- ✅ Isolated environment (no conflicts)
- ✅ Clean dependency management
- ✅ Easy to remove (just delete venv/)

### Method 3: Install from requirements.txt

Install dependencies without installing the package:

```bash
pip3 install -r requirements.txt

# Run using Python module syntax
python3 -m md_file_graph.cli --help
```

**Advantages:**
- ✅ Minimal installation
- ✅ Good for CI/CD environments

**Disadvantages:**
- ❌ No global `md-file-graph` command
- ❌ Must use `python3 -m md_file_graph.cli`

## Feature-Specific Dependencies

### Core Features (Always Installed)

```bash
click>=8.0.0          # CLI framework
markdown-it-py>=3.0.0 # Markdown parsing
```

### Graph Visualization

```bash
graphviz>=0.20.0      # Graph generation

# System dependency:
# Ubuntu/Debian: sudo apt-get install graphviz
# macOS: brew install graphviz
```

### HTML Generation (NEW!)

```bash
markdown>=3.5                # Markdown to HTML conversion
python-frontmatter>=1.0.0    # Frontmatter parsing
jinja2>=3.1.0                # HTML templating
beautifulsoup4>=4.12.0       # HTML manipulation
Pygments>=2.17.0             # Syntax highlighting
```

### Development Dependencies

```bash
pytest>=7.0.0         # Testing framework
pytest-cov>=4.0.0     # Code coverage
```

Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Verifying Installation

### Check Command Availability

```bash
md-file-graph --help
```

Expected output:
```
Usage: md-file-graph [OPTIONS] COMMAND [ARGS]...

  md-file-graph: Analyze and visualize markdown documentation.

Commands:
  graph  Analyze markdown files and generate a link graph visualization.
  html   Generate static HTML documentation site with SEO optimization.
```

### Test Graph Generation

```bash
# Try with example docs
md-file-graph graph ./example_docs -o ./test-output

# Check for output files
ls test-output/
# Should show: markdown_graph.dot, markdown_graph.svg
```

### Test HTML Generation

```bash
# Generate HTML from example docs
md-file-graph html ./example_docs \
    --output ./test-html \
    --base-url https://example.com

# Check for output
ls test-html/
# Should show: *.html, sitemap.xml, robots.txt
```

## Platform-Specific Notes

### Linux (Ubuntu/Debian)

```bash
# Install all system dependencies
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    graphviz

# Install md-file-graph
cd /path/to/md-file-graph
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### macOS

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python3 graphviz

# Install md-file-graph
cd /path/to/md-file-graph
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Windows

```powershell
# 1. Install Python from python.org
# 2. Install GraphViz from graphviz.org
# 3. Add GraphViz to PATH

# Install md-file-graph
cd C:\path\to\md-file-graph
python -m venv venv
venv\Scripts\activate
pip install -e .
```

## Docker Installation (Alternative)

If you prefer Docker:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Copy and install md-file-graph
COPY . /app/md-file-graph
WORKDIR /app/md-file-graph
RUN pip install -e .

ENTRYPOINT ["md-file-graph"]
```

Build and use:
```bash
docker build -t md-file-graph .
docker run md-file-graph --help
```

## Troubleshooting

### "command not found: md-file-graph"

**Cause:** Package not installed or not in PATH

**Solutions:**

1. **Check if installed:**
   ```bash
   pip3 list | grep md-file-graph
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Use Python module syntax:**
   ```bash
   python3 -m md_file_graph.cli --help
   ```

4. **Check PATH:**
   ```bash
   which md-file-graph
   echo $PATH
   ```

### "GraphViz executable not found"

**Cause:** GraphViz not installed or not in PATH

**Solutions:**

1. **Install GraphViz:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install graphviz
   
   # macOS
   brew install graphviz
   ```

2. **Verify installation:**
   ```bash
   dot -V
   which dot
   ```

3. **Add to PATH (Windows):**
   - Add `C:\Program Files\Graphviz\bin` to system PATH
   - Restart terminal

### "Missing required dependencies: markdown, python-frontmatter..."

**Cause:** HTML generation dependencies not installed

**Solution:**

```bash
# Install all dependencies
pip install markdown python-frontmatter jinja2 beautifulsoup4 Pygments

# Or reinstall package
pip install -e .
```

### "ImportError: No module named 'md_file_graph'"

**Cause:** Package not installed in current environment

**Solutions:**

1. **Install the package:**
   ```bash
   pip install -e .
   ```

2. **Check you're in the right directory:**
   ```bash
   pwd
   # Should be: /path/to/md-file-graph
   ```

3. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

### Permission Errors

**Cause:** Installing without proper permissions

**Solutions:**

1. **Use virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

2. **Install for user only:**
   ```bash
   pip install --user -e .
   ```

3. **Use sudo (not recommended):**
   ```bash
   sudo pip3 install -e .
   ```

### Python Version Issues

**Cause:** Python version < 3.8

**Solution:**

1. **Check Python version:**
   ```bash
   python3 --version
   ```

2. **Upgrade Python:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3.11
   
   # macOS
   brew install python@3.11
   ```

3. **Use specific Python version:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

## Upgrading

### Upgrade md-file-graph

```bash
# Navigate to repository
cd /path/to/md-file-graph

# Pull latest changes (if using git)
git pull

# Reinstall
pip install -e . --upgrade
```

### Upgrade Dependencies

```bash
# Upgrade all dependencies
pip install -r requirements.txt --upgrade

# Or specific package
pip install markdown --upgrade
```

## Uninstallation

### Uninstall Package

```bash
pip uninstall md-file-graph
```

### Remove Virtual Environment

```bash
# Deactivate first
deactivate

# Remove directory
rm -rf venv/
```

### Remove System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get remove graphviz

# macOS
brew uninstall graphviz
```

## Development Installation

For contributing to md-file-graph:

```bash
# Clone repository
git clone https://github.com/yourusername/md-file-graph.git
cd md-file-graph

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=md_file_graph
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test md-file-graph

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install system dependencies
        run: sudo apt-get install -y graphviz
      
      - name: Install md-file-graph
        run: pip install -e .
      
      - name: Test graph generation
        run: md-file-graph graph ./docs -o ./output
      
      - name: Test HTML generation
        run: |
          md-file-graph html ./docs \
            --output ./site \
            --base-url https://example.com
```

## Next Steps

After installation:

1. 📖 Read [QUICKSTART.md](QUICKSTART.md) for quick examples
2. 📚 Read [README.md](README.md) for complete documentation
3. 🧪 Try generating a graph: `md-file-graph graph ./example_docs`
4. 🌐 Try generating HTML: `md-file-graph html ./example_docs --output ./test --base-url https://example.com`
5. 🤝 Contribute: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Support

If you encounter issues:

1. Check this guide's [Troubleshooting](#troubleshooting) section
2. Check the [README.md](README.md) FAQ section
3. Search existing [GitHub Issues](https://github.com/yourusername/md-file-graph/issues)
4. Open a new issue with:
   - Your OS and Python version
   - Installation method used
   - Complete error message
   - Steps to reproduce
