"""
Deterministic (non-AI) blocking storyboard renderer for ogurasia page 8, v02.

Renders, on top of the exact panel geometry frozen in
docs/storyboards/ogurasia-page08-layout-lock-v01.png, only the elements
allowed at the "blocking" stage: circular heads with a gaze tick, a torso
line, minimal limb lines, simple-shaped props, and one empty speech-balloon
container per panel. No shading, no fill, no background, no text.

This is a fix for ogurasia-page08-blocking-v01.png (AI-generated, REJECTed
for two balloons in panel 1 and wrong balloon owner in panel 2). This script
places exactly one balloon per panel, with the owner fixed by hand below.

Run with: uv run --with pillow python3 tools/ogurasia_blocking_page08_v02.py
"""

import math
import os
from PIL import Image, ImageDraw

# ---------------------------------------------------------------------------
# Canvas & exact panel geometry (frozen by layout_lock v01 -- do not change)
# ---------------------------------------------------------------------------

CANVAS_W, CANVAS_H = 927, 1697
BORDER_STROKE = 3

PANELS = {
    "p08-c01": (9, 6, 918, 322),
    "p08-c02": (9, 369, 624, 794),
    "p08-c03": (641, 369, 918, 794),
    "p08-c04": (9, 841, 632, 1315),
    "p08-c05": (649, 841, 918, 1315),
    "p08-c06": (9, 1362, 918, 1686),
}

OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docs", "storyboards", "ogurasia-page08-blocking-v02.png",
)

# ---------------------------------------------------------------------------
# Figure proportions & stroke widths
# ---------------------------------------------------------------------------

FIGURE_STROKE = 5   # bolder than the 3px panel border, per spec
BALLOON_STROKE = 5

HEAD_FRAC = 0.22    # head diameter as a fraction of total figure height
TORSO_FRAC = 0.33   # neck-to-hip length as a fraction of total figure height
# remaining (1 - HEAD_FRAC - TORSO_FRAC) = 0.45 is hip-to-feet (legs)

# Two "shot scales" reused across panels, per the spec's instruction to
# define BOY_HEIGHT / JIA_HEIGHT constants per shot scale and reuse them.
# WIDE scale: the two full-width short panels (c01, c06), where both
# characters (or their implied conversational partner) share the frame.
WIDE_BOY_H = 130
WIDE_JIA_H = round(WIDE_BOY_H * 1.15)  # 150 -> ratio 1.1538

# TALL scale: the four taller solo panels (c02, c03, c04, c05).
TALL_BOY_H = 170
TALL_JIA_H = round(TALL_BOY_H * 1.15)  # 196 -> ratio 1.1529

print(f"[scale] WIDE_BOY_H={WIDE_BOY_H} WIDE_JIA_H={WIDE_JIA_H} "
      f"ratio={WIDE_JIA_H / WIDE_BOY_H:.4f}")
print(f"[scale] TALL_BOY_H={TALL_BOY_H} TALL_JIA_H={TALL_JIA_H} "
      f"ratio={TALL_JIA_H / TALL_BOY_H:.4f}")

img = Image.new("RGB", (CANVAS_W, CANVAS_H), "white")
draw = ImageDraw.Draw(img)

# Collected for the final plain-text report.
report = {}

# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------


def deg(angle_deg):
    return math.radians(angle_deg)


def point_at(cx, cy, angle_deg, length):
    r = deg(angle_deg)
    return (cx + math.cos(r) * length, cy + math.sin(r) * length)


def assert_in_panel(x, y, panel_box, label, pad=0):
    x0, y0, x1, y1 = panel_box
    ok = (x0 - pad) <= x <= (x1 + pad) and (y0 - pad) <= y <= (y1 + pad)
    if not ok:
        raise AssertionError(
            f"{label}: point ({x:.1f},{y:.1f}) falls outside panel "
            f"{panel_box} (pad={pad})"
        )


