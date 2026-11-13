"""The four headline visuals for the profile README: terminal, night city, career timeline, stack."""
import datetime as dt
import math
import random

FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace'

# Lines of code added this year. Astorie: git numstat of my commits (Nov 10 2026; build output and data
# files excluded). Adsgency AI: 600K+ lines, mostly Python (self-reported; no repo access).
# Order keeps neighbouring donut colours distinguishable (checked with the dataviz palette validator).
LANGUAGES = [("TypeScript", 794_408, "ts"), ("React (TSX)", 137_115, "tsx"), ("SQL", 60_051, "sql"),
             ("Python (Adsgency AI)", 600_000, "py"), ("Shell", 13_041, "sh"), ("Other", 11_461, "oth")]
FEATURES = "100+"
PRS_MERGED = 927  # Astorie fallback when STATS_TOKEN is missing (Nov 10 2026)
ADSGENCY_PRS = 1011  # @sohamshitole-mldev, private repos, job ended Jun 2026
# Product scale (Nov 2026). Astorie: app DB auth.users (211K) + PostHog generation:started since Jun 9 2026.
# AdsGency AI: the company's own homepage claims (adsgency.ai).
IMPACT = [("200K+", "users on the platform", "Astorie"), ("1.8M+", "AI generations run", "Astorie"),
          ("150+", "businesses on the platform", "AdsGency AI"), ("$50M+", "ad spend managed", "AdsGency AI")]
STACK = ["TypeScript", "Python", "SQL", "React", "Next.js", "Node.js", "LangGraph", "LangChain", "OpenAI",
         "Anthropic", "Vercel AI SDK", "FAL", "MCP", "Postgres", "Supabase", "Drizzle", "Zustand", "React Flow",
         "Stripe", "PostHog", "Railway", "Vercel"]
JOBS = [  # (name, start, end or None for current, css key, one-liner)
    ("Adsgency AI", dt.date(2025, 11, 1), dt.date(2026, 6, 30), "g", "ML engineering at an AI ads startup"),
    ("Astorie", dt.date(2026, 7, 1), None, "a", "AI agents, creative canvas & video tools, public API"),
]

THEMED = """
    :root {{ --bg:#ffffff; --border:#d0d7de; --ink:#1f2328; --ink2:#59636e; --muted:#818b98; --grid:#eaeef2; {light} }}
    @media (prefers-color-scheme: dark) {{
      :root {{ --bg:#0d1117; --border:#30363d; --ink:#e6edf3; --ink2:#9198a1; --muted:#6e7681; --grid:#21262d; {dark} }}
    }}
    text {{ font-family: %s; }}
    .bg {{ fill: var(--bg); stroke: var(--border); }}
    .h {{ fill: var(--ink); font-size: 16px; font-weight: 600; }}
    .num {{ fill: var(--ink); font-size: 22px; font-weight: 600; }}
    .lbl {{ fill: var(--ink2); font-size: 12px; }}
    .ax {{ fill: var(--muted); font-size: 11px; }}""" % FONT


def summary(totals, today):
    total = sum(totals.values())
    busiest = max(totals, key=totals.get) if totals else today
    run = longest = 0
    for i in range(400):
        run = run + 1 if totals.get(today - dt.timedelta(days=399 - i)) else 0
        longest = max(longest, run)
    return total, busiest, longest


# ---------------------------------------------------------------- terminal

