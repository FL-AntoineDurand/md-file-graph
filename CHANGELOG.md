# Changelog

All notable changes to md-file-graph will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-12-17

### Added

#### HTML Generation Feature 🌐
- **Static HTML documentation generator** with full SEO optimization
- New `md-file-graph html` command for generating static documentation sites
- Automatic sitemap.xml generation for search engines
- Robots.txt generation for web crawlers
- Complete SEO meta tags (title, description, keywords)
- Open Graph tags for social media (Facebook, LinkedIn)
- Twitter Card tags for Twitter sharing
- Structured data (JSON-LD) for rich snippets in search results
- Custom Jinja2 template support
- Markdown frontmatter parsing (YAML)
- Automatic metadata extraction from content
- Syntax highlighting support via Pygments
- Responsive HTML output

#### Enhanced CLI
- Restructured CLI as command group with subcommands
- `graph` subcommand - Original graph visualization functionality
- `html` subcommand - New HTML generation functionality
- Improved help text and documentation

#### Dependencies
- Added `markdown>=3.5` for HTML conversion
- Added `python-frontmatter>=1.0.0` for frontmatter parsing
- Added `jinja2>=3.1.0` for HTML templating
- Added `beautifulsoup4>=4.12.0` for HTML manipulation
- Added `Pygments>=2.17.0` for syntax highlighting

#### Documentation
- Complete rewrite of README.md with HTML generation examples
- Updated QUICKSTART.md with HTML generation quick start
- Enhanced INSTALL.md with HTML feature dependencies
- Added CHANGELOG.md (this file)
- Added comprehensive usage examples

### Changed
- **Breaking:** CLI structure changed from single command to command group
  - Old: `md-file-graph [OPTIONS] DIRECTORY`
  - New: `md-file-graph graph [OPTIONS] DIRECTORY`
  - New: `md-file-graph html [OPTIONS] DIRECTORY`
- Updated entry point in pyproject.toml from `main` to `cli`
- Enhanced requirements.txt with HTML generation dependencies
- Improved documentation structure and organization

### Technical Details

#### New Modules
- `src/md_file_graph/html_generator.py` - Complete HTML generation system
  - `HTMLGenerator` class for static site generation
  - `DocMetadata` dataclass for document metadata
  - Markdown to HTML conversion with extensions
  - Frontmatter extraction and parsing
  - Auto-metadata extraction (title, description, keywords)
  - Link conversion (`.md` → `.html`)
  - Template rendering with Jinja2
  - Sitemap and robots.txt generation

#### CLI Changes
- `src/md_file_graph/cli.py`
  - Added `generate_html` command function
  - Changed `main` to `cli` group function
  - Added command registration for both `graph` and `html`
  - Improved error handling for missing dependencies

#### Features
- Respects .gitignore files (configurable)
- Excludes common directories (node_modules, venv, etc.)
- Handles relative markdown links
- Converts markdown links to HTML links
- Generates proper canonical URLs
- Creates SEO-friendly slugs
- Supports custom templates
- Optional configuration file support

### Migration Guide

If you were using v0.1.0, update your commands:

```bash
# Old command (v0.1.0)
md-file-graph /path/to/docs -o ./output

# New command (v0.2.0)
md-file-graph graph /path/to/docs -o ./output

# New HTML generation
md-file-graph html /path/to/docs \
    --output ./website \
    --base-url https://example.com
```

### Use Cases

The new HTML generation feature enables:

1. **Static Documentation Sites**
   - Generate complete documentation websites
   - Deploy to any static hosting (GitHub Pages, Netlify, Vercel)
   - Full SEO optimization out of the box

2. **API Documentation**
   - Convert markdown API docs to HTML
   - Include in your project website
   - Improve API documentation discoverability

3. **Knowledge Bases**
   - Transform internal wikis to searchable websites
   - Make documentation search-engine friendly
   - Share knowledge effectively

4. **Project Documentation**
   - Generate project docs for open source projects
   - Include in CI/CD pipelines
   - Keep documentation always up-to-date

## [0.1.0] - 2024-11-01

### Added
- Initial release
- Markdown file discovery with .gitignore support
- Link extraction (internal and external)
- Graph generation in DOT format
- SVG visualization using GraphViz
- CLI with click framework
- Configurable exclusion patterns
- Default exclusion of common directories (node_modules, venv, etc.)

### Features
- Recursive markdown file scanning
- Internal and external link tracking
- Visual graph generation
- Link text and line number tracking
- Blue nodes for existing files
- Red nodes for broken/missing links
- Customizable output names and locations
- Options to include/exclude external URLs
- Option to hide isolated nodes

### Documentation
- README.md with usage examples
- QUICKSTART.md for quick start
- INSTALL.md for installation instructions
- CONTRIBUTING.md for contributors
- Example documentation for testing

---

## Semantic Versioning

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): New functionality, backwards-compatible
- **PATCH** version (0.0.X): Bug fixes, backwards-compatible

## Links

- [Repository](https://github.com/yourusername/md-file-graph)
- [Issues](https://github.com/yourusername/md-file-graph/issues)
- [Documentation](README.md)

