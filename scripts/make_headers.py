"""Generate the light and dark header banners (assets/header-*.svg).

Edit the TEXT/COLORS below and run:  python scripts/make_headers.py
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

NAME = "Samet Besni"
ROLE = "Engineer · Data Analyst · Builder"
STACK = "Python / SQL / Tableau / AI agents / Godot"

THEMES = {
    "dark": {
        "bg": "#0d1117", "grid": "#1b2330", "grid2": "#222c3b", "ink": "#e6edf3",
        "muted": "#8b949e", "accent": "#f0883e", "line": "#58a6ff",
    },
    "light": {
        "bg": "#ffffff", "grid": "#eef2f7", "grid2": "#e1e7ef", "ink": "#1f2328",
        "muted": "#59636e", "accent": "#d1580b", "line": "#0969da",
    },
}

W, H = 1280, 300
FONT = "'Segoe UI', -apple-system, Helvetica, Arial, sans-serif"
MONO = "'Cascadia Code', Consolas, 'SFMono-Regular', Menlo, monospace"


def svg(c: dict) -> str:
    # bar chart drawn like a technical drawing, on the right
    bars = [62, 88, 74, 118, 104, 146]
    x0, base, bw, gap = 860, 232, 34, 22
    bar_svg, pts = [], []
    for i, h in enumerate(bars):
        x = x0 + i * (bw + gap)
        last = i == len(bars) - 1
        fill = c["accent"] if last else "none"
        stroke = c["accent"] if last else c["line"]
        bar_svg.append(
            f'<rect x="{x}" y="{base - h}" width="{bw}" height="{h}" fill="{fill}" '
            f'fill-opacity="{0.18 if last else 0}" stroke="{stroke}" stroke-width="2"/>'
        )
        pts.append((x + bw / 2, base - h - 14))
    trend = " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    dots = "".join(
        f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="{c["bg"]}" stroke="{c["line"]}" stroke-width="2"/>'
        for x, y in pts
    )
    x_end = x0 + (len(bars) - 1) * (bw + gap) + bw
    tip_x, tip_y = pts[-1]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME}: {ROLE}">
  <defs>
    <pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M20 0H0V20" fill="none" stroke="{c['grid']}" stroke-width="1"/>
    </pattern>
    <pattern id="G" width="100" height="100" patternUnits="userSpaceOnUse">
      <rect width="100" height="100" fill="url(#g)"/>
      <path d="M100 0H0V100" fill="none" stroke="{c['grid2']}" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" rx="14" fill="{c['bg']}"/>
  <rect width="{W}" height="{H}" rx="14" fill="url(#G)"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{c['grid2']}"/>

  <rect x="64" y="78" width="6" height="64" rx="3" fill="{c['accent']}"/>
  <text x="88" y="132" font-family="{FONT}" font-size="64" font-weight="700" fill="{c['ink']}">{NAME}</text>
  <text x="90" y="178" font-family="{FONT}" font-size="24" fill="{c['ink']}">{ROLE}</text>
  <text x="90" y="222" font-family="{MONO}" font-size="16" letter-spacing="1" fill="{c['muted']}">{STACK}</text>

  <line x1="{x0 - 20}" y1="{base}" x2="{x_end + 20}" y2="{base}" stroke="{c['muted']}" stroke-width="1.5"/>
  {''.join(bar_svg)}
  <polyline points="{trend}" fill="none" stroke="{c['line']}" stroke-width="2" stroke-dasharray="6 5"/>
  {dots}
  <circle cx="{tip_x:.0f}" cy="{tip_y:.0f}" r="6" fill="{c['accent']}"/>
  <line x1="{x0}" y1="{base + 22}" x2="{x_end}" y2="{base + 22}" stroke="{c['muted']}" stroke-width="1"/>
  <line x1="{x0}" y1="{base + 15}" x2="{x0}" y2="{base + 29}" stroke="{c['muted']}" stroke-width="1"/>
  <line x1="{x_end}" y1="{base + 15}" x2="{x_end}" y2="{base + 29}" stroke="{c['muted']}" stroke-width="1"/>
  <text x="{(x0 + x_end) / 2:.0f}" y="{base + 46}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{c['muted']}">raw data  →  insight</text>
</svg>
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, colors in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(svg(colors), encoding="utf-8", newline="\n")
        print(f"wrote assets/header-{name}.svg")


if __name__ == "__main__":
    main()
