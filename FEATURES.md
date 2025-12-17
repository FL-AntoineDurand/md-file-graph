# md-file-graph Features

Complete overview of all features in md-file-graph.

## Core Features

### 1. Markdown Analysis

**Discover and analyze markdown files throughout your project:**

- ✅ Recursive directory scanning
- ✅ Respects .gitignore files
- ✅ Excludes common directories (node_modules, venv, build, etc.)
- ✅ Configurable exclusion patterns
- ✅ Fast scanning even on large repositories

**Example:**
```bash
md-file-graph graph ./docs
```

### 2. Link Extraction

**Extract and track all links in your markdown files:**

- ✅ Internal links (to other markdown files)
- ✅ External links (URLs)
- ✅ Tracks link text and line numbers
- ✅ Resolves relative paths
- ✅ Handles anchor links
- ✅ Identifies broken links

**Link Types Detected:**
- `[text](file.md)` - Relative file links
- `[text](../docs/file.md)` - Parent directory links
- `[text](/path/to/file.md)` - Absolute path links
- `[text](https://example.com)` - External URLs

### 3. Graph Visualization 📊

**Visualize your documentation structure:**

- ✅ DOT format generation (GraphViz)
- ✅ SVG visualization (beautiful, interactive)
- ✅ Color-coded nodes:
  - 🔵 Blue: Existing files
  - 🔴 Red: Missing/broken links
  - 🟡 Yellow: External URLs (optional)
- ✅ Edge labels with link text and line numbers
- ✅ Hide isolated nodes (optional)
- ✅ Include/exclude external URLs

**Example:**
```bash
md-file-graph graph ./docs \
    --output ./analysis \
    --include-external \
    --hide-isolated
```

**Output:**
- `markdown_graph.dot` - Graph data in DOT format
- `markdown_graph.svg` - Visual graph (open in browser)

### 4. Static HTML Generation 🌐

**Generate SEO-optimized static HTML documentation:**

- ✅ Individual HTML page for each markdown file
- ✅ Preserves directory structure
- ✅ Complete SEO optimization
- ✅ **Navigation menu generation** (docs.json)
- ✅ **Automatic image handling** (copy & rewrite paths)
- ✅ Responsive HTML output
- ✅ Custom Jinja2 templates
- ✅ Automatic sitemap.xml generation
- ✅ Robots.txt generation

**Example:**
```bash
md-file-graph html ./docs \
    --output ./website \
    --base-url https://docs.example.com \
    --template custom-template.html
```

**Output:**
- `*.html` - One page per markdown file
- `docs.json` - Hierarchical navigation structure
- `assets/` - Copied images from markdown files
- `sitemap.xml` - For search engines
- `robots.txt` - For web crawlers

### 5. Navigation Generation 🗺️

**Automatic hierarchical navigation structure:**

- ✅ Generates `docs.json` with complete document tree
- ✅ Organized by directory structure
- ✅ Includes titles, paths, URLs for each document
- ✅ Hierarchical levels (root, subdirectories)
- ✅ Ready for JavaScript consumption
- ✅ No configuration required

**docs.json Structure:**
```json
{
  "generated": "2025-12-17T14:44:16.343849",
  "base_url": "https://docs.example.com",
  "sections": [
    {
      "title": "Root",
      "items": [
        {
          "title": "Getting Started",
          "path": "README.html",
          "url": "https://docs.example.com/README.html",
          "level": 0
        }
      ]
    },
    {
      "title": "Guides",
      "items": [
        {
          "title": "Installation Guide",
          "path": "guides/INSTALL.html",
          "url": "https://docs.example.com/guides/INSTALL.html",
          "level": 1
        }
      ]
    }
  ]
}
```

### 6. Image Handling 📷

**Automatic image copying and path rewriting:**

- ✅ Finds all images referenced in markdown
- ✅ Copies images to `assets/` directory
- ✅ Rewrites image paths in generated HTML
- ✅ Handles relative paths from any location
- ✅ Supports both source-relative and repo-root paths
- ✅ Prevents duplicate copies
- ✅ Name collision handling

**Supported Image References:**
```markdown
![Logo](./logo.png)              # Relative to markdown file
![Logo](../images/logo.png)      # Parent directory
![Logo](website/logo.png)        # Repo root relative
```

**Result:**
- Images copied to `output/assets/`
- Paths rewritten: `<img src="assets/website_logo.png">`
- Original images remain untouched

## SEO Features

### Meta Tags (Every Page)

**Primary Meta Tags:**
```html
<title>Page Title - Site Name</title>
<meta name="description" content="...">
<meta name="keywords" content="...">
<meta name="author" content="...">
<meta name="robots" content="index, follow">
<link rel="canonical" href="...">
```

**Open Graph (Social Media):**
```html
<meta property="og:type" content="article">
<meta property="og:url" content="...">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="...">
<meta property="og:site_name" content="...">
```