def layout_standing(panel_box, height, cx, feet_margin=20):
    """Compute key skeleton points for a standing figure of given total
    height, feet `feet_margin` px above the panel's bottom border, centered
    horizontally at `cx`."""
    x0, y0, x1, y1 = panel_box
    feet_y = y1 - feet_margin
    head_diam = height * HEAD_FRAC
    r = head_diam / 2
    torso_len = height * TORSO_FRAC
    top_y = feet_y - height           # top edge of the head circle
    head_cy = top_y + r
    neck_y = head_cy + r
    hip_y = neck_y + torso_len
    return {
        "cx": cx, "height": height, "r": r,
        "head_top_y": top_y, "head_center": (cx, head_cy),
        "neck": (cx, neck_y), "hip": (cx, hip_y), "feet": (cx, feet_y),
    }


def draw_stick_figure(dr, lay, gaze_deg, leg_offsets=None):
    """Draw head (outline circle), gaze tick, torso line and legs.
    leg_offsets, if given, is (front_dx, back_dx) applied to the two feet
    x-positions relative to hip (for a walking mid-stride pose); otherwise a
    symmetric standing inverted-V is used."""
    cx = lay["cx"]
    r = lay["r"]
    hcx, hcy = lay["head_center"]
    neck = lay["neck"]
    hip = lay["hip"]
    feet_y = lay["feet"][1]

    # torso
    dr.line([neck, hip], fill="black", width=FIGURE_STROKE)

    # legs
    if leg_offsets is None:
        spread = lay["height"] * 0.12
        dr.line([hip, (cx - spread, feet_y)], fill="black", width=FIGURE_STROKE)
        dr.line([hip, (cx + spread, feet_y)], fill="black", width=FIGURE_STROKE)
    else:
        front_dx, back_dx = leg_offsets
        dr.line([hip, (cx + front_dx, feet_y)], fill="black", width=FIGURE_STROKE)
        dr.line([hip, (cx + back_dx, feet_y - lay["height"] * 0.05)],
                fill="black", width=FIGURE_STROKE)

    # head (outline only)
    dr.ellipse([hcx - r, hcy - r, hcx + r, hcy + r], outline="black",
               width=FIGURE_STROKE)

    # gaze tick: short segment from the circle's edge outward, at gaze_deg
    tick_len = r * 0.6
    start = point_at(hcx, hcy, gaze_deg, r)
    end = point_at(hcx, hcy, gaze_deg, r + tick_len)
    dr.line([start, end], fill="black", width=FIGURE_STROKE)


def draw_ellipse_outline(dr, box, stroke=BALLOON_STROKE):
    dr.ellipse(box, fill="black")
    x0, y0, x1, y1 = box
    dr.ellipse([x0 + stroke, y0 + stroke, x1 - stroke, y1 - stroke], fill="white")


def octagon_points(box, chamfer_frac=0.18):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    c = chamfer_frac * min(w, h)
    return [
        (x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c),
        (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c),
    ]


def draw_octagon_outline(dr, box, stroke=BALLOON_STROKE, chamfer_frac=0.18):
    dr.polygon(octagon_points(box, chamfer_frac), fill="black")
    x0, y0, x1, y1 = box
    inner = (x0 + stroke, y0 + stroke, x1 - stroke, y1 - stroke)
    dr.polygon(octagon_points(inner, chamfer_frac), fill="white")


def draw_tail(dr, balloon_box, head_top_point, r, base_half_width=8):
    """Small triangle-notch tail: two converging lines from the balloon's
    bottom edge down to a point just above the head circle's top."""
    x0, y0, x1, y1 = balloon_box
    bx = (x0 + x1) / 2
    by = y1
    hx, hy = head_top_point
    tail_gap = max(6.0, r * 0.25)
    tip = (hx, hy - tail_gap)
    left_base = (bx - base_half_width, by)
    right_base = (bx + base_half_width, by)
    dr.line([left_base, tip], fill="black", width=BALLOON_STROKE)
    dr.line([right_base, tip], fill="black", width=BALLOON_STROKE)
    return tip


