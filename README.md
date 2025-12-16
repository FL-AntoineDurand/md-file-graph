# md-file-graph

A tool to analyze markdown files and visualize their link structure as a graph.

## Features

- 📁 Recursively scans directories for markdown files
- 🔗 Extracts all internal (file) and external (URL) links
- 📊 Generates graph representation with files as nodes and links as edges
- 🎨 Produces beautiful SVG visualizations using GraphViz
- 📝 Tracks link text and line numbers for each connection
- 🚫 Automatically excludes common third-party directories (node_modules, vendor, etc.)
- 📋 Respects .gitignore files to focus on your actual documentation
- ⚙️ Configurable exclusion patterns

## Installation

```bash
pip install -e .
```

### Prerequisites

You need to have GraphViz installed on your system:

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Windows:**
Download from https://graphviz.org/download/

## Usage

### Basic Usage

Analyze a directory and generate a graph:

```bash
md-file-graph /path/to/markdown/folder
```

This will create two files in the current directory:
- `markdown_graph.dot` - GraphViz DOT format representation
- `markdown_graph.svg` - SVG visualization

### Advanced Options

```bash
# Specify output directory
md-file-graph /path/to/markdown/folder -o ./output

# Custom output filename
md-file-graph /path/to/markdown/folder -n my_graph

# Include external URLs in the graph
md-file-graph /path/to/markdown/folder --include-external

# Show only files with links (hide isolated nodes)
md-file-graph /path/to/markdown/folder --hide-isolated
```

### Full Command-Line Options

```
Usage: md-file-graph [OPTIONS] DIRECTORY

  Analyze markdown files and generate a link graph visualization.

Options:
  -o, --output PATH          Output directory for generated files (default: current directory)
  -n, --name TEXT            Base name for output files (default: markdown_graph)
  --include-external         Include external URLs as nodes in the graph
  --hide-isolated            Hide markdown files with no links
  --no-gitignore             Do not respect .gitignore files (include all files)
  --no-default-excludes      Do not exclude common directories like node_modules
  --help                     Show this message and exit
```

### Default Excluded Directories

By default, the tool excludes these common third-party directories:
- `node_modules` (JavaScript/Node.js)
- `vendor` (PHP, Go)
- `venv`, `env`, `.venv` (Python virtual environments)
- `target` (Rust, Java)
- `build`, `dist` (Build outputs)
- `.git`, `.svn`, `.hg` (Version control)
- `__pycache__`, `.pytest_cache`, `.mypy_cache` (Python caches)
- And 10+ more common patterns

Use `--no-default-excludes` to disable this filtering.

## Example Output

Given a directory structure like:

```
docs/
├── index.md          (links to guide.md and api.md)
├── guide.md          (links to api.md)
└── api.md            (links to https://example.com)
```

The tool generates a visual graph showing these relationships, with:
- Nodes representing each markdown file
- Directed edges showing links between files
- Edge labels showing the link text and line number

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd md-file-graph

# Install in development mode
pip install -e .
```

### Running Tests

```bash
python -m pytest tests/
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

