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


def latex_escape_url(url):
    """Escape a URL for use in LaTeX \\href — only escape %, #, and &."""
    if url is None:
        return ""
    url = str(url)
    # URLs need minimal escaping — just the chars that break LaTeX
    url = url.replace('%', r'\%')
    url = url.replace('#', r'\#')
    url = url.replace('&', r'\&')
    return url


def latex_escape_text(text):
    """Escape text for LaTeX (no link processing)."""
    if text is None:
        return ""
    text = str(text)
    # Replace Unicode symbols with placeholders BEFORE escaping
    # (placeholders won't be affected by special char escaping)
    placeholders = {
        '→': '\x00ARROW\x00',
        '—': '\x00EMDASH\x00',
        '–': '\x00ENDASH\x00',
        '\u2019': '\x00RSQUOTE\x00',
        '\u201C': '\x00LDQUOTE\x00',
        '\u201D': '\x00RDQUOTE\x00',
        '©': '\x00COPYRIGHT\x00',
        '®': '\x00REGISTERED\x00',
        '°': '\x00DEGREE\x00',
        '·': '\x00MIDDOT\x00',
        '•': '\x00BULLET\x00',
    }
    for char, placeholder in placeholders.items():
        text = text.replace(char, placeholder)
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
    text = text.replace(r'\textbackslash\{\}', r'\textbackslash{}')
    # Replace placeholders with LaTeX equivalents
    latex_replacements = {
        '\x00ARROW\x00': r'$\rightarrow$',
        '\x00EMDASH\x00': '---',
        '\x00ENDASH\x00': '--',
        '\x00RSQUOTE\x00': "'",
        '\x00LDQUOTE\x00': '``',
        '\x00RDQUOTE\x00': "''",
        '\x00COPYRIGHT\x00': r'\textcopyright{}',
        '\x00REGISTERED\x00': r'\textregistered{}',
        '\x00DEGREE\x00': r'\textdegree{}',
        '\x00MIDDOT\x00': r'\textperiodcentered{}',
        '\x00BULLET\x00': r'\textbullet{}',
    }
    for placeholder, replacement in latex_replacements.items():
        text = text.replace(placeholder, replacement)
    return text


def latex_escape(text):
    """Escape special LaTeX characters, converting markdown links to \\href."""
    if text is None:
        return ""
    text = str(text)

    # Convert markdown images ![alt](path) to \includegraphics — MUST be before link conversion
    def md_image_to_latex(match):
        alt = match.group(1)
        path = match.group(2)
        # Fix baseurl prefix — strip /resume/ to get relative path
        path = re.sub(r'^/resume/', '', path)
        return (r'\begin{center}' + '\n'
                r'\includegraphics[width=0.6\textwidth]{' + path + '}' + '\n'
                r'\end{center}')

    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', md_image_to_latex, text)

    # Convert markdown links [text](url){:attrs} to \href{url}{text}
    def md_link_to_href(match):
        link_text = match.group(1)
        url = match.group(2)
        return r'\href{' + latex_escape_url(url) + '}{' + latex_escape_text(link_text) + '}'

    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)(\{[^}]*\})?', md_link_to_href, text)

    # Convert HTML links <a href="url">text</a> to \href{url}{text}
    def html_link_to_href(match):
        url = match.group(1)
        link_text = match.group(2)
        return r'\href{' + latex_escape_url(url) + '}{' + latex_escape_text(link_text) + '}'

    text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>', html_link_to_href, text)

    # Remove kramdown attributes {:target="_blank"} etc (already handled above)
    text = re.sub(r'\{:[^}]*\}', '', text)
    # Remove markdown bold/italic markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)

    # Convert bullet list lines to LaTeX itemize items
    lines = text.split('\n')
    in_list = False
    result_lines = []
    for line in lines:
        stripped = line.lstrip()
        if re.match(r'^[-*]\s+', stripped):
            if not in_list:
                result_lines.append(r'\begin{itemize}')
                in_list = True
            item_text = re.sub(r'^[-*]\s+', '', stripped)
            # Don't double-escape lines that already have \href from link conversion
            if r'\href{' not in item_text:
                item_text = latex_escape_text(item_text)
            result_lines.append(r'  \item ' + item_text)
        else:
            if in_list:
                result_lines.append(r'\end{itemize}')
                in_list = False
            # Escape remaining text (but preserve \href and \includegraphics already inserted)
            if r'\href{' not in line and r'\includegraphics' not in line and r'\begin{center}' not in line and r'\end{center}' not in line:
                line = latex_escape_text(line)
            result_lines.append(line)
    if in_list:
        result_lines.append(r'\end{itemize}')
    text = '\n'.join(result_lines)

    return text.strip()


def latex_paragraphs(text):
    """Convert multi-paragraph text to LaTeX paragraph breaks.
    Preserves itemize environments intact."""
    if text is None:
        return ""
    # Don't split inside itemize environments
    # Just ensure paragraph breaks between non-list blocks
    paragraphs = re.split(r'\n\s*\n', text)
    return '\n\n'.join(p.strip() for p in paragraphs if p.strip())


def main():
    parser = argparse.ArgumentParser(description="Generate LaTeX resume from YAML data")
    parser.add_argument('--output', default='_site/downloads/McGarrah-Resume.tex',
                        help='Output .tex file path')
    parser.add_argument('--template', default='resume.tex.j2',
                        help='Template file in templates/ (default: resume.tex.j2)')
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
    template = env.get_template(args.template)
    from datetime import date
    rendered = template.render(
        sidebar=data.get('sidebar', {}),
        career_profile=data.get('career-profile', {}),
        education=data.get('education', {}),
        experiences=data.get('experiences', {}),
        certifications=data.get('certifications', {}),
        projects=data.get('projects', {}),
        publications=data.get('publications', {}),
        skills=data.get('skills', {}),
        generation_date=date.today().strftime('%B %d, %Y'),
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