**Twitter Cards:**
```html
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="...">
<meta property="twitter:title" content="...">
<meta property="twitter:description" content="...">
<meta property="twitter:image" content="...">
```

### Structured Data (JSON-LD)

Every page includes Schema.org structured data:

```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "...",
  "description": "...",
  "author": {...},
  "publisher": {...},
  "dateModified": "...",
  "keywords": "..."
}
```

**Benefits:**
- Rich snippets in search results
- Better search engine understanding
- Higher click-through rates

### Sitemap Generation

Automatic sitemap.xml with:
- All documentation pages
- Last modification dates
- Update frequency hints
- Priority values

### Robots.txt

Generated robots.txt with:
- Allow all crawlers
- Sitemap location
- Custom directives (configurable)

## Markdown Processing

### Supported Extensions

- ✅ Fenced code blocks with syntax highlighting
- ✅ Tables (GitHub-flavored markdown)
- ✅ Table of contents generation
- ✅ Newline to `<br>` conversion
- ✅ Sane lists (proper nesting)
- ✅ Attribute lists

### Code Highlighting

Uses Pygments for syntax highlighting:
- 500+ languages supported
- Multiple themes available
- Inline and block code
- Language auto-detection

### Link Conversion

Automatically converts markdown links to HTML:
- `[text](file.md)` → `<a href="file.html">text</a>`
- `[text](../doc.md)` → `<a href="../doc.html">text</a>`
- Preserves external URLs
- Handles anchor links

## Metadata Extraction

### Frontmatter Support

Parse YAML frontmatter from markdown files:

```markdown
---
title: Custom Title
description: SEO description
keywords: [seo, docs, tutorial]
author: John Doe
date: 2024-12-17
---

# Your Content
```

**Supported Fields:**
- `title` - Page title
- `description` - Meta description
- `keywords` - Array or comma-separated list
- `author` - Author name
- `date` - Publication/modification date

### Auto-Extraction

If no frontmatter is provided, automatically extracts:

**Title:**
1. First H1 heading in content
2. Filename (cleaned and formatted)

**Description:**
1. First paragraph of content
2. Skips HTML blocks, images, badges
3. Cleans markdown formatting
4. Limits to 300 characters

**Keywords:**
1. Words from title (> 3 characters)
2. Words from H2-H3 headings
3. Content analysis
4. Limits to 15 keywords

## Template System

### Custom Templates

Use Jinja2 templates for complete customization:

**Available Variables:**
- `metadata.title` - Document title
- `metadata.description` - Description
- `metadata.keywords` - List of keywords
- `metadata.author` - Author name
- `metadata.date_modified` - Last modified date
- `keywords` - Comma-separated keywords string
- `canonical_url` - Full URL for the page
- `base_url` - Base URL of the site
- `structured_data` - JSON-LD structured data
- `content` - Rendered HTML content

**Example Template:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ metadata.title }}</title>
    <meta name="description" content="{{ metadata.description }}">
    <link rel="canonical" href="{{ canonical_url }}">
    <script type="application/ld+json">{{ structured_data }}</script>
</head>
<body>
    <article>{{ content|safe }}</article>
</body>
</html>
```

### Default Template

If no template is provided, uses a clean default template with:
- Semantic HTML5
- Minimal, professional styling
- Responsive design
- All SEO tags included

## CLI Features

### Command Structure

```bash
md-file-graph [OPTIONS] COMMAND [ARGS]...

Commands:
  graph  # Analyze and visualize
  html   # Generate static HTML
```

### Graph Command Options

```bash
md-file-graph graph [OPTIONS] DIRECTORY

Options:
  -o, --output PATH          Output directory
  -n, --name TEXT            Base name for output files
  --include-external         Include external URLs
  --hide-isolated            Hide files with no links
  --no-gitignore             Include gitignored files
  --no-default-excludes      Include default excluded dirs
  --help                     Show help
```

### HTML Command Options

```bash
md-file-graph html [OPTIONS] DIRECTORY

Options:
  -o, --output PATH          Output directory [required]
  --base-url TEXT            Base URL [required]
  --template PATH            Custom Jinja2 template
  --config PATH              Configuration JSON file
  --no-gitignore             Include gitignored files
  --no-default-excludes      Include default excluded dirs
  --help                     Show help
