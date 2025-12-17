# Quick Start Guide

Get up and running with `md-file-graph` in minutes!

## What is md-file-graph?

A powerful tool that:
- 📊 **Analyzes** markdown documentation structure
- 🎨 **Visualizes** link relationships as beautiful graphs
- 🌐 **Generates** SEO-optimized static HTML documentation sites

## Installation

### 1. Install Prerequisites

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install graphviz python3-pip
```

**macOS:**
```bash
brew install graphviz python3
```

**Windows:**
- Download GraphViz from: https://graphviz.org/download/
- Install Python from: https://www.python.org/downloads/

### 2. Install md-file-graph

```bash
# Option A: With virtual environment (recommended)
cd /root/workspace/md-file-graph
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .

# Option B: Direct install
pip3 install -e .
```

### 3. Verify Installation

```bash
md-file-graph --help
```

You should see:
```
Usage: md-file-graph [OPTIONS] COMMAND [ARGS]...

  md-file-graph: Analyze and visualize markdown documentation.

Commands:
  graph  Analyze markdown files and generate a link graph visualization.
  html   Generate static HTML documentation site with SEO optimization.
```

## Quick Examples

### Example 1: Visualize Documentation Structure

```bash
# Analyze your markdown files and create a visual graph
md-file-graph graph ./docs

# Output:
# - markdown_graph.dot (graph data)
# - markdown_graph.svg (visual graph - open in browser!)
```

**What you'll see:**
- 📄 **Blue boxes** = Existing markdown files
- 🔴 **Red boxes** = Referenced but missing files
- ⚡ **Arrows** = Links between files
- 🏷️ **Labels** = Link text and line number

### Example 2: Generate Static HTML Documentation

```bash
# Generate SEO-optimized HTML documentation
md-file-graph html ./docs \
    --output ./website \
    --base-url https://example.com

# Output:
# - website/*.html (one page per markdown file)
# - website/sitemap.xml (for search engines)
# - website/robots.txt (for web crawlers)
```

**What you get:**
- ✅ Individual HTML page for each markdown file
- ✅ Full SEO optimization (meta tags, Open Graph, Twitter Cards)
- ✅ Structured data (JSON-LD) for rich snippets
- ✅ Automatic sitemap.xml generation
- ✅ Pre-rendered content for instant loading

## Command Overview

```bash
# Graph visualization
md-file-graph graph [OPTIONS] DIRECTORY

# HTML generation
md-file-graph html [OPTIONS] DIRECTORY
```

## Common Use Cases

### Use Case 1: Documentation Audit

Find broken links and orphaned pages:

```bash
# Create graph showing all links
md-file-graph graph ./docs --include-external

# Open the SVG and look for:
# - Red boxes (broken links)
# - Isolated nodes (orphaned pages)
```

### Use Case 2: Generate Documentation Website

Create a full documentation site:

```bash
# Step 1: Generate HTML
md-file-graph html ./docs \
    --output ./static \
    --base-url https://docs.myproject.com

# Step 2: Customize (optional)
# - Edit the HTML template
# - Add custom styles

# Step 3: Deploy
# - Upload ./static to your web server
# - Submit sitemap to Google Search Console
```

### Use Case 3: Documentation Structure Analysis

Understand your documentation hierarchy:

```bash
# Create clean graph without external links
md-file-graph graph ./docs \
    --hide-isolated \
    -o ./analysis

# Review the SVG to understand:
# - Documentation flow
# - Highly connected pages
# - Documentation gaps
```

## Advanced Options

### Graph Visualization Options

```bash
# Include external URLs
md-file-graph graph ./docs --include-external

# Hide files with no links
md-file-graph graph ./docs --hide-isolated

# Custom output location and name
md-file-graph graph ./docs -o ./output -n my_graph

# Include gitignored files
md-file-graph graph ./docs --no-gitignore
```

### HTML Generation Options

```bash
# With custom template
md-file-graph html ./docs \
    --output ./site \
    --base-url https://example.com \
    --template custom-template.html

