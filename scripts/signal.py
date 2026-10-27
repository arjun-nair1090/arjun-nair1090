"""Draws assets/signal-{dark,light}.svg: my last 12 months of GitHub activity as a trace.

Runs weekly in .github/workflows/signal.yml. Needs GITHUB_TOKEN; stdlib only.
"""
import base64
import datetime as dt
import json
import math
import os
import pathlib
import urllib.request

LOGIN = "arjun-nair1090"
ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1200, 600
X0, X1 = 64, 1136            # plot left/right
TOP, BASE = 110, 520         # plot top/baseline; tall peaks rise beside the name
REVEAL = 2.6                 # seconds for the trace to draw in

# Launches worth marking. Ones older than the window simply drop off.
MARKERS = [
    ("2026-02-25", "Resonance"),
    ("2026-03-01", "FitRank Pro"),
    ("2026-04-22", "TradeBot"),
    ("2026-07-27", "Pit Wall"),
    ("2026-10-06", "APEX"),
    ("2026-10-07", "Jewlerify"),
    ("2026-10-16", "PurpleSector"),
]

THEMES = {
    "dark": dict(bg="#0F1B33", ink="#EEF2F8", mist="#8B9BBA", grid="#22314F",
                 cold="#4C82FF", warm="#FFC23D", hot="#FF4F45", edge="#0F1B33"),
    "light": dict(bg="#F5F8FD", ink="#0F1B33", mist="#56688C", grid="#D5DEEC",
                  cold="#2A5FE0", warm="#E3A400", hot="#E5392F", edge="#D5DEEC"),
}


