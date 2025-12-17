  # md-file-graph

A tool to analyze markdown files, visualize their link structure, and generate static HTML documentation sites with full SEO optimization.

## Features

### Documentation Analysis
- 📁 Recursively scans directories for markdown files
- 🔗 Extracts all internal (file) and external (URL) links
- 📊 Generates graph representation with files as nodes and links as edges
- 🎨 Produces beautiful SVG visualizations using GraphViz
- 📝 Tracks link text and line numbers for each connection
- 🚫 Automatically excludes common third-party directories (node_modules, vendor, etc.)
- 📋 Respects .gitignore files to focus on your actual documentation
- ⚙️ Configurable exclusion patterns

### Static HTML Generation (NEW!)
- 🌐 Generates SEO-optimized static HTML documentation site
- 🎯 Full meta tags (title, description, keywords, Open Graph, Twitter Cards)
- 📊 Structured data (JSON-LD) for rich snippets in search results
- 🗺️ **Navigation menu** (docs.json with hierarchical structure)
- 📷 **Automatic image handling** (copies images, rewrites paths)
- 🗺️ Automatic sitemap.xml generation
- 🤖 Robots.txt for search engine crawlers
- 📱 Responsive HTML with custom templates
- ⚡ Pre-rendered pages for instant loading
- 🔍 Excellent SEO and social media integration

## Installation

```bash
pip install -e .
```

### Prerequisites

**For graph visualization:**
You need GraphViz installed on your system:

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

### Command Overview

```bash
md-file-graph --help

# Available commands:
md-file-graph graph    # Analyze and visualize documentation structure
md-file-graph html     # Generate static HTML documentation site
```

### 1. Graph Visualization

Analyze markdown files and generate a link graph:

```bash
# Basic usage
md-file-graph graph /path/to/markdown/folder

# Specify output directory
md-file-graph graph /path/to/markdown/folder -o ./output

# Custom output filename
md-file-graph graph /path/to/markdown/folder -n my_graph

# Include external URLs in the graph
md-file-graph graph /path/to/markdown/folder --include-external

# Show only files with links (hide isolated nodes)
md-file-graph graph /path/to/markdown/folder --hide-isolated
```

**Output:**
- `markdown_graph.dot` - GraphViz DOT format representation
- `markdown_graph.svg` - SVG visualization

**Graph Options:**
```
Usage: md-file-graph graph [OPTIONS] DIRECTORY

Options:
  -o, --output PATH          Output directory (default: current directory)
  -n, --name TEXT            Base name for output files (default: markdown_graph)
  --include-external         Include external URLs as nodes
  --hide-isolated            Hide markdown files with no links
  --no-gitignore             Do not respect .gitignore files
  --no-default-excludes      Do not exclude common directories
  --help                     Show this message and exit
```

### 2. Static HTML Generation

Generate a complete static documentation website:

```bash
# Basic usage
md-file-graph html /path/to/docs \
    --output ./static \
    --base-url https://example.com

# With custom template
md-file-graph html /path/to/docs \
    --output ./static \
    --base-url https://example.com \
    --template custom-template.html

# With configuration file
md-file-graph html /path/to/docs \
    --output ./static \
    --base-url https://example.com \
    --config docs-config.json
```

**Output Structure:**
```
static/
├── *.html           # HTML pages for each markdown file
├── docs.json        # Navigation structure (hierarchical)
├── assets/          # Copied images from markdown files
├── sitemap.xml      # Sitemap for search engines
└── robots.txt       # Robots directives
```

**HTML Generation Options:**
```
Usage: md-file-graph html [OPTIONS] DIRECTORY

Options:
  -o, --output PATH        Output directory [required]
  --base-url TEXT          Base URL (e.g., https://example.com) [required]
  --template PATH          Path to custom Jinja2 template
  --config PATH            Path to configuration JSON file
  --no-gitignore           Do not respect .gitignore files
  --no-default-excludes    Do not exclude common directories
  --help                   Show this message and exit
```

### HTML Template

You can provide a custom Jinja2 template with these variables:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ metadata.title }}</title>
    <meta name="description" content="{{ metadata.description }}">
    <meta name="keywords" content="{{ keywords }}">
    <link rel="canonical" href="{{ canonical_url }}">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{ structured_data }}
    </script>
</head>
<body>
    {{ content|safe }}
</body>
</html>
```

**Available template variables:**
- `metadata.title` - Document title
- `metadata.description` - Document description
- `metadata.keywords` - List of keywords
- `metadata.author` - Author name
- `metadata.date_modified` - Last modification date
- `keywords` - Comma-separated keywords string
- `canonical_url` - Full URL for the page
- `base_url` - Base URL of the site
- `structured_data` - JSON-LD structured data
- `content` - Rendered HTML content

### Frontmatter Support

Add metadata to your markdown files:

```markdown
---
title: My Custom Title
description: A brief description for SEO
keywords: [keyword1, keyword2, keyword3]
date: 2024-12-17
---

