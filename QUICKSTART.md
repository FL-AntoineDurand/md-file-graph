# Quick Start Guide

Get up and running with `md-file-graph` in minutes!

## Installation

### 1. Install Prerequisites

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install graphviz python3-pip
```

**macOS:**
```bash
brew install graphviz
```

### 2. Install md-file-graph

```bash
cd /root/workspace/md-file-graph
pip3 install -e .
```

Or without installation:
```bash
pip3 install -r requirements.txt
```

## Quick Example

Try it with the included example documentation:

```bash
# If installed via pip
md-file-graph ./example_docs

# Or run directly
python3 -m md_file_graph.cli ./example_docs
```

This will generate:
- `markdown_graph.dot` - Graph in DOT format
- `markdown_graph.svg` - Visual graph (open in browser)

## Basic Usage

```bash
# Analyze any markdown directory
md-file-graph /path/to/your/docs

# Custom output location
md-file-graph /path/to/docs -o ./output

# Custom filename
md-file-graph /path/to/docs -n my_docs_graph

# Include external URLs in graph
md-file-graph /path/to/docs --include-external

# Hide files with no links
md-file-graph /path/to/docs --hide-isolated
```

## Viewing the Output

1. **SVG File**: Open the `.svg` file in any web browser
2. **DOT File**: View/edit with GraphViz tools or text editor

## What You'll See

The generated graph shows:
- 📄 **Blue boxes** = Existing markdown files
- 🔴 **Red boxes** = Referenced but missing files
- ⚡ **Arrows** = Links between files
- 🏷️ **Labels** = Link text and line number

## Example Output

Given this file structure:
```
docs/
├── index.md          → links to guide.md, api.md
├── guide.md          → links to api.md
└── api.md            → links to https://example.com
```

You'll get a visual graph showing all these connections!

## Troubleshooting

**"command not found: md-file-graph"**
- Use: `python3 -m md_file_graph.cli` instead
- Or make sure pip's bin directory is in your PATH

**"GraphViz executable not found"**
- Install GraphViz: `sudo apt-get install graphviz` (Ubuntu)
- Verify: `dot -V` should show the version

## Next Steps

- Read the full [README.md](README.md)
- Check [INSTALL.md](INSTALL.md) for detailed installation
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Real-World Use Cases

- 📚 Visualize documentation structure
- 🔍 Find broken links in your markdown docs
- 🗺️ Understand complex documentation hierarchies
- 📊 Generate documentation maps for wikis
- ✅ Validate documentation completeness

Happy graphing! 🎉

