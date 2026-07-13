from PIL import Image, ImageOps, ImageEnhance

SRC = "photo.jpeg"
OUT = "portrait.txt"

# Output width in characters. Height is derived from image aspect ratio,
# corrected for the fact that monospace glyphs are taller than they are wide.
WIDTH = 100
CHAR_ASPECT = 0.52  # width/height ratio of a typical monospace glyph cell

# Density ramp, darkest -> brightest. Index 0 renders as blank (matches a
# dark SVG background), the far end renders as the densest glyph.
RAMP = " .'`^,:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

im = Image.open(SRC).convert("L")

# Crop to a tighter portrait framing (subject is centered, shoulders up)
w, h = im.size
left = int(w * 0.02)
right = int(w * 0.98)
top = int(h * 0.0)
bottom = int(h * 0.92)
im = im.crop((left, top, right, bottom))

# Boost contrast a touch so facial features read clearly at low res
im = ImageOps.autocontrast(im, cutoff=1)
im = ImageEnhance.Contrast(im).enhance(1.15)

w, h = im.size
new_h = max(1, int((WIDTH * (h / w)) * CHAR_ASPECT))
im = im.resize((WIDTH, new_h), Image.LANCZOS)

pixels = im.load()
lines = []
n = len(RAMP) - 1
for y in range(new_h):
    row = []
    for x in range(WIDTH):
        v = pixels[x, y] / 255.0
        # dark pixel (shadow / edge / hair / feature) -> dense glyph
        # bright pixel (background / bright skin) -> sparse glyph / blank
        row.append(RAMP[int((1.0 - v) * n)])
    lines.append("".join(row))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {OUT}: {WIDTH}x{new_h} characters")
