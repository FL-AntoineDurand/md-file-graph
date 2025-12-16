"""
Graph builder and visualizer for markdown file links.

Copyright (C) 2024 md-file-graph contributors
Licensed under GPL-3.0-or-later
"""

from pathlib import Path
from typing import List, Dict, Set, Optional
from collections import defaultdict
import graphviz
from .parser import Link


class GraphBuilder:
    """Builds a graph representation of markdown file links."""
    
    def __init__(self, base_dir: Path, include_external: bool = False, hide_isolated: bool = False):
        self.base_dir = base_dir
        self.include_external = include_external
        self.hide_isolated = hide_isolated
        
        # Graph data structures
        self.nodes: Set[Path] = set()
        self.external_nodes: Set[str] = set()
        self.edges: List[Dict] = []
    
    def add_links(self, links: List[Link]):
        """Add links to the graph."""
        from .parser import MarkdownParser
        parser = MarkdownParser()
        
        for link in links:
            # Add source file as node
            self.nodes.add(link.source_file)
            
            if link.is_external:
                if self.include_external:
                    self.external_nodes.add(link.target)
                    self.edges.append({
                        'source': link.source_file,
                        'target': link.target,
                        'label': f"{link.link_text} (L{link.line_number})",
                        'is_external': True
                    })
            else:
                # Resolve internal link to absolute path
                target_path = parser.resolve_internal_link(
                    link.source_file, 
                    link.target, 
                    self.base_dir
                )
                
                # Add target as node (even if it doesn't exist yet)
                self.nodes.add(target_path)
                
                self.edges.append({
                    'source': link.source_file,
                    'target': target_path,
                    'label': f"{link.link_text} (L{link.line_number})",
                    'is_external': False
                })
    
    def _get_relative_path(self, file_path: Path) -> str:
        """Get path relative to base directory."""
        try:
            return str(file_path.relative_to(self.base_dir))
        except ValueError:
            return str(file_path)
    
    def _get_connected_nodes(self) -> Set[Path]:
        """Get all nodes that have at least one connection."""
        connected = set()
        for edge in self.edges:
            if not edge['is_external']:
                connected.add(edge['source'])
                connected.add(edge['target'])
        return connected
    
    def generate_dot(self) -> str:
        """Generate DOT format graph representation."""
        lines = ["digraph markdown_links {"]
        lines.append("    rankdir=LR;")
        lines.append("    node [shape=box, style=rounded];")
        lines.append("")
        
        # Filter nodes if hiding isolated
        nodes_to_include = self.nodes
        if self.hide_isolated:
            nodes_to_include = self._get_connected_nodes()
        
        # Add markdown file nodes
        for node in sorted(nodes_to_include):
            rel_path = self._get_relative_path(node)
            node_id = self._get_node_id(node)
            
            # Check if file exists
            exists = node.exists()
            color = "lightblue" if exists else "lightcoral"
            
            lines.append(f'    {node_id} [label="{self._escape_label(rel_path)}", fillcolor={color}, style="rounded,filled"];')
        
        # Add external URL nodes
        if self.include_external:
            for url in sorted(self.external_nodes):
                url_id = self._get_external_node_id(url)
                # Truncate long URLs for display
                display_url = url if len(url) <= 50 else url[:47] + "..."
                lines.append(f'    {url_id} [label="{self._escape_label(display_url)}", fillcolor=lightyellow, style="rounded,filled", shape=ellipse];')
        
        lines.append("")
        
        # Add edges
        for edge in self.edges:
            source_id = self._get_node_id(edge['source'])
            
            if edge['is_external']:
                if self.include_external:
                    target_id = self._get_external_node_id(edge['target'])
                    lines.append(f'    {source_id} -> {target_id} [label="{self._escape_label(edge["label"])}"];')
            else:
                if not self.hide_isolated or (edge['target'] in nodes_to_include):
                    target_id = self._get_node_id(edge['target'])
                    lines.append(f'    {source_id} -> {target_id} [label="{self._escape_label(edge["label"])}"];')
        
        lines.append("}")
        return "\n".join(lines)
    
    def _get_node_id(self, path: Path) -> str:
        """Generate a unique node ID for a file path."""
        import re
        rel_path = self._get_relative_path(path)
        # Replace all non-alphanumeric characters with underscores
        node_id = re.sub(r'[^a-zA-Z0-9_]', '_', rel_path)
        # Remove consecutive underscores
        node_id = re.sub(r'_+', '_', node_id)
        return f'node_{node_id}'
    
    def _get_external_node_id(self, url: str) -> str:
        """Generate a unique node ID for an external URL."""
        # Create a simple hash-based ID
        import hashlib
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        return f'ext_{url_hash}'
    
    def _escape_label(self, label: str) -> str:
        """Escape special characters in labels."""
        # Escape backslashes first, then quotes and newlines
        label = label.replace('\\', '\\\\')
        label = label.replace('"', '\\"')
        label = label.replace('\n', '\\n')
        return label
    
    def generate_svg(self, output_path: Path, format: str = 'svg'):
        """Generate SVG visualization using graphviz."""
        dot_content = self.generate_dot()
        
        # Use graphviz to render
        graph = graphviz.Source(dot_content)
        
        # Save the graph
        output_file = str(output_path.with_suffix(''))
        graph.render(output_file, format=format, cleanup=True)
        
        return output_path