def octagon_balloon(dr, panel_box, head_top_point, r, size_mult=2.3):
    """Jia's balloon: chamfered-rectangle octagon, square bbox (aspect 1.0)."""
    hx, hy = head_top_point
    w = h = (2 * r) * size_mult
    tail_gap = max(6.0, r * 0.25)
    tail_len = max(10.0, r * 0.8)
    bottom_y = hy - tail_gap - tail_len
    top_y = bottom_y - h
    box = (hx - w / 2, top_y, hx + w / 2, bottom_y)
    assert_in_panel(box[0], box[1], panel_box, "octagon balloon top-left", pad=2)
    assert_in_panel(box[2], box[3], panel_box, "octagon balloon bottom-right", pad=2)
    draw_octagon_outline(dr, box)
    draw_tail(dr, box, head_top_point, r)
    return box


def cloud_balloon(dr, panel_box, head_top_point, r, size_mult=2.3):
    """Boy's balloon: two overlapping unequal circles (union outline), placed
    on a 45-degree diagonal so the union bounding box is exactly square
    (aspect 1.0), satisfying the 0.85-1.15 bbox aspect requirement -- a
    literal side-by-side horizontal placement of a 1.3x-radius pair computes
    to an aspect of ~1.6, which would violate that constraint. See deviation
    note in the final report."""
    hx, hy = head_top_point
    w = (2 * r) * size_mult
    big_r = w / 2.6
    small_r = big_r / 1.3
    overlap = small_r / 3
    center_dist = big_r + small_r - overlap
    delta = center_dist / math.sqrt(2)
    cx_mid = hx
    tail_gap = max(6.0, r * 0.25)
    tail_len = max(10.0, r * 0.8)
    # place so union bottom sits at bottom_y
    bottom_y_target = hy - tail_gap - tail_len
    cy_mid = bottom_y_target - big_r - delta / 2  # provisional, refined below

    big_c = (cx_mid - delta / 2, cy_mid - delta / 2)
    small_c = (cx_mid + delta / 2, cy_mid + delta / 2)

    # Union bbox
    left = min(big_c[0] - big_r, small_c[0] - small_r)
    right = max(big_c[0] + big_r, small_c[0] + small_r)
    top = min(big_c[1] - big_r, small_c[1] - small_r)
    bottom = max(big_c[1] + big_r, small_c[1] + small_r)

    # shift vertically so the union's bottom lands exactly at bottom_y_target
    shift = bottom_y_target - bottom
    big_c = (big_c[0], big_c[1] + shift)
    small_c = (small_c[0], small_c[1] + shift)
    top += shift
    bottom += shift

    box = (left, top, right, bottom)
    assert_in_panel(box[0], box[1], panel_box, "cloud balloon top-left", pad=2)
    assert_in_panel(box[2], box[3], panel_box, "cloud balloon bottom-right", pad=2)

    draw_ellipse_outline(dr, [big_c[0] - big_r, big_c[1] - big_r,
                               big_c[0] + big_r, big_c[1] + big_r])
    draw_ellipse_outline(dr, [small_c[0] - small_r, small_c[1] - small_r,
                               small_c[0] + small_r, small_c[1] + small_r])
    draw_tail(dr, box, head_top_point, r)
    return box


# ---------------------------------------------------------------------------
# Draw panel borders
# ---------------------------------------------------------------------------

for pid, box in PANELS.items():
    draw.rectangle(box, outline="black", width=BORDER_STROKE)
    report[pid] = {"figures": [], "balloon": None}

# ---------------------------------------------------------------------------
# p08-c01: Jia (left third, facing right) + Boy (right third, facing left).
# Only Jia has a balloon (octagon). Boy has none (this is the exact bug the
# rejected v01 had -- two balloons here / wrong owner).
# ---------------------------------------------------------------------------

