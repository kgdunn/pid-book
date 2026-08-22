#!/usr/bin/env python3
"""
Extract text from Design of Experiments .rst files, excluding comments.
"""

import os
import re
from pathlib import Path

def is_comment_start(line):
    """Check if line starts a reStructuredText comment."""
    stripped = line.lstrip()
    # Comments start with .. but are NOT directives (which have :: after the directive name)
    if stripped.startswith('.. '):
        # Check if it's a directive (has :: somewhere in the directive line)
        # Common directives: code-block, figure, image, note, warning, etc.
        directive_pattern = r'^\.\.\s+[\w-]+::'
        if re.match(directive_pattern, stripped):
            return False  # It's a directive, not a comment
        return True  # It's a comment
    return False

def get_indentation(line):
    """Get the indentation level of a line."""
    return len(line) - len(line.lstrip())

def extract_text_from_rst(file_path):
    """Extract text from RST file, excluding comments."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if is_comment_start(line):
            # Skip this comment block
            comment_indent = get_indentation(line)
            i += 1
            # Skip all following lines that are part of the comment block
            while i < len(lines):
                next_line = lines[i]
                # Empty lines are part of the comment
                if next_line.strip() == '':
                    i += 1
                    continue
                # Lines with greater indentation are part of the comment
                if get_indentation(next_line) > comment_indent:
                    i += 1
                    continue
                # Otherwise, we've exited the comment block
                break
        else:
            output_lines.append(line)
            i += 1

    return ''.join(output_lines)

def main():
    """Extract all DOE chapter text."""
    base_dir = Path('/home/user/pid-book/design-analysis-experiments')

    # Get all .rst files in the directory and subdirectories
    rst_files = sorted(base_dir.rglob('*.rst'))

    output_file = Path('/home/user/pid-book/doe_extracted_text.txt')

    with open(output_file, 'w', encoding='utf-8') as out:
        for rst_file in rst_files:
            out.write(f"\n{'='*80}\n")
            out.write(f"FILE: {rst_file.relative_to(base_dir.parent)}\n")
            out.write(f"{'='*80}\n\n")

            text = extract_text_from_rst(rst_file)
            out.write(text)
            out.write("\n\n")

    print(f"Extracted text from {len(rst_files)} files")
    print(f"Output written to: {output_file}")

    # Also print some statistics
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
        word_count = len(content.split())
        char_count = len(content)
        line_count = len(content.split('\n'))

    print(f"\nStatistics:")
    print(f"  Lines: {line_count:,}")
    print(f"  Words: {word_count:,}")
    print(f"  Characters: {char_count:,}")

if __name__ == '__main__':
    main()
