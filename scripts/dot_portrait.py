from PIL import Image
import math

INPUT = "assets/portrait.png"
OUTPUT = "assets/portrait.svg"

WIDTH = 300
HEIGHT = 300

# Load image
img = Image.open(INPUT).convert("L")

# Crop to square
side = min(img.size)
left = (img.width - side) // 2
top = (img.height - side) // 2

img = img.crop((left, top, left + side, top + side))
img = img.resize((WIDTH, HEIGHT))

# SVG settings
BACKGROUND = "#0D1117"
DOT_LIGHT = "#F0F6FC"
DOT_DARK = "#FF7B00"

# Create SVG
svg = []
svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'viewBox="0 0 {WIDTH} {HEIGHT}" '
    f'width="{WIDTH}" height="{HEIGHT}">'
)

svg.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND}"/>')

# Dot-matrix settings
spacing = 3
max_radius = 1.45

for y in range(0, HEIGHT, spacing):
    for x in range(0, WIDTH, spacing):

        brightness = img.getpixel((x, y)) / 255.0

        # Invert so darker parts of the photograph
        # become stronger/larger dots
        darkness = 1.0 - brightness

        radius = max_radius * (0.15 + darkness * 0.85)

        # Skip almost-empty areas
        if radius < 0.25:
            continue

        # Warm highlight for stronger facial areas
        if darkness > 0.55:
            opacity = 0.95
            fill = DOT_DARK
        else:
            opacity = 0.65 + darkness * 0.3
            fill = DOT_LIGHT

        svg.append(
            f'<circle cx="{x}" cy="{y}" '
            f'r="{radius:.2f}" '
            f'fill="{fill}" '
            f'opacity="{opacity:.2f}"/>'
        )

svg.append("</svg>")

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(svg))

print(f"Created {OUTPUT}")
