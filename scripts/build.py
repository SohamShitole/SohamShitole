"""Regenerate astorie-stats.svg and the dynamic README section from GitHub's contribution calendar.

Runs daily in .github/workflows/update.yml. Needs GITHUB_TOKEN (any token can read public calendars).
"""
import datetime as dt
import hashlib
import json
import os
import re
import urllib.request

import scenes

WORK_LOGIN = "soham406"
WORK_START = dt.date(2026, 7, 1)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def calendar(login, start, end):
    """Return {date: count} for login between start and end (a span of at most one year)."""
    query = """query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){
      contributionsCollection(from:$from,to:$to){contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
    body = json.dumps({"query": query, "variables": {
        "login": login, "from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", body, {
        "Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req))
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return {dt.date.fromisoformat(d["date"]): d["contributionCount"] for w in weeks for d in w["contributionDays"]}


def work_days(today):
    # ponytail: one query per year-long window; fine for a handful of years.
    days, start = {}, WORK_START
    while start <= today:
        end = min(start.replace(year=start.year + 1) - dt.timedelta(days=1), today)
        days.update(calendar(WORK_LOGIN, start, end))
        start = end + dt.timedelta(days=1)
    return days


def streaks(days, today):
    current = longest = run = 0
    for d in sorted(days):
        run = run + 1 if days[d] else 0
        longest = max(longest, run)
    d = today if days.get(today) else today - dt.timedelta(days=1)  # today may not have activity yet
    while days.get(d):
        current += 1
        d -= dt.timedelta(days=1)
    return current, longest


def card(days, today):
    total = sum(days.values())
    active = sum(1 for c in days.values() if c)
    current, longest = streaks(days, today)
    months = {}
    for d, c in days.items():
        months[(d.year, d.month)] = months.get((d.year, d.month), 0) + c
    shown = sorted(months)[-6:]
    peak = max(months[m] for m in shown) or 1
    step = 1000 if peak <= 4000 else 2000
    k = 160 / max(peak, step)
    base, x0, gap = 250, 452, 60
    width = 40 if len(shown) <= 5 else 36

    bars, labels, grid = [], [], []
    for v in range(step, int(peak) + 1, step):
        y = base - v * k
        grid.append(f'<line class="grid" x1="440" y1="{y:.1f}" x2="816" y2="{y:.1f}"/>'
                    f'<text class="ax" x="816" y="{y - 4:.1f}" style="text-anchor:end">{v:,}</text>')
    for i, m in enumerate(shown):
        n, x = months[m], x0 + gap * i
        top = base - max(n * k, 4)
        name = dt.date(m[0], m[1], 1).strftime("%b") + ("*" if m == (today.year, today.month) else "")
        bars.append(f'<path class="bar" d="M{x} {base} V{top + 4:.1f} a4 4 0 0 1 4 -4 h{width - 8} a4 4 0 0 1 4 4 V{base} Z"/>')
        labels.append(f'<text class="val" x="{x + width / 2}" y="{top - 6:.1f}">{n:,}</text>'
                      f'<text class="ax" x="{x + width / 2}" y="268">{name}</text>')

    span = f"{WORK_START:%b %Y} – {today:%b %Y}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="300" viewBox="0 0 840 300" role="img" aria-labelledby="t d">
  <title id="t">Work at Astorie: {span}</title>
  <desc id="d">{total:,} contributions over {active} active days. Current streak {current} days, longest {longest} days.</desc>
  <style>
    :root {{ --bg:#ffffff; --border:#d0d7de; --ink:#1f2328; --ink2:#59636e; --muted:#818b98; --grid:#eaeef2; --bar:#2f6fde; }}
    @media (prefers-color-scheme: dark) {{
      :root {{ --bg:#0d1117; --border:#30363d; --ink:#e6edf3; --ink2:#9198a1; --muted:#6e7681; --grid:#21262d; --bar:#4c8df6; }}
    }}
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    .bg {{ fill: var(--bg); stroke: var(--border); }}
    .h {{ fill: var(--ink); font-size: 16px; font-weight: 600; }}
    .sub {{ fill: var(--ink2); font-size: 12px; }}
    .num {{ fill: var(--ink); font-size: 26px; font-weight: 600; }}
    .lbl {{ fill: var(--ink2); font-size: 12px; }}
    .ax {{ fill: var(--muted); font-size: 11px; text-anchor: middle; }}
    .val {{ fill: var(--ink2); font-size: 11px; text-anchor: middle; }}
    .grid {{ stroke: var(--grid); stroke-width: 1; }}
    .bar {{ fill: var(--bar); }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="839" height="299" rx="8"/>
  <text class="h" x="24" y="36">Work at Astorie</text>
  <text class="sub" x="24" y="55">{span} · private repos, as @{WORK_LOGIN} · updated daily</text>
  <g transform="translate(24,92)">
    <text class="num" x="0" y="0">{total:,}</text><text class="lbl" x="0" y="20">contributions</text>
    <text class="num" x="150" y="0">{active}</text><text class="lbl" x="150" y="20">active days</text>
    <text class="num" x="0" y="66">{current}</text><text class="lbl" x="0" y="86">day current streak</text>
    <text class="num" x="150" y="66">{longest}</text><text class="lbl" x="150" y="86">day longest streak</text>
    <text class="sub" x="0" y="140">Contributions = commits, PRs, reviews and issues</text>
  </g>
  <text class="lbl" x="440" y="36">Contributions per month</text>
  <line class="grid" x1="440" y1="{base}" x2="816" y2="{base}"/>
  {''.join(grid)}
  {''.join(bars)}
  {''.join(labels)}
  <text class="ax" x="816" y="288" style="text-anchor:end">*{today:%b} to date ({today:%b} {today.day})</text>
</svg>
"""