def fetch_days(today):
    start = today - dt.timedelta(days=364)
    query = """query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){
      contributionsCollection(from:$from,to:$to){contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
    body = json.dumps({"query": query, "variables": {
        "login": LOGIN, "from": f"{start}T00:00:00Z", "to": f"{today}T23:59:59Z"}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", body, {
        "Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req))
    if "errors" in data:
        raise SystemExit(data["errors"])
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    counts = {d["date"]: d["contributionCount"] for w in weeks for d in w["contributionDays"]}
    return [(start + dt.timedelta(days=i), counts.get(str(start + dt.timedelta(days=i)), 0)) for i in range(365)]


def trace(days):
    # Square root keeps one-commit days visible next to 60-commit ones; a light
    # triangle filter turns daily spikes into something that reads as a signal.
    v = [math.sqrt(c) for _, c in days]
    k = [1, 2, 3, 2, 1]
    s = [sum(k[j] * v[min(max(i + j - 2, 0), len(v) - 1)] for j in range(5)) / 9 for i in range(len(v))]
    top = max(s) or 1
    return [(X0 + (X1 - X0) * i / (len(s) - 1), BASE - (BASE - TOP) * y / top) for i, y in enumerate(s)]


def path(pts):
    # Catmull-Rom through every point, as cubic Béziers.
    d = [f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"]
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}")
    return "".join(d)


def font(name):
    b64 = base64.b64encode((ROOT / f"assets/fonts/bricolage-{name}.woff2").read_bytes()).decode()
    return f"@font-face{{font-family:B{name[0]};src:url(data:font/woff2;base64,{b64}) format('woff2')}}"


def render(days, pts, t):
    start = days[0][0]
    x_of = lambda date: X0 + (X1 - X0) * (date - start).days / 364
    line = path(pts)
    area = f"{line}L{X1},{BASE}L{X0},{BASE}Z"

    months = []
    for date, _ in days:
        if date.day == 1:
            label = date.strftime("%b") + (f" {date.year}" if date.month == 1 else "")
            x = x_of(date)
            months.append(f'<line x1="{x:.1f}" y1="{BASE}" x2="{x:.1f}" y2="{BASE + 6}" stroke="{t["mist"]}"/>'
                          f'<text x="{x:.1f}" y="{BASE + 28}" class="t" font-size="15" fill="{t["mist"]}">{label}</text>')

    # Each label sits just above its point and steps up a line while it would
    # overlap one already placed (APEX and Jewlerify launched a day apart).
    # It also has to clear the trace beneath it and every marker dot.
    shown = [(dt.date.fromisoformat(d), label) for d, label in MARKERS]
    shown = [(d, label) for d, label in shown if start <= d <= days[-1][0]]
    dots = [(x_of(d) - 6, x_of(d) + 6, pts[(d - start).days][1] + 4) for d, _ in shown]
    placed, marks = [], []
    for date, label in shown:
        x, py = x_of(date), pts[(date - start).days][1]
        w = len(label) * 8.2
        flip = x + w > W - 32                      # near the right edge: hang the label left
        lx0 = x - w - 4 if flip else x - 2
        under = min(y for px, y in pts if lx0 - 4 <= px <= lx0 + w + 4)
        ly = min(py - 16, under - 10)
        while any(lx0 < b1 + 8 and b0 < lx0 + w + 8 and abs(ly - by) < 19 for b0, b1, by in placed + dots):
            ly -= 21
        placed.append((lx0, lx0 + w, ly))
        delay = 0.2 + REVEAL * (x - X0) / (X1 - X0)
        anchor = f'x="{x + 4:.1f}" text-anchor="end"' if flip else f'x="{x - 2:.1f}"'
        marks.append(
            f'<g class="mark" style="animation-delay:{delay:.2f}s">'
            f'<line x1="{x:.1f}" y1="{ly + 5:.1f}" x2="{x:.1f}" y2="{py - 5:.1f}" stroke="{t["mist"]}" stroke-dasharray="2 3"/>'
            f'<circle cx="{x:.1f}" cy="{py:.1f}" r="4" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="2"/>'
            f'<text {anchor} y="{ly:.1f}" class="t h" font-size="15" fill="{t["ink"]}">{label}</text></g>')

    nx, ny = pts[-1]
    total = sum(c for _, c in days)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Arjun Nair</title>
<desc id="d">AI/ML engineer in Mumbai. A trace of {total} GitHub contributions over the last 12 months, with project launches marked.</desc>
<style>{font("display")}{font("text")}
.d{{font-family:Bd,'Arial Narrow',sans-serif}}.h{{paint-order:stroke;stroke:{t['bg']};stroke-width:6px;stroke-linejoin:round}}.t{{font-family:Bt,'Segoe UI',Helvetica,Arial,sans-serif}}
.reveal{{transform-box:fill-box;transform-origin:left;animation:reveal {REVEAL}s cubic-bezier(.45,0,.25,1) .2s both}}
@keyframes reveal{{from{{transform:scaleX(0)}}}}
.mark{{animation:fade .5s ease-out both}}@keyframes fade{{from{{opacity:0}}}}
.now{{animation:fade .4s {REVEAL + 0.2}s both}}
.ring{{transform-box:fill-box;transform-origin:center;animation:ring 2.4s {REVEAL + 0.4}s ease-out infinite both}}
@keyframes ring{{0%{{transform:scale(1);opacity:.7}}100%{{transform:scale(4.5);opacity:0}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.ring{{opacity:0}}}}
</style>
<defs>
<linearGradient id="heat" gradientUnits="userSpaceOnUse" x1="0" y1="{BASE}" x2="0" y2="{TOP}">
<stop offset="0" stop-color="{t["cold"]}"/><stop offset=".55" stop-color="{t["warm"]}"/><stop offset="1" stop-color="{t["hot"]}"/></linearGradient>
<linearGradient id="wash" gradientUnits="userSpaceOnUse" x1="0" y1="{TOP}" x2="0" y2="{BASE}">
<stop offset="0" stop-color="{t["hot"]}" stop-opacity=".22"/><stop offset="1" stop-color="{t["cold"]}" stop-opacity="0"/></linearGradient>
<clipPath id="draw"><rect class="reveal" x="{X0 - 4}" y="{TOP - 20}" width="{X1 - X0 + 8}" height="{BASE - TOP + 24}"/></clipPath>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="{t["bg"]}" stroke="{t["edge"]}"/>

<line x1="{X0}" y1="{BASE}" x2="{X1}" y2="{BASE}" stroke="{t["grid"]}" stroke-width="1.5"/>
{"".join(months)}
<g clip-path="url(#draw)">
<path d="{area}" fill="url(#wash)"/>
<path d="{line}" fill="none" stroke="url(#heat)" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>
</g>
<text x="50" y="214" class="d h" font-size="212" fill="{t["ink"]}" letter-spacing="-2">Arjun Nair</text>
<text x="62" y="264" class="t h" font-size="25" fill="{t["ink"]}">AI/ML engineer in Mumbai. I build software that runs on live data.</text>
{"".join(marks)}
<g class="now"><circle class="ring" cx="{nx:.1f}" cy="{ny:.1f}" r="5" fill="none" stroke="{t["hot"]}" stroke-width="1.5"/>
<circle cx="{nx:.1f}" cy="{ny:.1f}" r="5" fill="{t["hot"]}"/></g>

<text x="64" y="578" class="t" font-size="14" fill="{t["mist"]}">My GitHub activity, day by day, over the last 12 months. Height is the square root of each day’s count. Redrawn every Monday.</text>
</svg>
"""


if __name__ == "__main__":
    today = dt.date.today()
    days = fetch_days(today)
    pts = trace(days)
    assert len(days) == len(pts) == 365 and all(TOP <= y <= BASE for _, y in pts)
    for name, theme in THEMES.items():
        (ROOT / f"assets/signal-{name}.svg").write_text(render(days, pts, theme), encoding="utf-8")
    print(f"{sum(c for _, c in days)} contributions, {today - dt.timedelta(days=364)} to {today}")