box = PANELS["p08-c01"]
jia = layout_standing(box, WIDE_JIA_H, cx=box[0] + (box[2] - box[0]) * 0.20, feet_margin=18)
boy = layout_standing(box, WIDE_BOY_H, cx=box[0] + (box[2] - box[0]) * 0.80, feet_margin=18)
draw_stick_figure(draw, jia, gaze_deg=0)    # facing right, toward Boy
draw_stick_figure(draw, boy, gaze_deg=180)  # facing left, toward Jia
bal = octagon_balloon(draw, box, (jia["cx"], jia["head_top_y"]), jia["r"])
report["p08-c01"]["figures"] = [
    ("Jia", jia["head_center"], jia["r"]),
    ("Boy", boy["head_center"], boy["r"]),
]
report["p08-c01"]["balloon"] = ("Jia", "octagon", bal)
report["p08-c01"]["note"] = "Both standing full body; Jia (left) faces right toward Boy, Boy (right) faces left toward Jia; only Jia has a balloon."

# ---------------------------------------------------------------------------
# p08-c02: Boy alone, centered-left, partially-unfolded rod with vibration
# ticks. Only Boy has a balloon (cloud).
# ---------------------------------------------------------------------------

box = PANELS["p08-c02"]
boy = layout_standing(box, TALL_BOY_H, cx=box[0] + (box[2] - box[0]) * 0.35, feet_margin=20)

shoulder = (boy["cx"], boy["neck"][1] + 5)
hand = (boy["cx"] + boy["r"] * 2.0, boy["neck"][1] + (boy["hip"][1] - boy["neck"][1]) * 0.55)
draw.line([shoulder, hand], fill="black", width=FIGURE_STROKE)

mid_joint = point_at(hand[0], hand[1], -50, boy["r"] * 2.6)
tip = point_at(mid_joint[0], mid_joint[1], -100, boy["r"] * 1.8)
draw.line([hand, mid_joint], fill="black", width=FIGURE_STROKE)
draw.line([mid_joint, tip], fill="black", width=FIGURE_STROKE)

# vibration ticks near the rod tip: 3 short perpendicular dashes
seg_angle = math.degrees(math.atan2(tip[1] - mid_joint[1], tip[0] - mid_joint[0]))
for i in range(3):
    back = point_at(tip[0], tip[1], seg_angle + 180, i * 9 + 6)
    p1 = point_at(back[0], back[1], seg_angle + 90, 6)
    p2 = point_at(back[0], back[1], seg_angle - 90, 6)
    draw.line([p1, p2], fill="black", width=3)

gaze_angle = math.degrees(math.atan2(mid_joint[1] - boy["head_center"][1],
                                      mid_joint[0] - boy["head_center"][0]))
draw_stick_figure(draw, boy, gaze_deg=gaze_angle)
bal = cloud_balloon(draw, box, (boy["cx"], boy["head_top_y"]), boy["r"])
report["p08-c02"]["figures"] = [("Boy", boy["head_center"], boy["r"])]
report["p08-c02"]["balloon"] = ("Boy", "cloud", bal)
report["p08-c02"]["note"] = "Boy alone, centered-left, gazing at his partially-unfolded rod (two-segment bent line) with 3 small vibration ticks near the tip; cloud balloon above his head."

# ---------------------------------------------------------------------------
# p08-c03: Jia alone, tall narrow panel, facing left. Balloon = octagon.
# ---------------------------------------------------------------------------

box = PANELS["p08-c03"]
jia = layout_standing(box, TALL_JIA_H, cx=(box[0] + box[2]) / 2, feet_margin=20)
draw_stick_figure(draw, jia, gaze_deg=180)
bal = octagon_balloon(draw, box, (jia["cx"], jia["head_top_y"]), jia["r"])
report["p08-c03"]["figures"] = [("Jia", jia["head_center"], jia["r"])]
report["p08-c03"]["balloon"] = ("Jia", "octagon", bal)
report["p08-c03"]["note"] = "Jia alone, centered, facing left toward Boy's panel; octagon balloon above her head."

# ---------------------------------------------------------------------------
# p08-c04: Boy alone, fully-extended rod reaching to the upper-left, small
# hook at the end. Balloon = cloud.
# ---------------------------------------------------------------------------

