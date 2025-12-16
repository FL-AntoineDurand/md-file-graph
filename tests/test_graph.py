"""
Tests for the graph builder.

Copyright (C) 2024 md-file-graph contributors
Licensed under GPL-3.0-or-later
"""

import pytest
from pathlib import Path
from md_file_graph.graph import GraphBuilder
from md_file_graph.parser import Link


def test_graph_builder_basic(tmp_path):
    """Test basic graph building functionality."""
    file1 = tmp_path / "file1.md"
    file2 = tmp_path / "file2.md"
    
    links = [
        Link(
            source_file=file1,
            target="./file2.md",
            link_text="Link to file2",
            line_number=1,
            is_external=False
        )
    ]
    
    builder = GraphBuilder(tmp_path)
    builder.add_links(links)
    
    assert file1 in builder.nodes
    assert len(builder.edges) == 1


def test_graph_dot_generation(tmp_path):
    """Test DOT format generation."""
    file1 = tmp_path / "file1.md"
    file2 = tmp_path / "file2.md"
    
    links = [
        Link(
            source_file=file1,
            target="./file2.md",
            link_text="Link",
            line_number=1,
            is_external=False
        )
    ]
    
    builder = GraphBuilder(tmp_path)
    builder.add_links(links)
    dot = builder.generate_dot()
    
    assert "digraph markdown_links" in dot
    assert "file1.md" in dot
    assert "file2.md" in dot


def test_external_links_excluded_by_default(tmp_path):
    """Test that external links are excluded by default."""
    file1 = tmp_path / "file1.md"
    
    links = [
        Link(
            source_file=file1,
            target="https://example.com",
            link_text="External",
            line_number=1,
            is_external=True
        )
    ]
    
    builder = GraphBuilder(tmp_path, include_external=False)
    builder.add_links(links)
    dot = builder.generate_dot()
    
    assert "example.com" not in dot


def test_external_links_included_when_enabled(tmp_path):
    """Test that external links are included when enabled."""
    file1 = tmp_path / "file1.md"
    
    links = [
        Link(
            source_file=file1,
            target="https://example.com",
            link_text="External",
            line_number=1,
            is_external=True
        )
    ]
    
    builder = GraphBuilder(tmp_path, include_external=True)
    builder.add_links(links)
    dot = builder.generate_dot()
    
    assert "example.com" in dot

