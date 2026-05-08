#!/usr/bin/env python3
"""Reorganize company logos into a consistent naming scheme.

Naming convention: {company}-{variant}.{ext}
- All lowercase, hyphens between words
- Variant describes the specific version (e.g., "mark", "shield", "classic-1990")
- Year suffix for era-specific logos when a newer version also exists

Directory structure:
  company-logos/          — Active logos used in the resume
  company-logos/original/ — Source files used to create cropped/modified versions
  company-logos/archive/  — Old low-quality logos kept for posterity
"""

import shutil
from pathlib import Path

LOGOS_DIR = Path("assets/images/company-logos")
ORIGINAL_DIR = LOGOS_DIR / "original"
ARCHIVE_DIR = LOGOS_DIR / "archive"

# Create subdirectories
ORIGINAL_DIR.mkdir(exist_ok=True)
ARCHIVE_DIR.mkdir(exist_ok=True)

# ============================================================
# ACTIVE LOGOS (top level) — used in the resume
# ============================================================
# Format: {company}-{variant}.{ext}
ACTIVE_RENAMES = {
    # Education
    "nc_state_classic_logo.svg": "ncsu-classic-1990.svg",
    "nc_state_athletic_logo.svg": "ncsu-block-s.svg",
    "georgia_tech_logo.svg": "georgia-tech.svg",
    "uncw_logo.svg": "uncw.svg",

    # Experience (chronological, most recent first)
    "envestnet_logo.svg": "envestnet.svg",
    "bluecrossnc_logo.png": "bcbsnc.png",
    "usps_eagle_logo.svg": "usps-eagle.svg",
    "akc_shield_v2.png": "akc-shield.png",
    "nc_dit_mark.png": "nc-dit.png",
    "measurement_inc_mark.svg": "measurement-inc.svg",
    "sas_logo.svg": "sas.svg",
    "nc_dor_mark.png": "nc-dor.png",
    "irs_logo.svg": "irs.svg",
    "bd_logo.svg": "bd.svg",
    "nc_community_colleges_logo.svg": "nc-community-colleges.svg",
    "tierpoint_logo.png": "tierpoint.png",
    "netiq_logo.png": "netiq.png",
    "nc_state_wordmark_2023.png": "ncsu-wordmark-2023.png",
    "interpath_communications_logo.png": "interpath.png",
    "nclive_logo_2000.jpg": "nclive-2000.jpg",
    "ziff_davis_zd_logo.svg": "ziff-davis-1990.svg",
    "roemer-weather_best_weather_inc_logo.jpg": "roemer-weather.jpg",

    # Additional logos (not primary but kept at top level)
    "seal_of_north_carolina.svg": "nc-seal.svg",
    "becton_dickinson_logo.svg": "bd-wordmark.svg",
    "springboard_hosting_logo.gif": "springboard-hosting-2004.gif",
}

# ============================================================
# ORIGINAL sources (moved to original/ subdirectory)
# These were used to create cropped/modified active logos
# ============================================================
ORIGINALS = {
    "american_kennel_club_logo.svg": "akc-full.svg",
    "measurement_incorporated_logo.svg": "measurement-inc-full.svg",
    "usps_logo.svg": "usps-full.svg",
    "nc_dit_logo.png": "nc-dit-full.png",
    "nc_dor_logo.png": "nc-dor-full.png",
    "nc_state_university_logo.svg": "ncsu-wordmark.svg",
    "nclive_logo.svg": "nclive-current.svg",
    "envestnet_logo.png": "envestnet.png",
    "ziff_davis_blue_logo.svg": "ziff-davis-modern.svg",
    "ziff-davis-publishing_logo.png": "ziff-davis-publishing.png",
    "hosted_solutions_logo.gif": "hosted-solutions-2004.gif",
}

# ============================================================
# ARCHIVE (old low-quality logos kept for posterity)
# ============================================================
ARCHIVE = {
    "envestnet_logo.jpg": "envestnet-old.jpg",
    "georgia_institute_of_technology.jpg": "georgia-tech-old.jpg",
    "north_carolina_state_university_logo.jpg": "ncsu-old.jpg",
    "bluecrossnc_logo.jpg": "bcbsnc-old.jpg",
    "nc_department_of_revenue_logo.jpg": "nc-dor-old.jpg",
    "state_of_north_carolina_logo.jpg": "nc-seal-old.jpg",
    "irs_logo.jpg": "irs-old.jpg",
    "sas_logo.jpg": "sas-old.jpg",
    "american_kennel_club_logo.jpg": "akc-old.jpg",
    "measurement_incorporated_logo.jpg": "measurement-inc-old.jpg",
    "ganymede_software_netiq_logo.jpg": "netiq-old.jpg",
    "bdbiosciences_logo.jpg": "bd-old.jpg",
    "nc_community_colleges_logo.jpg": "nc-community-colleges-old.jpg",
    "springboardhosting-tierpoint_logo.jpg": "tierpoint-old.jpg",
    "usps_logo.jpg": "usps-old.jpg",
}


def main():
    print("Logo Reorganization Plan")
    print("=" * 60)

    # Check all source files exist
    all_sources = list(ACTIVE_RENAMES.keys()) + list(ORIGINALS.keys()) + list(ARCHIVE.keys())
    missing = [f for f in all_sources if not (LOGOS_DIR / f).exists()]
    if missing:
        print(f"\nWARNING: {len(missing)} source files not found:")
        for f in missing:
            print(f"  - {f}")
        print()

    print(f"\nACTIVE (top level): {len(ACTIVE_RENAMES)} logos")
    for old, new in sorted(ACTIVE_RENAMES.items(), key=lambda x: x[1]):
        exists = "✓" if (LOGOS_DIR / old).exists() else "✗"
        print(f"  {exists} {old:45s} → {new}")

    print(f"\nORIGINAL (original/): {len(ORIGINALS)} source files")
    for old, new in sorted(ORIGINALS.items(), key=lambda x: x[1]):
        exists = "✓" if (LOGOS_DIR / old).exists() else "✗"
        print(f"  {exists} {old:45s} → original/{new}")

    print(f"\nARCHIVE (archive/): {len(ARCHIVE)} old logos")
    for old, new in sorted(ARCHIVE.items(), key=lambda x: x[1]):
        exists = "✓" if (LOGOS_DIR / old).exists() else "✗"
        print(f"  {exists} {old:45s} → archive/{new}")

    print(f"\n{'=' * 60}")
    print("Run with --execute to perform the moves")
    print("=" * 60)

    import sys
    if "--execute" in sys.argv:
        print("\nExecuting moves...")

        for old, new in ACTIVE_RENAMES.items():
            src = LOGOS_DIR / old
            dst = LOGOS_DIR / new
            if src.exists():
                shutil.copy2(src, dst)
                print(f"  Copied {old} → {new}")

        for old, new in ORIGINALS.items():
            src = LOGOS_DIR / old
            dst = ORIGINAL_DIR / new
            if src.exists():
                shutil.move(str(src), str(dst))
                print(f"  Moved {old} → original/{new}")

        for old, new in ARCHIVE.items():
            src = LOGOS_DIR / old
            dst = ARCHIVE_DIR / new
            if src.exists():
                shutil.move(str(src), str(dst))
                print(f"  Moved {old} → archive/{new}")

        # Remove old active files that were renamed (not moved)
        for old in ACTIVE_RENAMES.keys():
            src = LOGOS_DIR / old
            if src.exists() and old != ACTIVE_RENAMES[old]:
                src.unlink()
                print(f"  Removed old {old}")

        print("\nDone!")


if __name__ == "__main__":
    main()