box = PANELS["p08-c04"]
boy = layout_standing(box, TALL_BOY_H, cx=box[0] + (box[2] - box[0]) * 0.55, feet_margin=20)

shoulder = (boy["cx"], boy["neck"][1] + 5)
hand = (boy["cx"] + boy["r"] * 1.6, boy["neck"][1] + (boy["hip"][1] - boy["neck"][1]) * 0.5)
draw.line([shoulder, hand], fill="black", width=FIGURE_STROKE)

rod_end = (box[0] + (box[2] - box[0]) * 0.12, box[1] + (box[3] - box[1]) * 0.10)
draw.line([hand, rod_end], fill="black", width=FIGURE_STROKE)
# small hook: short arc near the line's end
hook_r = boy["r"] * 0.3
hook_box = [rod_end[0] - hook_r, rod_end[1], rod_end[0] + hook_r, rod_end[1] + hook_r * 2]
draw.arc(hook_box, start=200, end=340, fill="black", width=4)

gaze_angle = math.degrees(math.atan2(rod_end[1] - boy["head_center"][1],
                                      rod_end[0] - boy["head_center"][0]))
draw_stick_figure(draw, boy, gaze_deg=gaze_angle)
bal = cloud_balloon(draw, box, (boy["cx"], boy["head_top_y"]), boy["r"])
report["p08-c04"]["figures"] = [("Boy", boy["head_center"], boy["r"])]
report["p08-c04"]["balloon"] = ("Boy", "cloud", bal)
report["p08-c04"]["note"] = "Boy alone, holding a fully-extended rod (long diagonal line to a small hook near the panel's upper-left), gazing along the line; cloud balloon above his head."

# ---------------------------------------------------------------------------
# p08-c05: Jia alone, one arm raised with an open-hand gesture. Balloon =
# octagon.
# ---------------------------------------------------------------------------

box = PANELS["p08-c05"]
jia = layout_standing(box, TALL_JIA_H, cx=(box[0] + box[2]) / 2, feet_margin=20)

shoulder = (jia["cx"], jia["neck"][1] + 5)
hand = point_at(shoulder[0], shoulder[1], -60, jia["height"] * 0.35)
draw.line([shoulder, hand], fill="black", width=FIGURE_STROKE)
# open-hand gesture: 3 short splayed segments at the wrist end
for a in (-30, 0, 30):
    tip_pt = point_at(hand[0], hand[1], -60 + a, jia["r"] * 0.45)
    draw.line([hand, tip_pt], fill="black", width=3)

draw_stick_figure(draw, jia, gaze_deg=180)
bal = octagon_balloon(draw, box, (jia["cx"], jia["head_top_y"]), jia["r"])
report["p08-c05"]["figures"] = [("Jia", jia["head_center"], jia["r"])]
report["p08-c05"]["balloon"] = ("Jia", "octagon", bal)
report["p08-c05"]["note"] = "Jia alone, facing left, one arm raised with a splayed open-hand gesture; octagon balloon above her head."

# ---------------------------------------------------------------------------
# p08-c06: Jia and Boy walking together (mid-stride), Boy's rod now folded
# and resting over his shoulder. Only Boy has a balloon (cloud, he speaks).
# ---------------------------------------------------------------------------

box = PANELS["p08-c06"]
jia = layout_standing(box, WIDE_JIA_H, cx=box[0] + (box[2] - box[0]) * 0.35, feet_margin=18)
boy = layout_standing(box, WIDE_BOY_H, cx=box[0] + (box[2] - box[0]) * 0.62, feet_margin=25)

draw_stick_figure(draw, jia, gaze_deg=0,
                   leg_offsets=(jia["height"] * 0.18, -jia["height"] * 0.08))
draw_stick_figure(draw, boy, gaze_deg=0,
                   leg_offsets=(boy["height"] * 0.18, -boy["height"] * 0.08))

