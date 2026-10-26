"""Render p08's first deterministic guide_mock: six empty balloons only.

Run with: uv run --with pillow --with pyyaml python3 tools/ogurasia_guide_mock_page08_v01.py
"""

from pathlib import Path
import re

import yaml
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
PAGE_SPEC = ROOT / "docs/storyboards/pages/p08.md"
BASE_IMAGE = ROOT / "docs/storyboards/ogurasia-page08-layout-lock-v01.png"
OUTPUT = ROOT / "docs/storyboards/ogurasia-page08-guide-mock-v01.png"
STROKE = 5


def page_panels():
    text = PAGE_SPEC.read_text(encoding="utf-8")
    match = re.search(r"```yaml\s*(.*?)\s*```", text, re.S)
    if not match:
        raise ValueError(f"No canonical YAML block found in {PAGE_SPEC}")
    return yaml.safe_load(match.group(1))["panels"]


def octagon_points(box):
    x0, y0, x1, y1 = box
    chamfer = 0.18 * min(x1 - x0, y1 - y0)
    return [(x0 + chamfer, y0), (x1 - chamfer, y0), (x1, y0 + chamfer),
            (x1, y1 - chamfer), (x1 - chamfer, y1), (x0 + chamfer, y1),
            (x0, y1 - chamfer), (x0, y0 + chamfer)]


def draw_octagon(draw, box):
    draw.polygon(octagon_points(box), fill="black")
    x0, y0, x1, y1 = box
    inset = STROKE
    inner = (x0 + inset, y0 + inset, x1 - inset, y1 - inset)
    draw.polygon(octagon_points(inner), fill="white")


def draw_cloud(draw, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if abs(w - h) > 0.2:
        raise ValueError(f"Boy cloud bbox must be square, got {w:.2f}x{h:.2f}")

    # Invert blocking v02's exact cloud construction from its union bbox.
    # The larger radius is 1.3x the smaller; centers are separated diagonally
    # by (big_r + small_r - small_r/3) / sqrt(2).
    ratio = 1.3
    small_per_big = 1 / ratio
    delta_per_big = (1 + small_per_big - small_per_big / 3) / (2 ** 0.5)
    union_per_big = 1 + small_per_big + delta_per_big
    big_r = (w + h) / 2 / union_per_big
    small_r = big_r / ratio
    delta = big_r + small_r - small_r / 3
    diagonal = delta / (2 ** 0.5)
    # The large lobe defines the top-left union extrema; the small lobe
    # defines the bottom-right extrema, exactly as in blocking v02.
    big_cx, big_cy = x0 + big_r, y0 + big_r
    small_cx, small_cy = big_cx + diagonal, big_cy + diagonal
    ellipses = (
        (big_cx - big_r, big_cy - big_r, big_cx + big_r, big_cy + big_r),
        (small_cx - small_r, small_cy - small_r, small_cx + small_r, small_cy + small_r),
    )
    for ellipse in ellipses:
        draw.ellipse(ellipse, fill="black")
        draw.ellipse((ellipse[0] + STROKE, ellipse[1] + STROKE,
                      ellipse[2] - STROKE, ellipse[3] - STROKE), fill="white")


def draw_tail(draw, box, tip):
    x0, y0, x1, y1 = box
    bx = (x0 + x1) / 2
    half = 8
    # White out the base seam, then draw the two sides of the single downward tail.
    draw.line([(bx - half, y1), tip, (bx + half, y1)], fill="white", width=STROKE + 2)
    draw.line([(bx - half, y1), tip], fill="black", width=STROKE)
    draw.line([(bx + half, y1), tip], fill="black", width=STROKE)


def main():
    image = Image.open(BASE_IMAGE).convert("RGB")
    if image.size != (927, 1697):
        raise ValueError(f"layout_lock canvas must be 927x1697, got {image.size}")
    draw = ImageDraw.Draw(image)
    entries = []
    for panel in page_panels():
        panel_id = panel["panel_id"]
        for dialogue in panel.get("dialogue", []):
            geometry = dialogue["balloon_geometry"]
            box = tuple(float(v) for v in geometry["bbox"])
            tip = tuple(float(v) for v in geometry["tail_tip"])
            if dialogue["speaker"] == "jia":
                draw_octagon(draw, box)
            elif dialogue["speaker"] == "boy":
                draw_cloud(draw, box)
            else:
                raise ValueError(f"Unexpected speaker in {panel_id}: {dialogue['speaker']}")
            draw_tail(draw, box, tip)
            entries.append((panel_id, dialogue["speaker"], box, tip))
    if len(entries) != 6:
        raise ValueError(f"Expected six dialogue balloons, got {len(entries)}")
    image.save(OUTPUT)
    print(f"[saved] {OUTPUT} size={image.size}")
    for panel_id, speaker, box, tip in entries:
        print(f"{panel_id}: owner={speaker} bbox={box} tail_tip={tip}")


if __name__ == "__main__":
    main()
