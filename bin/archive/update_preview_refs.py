#!/usr/bin/env python3
"""Update preview.html to use the new logo filenames."""

from pathlib import Path

PREVIEW = Path("assets/images/company-logos/preview.html")

# Map old filenames to new filenames
RENAMES = {
    "akc_shield_v2.png": "akc-shield.png",
    "american_kennel_club_logo.svg": "akc-shield.png",
    "bluecrossnc_logo.png": "bcbsnc.png",
    "becton_dickinson_logo.svg": "bd-wordmark.svg",
    "bd_logo.svg": "bd.svg",
    "envestnet_logo.svg": "envestnet.svg",
    "envestnet_logo.png": "envestnet.svg",
    "georgia_tech_logo.svg": "georgia-tech.svg",
    "interpath_communications_logo.png": "interpath.png",
    "irs_logo.svg": "irs.svg",
    "irs_logo.jpg": "irs.svg",
    "measurement_inc_mark.svg": "measurement-inc.svg",
    "measurement_incorporated_logo.svg": "measurement-inc.svg",
    "nc_community_colleges_logo.svg": "nc-community-colleges.svg",
    "nc_dit_mark.png": "nc-dit.png",
    "nc_dit_logo.png": "nc-dit.png",
    "nc_dor_mark.png": "nc-dor.png",
    "nc_dor_logo.png": "nc-dor.png",
    "seal_of_north_carolina.svg": "nc-seal.svg",
    "nclive_logo_2000.jpg": "nclive-2000.jpg",
    "nclive_logo.svg": "nclive-2000.jpg",
    "nc_state_athletic_logo.svg": "ncsu-block-s.svg",
    "nc_state_classic_logo.svg": "ncsu-classic-1990.svg",
    "nc_state_wordmark_2023.png": "ncsu-wordmark-2023.png",
    "nc_state_university_logo.svg": "ncsu-block-s.svg",
    "netiq_logo.png": "netiq.png",
    "roemer-weather_best_weather_inc_logo.jpg": "roemer-weather.jpg",
    "sas_logo.svg": "sas.svg",
    "sas_logo.jpg": "sas.svg",
    "springboard_hosting_logo.gif": "springboard-hosting-2004.gif",
    "springboardhosting-tierpoint_logo.jpg": "tierpoint.png",
    "tierpoint_logo.png": "tierpoint.png",
    "uncw_logo.svg": "uncw.svg",
    "usps_eagle_logo.svg": "usps-eagle.svg",
    "usps_logo.svg": "usps-eagle.svg",
    "ziff_davis_zd_logo.svg": "ziff-davis-1990.svg",
    "ziff_davis_blue_logo.svg": "ziff-davis-1990.svg",
    "hosted_solutions_logo.gif": "springboard-hosting-2004.gif",
    "north_carolina_state_university_logo.jpg": "ncsu-classic-1990.svg",
    "ganymede_software_netiq_logo.jpg": "netiq.png",
    "bdbiosciences_logo.jpg": "bd.svg",
}

content = PREVIEW.read_text()

for old, new in RENAMES.items():
    content = content.replace(f'src="{old}"', f'src="{new}"')

PREVIEW.write_text(content)
print(f"Updated {sum(1 for old in RENAMES if old in PREVIEW.read_text())} references remaining (should be 0)")
print("Done.")
