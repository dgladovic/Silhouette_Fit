"""Build judge/results.html (local results page) from judge/results.json + model summaries. Run after judge.py."""
import os, json, html
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
R = json.load(open(os.path.join(HERE, 'results.json'), encoding='utf-8'))
rows = R['ranked'] + R['gated']


def cells(v, cls):
    return ''.join(f'<i class="{cls if x else "off"}" title="S{i+1:02d}"></i>' for i, x in enumerate(v))


def mdl(r):
    d = r['folder']
    return f"../models/{d}"


rank_rows = []
for r in rows:
    b, c = r['built'], r['components']
    rank_rows.append(f"""<tr><td class="n">{r.get('rank', '—')}</td><td><b>{r['id']}</b><span class="sub">{html.escape(r['title'])}</span></td>
<td class="n score">{r['score']:.3f}</td><td class="n">{b['front_pass']}/19</td><td class="n">{b['v34_pass']}/19</td>
<td class="n">{b['rib_mean']:.2f}</td><td class="n">{b['within1']:.0f} %</td><td class="n">{b['v34_mean']:.2f}</td>
<td class="n">{c['loc']:.2f}</td><td class="n">{r['n_params']}</td><td class="n">{r['fit']['cost']:.0f}</td></tr>""")

strips = []
for r in rows:
    strips.append(f"""<div class="strip"><div class="sid"><b>{r['id']}</b></div>
<div><div class="lab">front</div><div class="cells">{cells(r['seg_front'], 'ok')}</div></div>
<div><div class="lab">3/4 held out</div><div class="cells">{cells(r['seg_v34'], 'ok2')}</div></div></div>""")

top = R['ranked'][:3]
figs = []
for r in top:
    d = mdl(r)
    figs.append(f"""<figure><figcaption><b>{r['id']}</b> — rank {r['rank']}</figcaption>
<img src="{d}/E0_fit/overlay_front.png" alt="{r['id']} front overlay"><img src="{d}/E0_fit/overlay_v34.png" alt="{r['id']} 3/4 overlay">
<a href="{d}/MODEL.md">MODEL.md</a> · <a href="{d}/PROGRESS.md">PROGRESS.md</a> · <a href="{d}/E0_fit/report.md">E0 report</a> · <a href="{d}/E4_twist/influence_map.png">twist influence map</a></figure>""")

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lamp Model Study</title>
<style>
:root {{ --bg:#f6f7f5; --fg:#1d2321; --mut:#66706b; --line:#d9ddd9; --ok:#2f8f5b; --ok2:#3b6fb6; --off:#e3e6e3; --card:#ffffff;
  --mono: ui-monospace, "Cascadia Mono", Consolas, monospace; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#141816; --fg:#e7ebe8; --mut:#9aa39e; --line:#2c332f; --ok:#4cc286; --ok2:#6c9be0; --off:#2a302d; --card:#1b201d; }} }}
body {{ background:var(--bg); color:var(--fg); font:15px/1.5 "Segoe UI", system-ui, sans-serif; margin:0; padding:24px max(16px, 3vw); }}
h1 {{ font-size:1.6rem; margin:0 0 .2rem }} h2 {{ font-size:1.1rem; margin:2rem 0 .6rem }} .mut {{ color:var(--mut) }}
table {{ border-collapse:collapse; width:100%; font-variant-numeric:tabular-nums; }} .wrap {{ overflow-x:auto }}
th, td {{ padding:6px 8px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top }} th {{ font-size:.8rem; color:var(--mut); font-weight:600 }}
td.n {{ text-align:right; white-space:nowrap }} .score {{ font-weight:700 }} .sub {{ display:block; color:var(--mut); font-size:.82rem }}
.strip {{ display:grid; grid-template-columns:56px 1fr 1fr; gap:12px; align-items:end; padding:6px 0; border-bottom:1px solid var(--line) }}
.lab {{ font-size:.72rem; color:var(--mut) }} .cells {{ display:grid; grid-template-columns:repeat(19, 1fr); gap:2px }}
.cells i {{ height:14px; border-radius:2px; background:var(--off) }} .cells i.ok {{ background:var(--ok) }} .cells i.ok2 {{ background:var(--ok2) }}
.figs {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:16px }}
figure {{ margin:0; background:var(--card); border:1px solid var(--line); border-radius:6px; padding:10px; font-size:.85rem }} figure img {{ width:100%; display:block; margin:6px 0 }}
a {{ color:var(--ok2) }} ul {{ padding-left:1.2rem }} li {{ margin:.25rem 0 }}
</style></head><body>
<h1>Lamp Model Study</h1>
<p class="mut">10 model setups · fitted to the front drawing · scored as built per 10 mm segment (S01 bottom → S19 top) · 3/4 drawing held out · kernel v3 · scoring rules fixed before the runs</p>

<h2>Ranking</h2>
<div class="wrap"><table><thead><tr><th>#</th><th>Model</th><th>Score</th><th>Front pass</th><th>3/4 pass</th><th>Ribs mean mm</th><th>Ribs ≤1 mm</th><th>3/4 mean mm</th><th>Locality</th><th>Params</th><th>Fit cost</th></tr></thead>
<tbody>{''.join(rank_rows)}</tbody></table></div>
<p class="mut">Score = 0.35 front + 0.30 held-out 3/4 + 0.15 locality + 0.10 simplicity + 0.10 smoothness. Pass-count differences of about ±2 segments are within optimiser noise.</p>

<h2>Where each model passes</h2>
<div>{''.join(strips)}</div>

<h2>What the study found</h2>
<ul>
<li><b>The base shape decides most of it.</b> The custom spline (M01–M04) and the rose with an 8θ term (M07) reach fit cost 73–95. Every plain-rose model stays at 160–176, whatever its radius or twist curve. The drawing wants fuller lobes with sharper creases than a rose; a superformula (M08) can't do better than the rose.</li>
<li><b>The lamp in the drawing is rotated about −1.4°</b> against twist(0) = 0. Freeing that orientation halved the cost of M01 and M04.</li>
<li><b>Twist is the most sensitive parameter.</b> Scaling it by 3 % adds 0.5–0.9 mm of rib error in every model. Radius ±1 mm drops the front outline to 0/19.</li>
<li><b>Triangles mostly shift the outline.</b> Height moves it 1:1, count by up to ±0.5 mm, width by ≤ 0.2 mm; none of them moves the ribs. Sections matter little: ≥ 15 sections stay within 0.15 mm of the exact curves.</li>
<li><b>Local control isn't the bottleneck.</b> The 10 mm knot models move single segments cleanly (locality 0.96) but don't beat the 15–19-parameter custom-spline models.</li>
<li><b>Still failing in every top model:</b> S01 (the drawn rim edge is a rounded corner) and parts of the waist S08–S11, where neighbouring ribs are off in opposite directions.</li>
</ul>

<h2>Top 3 — overlays</h2>
<div class="figs">{''.join(figs)}</div>
<p class="mut">Full tables: <a href="RESULTS.md">judge/RESULTS.md</a> · verification: <a href="verify_e0.md">judge/verify_e0.md</a> · kernel history: <a href="../models/_common/PROGRESS.md">models/_common/PROGRESS.md</a></p>
</body></html>"""
open(os.path.join(HERE, 'results.html'), 'w', encoding='utf-8').write(page)
print('judge/results.html written')