def terminal(totals, accounts, today):
    total, busiest, longest = summary(totals, today)
    lines = [  # (is_command, text)
        (True, "whoami"),
        (False, "Soham Shitole · software engineer @ Astorie · San Francisco"),
        (True, "contributions --last-year --all-accounts"),
        (False, f"{total:,} across {accounts} accounts · {longest}-day best streak · {totals.get(busiest, 0):,} on {busiest:%b} {busiest.day}"),
        (True, "cat now.txt"),
        (False, "Building AI agents that drive a visual canvas for images, video and audio"),
        (True, "cat stack.txt"),
        (False, "languages  TypeScript · Python · SQL"),
        (False, "ai         LangGraph · LangChain · OpenAI · Anthropic · Vercel AI SDK · MCP"),
        (False, "web        React · Next.js · Node.js"),
        (False, "data/infra Postgres · Supabase · Drizzle · Railway · Vercel"),
    ]
    # CSS only: SMIL (<animate>/<set>) doesn't run in every browser when the SVG is shown as an <img>.
    out, t, y = [], 0.4, 76
    for i, (cmd, text) in enumerate(lines):
        if cmd:
            dur = 0.04 * len(text) + 0.2
            out.append(f'<text class="p" x="24" y="{y}">$</text><text class="c" x="40" y="{y}" '
                       f'style="animation-delay:{t:.2f}s;animation-duration:{dur:.2f}s;animation-timing-function:steps({len(text) + 1},jump-none)">{text}</text>')
            # jump-none reaches the full line on the last step, so a browser that stops one step short still shows it all.
            t += dur + 0.25
        else:
            out.append(f'<text class="o" x="40" y="{y}" style="animation-delay:{t:.2f}s;white-space:pre">{esc(text)}</text>')
            t += 0.2
            if i + 1 == len(lines) or lines[i + 1][0]:  # gap before the next command
                t += 0.15
                y += 8
        y += 24 if cmd or i + 1 == len(lines) or lines[i + 1][0] else 20
    out.append(f'<text class="p o" x="24" y="{y}" style="animation-delay:{t:.2f}s">$</text>'
               f'<rect class="cur" x="40" y="{y - 13}" width="9" height="17" style="animation-delay:{t:.2f}s,{t:.2f}s"/>')
    height = y + 30
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="{height}" viewBox="0 0 840 {height}" role="img" aria-labelledby="tt td">
  <title id="tt">Terminal: about Soham</title>
  <desc id="td">{esc(" ".join(text for _, text in lines))}</desc>
  <style>
    text {{ font-family: {MONO}; font-size: 14px; }}
    .p {{ fill: #3fb950; font-weight: 700; }} .c {{ fill: #e6edf3; animation: type 1s both; }}
    .o {{ fill: #9198a1; animation: show .01s both; }} .p.o {{ fill: #3fb950; }}
    .cur {{ fill: #e6edf3; animation: show .01s both, blink 1s steps(1) infinite; }}
    @keyframes type {{ from {{ clip-path: inset(0 100% 0 0); }} to {{ clip-path: inset(0 0 0 0); }} }}
    @keyframes show {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes blink {{ 50% {{ fill-opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <rect x="0.5" y="0.5" width="839" height="{height - 1}" rx="10" fill="#0d1117" stroke="#30363d"/>
  <path d="M0.5 32 V10.5 a10 10 0 0 1 10 -10 H829.5 a10 10 0 0 1 10 10 V32 Z" fill="#161b22"/>
  <circle cx="22" cy="16" r="6" fill="#ff5f57"/><circle cx="42" cy="16" r="6" fill="#febc2e"/><circle cx="62" cy="16" r="6" fill="#28c840"/>
  <text x="420" y="21" text-anchor="middle" style="font-size:12px;fill:#6e7681">soham@astorie: ~</text>
  {"".join(out)}
</svg>
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- night city

def city(totals, owner, today):
    """Isometric night city: one building per day, lit windows scale with that day's activity."""
    rng = random.Random(str(today))
    start = today - dt.timedelta(days=364)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)
    total, busiest, longest = summary(totals, today)
    vals = sorted(v for d, v in totals.items() if d >= start)
    top = vals[int(len(vals) * 0.98)] if vals else 1

    a, b, ox, oy, hmax = 9.5, 5.5, 320, 140, 120
    A, B = a * .9, b * .9
    pt = lambda x, y: f"{x:.1f},{y:.1f}"
    cells, tallest = [], []
    for i in range((today - start).days + 1):
        d = start + dt.timedelta(days=i)
        w, wd = divmod(i, 7)
        x, y = ox + (w - wd) * a, oy + (w + wd) * b
        n = totals.get(d, 0)
        if not n:
            cells.append((w + wd, f'<polygon class="lot" points="{pt(x, y)} {pt(x + A, y + B)} {pt(x, y + 2 * B)} {pt(x - A, y + B)}"/>'))
            continue
        k = owner[d]
        h = 6 + hmax * min(n / top, 1) ** 0.5
        tallest.append((h, x, y))
        faces = (f'<polygon class="{k}l" points="{pt(x - A, y + B - h)} {pt(x, y + 2 * B - h)} {pt(x, y + 2 * B)} {pt(x - A, y + B)}"/>'
                 f'<polygon class="{k}r" points="{pt(x, y + 2 * B - h)} {pt(x + A, y + B - h)} {pt(x + A, y + B)} {pt(x, y + 2 * B)}"/>'
                 f'<polygon class="{k}t" points="{pt(x, y - h)} {pt(x + A, y + B - h)} {pt(x, y + 2 * B - h)} {pt(x - A, y + B - h)}"/>')
        lit = 0.12 + 0.75 * min(n / top, 1) ** 0.5
        steady, blink = [], []
        for (sx, sy, ex, ey) in ((x - A, y + B - h, x, y + 2 * B - h), (x, y + 2 * B - h, x + A, y + B - h)):
            off = 6
            while off < h - 4:
                for t1, t2 in ((0.18, 0.42), (0.58, 0.82)):
                    if rng.random() < lit:
                        seg = f"M{sx + (ex - sx) * t1:.1f} {sy + (ey - sy) * t1 + off:.1f}L{sx + (ex - sx) * t2:.1f} {sy + (ey - sy) * t2 + off:.1f}"
                        (blink if rng.random() < 0.04 else steady).append(seg)
                off += 7
        win = f'<path class="w{k}" style="animation-delay:{0.6 + w * 0.04:.2f}s" d="{"".join(steady)}"/>' if steady else ""
        if blink:
            win += f'<path class="w{k} bl" style="animation-delay:{rng.uniform(0, 6):.1f}s" d="{"".join(blink)}"/>'
        tip = f"<title>{n:,} contribution{'s' * (n != 1)} on {d:%b} {d.day}, {d.year}</title>"
        cells.append((w + wd, f"<g>{tip}{faces}{win}</g>"))

    # Aircraft-warning lights on the three tallest buildings.
    for h, x, y in sorted(tallest, reverse=True)[:3]:
        cells.append((999, f'<circle class="beacon" cx="{x:.1f}" cy="{y + B - h - 4:.1f}" r="2.2" style="animation-delay:{rng.uniform(0, 2):.1f}s"/>'))
    body = "\n  ".join(s for _, s in sorted(cells, key=lambda c: c[0]))

    # Road along the front edge, with a car driving the year from left to right.
    weeks = (today - start).days // 7 + 1
    edge = lambda w, wd: (ox + (w - wd) * a, oy + (w + wd) * b)
    r0, r1 = edge(-1, 7.4), edge(weeks + 1, 7.4)
    q0, q1 = edge(-1, 9.4), edge(weeks + 1, 9.4)
    m0, m1 = edge(-1, 8.4), edge(weeks + 1, 8.4)
    road = (f'<polygon class="road" points="{pt(*r0)} {pt(*r1)} {pt(*q1)} {pt(*q0)}"/>'
            f'<line class="lane" x1="{m0[0]:.1f}" y1="{m0[1]:.1f}" x2="{m1[0]:.1f}" y2="{m1[1]:.1f}"/>'
            f'<g class="drive" style="offset-path:path(\'M{m0[0]:.1f} {m0[1]:.1f} L{m1[0]:.1f} {m1[1]:.1f}\')">'
            f'<path d="M-6 -2.5 h12 v5 h-12 Z" class="car"/><circle cx="7" cy="-1.5" r="1.3" class="hl"/><circle cx="7" cy="1.5" r="1.3" class="hl"/></g>')
    signs = []
    for name, s, e, _, _ in JOBS:  # street names under each job's stretch of the city
        first, last = max(s, start), min(e or today, today)
        if first > last:
            continue
        mid = first + (last - first) / 2
        wk = (mid - start).days / 7
        sx, sy = edge(wk, 11.2)
        signs.append(f'<text class="street" transform="translate({sx:.1f},{sy:.1f}) rotate(30.07)" text-anchor="middle">{name.upper()} AVE</text>')

    stars = []
    for _ in range(80):
        sx, sy = rng.uniform(10, 830), rng.uniform(10, 330)
        if sx < 260 and 70 < sy < 260:  # keep the stats text readable
            continue
        stars.append(f'<circle class="s{rng.randint(1, 3)}" cx="{sx:.0f}" cy="{sy:.0f}" r="{rng.uniform(.5, 1.4):.1f}" '
                     f'style="animation-delay:{rng.uniform(0, 4):.1f}s"/>')

    legend = "".join(f'<rect class="w{k}" x="{24 + 160 * i}" y="486" width="14" height="4" rx="1" style="animation:none;opacity:1"/>'
                     f'<text class="lbl" x="{44 + 160 * i}" y="492">{name} lights</text>' for i, (name, k) in enumerate(
                         [(n, k) for n, _, _, k, _ in JOBS if k in set(owner.values())]))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="520" viewBox="0 0 840 520" role="img" aria-labelledby="ct cd">
  <title id="ct">Contribution city: the last 12 months at night</title>
  <desc id="cd">An isometric city with one building per day; taller buildings and more lit windows mean more contributions. {total:,} contributions, busiest day {totals.get(busiest, 0):,} on {busiest:%b} {busiest.day}, longest streak {longest} days.</desc>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060914"/><stop offset=".6" stop-color="#121735"/><stop offset="1" stop-color="#241b45"/></linearGradient>
    <radialGradient id="glow"><stop offset="0" stop-color="#fff6d5" stop-opacity=".35"/><stop offset="1" stop-color="#fff6d5" stop-opacity="0"/></radialGradient>
  </defs>
  <style>
    text {{ font-family: {FONT}; }}
    .h {{ fill: #f0f3f8; font-size: 16px; font-weight: 600; }} .lbl {{ fill: #a8b0c2; font-size: 12px; }}
    .num {{ fill: #f0f3f8; font-size: 26px; font-weight: 600; }} .ax {{ fill: #6e7690; font-size: 11px; }}
    .street {{ fill: #8790ad; font-size: 8px; letter-spacing: 2px; font-weight: 600; }}
    .lot {{ fill: #171c36; }}
    .gt {{ fill: #4a3a80; }} .gl {{ fill: #2c2257; }} .gr {{ fill: #1e1740; }}
    .at {{ fill: #2d4a7c; }} .al {{ fill: #1b2f58; }} .ar {{ fill: #132241; }}
    .pt {{ fill: #2d5e48; }} .pl {{ fill: #1b3d2e; }} .pr {{ fill: #122a20; }}
    .wg, .wa, .wp {{ stroke-width: 2.2; fill: none; opacity: 0; animation: on .6s ease-out forwards; }}
    .wg {{ stroke: #e2b8ff; }} .wa {{ stroke: #ffd27a; }} .wp {{ stroke: #b6f5c8; }}
    rect.wg {{ fill: #e2b8ff; }} rect.wa {{ fill: #ffd27a; }} rect.wp {{ fill: #b6f5c8; }}
    .bl {{ animation: on .6s ease-out forwards, flicker 3s steps(1) infinite; }}
    .beacon {{ fill: #ff4d4d; animation: beacon 1.6s ease-in-out infinite; }}
    .road {{ fill: #10142a; }} .lane {{ stroke: #59627f; stroke-width: 1; stroke-dasharray: 6 6; }}
    .car {{ fill: #e86a5a; }} .hl {{ fill: #fff3b0; }}
    .drive {{ offset-rotate: auto; animation: drive 16s linear infinite; }}
    @keyframes drive {{ from {{ offset-distance: 0%; }} to {{ offset-distance: 100%; }} }}
    .s1, .s2, .s3 {{ fill: #ffffff; animation: twinkle 3s ease-in-out infinite; }}
    .s2 {{ animation-duration: 4.5s; }} .s3 {{ animation-duration: 6s; }}
    @keyframes on {{ to {{ opacity: .95; }} }}
    @keyframes flicker {{ 0%, 70% {{ opacity: .95; }} 71%, 100% {{ opacity: .15; }} }}
    @keyframes beacon {{ 0%, 100% {{ opacity: .2; }} 50% {{ opacity: 1; }} }}
    @keyframes twinkle {{ 0%, 100% {{ opacity: .9; }} 50% {{ opacity: .2; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .wg, .wa, .wp {{ opacity: .95; }} }}
  </style>
  <rect x="0" y="0" width="840" height="520" rx="10" fill="url(#sky)"/>
  {"".join(stars)}
  <circle cx="752" cy="74" r="60" fill="url(#glow)"/><circle cx="752" cy="74" r="22" fill="#f6efd2"/>
  <circle cx="745" cy="68" r="4" fill="#e4dbb6"/><circle cx="760" cy="82" r="3" fill="#e4dbb6"/>
  <text class="h" x="24" y="38">Contribution city</text>
  <text class="lbl" x="24" y="57">Every building is a day of code from the last 12 months</text>
  <text class="num" x="24" y="110">{total:,}</text><text class="lbl" x="24" y="129">contributions</text>
  <text class="num" x="24" y="172">{totals.get(busiest, 0):,}</text><text class="lbl" x="24" y="191">on my busiest day ({busiest:%b} {busiest.day})</text>
  <text class="num" x="24" y="234">{longest}</text><text class="lbl" x="24" y="253">day longest streak</text>
  {road}
  {"".join(signs)}
  {body}
  {legend}
  <text class="ax" x="816" y="505" text-anchor="end">updated {today:%b} {today.day}, {today.year}</text>
</svg>
"""


# ---------------------------------------------------------------- career timeline

def timeline(by_job, today):
    """by_job: {css key: {date: count}} restricted to that job's dates."""
    t0, t1 = JOBS[0][1], today
    x0, x1, base = 40, 800, 150
    X = lambda d: x0 + (x1 - x0) * (d - t0).days / max((t1 - t0).days, 1)
    weekly = {}
    for k, days in by_job.items():
        for d, c in days.items():
            if t0 <= d <= t1:
                wk = d - dt.timedelta(days=d.weekday())
                weekly.setdefault(k, {}).setdefault(wk, 0)
                weekly[k][wk] += c
    peak = max((v for wk in weekly.values() for v in wk.values()), default=1)
    areas, blocks = [], []
    for i, (name, s, e, k, blurb) in enumerate(JOBS):
        e = e or today
        weeks = weekly.get(k, {})
        pts = [(X(s), base)]
        wk = s - dt.timedelta(days=s.weekday())
        while wk <= e:
            v = weeks.get(wk, 0)
            pts.append((X(max(wk, s) + dt.timedelta(days=3)), base - 70 * (v / peak) ** 0.6))
            wk += dt.timedelta(days=7)
        pts.append((X(e), base))
        d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
        n = sum(by_job.get(k, {}).get(day, 0) for day in by_job.get(k, {}) if s <= day <= e)
        areas.append(f'<path class="{k}a" d="{d} Z" style="animation-delay:{0.3 + i * 0.9}s"/>'
                     f'<path class="{k}s" d="{d}" pathLength="1" style="animation-delay:{0.3 + i * 0.9}s"/>')
        cx = (X(s) + X(e)) / 2
        span = f"{s:%b %Y} – " + ("now" if JOBS[i][2] is None else f"{e:%b %Y}")
        blocks.append(f'<line class="{k}s tick" x1="{X(s):.1f}" y1="{base - 2}" x2="{X(s):.1f}" y2="{base + 10}"/>'
                      f'<text class="name" x="{cx:.1f}" y="{base + 34}" text-anchor="middle">{name}</text>'
                      f'<text class="ax" x="{cx:.1f}" y="{base + 52}" text-anchor="middle">{span} · {n:,} contributions</text>'
                      f'<text class="lbl" x="{cx:.1f}" y="{base + 70}" text-anchor="middle">{esc(blurb)}</text>')
    now = X(today)
    light = "--ga:#8250df; --aa:#2f6fde;"
    dark = "--ga:#a371f7; --aa:#4c8df6;"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="250" viewBox="0 0 840 250" role="img" aria-labelledby="lt ld">
  <title id="lt">Career timeline</title>
  <desc id="ld">{"; ".join(f"{n}: {s:%b %Y} to {'now' if e is None else f'{e:%b %Y}'}" for n, s, e, _, _ in JOBS)}. Area shows weekly contributions.</desc>
  <style>{THEMED.format(light=light, dark=dark)}
    .name {{ fill: var(--ink); font-size: 15px; font-weight: 600; }}
    .ga {{ fill: var(--ga); }} .aa {{ fill: var(--aa); }}
    .ga, .aa {{ fill-opacity: 0; animation: fill .8s ease-out forwards; }}
    .gs, .as {{ fill: none; stroke-width: 2; stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 1.2s ease-out forwards; }}
    .gs {{ stroke: var(--ga); }} .as {{ stroke: var(--aa); }}
    .tick {{ stroke-dasharray: none; stroke-dashoffset: 0; animation: none; }}
    .axis {{ stroke: var(--border); stroke-width: 2; }}
    .now {{ fill: var(--aa); }} .pulse {{ fill: none; stroke: var(--aa); stroke-width: 2; animation: pulse 2s ease-out infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes fill {{ to {{ fill-opacity: .18; }} }}
    @keyframes pulse {{ from {{ transform: scale(1); opacity: 1; }} to {{ transform: scale(3); opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; stroke-dashoffset: 0 !important; }} .ga, .aa {{ fill-opacity: .18; }} }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="839" height="249" rx="8"/>
  <text class="h" x="24" y="34">Career</text>
  <text class="ax" x="816" y="34" text-anchor="end">area = weekly contributions</text>
  <line class="axis" x1="{x0}" y1="{base}" x2="{x1}" y2="{base}"/>
  {"".join(areas)}
  {"".join(blocks)}
  <circle class="pulse" cx="{now:.1f}" cy="{base}" r="5"/><circle class="now" cx="{now:.1f}" cy="{base}" r="5"/>
  <text class="ax" x="{now - 8:.1f}" y="{base - 80}" text-anchor="end">now</text>
</svg>
"""


# ---------------------------------------------------------------- stack

def stack(today):
    total = sum(n for _, n, _ in LANGUAGES)
    cx, cy, r = 130, 135, 70
    circ = 2 * math.pi * r
    arcs, legend, acc = [], [], 0
    for i, (name, n, k) in enumerate(LANGUAGES):
        frac = n / total
        gap = 2 if frac > 0.01 else 0
        arcs.append(f'<circle class="arc {k}" cx="{cx}" cy="{cy}" r="{r}" pathLength="{circ:.1f}" '
                    f'stroke-dasharray="{max(frac * circ - gap, 0.5):.1f} {circ:.1f}" stroke-dashoffset="{-acc * circ:.1f}" '
                    f'style="animation-delay:{0.2 + i * 0.15:.2f}s"/>')
        acc += frac
        y = 70 + i * 26
        legend.append(f'<rect class="{k}f" x="250" y="{y - 10}" width="12" height="12" rx="3"/>'
                      f'<text class="lbl" x="270" y="{y}">{name}</text>'
                      f'<text class="v" x="430" y="{y}" text-anchor="end">{frac:.0%}</text>'
                      f'<text class="ax" x="440" y="{y}">{n / 1000:,.0f}K lines</text>')
    pills, px, py = [], 520, 72
    for name in STACK:
        w = 18 + len(name) * 6.8
        if px + w > 816:
            px, py = 520, py + 30
        pills.append(f'<rect class="pill" x="{px:.0f}" y="{py - 15}" width="{w:.0f}" height="22" rx="11"/>'
                     f'<text class="pt" x="{px + w / 2:.0f}" y="{py}" text-anchor="middle">{name}</text>')
        px += w + 8
    light = "--ts:#2f6fde; --tsx:#1fa3a3; --sql:#d9822b; --py:#c2477f; --sh:#7a5af5; --oth:#8c959f;"
    dark = "--ts:#4c8df6; --tsx:#22a5a5; --sql:#cf7f33; --py:#d0578f; --sh:#8a6ff0; --oth:#6e7681;"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="270" viewBox="0 0 840 270" role="img" aria-labelledby="kt kd">
  <title id="kt">What I write and what I build with</title>
  <desc id="kd">Lines of code added this year by language: {", ".join(f"{n} {c / total:.0%}" for n, c, _ in LANGUAGES)}. Stack: {", ".join(STACK)}.</desc>
  <style>{THEMED.format(light=light, dark=dark)}
    .v {{ fill: var(--ink); font-size: 12px; font-weight: 600; }}
    .arc {{ fill: none; stroke-width: 22; transform: rotate(-90deg); transform-origin: {cx}px {cy}px; opacity: 0; animation: in .5s ease-out forwards; }}
    .ts {{ stroke: var(--ts); }} .tsx {{ stroke: var(--tsx); }} .sql {{ stroke: var(--sql); }} .py {{ stroke: var(--py); }} .sh {{ stroke: var(--sh); }} .oth {{ stroke: var(--oth); }}
    .tsf {{ fill: var(--ts); }} .tsxf {{ fill: var(--tsx); }} .sqlf {{ fill: var(--sql); }} .pyf {{ fill: var(--py); }} .shf {{ fill: var(--sh); }} .othf {{ fill: var(--oth); }}
    .pill {{ fill: var(--bg); stroke: var(--border); }}
    .pt {{ fill: var(--ink2); font-size: 11.5px; }}
    @keyframes in {{ to {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{ .arc {{ animation: none; opacity: 1; }} }}
  </style>
  <rect class="bg" x="0.5" y="0.5" width="839" height="269" rx="8"/>
  <text class="h" x="24" y="34">What I write</text>
  <text class="h" x="520" y="34">What I build with</text>
  {"".join(arcs)}
  <text class="num" x="{cx}" y="{cy + 4}" text-anchor="middle">{total / 1e6:.1f}M</text>
  <text class="ax" x="{cx}" y="{cy + 22}" text-anchor="middle">lines this year</text>
  {"".join(legend)}
  {"".join(pills)}
  <text class="ax" x="24" y="252">Lines added this year · Astorie from git, Adsgency AI (600K+) self-reported · Nov 2026</text>
</svg>
"""


# ---------------------------------------------------------------- highlights

def highlights(year_total, today, prs=PRS_MERGED):
    lines = sum(n for _, n, _ in LANGUAGES)
    output = [(f"{lines / 1e6:.1f}M+", "lines of code this year", "Astorie + AdsGency AI"),
              (FEATURES, "features shipped", "Astorie + AdsGency AI"),
              (f"{year_total / 1000:.1f}K", "contributions in 12 months", "all GitHub accounts"),
              (f"{prs + ADSGENCY_PRS:,}", "PRs merged", "Astorie + AdsGency AI")]
    rows = [("Scale of what I build on", IMPACT), ("What I ship", output)]
    tiles = [t for _, row in rows for t in row]
    body = []
    for r, (title, row) in enumerate(rows):
        y = 34 + r * 158
        body.append(f'<text class="h" x="24" y="{y}">{title}</text>')
        for i, (big, small, src) in enumerate(row):
            x, n = 24 + i * 204, r * 4 + i
            body.append(f'<g class="tile" style="animation-delay:{0.1 + n * 0.1:.2f}s">'
                        f'<rect class="card" x="{x}" y="{y + 14}" width="188" height="118" rx="10"/>'
                        f'<rect class="k{i}" x="{x}" y="{y + 14}" width="4" height="118" rx="2"/>'
                        f'<text class="big" x="{x + 20}" y="{y + 64}">{esc(big)}</text>'
                        f'<text class="lbl" x="{x + 20}" y="{y + 90}">{small}</text>'
                        f'<text class="ax" x="{x + 20}" y="{y + 112}">{src}</text></g>')
    light = "--k0:#2f6fde; --k1:#c2477f; --k2:#1fa3a3; --k3:#7a5af5; --card:#f6f8fa;"
    dark = "--k0:#4c8df6; --k1:#d0578f; --k2:#22a5a5; --k3:#8a6ff0; --card:#161b22;"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="840" height="340" viewBox="0 0 840 340" role="img" aria-labelledby="ht hd">
  <title id="ht">Highlights</title>
  <desc id="hd">{"; ".join(f"{esc(b)} {s} ({src})" for b, s, src in tiles)}.</desc>
  <style>{THEMED.format(light=light, dark=dark)}
    .card {{ fill: var(--card); stroke: var(--border); }}
    .big {{ fill: var(--ink); font-size: 30px; font-weight: 700; }}
    .k0 {{ fill: var(--k0); }} .k1 {{ fill: var(--k1); }} .k2 {{ fill: var(--k2); }} .k3 {{ fill: var(--k3); }}
    .tile {{ animation: up .6s cubic-bezier(.2,.8,.3,1) both; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(12px); }} to {{ opacity: 1; transform: none; }} }}
    @media (prefers-reduced-motion: reduce) {{ .tile {{ animation: none; }} }}
  </style>
  {"".join(body)}
</svg>
"""
