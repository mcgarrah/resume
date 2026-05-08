#!/usr/bin/env python3
"""Generate the Open Graph social preview image (1200x630 PNG)."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
AVATAR_PATH = REPO_DIR / "assets" / "images" / "mcgarrah-profile-100x100.png"
OUTPUT_PATH = REPO_DIR / "assets" / "images" / "og-resume.png"

# Dimensions (Open Graph standard)
WIDTH = 1200
HEIGHT = 630

# Colors — sky/light blue background with white text
BG_START = (91, 163, 201)     # #5ba3c9 sky blue
BG_END = (61, 138, 181)       # #3d8ab5 slightly deeper blue
ACCENT = (255, 255, 255)      # white accents on light bg
TEXT_WHITE = (255, 255, 255)
TEXT_LIGHT = (232, 244, 250)   # #e8f4fa
TEXT_MUTED = (208, 232, 242)   # #d0e8f2


def create_gradient(width, height, start_color, end_color):
    """Create a diagonal gradient background."""
    img = Image.new("RGB", (width, height))
    for y in range(height):
        for x in range(width):
            factor = (x / width * 0.6 + y / height * 0.4)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * factor)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * factor)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * factor)
            img.putpixel((x, y), (r, g, b))
    return img


def create_circular_avatar(avatar_path, size):
    """Create a circular-cropped avatar with anti-aliased edges."""
    avatar = Image.open(avatar_path).convert("RGBA")
    avatar = avatar.resize((size, size), Image.LANCZOS)

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size - 1, size - 1), fill=255)

    output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    output.paste(avatar, (0, 0), mask)
    return output


def get_font(size, bold=False):
    """Load a system font at the given size."""
    font_paths_bold = [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    font_paths_regular = [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    paths = font_paths_bold if bold else font_paths_regular
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def main():
    print(f"Generating OG image: {WIDTH}x{HEIGHT}")

    # Create gradient background
    img = create_gradient(WIDTH, HEIGHT, BG_START, BG_END)
    draw = ImageDraw.Draw(img)

    # Top accent bar (thicker)
    draw.rectangle([(0, 0), (WIDTH, 6)], fill=(255, 255, 255, 100))

    # Layout: avatar on left, stacked text filling the right
    avatar_size = 200
    avatar_x = 80
    avatar_y = (HEIGHT - avatar_size) // 2

    # Avatar border ring
    ring_pad = 5
    draw.ellipse(
        [(avatar_x - ring_pad, avatar_y - ring_pad),
         (avatar_x + avatar_size + ring_pad, avatar_y + avatar_size + ring_pad)],
        outline=(255, 255, 255, 130), width=3
    )

    # Place avatar
    avatar = create_circular_avatar(AVATAR_PATH, avatar_size)
    img.paste(avatar, (avatar_x, avatar_y), avatar)

    # Text block — starts after avatar, uses remaining width
    text_x = avatar_x + avatar_size + 70

    # Name — large and dominant
    font_name = get_font(64, bold=True)
    draw.text((text_x, 120), "Michael McGarrah", fill=TEXT_WHITE, font=font_name)

    # Separator line
    draw.rectangle([(text_x, 200), (text_x + 500, 203)], fill=(255, 255, 255, 100))

    # Tagline — prominent
    font_tagline = get_font(34)
    draw.text((text_x, 225), "Engineering Leader", fill=TEXT_LIGHT, font=font_tagline)

    # Specializations — each on its own line for visual weight
    font_spec = get_font(26)
    specs = [
        "Enterprise Architecture",
        "AI / Machine Learning",
        "Cloud Platforms & Kubernetes",
    ]
    y = 285
    for spec in specs:
        draw.text((text_x, y), spec, fill=TEXT_MUTED, font=font_spec)
        y += 38

    # Bottom section — credentials summary
    font_creds = get_font(20)
    creds_y = 470
    draw.rectangle([(text_x, creds_y - 10), (text_x + 580, creds_y - 8)],
                   fill=(255, 255, 255, 60))

    creds = "30+ years  \u00b7  MS CS Georgia Tech  \u00b7  EMBA UNC Wilmington  \u00b7  AWS  \u00b7  ISC2 CC"
    draw.text((text_x, creds_y), creds, fill=TEXT_MUTED, font=font_creds)

    # URL at bottom
    font_url = get_font(22)
    draw.text((text_x, 530), "mcgarrah.org/resume", fill=TEXT_WHITE, font=font_url)

    # Bottom accent bar
    draw.rectangle([(0, HEIGHT - 6), (WIDTH, HEIGHT)], fill=(255, 255, 255, 100))

    # Save
    img.save(OUTPUT_PATH, "PNG", optimize=True)
    file_size = OUTPUT_PATH.stat().st_size
    print(f"Saved: {OUTPUT_PATH}")
    print(f"Size: {file_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
