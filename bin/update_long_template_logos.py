#!/usr/bin/env python3
"""Show the mapping from anchor IDs to logo filenames for the long template."""

# This maps each anchor to its logo file in latex-logos/
# Used to build the logo lookup in the Jinja2 template

LOGO_MAP = {
    # Education
    "edu-uncw-2025": "uncw",
    "edu-gatech-2014": "georgia-tech",
    "edu-ncsu-1990": "ncsu-classic-1990",
    # Experience
    "envestnet-2021": "envestnet",
    "bcbsnc-2019": "bcbsnc",
    "usps-2017": "usps-eagle",
    "akc-2016": "akc-shield",
    "ncdit-2015": "nc-dit",
    "measurement-inc-2013": "measurement-inc",
    "sas-2011": "sas",
    "ncdor-2007": "nc-dor",
    "etaac-2009": "irs",
    "freeman-dds-1998": "freeman-dds",  # generic tooth icon
    "vr-aids-2001": "do2learn",  # Do2Learn tagline (VR Aids operated do2learn.com)
    "bd-2006": "bd",
    "ncccs-2005": "nc-community-colleges",
    "hosted-solutions-2004": "tierpoint",
    "netiq-2002": "netiq",
    "ncsu-2000": "ncsu-block-s",
    "interpath-2000": "interpath",
    "ncsu-nclive-1999": "nclive-2000",
    "ncsu-1998": "ncsu-block-s",
    "ziff-davis-1994": "ziff-davis-1990",
    "interpath-1998": "interpath",
    "db-basics-1994": "db-basics",  # generic database cylinder icon
    "pioneer-software-1992": "qe-software",
    "roemer-weather-1992": "roemer-weather",
    "ncsu-ta-1990": "ncsu-classic-1990",
    "ncsu-library-1990": "ncsu-classic-1990",
    "ncsu-operator-1990": "ncsu-classic-1990",
}

for anchor, logo in LOGO_MAP.items():
    status = f"latex-logos/{logo}.png" if logo else "PLACEHOLDER"
    print(f"  {anchor:30s} → {status}")
