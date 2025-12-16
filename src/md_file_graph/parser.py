"""
Markdown file parser for extracting links.

Copyright (C) 2024 md-file-graph contributors
Licensed under GPL-3.0-or-later
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
import fnmatch


@dataclass
class Link:
    """Represents a link found in a markdown file."""
    source_file: Path
    target: str
    link_text: str
    line_number: int
    is_external: bool


class MarkdownParser:
    """Parser for extracting links from markdown files."""
    
    # Common third-party library directories to exclude by default
    DEFAULT_EXCLUDE_DIRS = {
        'node_modules',
        'vendor',
        'bower_components',
        '.git',
        '.svn',
        '.hg',
        '__pycache__',
        '.pytest_cache',
        '.mypy_cache',
        '.tox',
        '.nox',
        'venv',
        'env',
        'ENV',
        '.venv',
        'virtualenv',
        'target',  # Rust, Java
        'build',
        'dist',
        '.next',
        '.nuxt',
        '.cache',
        'pkg',  # Go
        'Pods',  # iOS CocoaPods
        'Carthage',  # iOS Carthage
    }
    
    def __init__(self, respect_gitignore: bool = True, additional_excludes: Set[str] = None, use_default_excludes: bool = True):
        self.md = MarkdownIt()
        # Regex for matching markdown links: [text](url)
        self.link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
        self.respect_gitignore = respect_gitignore
        
        # Set up exclude directories
        if use_default_excludes:
            self.exclude_dirs = self.DEFAULT_EXCLUDE_DIRS.copy()
        else:
            self.exclude_dirs = set()
        
        if additional_excludes:
            self.exclude_dirs.update(additional_excludes)
        
        self.gitignore_patterns: Dict[Path, List[str]] = {}
    
    def _load_gitignore(self, directory: Path) -> List[str]:
        """Load and parse .gitignore file."""
        gitignore_file = directory / '.gitignore'
        patterns = []
        
        if gitignore_file.exists():
            try:
                content = gitignore_file.read_text(encoding='utf-8')
                for line in content.splitlines():
                    line = line.strip()
                    # Skip comments and empty lines
                    if line and not line.startswith('#'):
                        patterns.append(line)
            except Exception as e:
                print(f"Warning: Could not read .gitignore at {gitignore_file}: {e}")
        
        return patterns
    
    def _should_exclude_path(self, path: Path, base_dir: Path) -> bool:
        """Check if a path should be excluded based on gitignore and default excludes."""
        # Check if any parent directory is in exclude list
        try:
            rel_path = path.relative_to(base_dir)
            parts = rel_path.parts
            
            # Check if any part of the path is in default excludes
            for part in parts:
                if part in self.exclude_dirs:
                    return True
            
            # Check gitignore patterns if enabled
            if self.respect_gitignore:
                # Find the closest .gitignore
                current = path if path.is_dir() else path.parent
                while current >= base_dir:
                    if current not in self.gitignore_patterns:
                        self.gitignore_patterns[current] = self._load_gitignore(current)
                    
                    patterns = self.gitignore_patterns[current]
                    if patterns:
                        try:
                            check_path = path.relative_to(current)
                            for pattern in patterns:
                                # Handle directory patterns
                                if pattern.endswith('/'):
                                    if any(fnmatch.fnmatch(part, pattern.rstrip('/')) for part in check_path.parts):
                                        return True
                                # Handle file patterns
                                elif fnmatch.fnmatch(str(check_path), pattern) or \
                                     fnmatch.fnmatch(str(check_path), f"**/{pattern}"):
                                    return True
                        except ValueError:
                            pass
                    
                    if current == base_dir:
                        break
                    current = current.parent
        
        except ValueError:
            # Path is not relative to base_dir
            pass
        
        return False
    
    def find_markdown_files(self, directory: Path) -> List[Path]:
        """Recursively find all markdown files in a directory, respecting exclusions."""
        md_files = []
        
        # Use iterative approach to respect exclusions
        def scan_directory(dir_path: Path):
            try:
                for item in dir_path.iterdir():
                    # Skip if should be excluded
                    if self._should_exclude_path(item, directory):
                        continue
                    
                    if item.is_file() and item.suffix.lower() == '.md':
                        md_files.append(item)
                    elif item.is_dir():
                        scan_directory(item)
            except PermissionError:
                print(f"Warning: Permission denied accessing {dir_path}")
            except Exception as e:
                print(f"Warning: Error scanning {dir_path}: {e}")
        
        scan_directory(directory)
        return sorted(md_files)
    
    def extract_links(self, file_path: Path) -> List[Link]:
        """Extract all links from a markdown file."""
        links = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, start=1):
                # Find all markdown links in the line
                matches = self.link_pattern.finditer(line)
                
                for match in matches:
                    link_text = match.group(1)
                    target = match.group(2)
                    
                    # Determine if it's an external link
                    is_external = self._is_external_link(target)
                    
                    # Clean up the target (remove anchors for internal links)
                    if not is_external and '#' in target:
                        target = target.split('#')[0]
                    
                    if target:  # Skip empty links
                        links.append(Link(
                            source_file=file_path,
                            target=target,
                            link_text=link_text,
                            line_number=line_num,
                            is_external=is_external
                        ))
        
        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}")
        
        return links
    
    def _is_external_link(self, target: str) -> bool:
        """Determine if a link target is external (URL) or internal (file)."""
        # Check if it's a URL with protocol
        if any(target.startswith(proto) for proto in ['http://', 'https://', 'ftp://', 'mailto:']):
            return True
        
        # Check if it starts with // (protocol-relative URL)
        if target.startswith('//'):
            return True
        
        # Everything else is considered internal
        return False
    
    def resolve_internal_link(self, source_file: Path, target: str, base_dir: Path) -> Path:
        """Resolve an internal link to an absolute path."""
        # Handle absolute paths from base_dir
        if target.startswith('/'):
            return base_dir / target.lstrip('/')
        
        # Handle relative paths from source file location
        resolved = (source_file.parent / target).resolve()
        return resolved

