"""
Command-line interface for md-file-graph.

Copyright (C) 2024 md-file-graph contributors
Licensed under GPL-3.0-or-later
"""

import click
from pathlib import Path
from .parser import MarkdownParser
from .graph import GraphBuilder
from .html_generator import HTMLGenerator


@click.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-o', '--output', type=click.Path(), default='.',
              help='Output directory for generated files (default: current directory)')
@click.option('-n', '--name', default='markdown_graph',
              help='Base name for output files (default: markdown_graph)')
@click.option('--include-external', is_flag=True,
              help='Include external URLs as nodes in the graph')
@click.option('--hide-isolated', is_flag=True,
              help='Hide markdown files with no links')
@click.option('--no-gitignore', is_flag=True,
              help='Do not respect .gitignore files (include all files)')
@click.option('--no-default-excludes', is_flag=True,
              help='Do not exclude common directories like node_modules')
def main(directory, output, name, include_external, hide_isolated, no_gitignore, no_default_excludes):
    """
    Analyze markdown files and generate a link graph visualization.
    
    DIRECTORY: Path to the directory containing markdown files to analyze.
    """
    # Convert to Path objects
    dir_path = Path(directory).resolve()
    output_path = Path(output).resolve()
    
    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)
    
    click.echo(f"🔍 Scanning directory: {dir_path}")
    
    # Initialize parser with options
    parser = MarkdownParser(
        respect_gitignore=not no_gitignore,
        use_default_excludes=not no_default_excludes
    )
    
    if not no_gitignore:
        click.echo("📋 Respecting .gitignore files")
    if not no_default_excludes:
        click.echo(f"🚫 Excluding {len(parser.exclude_dirs)} common third-party directories")
    
    # Find all markdown files
    md_files = parser.find_markdown_files(dir_path)
    click.echo(f"📁 Found {len(md_files)} markdown file(s)")
    
    if not md_files:
        click.echo("⚠️  No markdown files found in the directory")
        return
    
    # Extract links from all files
    all_links = []
    for md_file in md_files:
        links = parser.extract_links(md_file)
        all_links.extend(links)
    
    internal_links = [l for l in all_links if not l.is_external]
    external_links = [l for l in all_links if l.is_external]
    
    click.echo(f"🔗 Found {len(internal_links)} internal link(s)")
    click.echo(f"🌐 Found {len(external_links)} external link(s)")
    
    # Build graph
    click.echo("📊 Building graph...")
    graph_builder = GraphBuilder(
        base_dir=dir_path,
        include_external=include_external,
        hide_isolated=hide_isolated
    )
    graph_builder.add_links(all_links)
    
    # Generate DOT file
    dot_file = output_path / f"{name}.dot"
    dot_content = graph_builder.generate_dot()
    dot_file.write_text(dot_content)
    click.echo(f"✅ Generated DOT file: {dot_file}")
    
    # Generate SVG
    click.echo("🎨 Generating SVG visualization...")
    try:
        svg_file = output_path / f"{name}.svg"
        graph_builder.generate_svg(svg_file)
        click.echo(f"✅ Generated SVG file: {svg_file}")
    except Exception as e:
        click.echo(f"❌ Error generating SVG: {e}")
        click.echo("   Make sure GraphViz is installed on your system")
        click.echo("   Ubuntu/Debian: sudo apt-get install graphviz")
        click.echo("   macOS: brew install graphviz")
        return
    
    click.echo("✨ Done!")


@click.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-o', '--output', type=click.Path(), required=True,
              help='Output directory for generated HTML files')
@click.option('--base-url', required=True,
              help='Base URL for the website (e.g., https://example.com)')
@click.option('--template', type=click.Path(exists=True), default=None,
              help='Path to custom Jinja2 HTML template')
@click.option('--config', type=click.Path(exists=True), default=None,
              help='Path to configuration JSON file')
@click.option('--no-gitignore', is_flag=True,
              help='Do not respect .gitignore files (include all files)')
@click.option('--no-default-excludes', is_flag=True,
              help='Do not exclude common directories like node_modules')
def generate_html(directory, output, base_url, template, config, no_gitignore, no_default_excludes):
    """
    Generate static HTML documentation site with SEO optimization.
    
    DIRECTORY: Path to the directory containing markdown files to convert.
    """
    try:
        # Convert to Path objects
        dir_path = Path(directory).resolve()
        output_path = Path(output).resolve()
        template_path = Path(template) if template else None
        config_path = Path(config) if config else None
        
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize HTML generator
        generator = HTMLGenerator(
            base_dir=dir_path,
            output_dir=output_path,
            base_url=base_url,
            template_path=template_path,
            config_path=config_path
        )
        
        # Generate site
        stats = generator.generate_all()
        
        # Display summary
        click.echo()
        click.echo("📊 Generation Summary:")
        click.echo(f"   Pages generated: {stats['pages_generated']}/{stats['pages_total']}")
        click.echo(f"   URLs in sitemap: {stats['urls_in_sitemap']}")
        click.echo(f"   Output directory: {stats['output_dir']}")
        
    except ImportError as e:
        click.echo(f"❌ Error: {e}")
        click.echo()
        click.echo("Install required dependencies:")
        click.echo("  pip install markdown python-frontmatter jinja2 beautifulsoup4 Pygments")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        raise


@click.group()
def cli():
    """md-file-graph: Analyze and visualize markdown documentation."""
    pass


cli.add_command(main, name='graph')
cli.add_command(generate_html, name='html')


if __name__ == '__main__':
    cli()