def main():
    today = dt.datetime.now(dt.timezone.utc).date()
    days = work_days(today)
    adsgency = calendar("sohamshitole-mldev", scenes.JOBS[0][1], scenes.JOBS[0][2])
    personal = calendar("SohamShitole", today - dt.timedelta(days=364), today)

    # Each day belongs to whichever account did the most that day.
    totals, owner, best = {}, {}, {}
    for key, cal in (("p", personal), ("g", adsgency), ("a", days)):
        for d, c in cal.items():
            if c:
                totals[d] = totals.get(d, 0) + c
                if c > best.get(d, 0):
                    best[d], owner[d] = c, key
    year = {d: c for d, c in totals.items() if d > today - dt.timedelta(days=365)}

    images = {  # file name -> (svg, alt text), in README order
        "terminal.svg": (scenes.terminal(year, 3, today), "Terminal: whoami, contributions in the last year, current focus"),
        "highlights.svg": (scenes.highlights(sum(year.values()), today), "Highlights: 1.6M+ lines of code this year, 100+ features shipped"),
        "city.svg": (scenes.city(totals, owner, today), "Contribution city: one building per day over the last 12 months"),
        "timeline.svg": (scenes.timeline({"g": adsgency, "a": days}, today), "Career timeline: Adsgency AI, then Astorie"),
        "stack.svg": (scenes.stack(today), "Languages I write and the stack I build with"),
        "astorie-stats.svg": (card(days, today), f"Work at Astorie: {sum(days.values()):,} contributions since {WORK_START:%b %Y}"),
    }
    for name, (svg, _) in images.items():
        with open(os.path.join(ROOT, name), "w") as f:
            f.write(svg)

    # GitHub's image proxy caches by URL, so key each URL on the image's content.
    raw = "https://raw.githubusercontent.com/SohamShitole/SohamShitole/main"
    img = lambda name: (f'<img src="{raw}/{name}?v={hashlib.sha1(images[name][0].encode()).hexdigest()[:8]}" '
                        f'alt="{images[name][1]}" width="100%">')
    section = "\n\n".join([
        img("terminal.svg"), img("highlights.svg"), img("city.svg"), img("timeline.svg"), img("stack.svg"),
        "<details>\n<summary><b>Detailed stats</b></summary>\n",
        img("astorie-stats.svg"),
        f'<img src="{raw}/startup-stats.svg?v=3" alt="Before Astorie at Adsgency AI, Nov 2025 to Jun 2026: '
        f'5,043 contributions over 158 active days" width="100%">',
        "This year: **1.6M+ lines of code** (1.0M at Astorie, 600K+ at Adsgency AI) · **100+ features shipped** · at Astorie **4,600+ commits** and **927 PRs merged** (Nov 2026).",
        "</details>",
        f"_Updated daily · last run {today:%b} {today.day}, {today.year}_",
    ])

    path = os.path.join(ROOT, "README.md")
    readme = open(path).read()
    assert "<!-- STATS:START -->" in readme, "STATS markers missing from README.md"
    new = re.sub(r"(<!-- STATS:START -->).*?(<!-- STATS:END -->)",
                 lambda m: f"{m.group(1)}\n{section}\n{m.group(2)}", readme, flags=re.S)
    with open(path, "w") as f:
        f.write(new)


if __name__ == "__main__":
    main()
