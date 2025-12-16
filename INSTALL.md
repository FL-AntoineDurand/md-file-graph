# Installation Guide

## Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python3 --version
   ```

2. **GraphViz** (required for SVG generation)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install graphviz python3-pip
   ```
   
   **macOS:**
   ```bash
   brew install graphviz
   brew install python3
   ```
   
   **Windows:**
   - Download GraphViz from: https://graphviz.org/download/
   - Add GraphViz to your PATH
   - Install Python from: https://www.python.org/downloads/

## Installation Methods

### Method 1: Install from source (Recommended)

```bash
# Clone the repository
cd /path/to/md-file-graph

# Install in development mode
pip3 install -e .
```

### Method 2: Install from requirements.txt

```bash
pip3 install -r requirements.txt

# Then you can run the tool using:
python3 -m md_file_graph.cli <directory>
```

### Method 3: Using a virtual environment (Best practice)

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Verifying Installation

After installation, verify it works:

```bash
md-file-graph --help
```

You should see the usage information.

## Troubleshooting

### "command not found: md-file-graph"

If you installed in a virtual environment, make sure it's activated. Otherwise, try:
```bash
python3 -m md_file_graph.cli --help
```

### "GraphViz executable not found"

Make sure GraphViz is installed and in your system PATH:
```bash
# Test if dot command is available
dot -V
```

### Import errors

Make sure all dependencies are installed:
```bash
pip3 install -r requirements.txt
```

