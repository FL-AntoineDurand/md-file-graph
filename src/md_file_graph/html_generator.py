"""
HTML documentation generator with SEO optimization.

Copyright (C) 2024 md-file-graph contributors
Licensed under GPL-3.0-or-later
"""

import json
import re
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    import markdown
    from markdown.extensions import fenced_code, tables, toc, codehilite
except ImportError:
    markdown = None

try:
    import frontmatter
except ImportError:
    frontmatter = None

try:
    from jinja2 import Template
except ImportError:
    Template = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


@dataclass
class DocMetadata:
    """Container for document metadata extracted from frontmatter and content."""
    
    title: str
    description: str = ""
    keywords: List[str] = None
    author: str = "Documentation"
    date_modified: str = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.date_modified is None:
            self.date_modified = datetime.now().isoformat()


class HTMLGenerator:
    """Generates static HTML documentation site with full SEO optimization."""
    
    def __init__(self, base_dir: Path, output_dir: Path, base_url: str, 
                 template_path: Optional[Path] = None, config_path: Optional[Path] = None):
        """
        Initialize HTML generator.
        
        Args:
            base_dir: Root directory containing markdown files
            output_dir: Directory where HTML files will be generated
            base_url: Base URL for the website (e.g., https://example.com)
            template_path: Optional path to custom Jinja2 template
            config_path: Optional path to configuration JSON file
        """
        self.base_dir = base_dir
        self.output_dir = output_dir
        self.base_url = base_url.rstrip('/')
        self.template_path = template_path
        self.config_path = config_path
        
        # Check dependencies
        self._check_dependencies()
        
        # Initialize markdown processor
        self.md = markdown.Markdown(extensions=[
            'fenced_code',
            'tables',
            'toc',
            'codehilite',
            'nl2br',
            'sane_lists',
            'attr_list'
        ])
        
        self.config = None
        self.generated_pages = []
        self.doc_tree = []  # For navigation structure
        self.copied_images = set()  # Track copied images
    
    def _check_dependencies(self):
        """Check if required dependencies are installed."""
        missing = []
        if markdown is None:
            missing.append('markdown')
        if frontmatter is None:
            missing.append('python-frontmatter')
        if Template is None:
            missing.append('jinja2')
        if BeautifulSoup is None:
            missing.append('beautifulsoup4')
        
        if missing:
            raise ImportError(
                f"Missing required dependencies: {', '.join(missing)}\n"
                f"Install with: pip install {' '.join(missing)}"
            )
    
    def load_config(self) -> Optional[Dict]:
        """Load documentation configuration from JSON file if provided."""
        if not self.config_path or not self.config_path.exists():
            return None
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        return self.config
    
    def discover_markdown_files(self) -> List[Path]:
        """Discover all markdown files in base directory."""
        from .parser import MarkdownParser
        
        parser = MarkdownParser()
        return parser.find_markdown_files(self.base_dir)
    
    def should_publish(self, md_content: str, file_path: Path) -> bool:
        """
        Check if a document should be published based on frontmatter and path.
        
        Returns False if:
        - Frontmatter contains 'publish: false'
        - Content contains '__DO_NOT_PUBLISH__' tag
        - File is in an excluded path pattern
        """
        # Parse frontmatter
        post = frontmatter.loads(md_content)
        
        # Check frontmatter publish flag
        if post.get('publish') is False or post.get('published') is False:
            return False
        
        # Check for __DO_NOT_PUBLISH__ tag in content
        if '__DO_NOT_PUBLISH__' in md_content:
            return False
        
        # Check excluded paths (doc/archive, etc.)
        relative_path = file_path.relative_to(self.base_dir).as_posix()
        excluded_patterns = [
            'doc/archive',
            '/archive/',
            '/.archive/',
            '/draft/',
            '/.draft/',
        ]
        
        for pattern in excluded_patterns:
            if pattern in relative_path:
                return False
        
        return True
    
    def extract_metadata(self, md_content: str, file_path: Path) -> Tuple[DocMetadata, str]:
        """Extract metadata from markdown frontmatter and content."""
        # Parse frontmatter
        post = frontmatter.loads(md_content)
        
        # Extract title
        title = post.get('title', '')
        if not title:
            h1_match = re.search(r'^#\s+(.+)$', post.content, re.MULTILINE)
            if h1_match:
                title = h1_match.group(1).strip()
            else:
                title = file_path.stem.replace('_', ' ').replace('-', ' ').title()
        
        # Extract description
        description = post.get('description', '')
        if not description:
            paragraphs = []
            in_html_block = False
            for line in post.content.split('\n'):
                line = line.strip()
                
                # Skip HTML blocks
                if line.startswith('<') or line.startswith('</'):
                    in_html_block = True
                    continue
                if in_html_block and (line.startswith('</') or line.endswith('>')):
                    in_html_block = False
                    continue
                if in_html_block:
                    continue
                
                # Look for text paragraphs
                if (line and 
                    not line.startswith('#') and 
                    not line.startswith('```') and 
                    not line.startswith('![') and 
                    not line.startswith('[![') and
                    not line.startswith('>') and
                    not line.startswith('---') and
                    'shield.io' not in line and
                    'badge' not in line.lower()):
                    paragraphs.append(line)
                    if len(' '.join(paragraphs)) > 80:
                        break
            
            if paragraphs:
                description = ' '.join(paragraphs)[:300]
                # Clean up markdown syntax
                description = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', description)
                description = re.sub(r'[*_`]', '', description)
                description = re.sub(r'<[^>]+>', '', description)
        
        # Extract keywords
        keywords = post.get('keywords', [])
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(',')]
        
        if not keywords:
            keywords = self._extract_keywords_from_content(post.content, title)
        
        # Get modification date
        date_modified = post.get('date', datetime.now().isoformat())
        
        metadata = DocMetadata(
            title=title,
            description=description,
            keywords=keywords,
            date_modified=date_modified
        )
        
        return metadata, post.content
    
    def _extract_keywords_from_content(self, content: str, title: str) -> List[str]:
        """Extract relevant keywords from content."""
        keywords = []
        
        # Add words from title
        title_words = [w.lower() for w in re.findall(r'\b\w+\b', title) if len(w) > 3]
        keywords.extend(title_words[:5])
        
        # Extract headings as keywords
        headings = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
        for heading in headings[:5]:
            words = [w.lower() for w in re.findall(r'\b\w+\b', heading) if len(w) > 3]
            keywords.extend(words[:2])
        
        # Add default keywords
        keywords.append('documentation')
        
        return list(set(keywords))[:15]
    
    def copy_images(self, html: str, source_file: Path) -> str:
        """
        Find and copy images referenced in HTML, rewrite paths.
        
        Args:
            html: HTML content with image tags
            source_file: Path to the source markdown file
            
        Returns:
            HTML with rewritten image paths
        """
        soup = BeautifulSoup(html, 'html.parser')
        assets_dir = self.output_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        
        for img in soup.find_all('img', src=True):
            src = img['src']
            
            # Skip external images
            if src.startswith(('http://', 'https://', 'data:', '//')):
                continue
            
            # Resolve image path relative to source file
            source_dir = source_file.parent
            image_path = (source_dir / src).resolve()
            
            # If image doesn't exist relative to source, try relative to base_dir
            if not image_path.exists():
                image_path = (self.base_dir / src).resolve()
            
            if image_path.exists() and image_path not in self.copied_images:
                # Copy image to assets directory
                dest_name = f"{image_path.parent.name}_{image_path.name}" if image_path.parent.name != self.base_dir.name else image_path.name
                dest_path = assets_dir / dest_name
                
                # Avoid name collisions
                counter = 1
                while dest_path.exists() and dest_path not in self.copied_images:
                    dest_path = assets_dir / f"{image_path.stem}_{counter}{image_path.suffix}"
                    counter += 1
                
                try:
                    shutil.copy2(image_path, dest_path)
                    self.copied_images.add(image_path)
                    
                    # Rewrite image path to point to assets directory
                    img['src'] = f"assets/{dest_path.name}"
                    print(f"  📷 Copied image: {image_path.name} -> assets/{dest_path.name}")
                except Exception as e:
                    print(f"  ⚠️  Failed to copy image {image_path}: {e}")
        
        return str(soup)
    
    def convert_markdown_links(self, html: str) -> str:
        """Convert markdown file links to HTML page links."""
        soup = BeautifulSoup(html, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            if href.endswith('.md') and not href.startswith(('http://', 'https://', 'mailto:', '#')):
                new_href = href.replace('.md', '.html')
                if href.startswith('../'):
                    link['href'] = new_href
                elif href.startswith('./'):
                    link['href'] = new_href.replace('./', '')
                else:
                    link['href'] = new_href
        
        return str(soup)
    
    def generate_structured_data(self, metadata: DocMetadata, url: str) -> str:
        """Generate JSON-LD structured data for SEO."""
        structured_data = {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": metadata.title,
            "description": metadata.description,
            "author": {
                "@type": "Organization",
                "name": metadata.author,
            },
            "dateModified": metadata.date_modified,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": url
            },
            "keywords": ", ".join(metadata.keywords)
        }
        
        return json.dumps(structured_data, indent=2)
    
    def get_default_template(self) -> str:
        """Get default HTML template."""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Primary Meta Tags -->
    <title>{{ metadata.title }}</title>
    <meta name="title" content="{{ metadata.title }}">
    <meta name="description" content="{{ metadata.description }}">
    <meta name="keywords" content="{{ keywords }}">
    <meta name="author" content="{{ metadata.author }}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{{ canonical_url }}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{{ canonical_url }}">
    <meta property="og:title" content="{{ metadata.title }}">
    <meta property="og:description" content="{{ metadata.description }}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="{{ canonical_url }}">
    <meta property="twitter:title" content="{{ metadata.title }}">
    <meta property="twitter:description" content="{{ metadata.description }}">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
{{ structured_data }}
    </script>
    
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
        pre { background: #f4f4f4; padding: 15px; overflow-x: auto; border-radius: 5px; }
        code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
        h1, h2, h3 { margin-top: 1.5em; }
        a { color: #0066cc; }
    </style>
</head>
<body>
    <article>
        {{ content|safe }}
    </article>
</body>
</html>'''
    
    def load_template(self) -> Template:
        """Load Jinja2 template."""
        if self.template_path and self.template_path.exists():
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_str = f.read()
        else:
            template_str = self.get_default_template()
        
        return Template(template_str)
    
    def generate_page(self, source_path: Path, relative_path: Path, template: Template) -> Path:
        """Generate a single HTML page from markdown source."""
        # Read markdown content
        with open(source_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Extract metadata and content
        metadata, content = self.extract_metadata(md_content, source_path)
        
        # Convert markdown to HTML
        html_content = self.md.convert(content)
        self.md.reset()
        
        # Copy images and rewrite paths
        html_content = self.copy_images(html_content, source_path)
        
        # Fix markdown links
        html_content = self.convert_markdown_links(html_content)
        
        # Generate URL
        html_relative = relative_path.with_suffix('.html')
        canonical_url = f"{self.base_url}/{html_relative.as_posix()}"
        
        # Generate structured data
        structured_data = self.generate_structured_data(metadata, canonical_url)
        
        # Render template
        html = template.render(
            metadata=metadata,
            content=html_content,
            keywords=', '.join(metadata.keywords),
            canonical_url=canonical_url,
            base_url=self.base_url,
            structured_data=structured_data
        )
        
        # Write HTML file
        output_path = self.output_dir / html_relative
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Track for sitemap and doc tree
        self.generated_pages.append({
            'url': canonical_url,
            'lastmod': metadata.date_modified,
            'priority': '0.8' if source_path.name == 'README.md' else '0.6'
        })
        
        # Add to doc tree
        self.doc_tree.append({
            'title': metadata.title,
            'path': html_relative.as_posix(),
            'url': canonical_url,
            'level': len(relative_path.parts) - 1,
            'parent_dir': relative_path.parent.as_posix() if relative_path.parent.as_posix() != '.' else ''
        })
        
        return output_path
    
    def generate_sitemap(self) -> Path:
        """Generate sitemap.xml for all documentation pages."""
        sitemap_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]
        
        for page in sorted(self.generated_pages, key=lambda x: x['url']):
            date_str = page['lastmod'].split('T')[0] if 'T' in page['lastmod'] else page['lastmod']
            
            sitemap_lines.extend([
                '  <url>',
                f'    <loc>{page["url"]}</loc>',
                f'    <lastmod>{date_str}</lastmod>',
                '    <changefreq>weekly</changefreq>',
                f'    <priority>{page["priority"]}</priority>',
                '  </url>',
            ])
        
        sitemap_lines.append('</urlset>')
        
        sitemap_path = self.output_dir / 'sitemap.xml'
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sitemap_lines))
        
        return sitemap_path
    
    def generate_robots_txt(self) -> Path:
        """Generate robots.txt file."""
        robots_content = f"""User-agent: *
Allow: /

Sitemap: {self.base_url}/sitemap.xml
"""
        
        robots_path = self.output_dir / 'robots.txt'
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write(robots_content)
        
        return robots_path
    
    def generate_docs_json(self) -> Path:
        """
        Generate docs.json navigation file with hierarchical structure.
        
        Returns:
            Path to generated docs.json file
        """
        # Build hierarchical navigation structure
        sections = {}
        
        for doc in sorted(self.doc_tree, key=lambda x: x['path']):
            parent_dir = doc['parent_dir']
            
            # Determine section based on directory structure
            if not parent_dir:
                section_name = 'Root'
            else:
                # Use first directory as section name
                parts = parent_dir.split('/')
                section_name = parts[0].replace('_', ' ').replace('-', ' ').title()
            
            if section_name not in sections:
                sections[section_name] = {
                    'title': section_name,
                    'items': []
                }
            
            sections[section_name]['items'].append({
                'title': doc['title'],
                'path': doc['path'],
                'url': doc['url'],
                'level': doc['level']
            })
        
        # Convert to list format
        navigation = {
            'generated': datetime.now().isoformat(),
            'base_url': self.base_url,
            'sections': [
                {
                    'title': section_data['title'],
                    'items': section_data['items']
                }
                for section_name, section_data in sections.items()
            ]
        }
        
        # Write JSON file
        docs_json_path = self.output_dir / 'docs.json'
        with open(docs_json_path, 'w', encoding='utf-8') as f:
            json.dump(navigation, f, indent=2)
        
        return docs_json_path
    
    def generate_all(self) -> Dict:
        """
        Generate complete static documentation site.
        
        Returns:
            dict: Statistics about generation (pages_count, urls_count, etc.)
        """
        print(f"🚀 Generating static HTML documentation site...")
        print(f"📂 Source: {self.base_dir}")
        print(f"📂 Output: {self.output_dir}")
        print(f"🌐 Base URL: {self.base_url}")
        print()
        
        # Load configuration if available
        if self.config_path:
            print("📋 Loading configuration...")
            self.load_config()
        
        # Load template
        template = self.load_template()
        
        # Discover markdown files
        print("🔍 Discovering markdown files...")
        md_files = self.discover_markdown_files()
        print(f"✅ Found {len(md_files)} markdown file(s)")
        print()
        
        # Generate pages
        print("📝 Generating HTML pages...")
        generated_count = 0
        skipped_count = 0
        
        for md_file in md_files:
            try:
                relative_path = md_file.relative_to(self.base_dir)
                
                # Check if file should be published
                with open(md_file, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                
                if not self.should_publish(md_content, md_file):
                    print(f"  ⏭️  Skipped (excluded): {relative_path}")
                    skipped_count += 1
                    continue
                
                output_path = self.generate_page(md_file, relative_path, template)
                print(f"  ✅ {relative_path}")
                generated_count += 1
            except Exception as e:
                print(f"  ❌ Error generating {md_file.name}: {e}")
        
        print(f"\n✅ Generated {generated_count}/{len(md_files)} page(s)")
        if skipped_count > 0:
            print(f"⏭️  Skipped {skipped_count} excluded file(s)")
        print()
        
        # Generate sitemap
        print("🗺️  Generating sitemap.xml...")
        sitemap_path = self.generate_sitemap()
        print(f"✅ Sitemap: {sitemap_path}")
        print()
        
        # Generate robots.txt
        print("🤖 Generating robots.txt...")
        robots_path = self.generate_robots_txt()
        print(f"✅ Robots.txt: {robots_path}")
        print()
        
        # Generate docs.json navigation
        print("📋 Generating docs.json navigation...")
        docs_json_path = self.generate_docs_json()
        print(f"✅ Navigation: {docs_json_path}")
        print()
        
        # Report images copied
        if self.copied_images:
            print(f"📷 Copied {len(self.copied_images)} image(s) to assets/")
            print()
        
        print("✨ Static documentation site generation complete!")
        
        return {
            'pages_generated': generated_count,
            'pages_skipped': skipped_count,
            'pages_total': len(md_files),
            'urls_in_sitemap': len(self.generated_pages),
            'images_copied': len(self.copied_images),
            'output_dir': str(self.output_dir)
        }