# With configuration file
md-file-graph html ./docs \
    --output ./site \
    --base-url https://example.com \
    --config docs-config.json
```

## Custom HTML Template

Create a `template.html` file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
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
    <article>
        {{ content|safe }}
    </article>
</body>
</html>
```

Then use it:
```bash
md-file-graph html ./docs \
    --output ./site \
    --base-url https://example.com \
    --template template.html
```

## Markdown Frontmatter

Add metadata to your markdown files:

```markdown
---
title: Custom Page Title
description: SEO description for this page
keywords: [documentation, guide, tutorial]
date: 2024-12-17
---

# Your Content Here

The rest of your markdown...
```

If you don't add frontmatter, metadata is automatically extracted from:
- **Title**: First H1 heading or filename
- **Description**: First paragraph of content
- **Keywords**: Extracted from headings and content

## Example: Complete Documentation Pipeline

```bash
# 1. Analyze structure
md-file-graph graph ./docs -o ./analysis

# 2. Review the SVG graph
open ./analysis/markdown_graph.svg

# 3. Fix any broken links you found

# 4. Generate HTML site
md-file-graph html ./docs \
    --output ./website \
    --base-url https://docs.myproject.com \
    --template custom-template.html

# 5. Test locally
cd website
python3 -m http.server 8000
# Visit http://localhost:8000

# 6. Deploy
rsync -avz ./website/ user@server:/var/www/docs/

# 7. Submit sitemap
# Go to Google Search Console
# Submit: https://docs.myproject.com/sitemap.xml
```

## Troubleshooting

### "command not found: md-file-graph"

Try these solutions:
```bash
# Solution 1: Activate virtual environment
source venv/bin/activate

# Solution 2: Use Python module syntax
python3 -m md_file_graph.cli --help

# Solution 3: Check pip's bin directory is in PATH
echo $PATH
```

### "GraphViz executable not found"

```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz

# Verify installation
dot -V
```

### "Missing required dependencies"

For HTML generation, you need additional packages:
```bash
pip install markdown python-frontmatter jinja2 beautifulsoup4 Pygments
```

Or install everything:
```bash
pip install -e .
```

### Generated HTML missing styles

The HTML pages reference your CSS files. Make sure to:
```bash
# Copy your CSS to the output directory
cp styles.css ./website/
```

## Real-World Examples

### Example 1: Open Source Project Documentation

```bash
# Generate documentation for your GitHub project
md-file-graph html /path/to/your/repo \
    --output ./docs-site \
    --base-url https://yourproject.github.io

# Deploy to GitHub Pages
cd docs-site
git init
git add .
git commit -m "Documentation"
git push origin gh-pages
```

### Example 2: Company Internal Documentation

```bash
# Create internal docs with custom branding
md-file-graph html ./company-docs \
    --output ./intranet/docs \
    --base-url https://intranet.company.com \
    --template company-template.html
```

### Example 3: API Documentation

```bash
# Generate API docs with structure analysis
md-file-graph graph ./api-docs --include-external
md-file-graph html ./api-docs \
    --output ./api-website \
    --base-url https://api.example.com
```

## What's Next?

- 📖 Read the full [README.md](README.md) for complete documentation
- 🔧 Check [INSTALL.md](INSTALL.md) for detailed installation options
- 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- 🎨 Explore custom templates and styling
- 🚀 Deploy your documentation site

## SEO Benefits

When you generate HTML with md-file-graph:

✅ **Search Engine Optimization**
- Every page has unique meta tags
- Structured data for rich snippets
- Automatic sitemap.xml
- Fast page loads (pre-rendered)

✅ **Social Media Integration**
- Open Graph tags (Facebook, LinkedIn)
- Twitter Card tags
- Custom preview images

✅ **Professional Results**
- Clean, semantic HTML
- Responsive by default
- Works without JavaScript
- Accessible to all users

Happy documenting! 🎉