```

## Performance Features

### Efficient Scanning

- Iterative directory traversal
- Early exclusion of ignored paths
- Caches .gitignore patterns
- Minimal memory footprint

### Smart Processing

- Processes files only once
- Reuses markdown parser
- Efficient regex matching
- Batch operations

### Scalability

Tested on repositories with:
- ✅ 1000+ markdown files
- ✅ 10,000+ links
- ✅ Deep directory structures
- ✅ Complex link patterns

## Default Exclusions

Automatically excludes common directories:

**Package Managers:**
- `node_modules` (JavaScript/Node.js)
- `vendor` (PHP, Go)
- `Pods` (iOS CocoaPods)

**Virtual Environments:**
- `venv`, `env`, `.venv`, `ENV` (Python)
- `virtualenv`

**Build Outputs:**
- `target` (Rust, Java)
- `build`, `dist`
- `.next`, `.nuxt` (JavaScript frameworks)

**Version Control:**
- `.git`, `.svn`, `.hg`

**Caches:**
- `__pycache__`, `.pytest_cache`, `.mypy_cache` (Python)
- `.tox`, `.nox` (Python testing)
- `.cache`

**And more...**

Disable with `--no-default-excludes` flag.

## Use Cases

### 1. Documentation Maintenance

**Find broken links:**
```bash
md-file-graph graph ./docs --include-external
# Look for red nodes in the SVG
```

**Find orphaned pages:**
```bash
md-file-graph graph ./docs --hide-isolated
# Pages not in the graph are orphaned
```

### 2. Static Site Generation

**Generate documentation website:**
```bash
md-file-graph html ./docs \
    --output ./website \
    --base-url https://docs.example.com
```

**Deploy to GitHub Pages:**
```bash
# Generate
md-file-graph html ./docs --output ./gh-pages --base-url https://user.github.io/project

# Deploy
cd gh-pages
git init && git add . && git commit -m "Docs"
git push origin gh-pages --force
```

### 3. Documentation Analysis

**Visualize structure:**
```bash
md-file-graph graph ./docs -o ./analysis
open ./analysis/markdown_graph.svg
```

**Analyze complexity:**
- Count nodes = number of documents
- Count edges = number of links
- Find highly connected nodes = central documents

### 4. CI/CD Integration

**Validate documentation:**
```bash
# Generate graph and check for broken links
md-file-graph graph ./docs -o ./check
# Parse output for red nodes
```

**Auto-generate documentation:**
```bash
# In CI pipeline
md-file-graph html ./docs --output ./public --base-url $SITE_URL
# Deploy public/ directory
```

## Advanced Features

### Configuration File Support

Provide a JSON configuration file:

```json
{
  "base_url": "https://example.com",
  "author": "Your Name",
  "site_name": "My Documentation",
  "social_image": "/images/og-image.png"
}
```

Use with:
```bash
md-file-graph html ./docs \
    --output ./site \
    --config config.json
```

### Custom Styling

Generate HTML and add custom CSS:

```bash
# Generate HTML
md-file-graph html ./docs --output ./site --base-url https://example.com

# Add your styles
cp custom.css ./site/
# Edit template to include custom.css
```

### Multi-Version Documentation

Generate docs for multiple versions:

```bash
# Version 1.0
md-file-graph html ./docs/v1.0 \
    --output ./site/v1.0 \
    --base-url https://docs.example.com/v1.0

# Version 2.0
md-file-graph html ./docs/v2.0 \
    --output ./site/v2.0 \
    --base-url https://docs.example.com/v2.0
```

## Integration Examples

### GitHub Actions

```yaml
name: Deploy Docs
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
      - name: Install md-file-graph
        run: pip install md-file-graph
      - name: Generate docs
        run: |
          md-file-graph html ./docs \
            --output ./public \
            --base-url https://example.com
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

### Make Target

```makefile
.PHONY: docs
docs:
	md-file-graph html ./docs \
		--output ./website \
		--base-url https://docs.example.com \
		--template templates/doc.html
```

### NPM Script

```json
{
  "scripts": {
    "docs:build": "md-file-graph html ./docs --output ./dist/docs --base-url https://example.com",
    "docs:analyze": "md-file-graph graph ./docs --output ./analysis"
  }
}
```

## Compatibility

### Python Versions
- ✅ Python 3.8
- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12

### Operating Systems
- ✅ Linux (Ubuntu, Debian, CentOS, etc.)
- ✅ macOS (10.15+)
- ✅ Windows (10, 11)
- ✅ WSL (Windows Subsystem for Linux)

### Markdown Flavors
- ✅ GitHub Flavored Markdown (GFM)
- ✅ CommonMark
- ✅ Standard Markdown
- ✅ Python-Markdown extensions

## Roadmap

### Planned Features

**v0.3.0:**
- [ ] Search index generation (lunr.js)
- [ ] Documentation metrics
- [ ] Broken link reporting
- [ ] Markdown linting

**v0.4.0:**
- [ ] Multi-language support
- [ ] Theme system
- [ ] Plugin architecture
- [ ] API documentation from code

**v0.5.0:**
- [ ] Real-time preview server
- [ ] Live reload
- [ ] Incremental builds
- [ ] Watch mode

## Summary

md-file-graph is a comprehensive tool for:
- 📊 **Analyzing** markdown documentation structure
- 🎨 **Visualizing** documentation relationships
- 🌐 **Generating** SEO-optimized static HTML sites

With features for:
- ✅ Complete SEO optimization
- ✅ Beautiful visualizations
- ✅ Custom templates
- ✅ CI/CD integration
- ✅ Professional output

Perfect for:
- 📚 Documentation websites
- 🔍 Link validation
- 🗺️ Structure analysis
- 🚀 Static site generation