# Your Content Here
```

If no frontmatter is provided, metadata is automatically extracted from:
- Title: First H1 heading or filename
- Description: First paragraph
- Keywords: Headings and content analysis

### Default Excluded Directories

By default, the tool excludes these common directories:
- `node_modules` (JavaScript/Node.js)
- `vendor` (PHP, Go)
- `venv`, `env`, `.venv` (Python virtual environments)
- `target` (Rust, Java)
- `build`, `dist` (Build outputs)
- `.git`, `.svn`, `.hg` (Version control)
- `__pycache__`, `.pytest_cache`, `.mypy_cache` (Python caches)
- And 10+ more common patterns

Use `--no-default-excludes` to disable this filtering.

## Example Workflows

### Complete Documentation Pipeline

```bash
# 1. Visualize documentation structure
md-file-graph graph ./docs -o ./analysis --hide-isolated

# 2. Generate static HTML site
md-file-graph html ./docs \
    --output ./website \
    --base-url https://docs.example.com \
    --template custom-template.html

# 3. Deploy
rsync -avz ./website/ user@server:/var/www/docs/
```

### SEO-Optimized Documentation

```bash
# Generate with full SEO
md-file-graph html ./documentation \
    --output ./public \
    --base-url https://example.com

# Generated pages include:
# - Primary meta tags (title, description, keywords)
# - Open Graph tags (Facebook, LinkedIn)
# - Twitter Card tags
# - Structured data (JSON-LD)
# - Sitemap.xml
# - Robots.txt
```

## SEO Features

Every generated HTML page includes:

### Primary Meta Tags
```html
<title>Page Title - Site Name</title>
<meta name="description" content="...">
<meta name="keywords" content="...">
<meta name="robots" content="index, follow">
<link rel="canonical" href="...">
```

### Social Media Tags
```html
<!-- Open Graph (Facebook, LinkedIn) -->
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:url" content="...">

<!-- Twitter Cards -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:title" content="...">
```

### Structured Data
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "...",
  "description": "...",
  "author": {...},
  "dateModified": "..."
}
</script>
```

## Example Output

### Graph Visualization

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
- Color coding (blue for existing files, red for broken links)

### HTML Documentation

Input: `docs/` directory with markdown files

Output: `static/` directory with:
- Individual HTML pages for each markdown file
- Full SEO optimization
- Sitemap.xml listing all pages
- Robots.txt for search engines

## Integration Example

Use in your project's build process:

```bash
#!/bin/bash
# build-docs.sh

# Generate documentation
md-file-graph html ./docs \
    --output ./dist/docs \
    --base-url https://example.com \
    --template ./templates/doc-page.html

# Copy assets
cp -r ./assets/* ./dist/docs/

# Deploy
aws s3 sync ./dist/docs s3://my-bucket/docs/
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd md-file-graph

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .
```

### Running Tests

```bash
python -m pytest tests/
```

## Dependencies

### Core
- `click>=8.0.0` - CLI framework
- `markdown-it-py>=3.0.0` - Markdown parsing

### Graph Visualization
- `graphviz>=0.20.0` - Graph generation

### HTML Generation
- `markdown>=3.5` - Markdown to HTML conversion
- `python-frontmatter>=1.0.0` - Frontmatter parsing
- `jinja2>=3.1.0` - HTML templating
- `beautifulsoup4>=4.12.0` - HTML manipulation
- `Pygments>=2.17.0` - Syntax highlighting

## Use Cases

1. **Documentation Maintenance**
   - Find broken links in your documentation
   - Visualize documentation structure
   - Identify orphaned pages

2. **Static Site Generation**
   - Generate SEO-optimized documentation websites
   - Create searchable documentation
   - Build with custom templates

3. **Documentation Analysis**
   - Understand documentation complexity
   - Find documentation gaps
   - Plan documentation restructuring

4. **CI/CD Integration**
   - Validate documentation links
   - Auto-generate documentation sites
   - Check documentation coverage

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

### v0.2.0 (Current)
- ✨ Added static HTML generation with SEO optimization
- ✨ Added frontmatter support
- ✨ Added sitemap and robots.txt generation
- ✨ Added custom template support
- ✨ Restructured CLI with subcommands (graph, html)

### v0.1.0
- Initial release with graph visualization
- Markdown file discovery
- Link extraction
- SVG graph generation
