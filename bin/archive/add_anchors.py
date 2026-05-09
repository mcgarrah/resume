#!/usr/bin/env python3
"""Add stable anchor IDs to experience and education entries in data.yml.

These anchors are used for internal linking from the ultra-brief PDF
to the full interactive resume. Once published, they MUST NOT change
without explicit override — external documents link to them.

Convention: {company-slug}-{start-year}
"""

import re
from pathlib import Path

DATA_FILE = Path("_data/data.yml")

# Mapping of (role, company) → anchor ID
# Order matches the data.yml experience entries
EXPERIENCE_ANCHORS = [
    ("Lead Principal Engineer", "envestnet-2021"),
    ("Principal Data & Analytics Platform Engineer", "bcbsnc-2019"),
    ("Data Engineer", "usps-2017"),
    ("Cloud Architect", "akc-2016"),
    ("Enterprise Architect for Strategic Initiatives", "ncdit-2015"),
    ("Senior Systems Programmer & Administrator (AI Technologies)", "measurement-inc-2013"),
    ("Systems Administrator", "sas-2011"),
    ("Application and Network Security Specialist", "ncdor-2007"),
    ("Congressional Subcommittee Member", "etaac-2009"),
    ("Consultant (part-time as needed)", "freeman-dds-1998"),  # first one (Dr. Freeman)
    ("Consultant (part-time as needed)", "vr-aids-2001"),      # second one (VR Aids)
    ("IT Engineer (IT Director)", "bd-2006"),
    ("Systems Programmer", "ncccs-2005"),
    ("Systems Engineer", "hosted-solutions-2004"),
    ("UNIX Engineer", "netiq-2002"),
    ("Systems Programmer II", "ncsu-2000"),
    ("Senior Operations Technician in NOC", "interpath-2000"),
    ("Development Manager / Operations Manager", "ncsu-nclive-1999"),
    ("Application Analyst Programmer", "ncsu-1998"),
    ("Benchmark Developer", "ziff-davis-1994"),
    ("Operations Technician / Technical Writer", "interpath-1998"),
    ("Consultant (full-time)", "db-basics-1994"),
    ("Technical Services Manager", "pioneer-software-1992"),
    ("Computer Consultant (part-time)", "roemer-weather-1992"),
    ("Teaching Assistant", "ncsu-ta-1990"),
    ("Consultant for Library Systems", "ncsu-library-1990"),
    ("Computer Operator", "ncsu-operator-1990"),
]

EDUCATION_ANCHORS = [
    ("Executive Masters", "edu-uncw-2025"),
    ("Masters of Science", "edu-gatech-2014"),
    ("Bachelor of Science", "edu-ncsu-1990"),
]


def add_anchors():
    content = DATA_FILE.read_text()
    lines = content.split('\n')
    
    # Track which anchors we've used (for duplicate role names)
    anchor_iter = iter(EXPERIENCE_ANCHORS)
    edu_iter = iter(EDUCATION_ANCHORS)
    
    new_lines = []
    i = 0
    exp_anchor_idx = 0
    edu_anchor_idx = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is an experience role line
        if re.match(r'\s+- role:', line) and exp_anchor_idx < len(EXPERIENCE_ANCHORS):
            role_prefix, anchor_id = EXPERIENCE_ANCHORS[exp_anchor_idx]
            if role_prefix in line:
                new_lines.append(line)
                # Check if next line is already 'anchor:'
                if i + 1 < len(lines) and 'anchor:' in lines[i + 1]:
                    # Already has anchor, skip
                    i += 1
                    new_lines.append(lines[i])
                else:
                    # Insert anchor line after role line
                    indent = re.match(r'(\s+)', line).group(1) + '  '
                    new_lines.append(f'{indent}anchor: "{anchor_id}"')
                exp_anchor_idx += 1
                i += 1
                continue
        
        # Check if this is an education degree line
        if re.match(r'\s+- degree:', line) and edu_anchor_idx < len(EDUCATION_ANCHORS):
            degree_prefix, anchor_id = EDUCATION_ANCHORS[edu_anchor_idx]
            if degree_prefix in line:
                new_lines.append(line)
                if i + 1 < len(lines) and 'anchor:' in lines[i + 1]:
                    i += 1
                    new_lines.append(lines[i])
                else:
                    indent = re.match(r'(\s+)', line).group(1) + '  '
                    new_lines.append(f'{indent}anchor: "{anchor_id}"')
                edu_anchor_idx += 1
                i += 1
                continue
        
        new_lines.append(line)
        i += 1
    
    DATA_FILE.write_text('\n'.join(new_lines))
    print(f"Added {exp_anchor_idx} experience anchors and {edu_anchor_idx} education anchors")


if __name__ == "__main__":
    add_anchors()
