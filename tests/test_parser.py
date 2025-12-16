"""
Tests for the markdown parser.

Copyright (C) 2024 md-file-graph contributors
Licensed under GPL-3.0-or-later
"""

import pytest
from pathlib import Path
from md_file_graph.parser import MarkdownParser, Link


def test_find_markdown_files(tmp_path):
    """Test finding markdown files in a directory."""
    # Create test directory structure
    (tmp_path / "file1.md").write_text("# Test")
    (tmp_path / "file2.md").write_text("# Test")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file3.md").write_text("# Test")
    (tmp_path / "not_markdown.txt").write_text("Not markdown")
    
    parser = MarkdownParser()
    md_files = parser.find_markdown_files(tmp_path)
    
    assert len(md_files) == 3
    assert all(f.suffix == '.md' for f in md_files)


def test_extract_internal_links(tmp_path):
    """Test extracting internal links from markdown."""
    content = """# Test Document
    
This is a [link to another doc](./other.md).
Here's [another link](docs/guide.md) on line 4.
"""
    
    test_file = tmp_path / "test.md"
    test_file.write_text(content)
    
    parser = MarkdownParser()
    links = parser.extract_links(test_file)
    
    assert len(links) == 2
    assert links[0].target == "./other.md"
    assert links[0].link_text == "link to another doc"
    assert links[0].line_number == 3
    assert not links[0].is_external
    
    assert links[1].target == "docs/guide.md"
    assert links[1].line_number == 4


def test_extract_external_links(tmp_path):
    """Test extracting external links from markdown."""
    content = """# Test Document
    
Visit [Google](https://www.google.com) for search.
Check [Example](http://example.com).
"""
    
    test_file = tmp_path / "test.md"
    test_file.write_text(content)
    
    parser = MarkdownParser()
    links = parser.extract_links(test_file)
    
    assert len(links) == 2
    assert all(link.is_external for link in links)
    assert links[0].target == "https://www.google.com"
    assert links[1].target == "http://example.com"


def test_mixed_links(tmp_path):
    """Test extracting both internal and external links."""
    content = """# Mixed Links
    
[Internal](./doc.md)
[External](https://example.com)
[Another internal](../parent.md)
"""
    
    test_file = tmp_path / "test.md"
    test_file.write_text(content)
    
    parser = MarkdownParser()
    links = parser.extract_links(test_file)
    
    assert len(links) == 3
    internal = [l for l in links if not l.is_external]
    external = [l for l in links if l.is_external]
    
    assert len(internal) == 2
    assert len(external) == 1


def test_links_with_anchors(tmp_path):
    """Test that anchors are stripped from internal links."""
    content = "[Link](./doc.md#section)"
    
    test_file = tmp_path / "test.md"
    test_file.write_text(content)
    
    parser = MarkdownParser()
    links = parser.extract_links(test_file)
    
    assert len(links) == 1
    assert links[0].target == "./doc.md"

