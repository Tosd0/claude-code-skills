#!/usr/bin/env python3
"""Fetch GitHub clone traffic, merge into historical JSON, generate SVG chart."""

import json
import subprocess
import os
from pathlib import Path

REPO = os.environ.get("GITHUB_REPOSITORY", "lldxflwb/claude-code-skills")
DATA_DIR = Path(__file__).resolve().parent.parent / "traffic"
DATA_FILE = DATA_DIR / "clones.json"
SVG_FILE = DATA_DIR / "clones.svg"


def fetch_clones():
    """Fetch clone data from GitHub API via gh CLI."""
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/traffic/clones"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"gh api failed (exit {result.returncode}): {result.stderr.strip()}")
        raise SystemExit(1)
    return json.loads(result.stdout)


def load_history():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {}


def merge(history, fresh):
    """Merge fresh API data into history. Key = date string."""
    for entry in fresh.get("clones", []):
        date = entry["timestamp"][:10]  # "2026-03-13"
        count = entry["count"]
        uniques = entry["uniques"]
        if count == 0 and date not in history:
            continue  # skip zero days we haven't seen
        history[date] = {"count": count, "uniques": uniques}
    return history


def generate_svg(history):
    """Generate a minimal SVG line chart."""
    if not history:
        return

    dates = sorted(history.keys())
    counts = [history[d]["count"] for d in dates]
    uniques = [history[d]["uniques"] for d in dates]

    # Chart dimensions
    w, h = 720, 260
    pad_l, pad_r, pad_t, pad_b = 45, 20, 30, 50
    chart_w = w - pad_l - pad_r
    chart_h = h - pad_t - pad_b

    n = len(dates)
    max_val = max(max(counts), 1)

    def x(i):
        return pad_l + (i / max(n - 1, 1)) * chart_w

    def y(v):
        return pad_t + chart_h - (v / max_val) * chart_h

    # Build polyline points
    count_points = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(counts))
    unique_points = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(uniques))

    font = "font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"

    # Y-axis ticks (5 ticks)
    y_ticks = []
    for i in range(5):
        val = round(max_val * i / 4)
        yy = y(val)
        y_ticks.append(
            f'<text x="{pad_l - 8}" y="{yy + 4}" text-anchor="end" '
            f'font-size="11" fill="#6b7280" style="{font}">{val}</text>'
            f'<line x1="{pad_l}" y1="{yy}" x2="{w - pad_r}" y2="{yy}" '
            f'stroke="#e5e7eb" stroke-width="1"/>'
        )

    # X-axis labels (show ~6 evenly spaced dates)
    x_labels = []
    label_count = min(n, 6)
    for i in range(label_count):
        idx = round(i * (n - 1) / max(label_count - 1, 1))
        label = dates[idx][5:]  # "03-13"
        xx = x(idx)
        x_labels.append(
            f'<text x="{xx}" y="{h - 8}" text-anchor="middle" '
            f'font-size="11" fill="#6b7280" style="{font}">{label}</text>'
        )

    # Total stats
    total_clones = sum(counts)
    total_uniques = sum(uniques)

    # Dots for count line
    count_dots = "".join(
        f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3" fill="#2563eb"/>'
        for i, v in enumerate(counts)
    )
    unique_dots = "".join(
        f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3" fill="#16a34a"/>'
        for i, v in enumerate(uniques)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect width="{w}" height="{h}" rx="8" fill="#fff"/>

<!-- Title -->
<text x="{pad_l}" y="20" font-size="14" font-weight="600" fill="#111" style="{font}">
  Clone Traffic — Total: {total_clones} clones / {total_uniques} unique
</text>

<!-- Grid -->
{"".join(y_ticks)}

<!-- Lines -->
<polyline points="{count_points}" fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linejoin="round"/>
<polyline points="{unique_points}" fill="none" stroke="#16a34a" stroke-width="2" stroke-dasharray="6,3" stroke-linejoin="round"/>

<!-- Dots -->
{count_dots}
{unique_dots}

<!-- X labels -->
{"".join(x_labels)}

<!-- Legend -->
<circle cx="{w - 200}" cy="18" r="4" fill="#2563eb"/>
<text x="{w - 192}" y="22" font-size="12" fill="#374151" style="{font}">Clones</text>
<circle cx="{w - 120}" cy="18" r="4" fill="#16a34a"/>
<text x="{w - 112}" y="22" font-size="12" fill="#374151" style="{font}">Unique visitors</text>
</svg>"""

    SVG_FILE.write_text(svg)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    fresh = fetch_clones()
    history = load_history()
    history = merge(history, fresh)

    # Save sorted
    sorted_history = dict(sorted(history.items()))
    DATA_FILE.write_text(json.dumps(sorted_history, indent=2) + "\n")

    generate_svg(sorted_history)

    total = sum(v["count"] for v in sorted_history.values())
    unique = sum(v["uniques"] for v in sorted_history.values())
    print(f"Updated: {len(sorted_history)} days, {total} clones, {unique} unique")


if __name__ == "__main__":
    main()
