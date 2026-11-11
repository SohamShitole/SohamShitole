"""Regenerate astorie-stats.svg and the dynamic README section from GitHub's contribution calendar.

Runs daily in .github/workflows/update.yml. Needs GITHUB_TOKEN (any token can read public calendars).
"""
import datetime as dt
import hashlib
import json
import os
import re
import urllib.request

WORK_LOGIN = "soham406"
WORK_START = dt.date(2026, 7, 1)
OTHER_LOGINS = ["SohamShitole", "sohamshitole-mldev"]
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


# (login, legend label, css key): towers take the colour of whichever account did most that day.
SKYLINE_ACCOUNTS = [("sohamshitole-mldev", "Adsgency AI", "g"), (WORK_LOGIN, "Astorie", "a"),
                    ("SohamShitole", "Personal", "p")]


def skyline(by_login, today):
    """Animated isometric skyline of the last 53 weeks, one tower per day."""
    start = today - dt.timedelta(days=364)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)  # back to Sunday, like GitHub's graph
    totals, owner = {}, {}
    for login, _, key in SKYLINE_ACCOUNTS:
        for d, c in by_login[login].items():
            if start <= d <= today and c:
                totals[d] = totals.get(d, 0) + c
                if c > owner.get(d, (None, 0))[1]:
                    owner[d] = (key, c)
    top = sorted(totals.values())[int(len(totals) * 0.98)] if totals else 1  # cap outliers

    a, b, ox, oy, hmax = 9.5, 5.5, 320, 130, 110
    cells = []
    for i in range((today - start).days + 1):
        d = start + dt.timedelta(days=i)
        w, wd = divmod(i, 7)
        x, y = ox + (w - wd) * a, oy + (w + wd) * b
        n = totals.get(d, 0)
        top_face = f"{x:.1f},{y:.1f} {x + a * .9:.1f},{y + b * .9:.1f} {x:.1f},{y + b * 1.8:.1f} {x - a * .9:.1f},{y + b * .9:.1f}"
        if not n:
            cells.append((w + wd, f'<polygon class="e" points="{top_face}"/>'))
            continue
        h = 4 + hmax * min(n / top, 1) ** 0.5
        k = owner[d][0]
        lift = lambda pts: " ".join(f"{px},{float(py) - h:.1f}" for px, py in (p.split(",") for p in pts.split()))
        bx, by = f"{x:.1f}", f"{y + b * 1.8:.1f}"
        left = f"{x - a * .9:.1f},{y + b * .9 - h:.1f} {bx},{y + b * 1.8 - h:.1f} {bx},{by} {x - a * .9:.1f},{y + b * .9:.1f}"
        right = f"{bx},{y + b * 1.8 - h:.1f} {x + a * .9:.1f},{y + b * .9 - h:.1f} {x + a * .9:.1f},{y + b * .9:.1f} {bx},{by}"
        tip = f"{n:,} contribution{'s' * (n != 1)} on {d:%b} {d.day}, {d.year}"
        cells.append((w + wd, f'<g class="t" style="animation-delay:{w * 0.035:.2f}s"><title>{tip}</title>'
                              f'<polygon class="{k}l" points="{left}"/><polygon class="{k}r" points="{right}"/>'
                              f'<polygon class="{k}t" points="{lift(top_face)}"/></g>'))
    body = "\n  ".join(svg for _, svg in sorted(cells, key=lambda c: c[0]))

    total = sum(totals.values())
    busiest = max(totals, key=totals.get) if totals else today
    run = longest = 0
    for i in range((today - start).days + 1):
        run = run + 1 if totals.get(start + dt.timedelta(days=i)) else 0
        longest = max(longest, run)
    used = [(label, key) for login, label, key in SKYLINE_ACCOUNTS if any(o[0] == key for o in owner.values())]
    legend = "".join(f'<rect class="{key}t" x="{24 + 110 * i}" y="466" width="12" height="12" rx="3"/>'
                     f'<text class="lbl" x="{42 + 110 * i}" y="476">{label}</text>' for i, (label, key) in enumerate(used))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="500" viewBox="0 0 840 500" role="img" aria-labelledby="st sd">
  <title id="st">Contribution skyline: last 12 months</title>
  <desc id="sd">One tower per day across all of Soham's GitHub accounts: {total:,} contributions, busiest day {totals.get(busiest, 0):,} on {busiest:%b} {busiest.day}, longest streak {longest} days.</desc>
  <style>
    :root {{ --bg:#ffffff; --border:#d0d7de; --ink:#1f2328; --ink2:#59636e; --muted:#818b98; --e:#ebedf0;
      --at:#6ea2f7; --al:#2f6fde; --ar:#1f4fa8; --gt:#b892f5; --gl:#8250df; --gr:#5e36a8; --pt:#5fd27c; --pl:#2da44e; --pr:#1a7f37; }}
    @media (prefers-color-scheme: dark) {{
      :root {{ --bg:#0d1117; --border:#30363d; --ink:#e6edf3; --ink2:#9198a1; --muted:#6e7681; --e:#161b22;
        --at:#8bb6ff; --al:#4c8df6; --ar:#2b5cb8; --gt:#c9a8ff; --gl:#a371f7; --gr:#6e40c9; --pt:#7ee2a8; --pl:#3fb950; --pr:#238636; }}
    }}
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
    .bg {{ fill: var(--bg); stroke: var(--border); }}
    .h {{ fill: var(--ink); font-size: 16px; font-weight: 600; }}
    .num {{ fill: var(--ink); font-size: 26px; font-weight: 600; }}
    .lbl {{ fill: var(--ink2); font-size: 12px; }}
    .ax {{ fill: var(--muted); font-size: 11px; }}
    .e {{ fill: var(--e); }}
    .at {{ fill: var(--at); }} .al {{ fill: var(--al); }} .ar {{ fill: var(--ar); }}
    .gt {{ fill: var(--gt); }} .gl {{ fill: var(--gl); }} .gr {{ fill: var(--gr); }}
    .pt {{ fill: var(--pt); }} .pl {{ fill: var(--pl); }} .pr {{ fill: var(--pr); }}
    .t {{ transform-box: fill-box; transform-origin: 50% 100%; animation: rise .7s cubic-bezier(.2,.8,.3,1.2) both; }}
    @keyframes rise {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
    @media (prefers-reduced-motion: reduce) {{ .t {{ animation: none; }} }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="839" height="499" rx="8"/>
  <text class="h" x="24" y="36">Contribution skyline</text>
  <text class="lbl" x="24" y="55">Last 12 months, all my GitHub accounts · one tower per day</text>
  <text class="num" x="24" y="98">{total:,}</text><text class="lbl" x="24" y="117">contributions</text>
  <text class="num" x="24" y="162">{totals.get(busiest, 0):,}</text><text class="lbl" x="24" y="181">on my busiest day ({busiest:%b} {busiest.day})</text>
  <text class="num" x="24" y="226">{longest}</text><text class="lbl" x="24" y="245">day longest streak</text>
  {legend}
  <text class="ax" x="816" y="486" text-anchor="end">updated {today:%b} {today.day}, {today.year}</text>
  {body}
</svg>
"""


def main():
    today = dt.datetime.now(dt.timezone.utc).date()
    days = work_days(today)
    svg = card(days, today)
    with open(os.path.join(ROOT, "astorie-stats.svg"), "w") as f:
        f.write(svg)

    year_ago = today - dt.timedelta(days=370)
    by_login = {login: calendar(login, year_ago, today) for login in OTHER_LOGINS}
    by_login[WORK_LOGIN] = days
    city = skyline(by_login, today)
    with open(os.path.join(ROOT, "skyline.svg"), "w") as f:
        f.write(city)

    # GitHub's image proxy caches by URL, so key each URL on the image's content.
    version = lambda s: hashlib.sha1(s.encode()).hexdigest()[:8]
    raw = "https://raw.githubusercontent.com/SohamShitole/SohamShitole/main"
    last_year = sum(c for login in by_login for d, c in by_login[login].items() if d > today - dt.timedelta(days=365))
    section = (f'<img src="{raw}/skyline.svg?v={version(city)}" alt="Contribution skyline: one tower per day '
               f'over the last 12 months" width="100%">\n\n'
               f'<img src="{raw}/astorie-stats.svg?v={version(svg)}" alt="Work at Astorie: '
               f'{sum(days.values()):,} contributions since {WORK_START:%b %Y}" width="100%">\n\n'
               f'**{last_year:,} contributions in the last year** across all my GitHub accounts · '
               f'_updated {today:%b} {today.day}, {today.year}_')

    path = os.path.join(ROOT, "README.md")
    readme = open(path).read()
    assert "<!-- STATS:START -->" in readme, "STATS markers missing from README.md"
    new = re.sub(r"(<!-- STATS:START -->).*?(<!-- STATS:END -->)",
                 lambda m: f"{m.group(1)}\n{section}\n{m.group(2)}", readme, flags=re.S)
    with open(path, "w") as f:
        f.write(new)


if __name__ == "__main__":
    main()
