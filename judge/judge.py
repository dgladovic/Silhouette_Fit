"""
Judge (docs/05_EXPERIMENTS.md §5.8 — weights fixed before any result was seen, approved by the user).

  score = 0.35 Fit + 0.30 Held-out + 0.15 Locality + 0.10 Simplicity + 0.10 Smoothness
  Fit        = segments passing front outline + ribs (E0, as built) / 19
  Held-out   = segments with 3/4 mean <= 0.75 mm (E0, as built) / 19
  Locality   = mean share of a 1-knot bump that stays in its 2 segments (E4b twist + E5b radius)
  Simplicity = 1 / (1 + n_params / 30)
  Smoothness = 1 / (1 + extra inflections / 2)
  Gate       = buildable (constraints pass, loft deviation at 20 uniform sections <= 0.3 mm); not ranked otherwise
  Ties within 0.02 -> the simpler model ranks first.

Run: python judge/judge.py   -> judge/RESULTS.md, judge/results.json
Reading: pass-count differences of about ±2 segments are within optimiser noise (models/_common/PROGRESS.md).
"""
import os, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W = dict(fit=0.35, held=0.30, loc=0.15, simple=0.10, smooth=0.10)


def strip(v):
    return ''.join('█' if x else '·' for x in v)


def main():
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'models', 'M*', 'summary.json'))):
        s = json.load(open(f, encoding='utf-8'))
        c = dict(fit=s['built']['front_pass'] / 19, held=s['built']['v34_pass'] / 19,
                 loc=s['locality'] if s['locality'] is not None else 0.0,
                 simple=1 / (1 + s['n_params'] / 30), smooth=s['smooth']['score'])
        s['components'] = c
        s['score'] = sum(W[k] * c[k] for k in W)
        rows.append(s)
    ranked = sorted([r for r in rows if r['buildable']], key=lambda r: (-round(r['score'] / 0.02), r['n_params'], -r['score']))
    gated = [r for r in rows if not r['buildable']]
    for i, r in enumerate(ranked):
        r['rank'] = i + 1
    json.dump(dict(weights=W, ranked=ranked, gated=gated), open(os.path.join(HERE, 'results.json'), 'w'), indent=1)

    L = ["# Model study — results\n",
         "Scoring rules fixed before the runs (`docs/05_EXPERIMENTS.md` §5.8). All numbers **as built** (loft through the "
         "model's own sections), E0 fit on the front drawing only, 3/4 drawing held out. Kernel v3: free orientation offset, "
         "multi-start from a shared pool. Pass-count differences of about ±2 segments are within optimiser noise; ties "
         "within 0.02 go to the simpler model.\n",
         "## Ranking\n",
         "| # | Model | Score | Front pass | 3/4 pass | Locality (twist / radius) | Params | Smooth | Ribs mean · ≤1 mm | 3/4 mean | Outline max |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in ranked:
        b = r['built']
        L.append(f"| {r['rank']} | **{r['id']}** {r['title']} | **{r['score']:.3f}** | {b['front_pass']}/19 | {b['v34_pass']}/19 | "
                 f"{r['components']['loc']:.2f} ({(r['locality_twist'] or 0):.2f} / {(r['locality_radius'] or 0):.2f}) | {r['n_params']} | "
                 f"{r['components']['smooth']:.2f} | {b['rib_mean']:.2f} mm · {b['within1']:.0f} % | {b['v34_mean']:.2f} mm | {b['sil_max']:.2f} mm |")
    for r in gated:
        L.append(f"| — | {r['id']} (not buildable: {r['constraints'] or 'loft deviation ' + str(r['loft_dev_20'])}) | {r['score']:.3f} | | | | | | | | |")
    L += ["\n## Per segment (S01 → S19, █ = pass)\n", "| Model | Front (as built) | Front (exact curves) | 3/4 (held out) |", "|---|---|---|---|"]
    for r in ranked + gated:
        L.append(f"| {r['id']} | `{strip(r['seg_front'])}` | `{strip(r['seg_front_exact'])}` | `{strip(r['seg_v34'])}` |")
    L += ["\n## Rib mean per segment (mm, as built)\n", "| Model | " + " | ".join(f"S{i:02d}" for i in range(1, 20)) + " |",
          "|---|" + "---|" * 19]
    for r in ranked + gated:
        L.append(f"| {r['id']} | " + " | ".join('—' if v is None else f"{v:.2f}" for v in r['seg_rib_mean']) + " |")
    L += ["\n## Score components\n", "| Model | Fit ×0.35 | Held-out ×0.30 | Locality ×0.15 | Simplicity ×0.10 | Smoothness ×0.10 | Loft dev @20 sections |",
          "|---|---|---|---|---|---|---|"]
    for r in ranked + gated:
        c = r['components']
        L.append(f"| {r['id']} | {c['fit']:.2f} | {c['held']:.2f} | {c['loc']:.2f} | {c['simple']:.2f} | {c['smooth']:.2f} | "
                 f"{'—' if r['loft_dev_20'] is None else f'{r['loft_dev_20']:.2f} mm'} |")
    open(os.path.join(HERE, 'RESULTS.md'), 'w', encoding='utf-8').write("\n".join(L) + "\n")
    for r in ranked:
        print(f"{r['rank']:2d} {r['id']} {r['score']:.3f} front {r['built']['front_pass']}/19 3/4 {r['built']['v34_pass']}/19 params {r['n_params']}")


if __name__ == '__main__':
    main()
