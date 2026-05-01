# Company & University Logo Assets

Logo images used in the resume's experience and education sections.

## Inventory

### ✅ Present

| File | Organization | Notes |
|------|-------------|-------|
| `envestnet_logo.png` | Envestnet, Inc. | Use PNG (30K) — better quality than JPG |
| `envestnet_logo.jpg` | Envestnet, Inc. | Duplicate — prefer PNG above |
| `bluecrossnc_logo.jpg` | Blue Cross and Blue Shield of NC | |
| `usps_logo.jpg` | United States Postal Service | |
| `american_kennel_club_logo.jpg` | American Kennel Club | |
| `state_of_north_carolina_logo.jpg` | NC DIT / NC DOR / NC Community Colleges | Generic NC state seal — usable for all NC state agency roles |
| `nc_department_of_revenue_logo.jpg` | NC Department of Revenue | Agency-specific logo |
| `nc_community_colleges_logo.jpg` | NC Community College System | |
| `measurement_incorporated_logo.jpg` | Measurement Incorporated | |
| `sas_logo.jpg` | SAS Institute, Inc. | |
| `bdbiosciences_logo.jpg` | BD Biosciences | |
| `ganymede_software_netiq_logo.jpg` | NetIQ / Ganymede Software | Ganymede was acquired by NetIQ |
| `springboardhosting-tierpoint_logo.jpg` | Hosted Solutions / Springboard Hosting | Company was acquired by TierPoint |
| `interpath_communications_logo.png` | Interpath Communications | Defunct ISP — logo sourced from archive |
| `irs_logo.jpg` | IRS / ETAAC Subcommittee | Used for Congressional Subcommittee role |
| `roemer-weather_best_weather_inc_logo.jpg` | Roemer Weather, Inc. | |
| `ziff-davis-publishing_logo.png` | Ziff-Davis Publishing | |
| `north_carolina_state_university_logo.jpg` | NC State University | |
| `georgia_institute_of_technology.jpg` | Georgia Institute of Technology | Low resolution — see below |

### ❌ Missing

| Organization | Role | Suggested Source |
|-------------|------|-----------------|
| University of North Carolina Wilmington | Executive MBA | https://www.uncw.edu/marketing/brand.html |
| Georgia Institute of Technology (SVG) | MS Computer Science | https://brand.gatech.edu/our-brand/logos — replace low-res JPG |
| NC State University (SVG) | BS Computer Science | https://brand.ncsu.edu/downloads/ — replace low-res JPG |
| UNC Chapel Hill / NC LIVE | Dev/Ops Manager (NCSU NC LIVE role) | https://identity.unc.edu/brand-resources/ |
| Pioneer Software / Q+E / Intersolv / Merant | Technical Services Manager | Defunct — try Wikimedia Commons or skip |
| DB Basics, Inc. | Consultant | Defunct small company — skip |
| Ziff-Davis (current brand) | Benchmark Developer | ziffdavis.com press page — current logo differs from 1990s era |

## Quality Notes

- Several JPGs are very small (2–4KB) — likely low-resolution LinkedIn thumbnails. They may render poorly at larger sizes.
- Prefer SVG or high-resolution PNG from official brand kits where available.
- The `envestnet_logo.jpg` (2.2K) is noticeably lower quality than `envestnet_logo.png` (30K) — use the PNG.
- `georgia_institute_of_technology.jpg` (2.2K) is low resolution — replace with official SVG from Georgia Tech brand site.

## Official Brand Kit URLs

| Organization | Brand/Logo Download URL |
|-------------|------------------------|
| NC State University | https://brand.ncsu.edu/downloads/ |
| Georgia Institute of Technology | https://brand.gatech.edu/our-brand/logos |
| UNC Wilmington | https://www.uncw.edu/marketing/brand.html |
| UNC Chapel Hill | https://identity.unc.edu/brand-resources/ |
| SAS Institute | https://www.sas.com/en_us/news/press-releases.html (media kit) |
| USPS | https://about.usps.com/newsroom/media-resources/ |
| BD Biosciences | https://www.bd.com/en-us/about-bd/news-and-media |

## Lessons Learned

### Clearbit Logo API — Defunct
The Clearbit logo API (`https://logo.clearbit.com/<domain>`) was a convenient
free service for pulling company logos by domain. It no longer resolves — Clearbit
was acquired by HubSpot and the public logo API has been shut down. Do not attempt
to use it.

### LinkedIn Logos — Not Downloadable
LinkedIn company and university logos are proprietary assets. They cannot be
downloaded or redistributed. The logos currently in this directory were sourced
separately, not from LinkedIn.

### Defunct Companies
Several employers no longer exist (Interpath, Pioneer/Q+E, DB Basics, Roemer Weather,
Ganymede/NetIQ pre-acquisition). For these:
- Check [Wikimedia Commons](https://commons.wikimedia.org) for historical logos
- Check [archive.org](https://web.archive.org) for old company websites with logo assets
- If nothing usable is found, skip the logo — a missing logo is better than a broken image

### File Naming Convention
Use lowercase with hyphens: `company-name-logo.png`
Existing files use underscores — either convention is fine but be consistent going forward.

### Preferred Formats
1. SVG — scalable, smallest file, best for logos with flat design
2. PNG — good for logos with transparency
3. JPG — avoid for logos; compression artifacts look bad at small sizes
