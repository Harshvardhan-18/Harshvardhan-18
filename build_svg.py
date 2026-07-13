from pathlib import Path

TSPANS = Path("portrait_tspan.txt").read_text(encoding="utf-8")

MONO = "SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

SKILLS = ["C++", "Python", "TypeScript", "Next.js", "FastAPI", "LangGraph",
          "PostgreSQL", "AWS", "Docker", "ChromaDB", "React", "Redis"]

# --- chip layout (wrap skill badges to fit the right column width) ---
PANEL_X = 450
PANEL_W = 890 - PANEL_X  # right column width
CHIP_H = 26
CHIP_GAP = 8
CHIP_PAD = 14
CHAR_W = 7.1  # approx px per char at font-size 12 monospace


def layout_chips(skills, start_x, start_y):
    chips = []
    x, y = start_x, start_y
    for s in skills:
        w = int(len(s) * CHAR_W + CHIP_PAD * 2)
        if x + w > start_x + PANEL_W:
            x = start_x
            y += CHIP_H + CHIP_GAP
        chips.append((s, x, y, w))
        x += w + CHIP_GAP
    end_y = y + CHIP_H
    return chips, end_y


CHIPS, CHIPS_END_Y = layout_chips(SKILLS, PANEL_X, 428)


def chip_svg(chips, fill, stroke, text_fill):
    out = []
    for s, x, y, w in chips:
        out.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{CHIP_H}" rx="13" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        )
        out.append(
            f'<text x="{x + w / 2}" y="{y + CHIP_H / 2 + 4}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="12" fill="{text_fill}">{s}</text>'
        )
    return "\n  ".join(out)


def stat_row(y, icon, label, value_id, dots_id=None, extra=""):
    dots_tspan = f'<tspan id="{dots_id}" class="dots"> </tspan>' if dots_id else ""
    return (
        f'<text x="{PANEL_X}" y="{y}" font-family="{MONO}" font-size="14" class="row">'
        f'<tspan class="icon">{icon}</tspan>'
        f'<tspan class="label" dx="8">{label}</tspan>'
        f'{dots_tspan}'
        f'<tspan id="{value_id}" class="value">0</tspan>'
        f'{extra}'
        f'</text>'
    )


STAT_ROWS_Y0 = 200
STAT_GAP = 30

rows = [
    stat_row(STAT_ROWS_Y0 + 0 * STAT_GAP, "&#128337;", "Coding Since   ", "age_data"),
    stat_row(STAT_ROWS_Y0 + 1 * STAT_GAP, "&#128172;", "Total Commits  ", "commit_data", "commit_data_dots"),
    stat_row(STAT_ROWS_Y0 + 2 * STAT_GAP, "&#11088;", "Stars Earned   ", "star_data", "star_data_dots"),
    stat_row(STAT_ROWS_Y0 + 3 * STAT_GAP, "&#128193;", "Repositories   ", "repo_data", "repo_data_dots"),
    stat_row(STAT_ROWS_Y0 + 4 * STAT_GAP, "&#129309;", "Contributed To ", "contrib_data"),
    stat_row(STAT_ROWS_Y0 + 5 * STAT_GAP, "&#128101;", "Followers      ", "follower_data", "follower_data_dots"),
    stat_row(
        STAT_ROWS_Y0 + 6 * STAT_GAP, "&#9999;", "Lines Changed  ", "loc_data", "loc_data_dots",
        extra=(
            '<tspan class="label" dx="6">(</tspan>'
            '<tspan class="add">+</tspan><tspan id="loc_add" class="add">0</tspan>'
            '<tspan class="label">, </tspan>'
            '<tspan class="del">-</tspan><tspan id="loc_del" class="del">0</tspan>'
            '<tspan id="loc_del_dots" class="dots"> </tspan>'
            '<tspan class="label">)</tspan>'
        ),
    ),
]
ROWS_SVG = "\n  ".join(rows)

SKILLS_LABEL_Y = 408
FOOTER_Y = CHIPS_END_Y + 34

