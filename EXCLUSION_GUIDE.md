# Document Exclusion Guide

Learn how to exclude documents from your generated documentation site.

## Three Ways to Exclude Documents

### 1. **Frontmatter Flag** (Recommended)

Add `publish: false` to your markdown frontmatter:

```markdown
---
title: Internal Planning Document
publish: false
---

# Internal Planning

This document won't be published to the website.
```

**Alternative frontmatter keys:**
- `publish: false`
- `published: false`

### 2. **Content Tag**

Add `__DO_NOT_PUBLISH__` anywhere in your markdown file:

```markdown
# Secret Documentation

__DO_NOT_PUBLISH__

This document contains internal information.
```

**Best practice:** Place the tag at the top after the title for visibility.

### 3. **Path Patterns** (Automatic)

Files in these paths are automatically excluded:

- `doc/archive/` - Archived documentation
- `/archive/` - Any archive folder
- `/.archive/` - Hidden archive folders  
- `/draft/` - Draft documents
- `/.draft/` - Hidden draft folders

**Example:**
```
project/
├── doc/
│   ├── guides/              ✅ Published
│   ├── archive/             ❌ Excluded (automatic)
│   │   ├── old-guide.md
│   │   └── deprecated.md
│   └── draft/               ❌ Excluded (automatic)
│       └── wip-doc.md
```

## Usage Examples

### Example 1: Exclude Archive Folder

```bash
# All files in doc/archive/ are automatically excluded
mkdir -p doc/archive
mv old-docs/*.md doc/archive/
```

**Result:** 
- All files in `doc/archive/` won't appear in the generated site
- Sitemap won't include these pages
- Navigation menu won't show them

### Example 2: Mark Single File as Draft

```markdown
---
title: New Feature Documentation
publish: false
date: 2024-12-17
---

# New Feature

Work in progress...
```

**Result:** This specific file is excluded, even if it's in a published directory.

### Example 3: Temporary Exclusion

```markdown
# Breaking Changes Guide

__DO_NOT_PUBLISH__

**Note:** Remove tag above when ready to publish.

## Overview
...
```

**Benefit:** Easy to toggle on/off by adding/removing one line.

## Build Output

When documents are excluded, you'll see:

```bash
📝 Generating HTML pages...
  ✅ doc/guides/INSTALL.md
  ✅ doc/guides/USAGE.md
  ⏭️  Skipped (excluded): doc/archive/old-api.md
  ⏭️  Skipped (excluded): doc/draft/new-feature.md
  
✅ Generated 45/50 page(s)
⏭️  Skipped 5 excluded file(s)
```

## Exclusion Rules Summary

| Method | Priority | Use Case | Visibility |
|--------|----------|----------|-----------|
| Frontmatter `publish: false` | High | Individual files | Explicit |
| `__DO_NOT_PUBLISH__` tag | High | Quick toggle | Very visible |
| Path patterns | Medium | Bulk exclusion | Automatic |

## Best Practices

### 1. **Choose the Right Method**

- **Frontmatter:** For permanent exclusions or when you need structured metadata
- **Tag:** For temporary exclusions or visual prominence
- **Path:** For organizing many excluded documents

### 2. **Organize Archive/Draft Folders**

```
doc/
├── guides/          # Published
├── reference/       # Published  
├── archive/         # Automatically excluded
│   ├── 2023/
│   └── deprecated/
└── draft/           # Automatically excluded
    └── wip/
```

### 3. **Document Why Files Are Excluded**

```markdown
---
title: Legacy API Documentation
publish: false
archived: true
archived_reason: "Replaced by REST API v2"
archived_date: "2024-01-15"
---
```

### 4. **Use Exclusion for Sensitive Content**

```markdown
---
title: Internal Security Procedures
publish: false
internal_only: true
---

__DO_NOT_PUBLISH__

# Security Procedures

Confidential information...
```

## Integration with md-file-graph

The exclusion feature is built into the HTML generator:

```python
# Automatically called during generation
def should_publish(md_content: str, file_path: Path) -> bool:
    # Check frontmatter
    if post.get('publish') is False:
        return False
    
    # Check content tag
    if '__DO_NOT_PUBLISH__' in md_content:
        return False
    
    # Check path patterns
    if 'doc/archive' in relative_path:
        return False
    
    return True
```

## Custom Exclusion Patterns

To add custom exclusion patterns, edit the `html_generator.py`:

```python
excluded_patterns = [
    'doc/archive',
    '/archive/',
    '/draft/',
    '/internal/',    # Add your pattern
    '/private/',     # Add your pattern
]
```

## Verification

After building, verify exclusions:

```bash
# Build documentation
cd website && ./build-docs.sh

# Check what was excluded
grep "Skipped (excluded)" build.log

# Verify sitemap doesn't include excluded files
cat static/sitemap.xml | grep -i "archive"  # Should return nothing
```

## FAQ

**Q: Can I exclude an entire directory?**  
A: Yes, put it in `doc/archive/` or add the path pattern to the exclusion list.

**Q: What if I want to publish archived docs later?**  
A: Move them out of `doc/archive/` or remove the exclusion tag.

**Q: Are excluded files still in the repository?**  
A: Yes! Exclusion only affects the generated website, not Git.

**Q: Can I use both methods together?**  
A: Yes, but it's redundant. Choose the method that fits your workflow best.

**Q: Do excluded files count toward the total?**  
A: Yes, they're counted but marked as skipped in the build output.

## Summary

✅ **Three exclusion methods:** Frontmatter, content tag, path patterns  
✅ **Automatic exclusion:** `doc/archive/`, `/draft/` folders  
✅ **Build visibility:** See what's excluded in the build output  
✅ **SEO safe:** Excluded pages won't appear in sitemap or navigation  
✅ **Git friendly:** Exclusion is for generated site only  

Choose the method that works best for your workflow and document organization!
