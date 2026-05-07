#!/usr/bin/env python3
"""Generate LaTeX resume from _data/data.yml using Jinja2 template.

Usage:
    python bin/generate-latex.py [--output FILE] [--compile]

Options:
    --output FILE   Output .tex file path (default: _site/downloads/McGarrah-Resume.tex)
    --compile       Also compile to PDF using xelatex
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
import shutil

import yaml
from jinja2 import Environment, FileSystemLoader


def latex_escape(text):
    """Escape special LaTeX characters in text."""
    if text is None:
        return ""
    text = str(text)
    # Remove markdown links — convert [text](url) to text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)(\{[^}]*\})?', r'\1', text)
    # Remove HTML links — convert <a href="...">text</a> to text
    text = re.sub(r'<a[^>]*>([^<]*)</a>', r'\1', text)
    # Remove kramdown attributes {:target="_blank"} etc
    text = re.sub(r'\{:[^}]*\}', '', text)
    # Remove markdown bold/italic markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # Remove markdown image syntax ![alt](url)
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', text)
    # Remove bullet list markers at start of lines
    text = re.sub(r'^\s*[-*]\s+', '', text, flags=re.MULTILINE)
    # Escape LaTeX special characters (order matters)
    chars = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    for char, replacement in chars.items():
        text = text.replace(char, replacement)
    # Fix the textbackslash that got double-escaped
    text = text.replace(r'\textbackslash\{\}', r'\textbackslash{}')
    return text.strip()


def latex_paragraphs(text):
    """Convert multi-paragraph text to LaTeX paragraph breaks."""
    if text is None:
        return ""
    # Split on double newlines (paragraph breaks)
    paragraphs = re.split(r'\n\s*\n', text)
    return '\n\n'.join(p.strip() for p in paragraphs if p.strip())


def main():
    parser = argparse.ArgumentParser(description="Generate LaTeX resume from YAML data")
    parser.add_argument('--output', default='_site/downloads/McGarrah-Resume.tex',
                        help='Output .tex file path')
    parser.add_argument('--compile', action='store_true',
                        help='Compile to PDF using xelatex')
    args = parser.parse_args()

    # Load data
    data_file = '_data/data.yml'
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found. Run from the resume project root.", file=sys.stderr)
        sys.exit(1)

    with open(data_file, 'r') as f:
        data = yaml.safe_load(f)

    # Setup Jinja2 with LaTeX-friendly delimiters
    env = Environment(
        loader=FileSystemLoader('templates'),
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<#',
        comment_end_string='#>',
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Register custom filters
    env.filters['latex_escape'] = latex_escape
    env.filters['latex_paragraphs'] = latex_paragraphs
    env.filters['default'] = lambda value, default_value='': value if value else default_value

    # Load and render template
    template = env.get_template('resume.tex.j2')
    rendered = template.render(
        sidebar=data.get('sidebar', {}),
        career_profile=data.get('career-profile', {}),
        education=data.get('education', {}),
        experiences=data.get('experiences', {}),
        certifications=data.get('certifications', {}),
        projects=data.get('projects', {}),
        publications=data.get('publications', {}),
        skills=data.get('skills', {}),
    )

    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)

    # Write .tex file
    with open(args.output, 'w') as f:
        f.write(rendered)
    print(f"Generated: {args.output}")

    # Optionally compile to PDF
    if args.compile:
        compile_pdf(args.output)


def compile_pdf(tex_file):
    """Compile .tex to PDF using xelatex."""
    if not shutil.which('xelatex'):
        print("Warning: xelatex not found. Install TeX Live to compile PDF.", file=sys.stderr)
        print("  macOS: brew install --cask mactex", file=sys.stderr)
        print("  Ubuntu: apt-get install texlive-xetex texlive-fonts-recommended", file=sys.stderr)
        return

    output_dir = os.path.dirname(tex_file) or '.'
    basename = os.path.splitext(os.path.basename(tex_file))[0]

    # Run xelatex twice for cross-references
    for i in range(2):
        result = subprocess.run(
            ['xelatex', '-interaction=nonstopmode', '-output-directory', output_dir, tex_file],
            capture_output=True, text=True
        )
        if result.returncode != 0 and i == 1:
            print(f"Warning: xelatex returned non-zero exit code", file=sys.stderr)
            # Print last 20 lines of log for debugging
            log_file = os.path.join(output_dir, f"{basename}.log")
            if os.path.exists(log_file):
                with open(log_file) as f:
                    lines = f.readlines()
                    print("Last 20 lines of log:", file=sys.stderr)
                    for line in lines[-20:]:
                        print(f"  {line.rstrip()}", file=sys.stderr)

    pdf_file = os.path.join(output_dir, f"{basename}.pdf")
    if os.path.exists(pdf_file):
        print(f"Compiled: {pdf_file}")
    else:
        print(f"Error: PDF not generated", file=sys.stderr)


if __name__ == '__main__':
    main()
