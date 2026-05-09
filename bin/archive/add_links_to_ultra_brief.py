#!/usr/bin/env python3
"""Add anchor links from ultra-brief entries to the full print resume.

Each job title becomes a link to mcgarrah.org/resume/print/#anchor-id
"""

import re
from pathlib import Path

ULTRA_BRIEF = Path("ultra-brief.html")

# Map entry titles (partial match) to anchor IDs
LINKS = {
    "Lead Principal Engineer": "envestnet-2021",
    "Principal Data &amp; Analytics": "bcbsnc-2019",
    "Data Engineer": "usps-2017",
    "Cloud Architect": "akc-2016",
    "Enterprise Architect for Strategic": "ncdit-2015",
    "Senior Systems Programmer &amp; Administrator": "measurement-inc-2013",
    "Systems Administrator": "sas-2011",
    "Application and Network Security": "ncdor-2007",
    "Congressional Subcommittee": "etaac-2009",
    "IT Engineer (IT Director)": "bd-2006",
    "Systems Programmer</span>": "ncccs-2005",  # exact to avoid matching "Systems Programmer II"
    "Systems Engineer": "hosted-solutions-2004",
    "UNIX Engineer": "netiq-2002",
    "Development Manager / Operations Manager": "ncsu-nclive-1999",
    "Application Analyst Programmer": "ncsu-1998",
    "Benchmark Developer": "ziff-davis-1994",
    "Senior Operations Technician": "interpath-2000",
}

content = ULTRA_BRIEF.read_text()

base_url = "https://mcgarrah.org/resume/print/"

for title_fragment, anchor in LINKS.items():
    # Find: <span class="entry-title">...title...</span>
    # Replace with: <a href="...#anchor" ...><span ...>title</span></a>
    # Actually simpler: just wrap the text content in a link
    old = f'<span class="entry-title">{title_fragment}'
    if old in content:
        # Don't double-wrap if already linked
        if f'<a href="{base_url}#{anchor}"' not in content:
            new = f'<a href="{base_url}#{anchor}" style="color: inherit; text-decoration: none;"><span class="entry-title">{title_fragment}'
            # Find the closing </span> for this entry-title
            content = content.replace(old, new, 1)
            # Now close the <a> after the </span>
            # Find the first </span> after our insertion point
            idx = content.find(new)
            span_close = content.find('</span>', idx)
            if span_close > 0:
                content = content[:span_close+7] + '</a>' + content[span_close+7:]
            print(f"  Linked: {title_fragment[:40]} → #{anchor}")
    else:
        print(f"  NOT FOUND: {title_fragment[:40]}")

ULTRA_BRIEF.write_text(content)
print(f"\nDone.")