TEMPLATE = """<svg width="920" height="{height}" viewBox="0 0 920 {height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .row {{ fill: {text}; }}
    .label {{ fill: {text}; }}
    .value {{ fill: {accent2}; font-weight: 600; }}
    .dots {{ fill: {muted}; }}
    .add {{ fill: {green}; }}
    .del {{ fill: {red}; }}
    .icon {{ font-family: sans-serif; }}
  </style>

  <rect x="0.5" y="0.5" width="919" height="{height_m1}" rx="16" fill="{bg}" stroke="{border}"/>

  <!-- terminal title bar -->
  <rect x="0.5" y="0.5" width="919" height="40" rx="16" fill="{bg_alt}"/>
  <rect x="0.5" y="24.5" width="919" height="16" fill="{bg_alt}"/>
  <circle cx="24" cy="20" r="6" fill="#ff5f56"/>
  <circle cx="44" cy="20" r="6" fill="#ffbd2e"/>
  <circle cx="64" cy="20" r="6" fill="#27c93f"/>
  <text x="460" y="25" text-anchor="middle" font-family="{mono}" font-size="13" fill="{muted}">harshvardhan@github: ~ %</text>
  <line x1="0.5" y1="41" x2="919.5" y2="41" stroke="{border}"/>

  <!-- ascii portrait frame -->
  <rect x="30" y="61" width="380" height="{frame_h}" rx="10" fill="{bg_alt}" stroke="{border}"/>
  <g transform="translate(56,158) scale(0.63)">
    <text font-family="{mono}" font-size="9" fill="{portrait}" xml:space="preserve">
      {tspans}
    </text>
  </g>
  <text x="220" y="{caption_y}" text-anchor="middle" font-family="{mono}" font-size="12" fill="{muted}">// harshvardhan.yadav</text>

  <!-- name / tagline -->
  <text x="450" y="100" font-family="{mono}" font-size="26" font-weight="700" fill="{text}">Harshvardhan Yadav</text>
  <text x="450" y="124" font-family="{mono}" font-size="13" fill="{muted}">B.Tech IT @ IIIT Una &#183; Building AI systems &amp; full-stack platforms</text>
  <line x1="450" y1="140" x2="890" y2="140" stroke="{border}"/>

  <text x="450" y="168" font-family="{mono}" font-size="13" fill="{accent}">$ cat github_stats.log</text>
  {rows}

  <line x1="450" y1="385" x2="890" y2="385" stroke="{border}"/>
  <text x="450" y="{skills_label_y}" font-family="{mono}" font-size="13" fill="{accent}">$ cat skills.json</text>
  {chips}

  <text x="450" y="{footer_y}" font-family="{mono}" font-size="11" fill="{muted}">LeetCode Knight (1850+) &#183; 600+ DSA solved &#183; NTSE Scholar</text>
  <text x="450" y="{footer_y2}" font-family="{mono}" font-size="10" fill="{muted}">auto-updated via GitHub Actions</text>
</svg>
"""


def build(path, *, bg, bg_alt, border, text, muted, accent, accent2, portrait, green, red):
    height = FOOTER_Y + 40
    svg = TEMPLATE.format(
        height=height,
        height_m1=height - 1,
        frame_h=height - 61 - 30,
        caption_y=height - 45,
        mono=MONO,
        tspans=TSPANS,
        rows=ROWS_SVG,
        skills_label_y=SKILLS_LABEL_Y,
        chips=chip_svg(CHIPS, fill=bg, stroke=border, text_fill=text),
        footer_y=FOOTER_Y,
        footer_y2=FOOTER_Y + 18,
        bg=bg, bg_alt=bg_alt, border=border, text=text, muted=muted,
        accent=accent, accent2=accent2, portrait=portrait, green=green, red=red,
    )
    Path(path).write_text(svg, encoding="utf-8")


build(
    "dark.svg",
    bg="#0d1117", bg_alt="#161b22", border="#30363d",
    text="#c9d1d9", muted="#8b949e", accent="#58a6ff", accent2="#79c0ff",
    portrait="#58a6ff", green="#3fb950", red="#f85149",
)

build(
    "light.svg",
    bg="#ffffff", bg_alt="#f6f8fa", border="#d0d7de",
    text="#24292f", muted="#57606a", accent="#0969da", accent2="#0a5cc9",
    portrait="#0969da", green="#1a7f37", red="#cf222e",
)

print("Wrote dark.svg and light.svg")
