#!/usr/bin/env python3
"""Add stable anchor IDs to section headers in all view templates.

Section anchors:
  #career-profile, #education, #experience, #certifications,
  #projects, #publications, #skills

These are added to both brief and print view includes.
"""

import re
from pathlib import Path

INCLUDES_DIR = Path("_includes")

# Map: (filename, section_id)
# Each file has an <h2 class="section-title"> that needs an id attribute
SECTIONS = [
    ("career-profile.html", "career-profile"),
    ("career-profile-print.html", "career-profile"),
    ("education.html", "education"),
    ("education-print.html", "education"),
    ("experiences.html", "experience"),
    ("experiences-print.html", "experience"),
    ("certifications.html", "certifications"),
    ("certifications-print.html", "certifications"),
    ("projects.html", "projects"),
    ("projects-print.html", "projects"),
    ("publications.html", "publications"),
    ("skills.html", "skills"),
]


def add_anchor(filename, section_id):
    filepath = INCLUDES_DIR / filename
    if not filepath.exists():
        print(f"  SKIP: {filename} not found")
        return

    content = filepath.read_text()

    # Check if already has the anchor
    if f'id="{section_id}"' in content:
        print(f"  SKIP: {filename} already has id=\"{section_id}\"")
        return

    # Find <h2 class="section-title"> and add id attribute
    # Handle both single-line and multi-line h2 tags
    old = '<h2 class="section-title">'
    new = f'<h2 class="section-title" id="{section_id}">'

    if old in content:
        content = content.replace(old, new, 1)
        filepath.write_text(content)
        print(f"  Added: {filename} → id=\"{section_id}\"")
    else:
        print(f"  WARN: {filename} — h2 pattern not found")


def main():
    print("Adding section anchors to includes:")
    for filename, section_id in SECTIONS:
        add_anchor(filename, section_id)
    print("\nDone.")


if __name__ == "__main__":
    main()
