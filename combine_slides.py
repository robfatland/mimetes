#!/usr/bin/env python3
"""
combine_slides.py — Merge multiple Marp slides.md files into one.

Rewrites relative image paths so they resolve from the repo root.
Strips front-matter from all files except the first (uses it as the
combined deck's front-matter). Inserts slide separators between files.

Usage:
    python3 combine_slides.py slides.md case_studies/*/slides.md > all_slides.md
"""

import re
import os
import sys


def strip_frontmatter(content):
    """Remove YAML front-matter (--- ... ---) from the top of a file."""
    match = re.match(r'^---\n.*?\n---\n', content, re.DOTALL)
    if match:
        return content[match.end():]
    return content


def rewrite_image_paths(content, directory):
    """Prefix relative image paths with the file's directory."""
    if not directory:
        return content
    # Match ![...](path) where path doesn't start with http
    def replacer(m):
        return m.group(1) + directory + '/' + m.group(2)
    return re.sub(r'(\!\[[^\]]*\]\()([^)]*\))', lambda m:
        m.group(0) if m.group(2).startswith('http') else
        m.group(1) + directory + '/' + m.group(2), content)


def main():
    if len(sys.argv) < 2:
        print("Usage: combine_slides.py file1.md [file2.md ...]", file=sys.stderr)
        sys.exit(1)

    files = sys.argv[1:]
    parts = []

    for i, filepath in enumerate(files):
        with open(filepath) as f:
            content = f.read()

        directory = os.path.dirname(filepath)

        if i == 0:
            # Keep front-matter from the first file
            content = rewrite_image_paths(content, directory)
        else:
            # Strip front-matter, rewrite paths, add separator
            content = strip_frontmatter(content)
            content = rewrite_image_paths(content, directory)
            # Ensure there's a slide separator before this deck's content
            if not content.startswith('\n---'):
                content = '\n---\n\n' + content.lstrip('\n')

        parts.append(content)

    print('\n'.join(parts))


if __name__ == '__main__':
    main()