shoulder = (boy["cx"], boy["neck"][1] + 5)
rod_end = point_at(shoulder[0], shoulder[1], -150, boy["height"] * 0.4)
draw.line([shoulder, rod_end], fill="black", width=FIGURE_STROKE)

bal = cloud_balloon(draw, box, (boy["cx"], boy["head_top_y"]), boy["r"])
report["p08-c06"]["figures"] = [
    ("Jia", jia["head_center"], jia["r"]),
    ("Boy", boy["head_center"], boy["r"]),
]
report["p08-c06"]["balloon"] = ("Boy", "cloud", bal)
report["p08-c06"]["note"] = "Both walking together mid-stride (Jia left, Boy slightly staggered right), facing/traveling right; Boy's rod now folded, resting diagonally over his shoulder; cloud balloon above his head."

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
img.save(OUTPUT_PATH)
print(f"[saved] {OUTPUT_PATH} size={img.size}")
assert img.size == (CANVAS_W, CANVAS_H), "output canvas size mismatch"

# ---------------------------------------------------------------------------
# Self-verification: re-measure the panel borders from the rendered PNG and
# compare against the target geometry (rows/cols where >30% of pixels in the
# panel's own band are dark), same method used to originally measure
# layout_lock v01.
# ---------------------------------------------------------------------------


def measure_panel(gray_bytes, w, h, box, search=6, dark=128, frac_thresh=0.30):
    x0, y0, x1, y1 = box

    def row_frac(y, xa, xb):
        cnt = 0
        base = y * w
        for x in range(xa, xb + 1):
            if gray_bytes[base + x] < dark:
                cnt += 1
        return cnt / (xb - xa + 1)

    def col_frac(x, ya, yb):
        cnt = 0
        for y in range(ya, yb + 1):
            if gray_bytes[y * w + x] < dark:
                cnt += 1
        return cnt / (yb - ya + 1)

    top = next((y for y in range(max(0, y0 - search), min(h, y0 + search + 1))
                if row_frac(y, x0, x1) > frac_thresh), None)
    bottom = next((y for y in range(min(h - 1, y1 + search), max(-1, y1 - search - 1), -1)
                   if row_frac(y, x0, x1) > frac_thresh), None)
    left = next((x for x in range(max(0, x0 - search), min(w, x0 + search + 1))
                 if col_frac(x, y0, y1) > frac_thresh), None)
    right = next((x for x in range(min(w - 1, x1 + search), max(-1, x1 - search - 1), -1)
                  if col_frac(x, y0, y1) > frac_thresh), None)
    return left, top, right, bottom


gray = img.convert("L")
gray_bytes = gray.tobytes()
W, H = gray.size

print("\n=== panel bbox verification (vs. locked layout_lock v01 geometry) ===")
all_pass = True
for pid, target in PANELS.items():
    measured = measure_panel(gray_bytes, W, H, target)
    tol = 2
    ok = all(m is not None and abs(m - t) <= tol for m, t in zip(measured, target))
    all_pass = all_pass and ok
    status = "PASS" if ok else "FAIL"
    print(f"{pid}: target={target} measured={measured} -> {status}")
print(f"=== overall: {'ALL PANELS PASS' if all_pass else 'SOME PANELS FAILED'} ===\n")

# ---------------------------------------------------------------------------
# Plain-text per-panel report
# ---------------------------------------------------------------------------

print("=== per-panel content report ===")
for pid in PANELS:
    r = report[pid]
    print(f"\n{pid}:")
    for name, center, radius in r["figures"]:
        print(f"  figure {name}: head_center=({center[0]:.1f},{center[1]:.1f}) "
              f"head_radius={radius:.1f}")
    owner, shape, bbox = r["balloon"]
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    print(f"  balloon: owner={owner} shape={shape} bbox=({bbox[0]:.1f},{bbox[1]:.1f})-"
          f"({bbox[2]:.1f},{bbox[3]:.1f}) aspect={w / h:.3f}")
    print(f"  balloon count in panel: 1 (confirmed by construction)")
    print(f"  note: {r['note']}")
