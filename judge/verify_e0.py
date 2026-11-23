"""
Independent E0 check (docs/05 §5.10 'verify'): rebuild every model from E0_fit/params.json, recompute all 19-segment
metrics from scratch (as built, with the saved camera) and compare with E0_fit/metrics.json. Also re-checks constraints.

Run: python judge/verify_e0.py [M01 M02 ...]   -> judge/verify_e0.md
"""
import os, sys, glob, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'models', '_common'))
import study as S, score as SC

TOL = 0.02


def check(model_dir):
    model, p, cam = S.load_E0(model_dir)
    saved = json.load(open(os.path.join(model_dir, 'E0_fit', 'metrics.json')))['built']
    res = SC.evaluate(model.shape(p), model.SETTINGS, built=True, camera=cam)
    bad = []
    for a, b in zip(res['seg'], saved['seg']):
        for k in ('sil_max', 'sil_bias', 'rib_mean', 'within1', 'v34_mean'):
            x, y = a[k], b[k]
            if (x is None) != (y is None) or (x is not None and abs(x - y) > (1.0 if k == 'within1' else TOL)):
                bad.append(f"{a['id']} {k}: recomputed {x} vs saved {y}")
        if a['pass_front'] != b['pass_front'] or a['pass_v34'] != b['pass_v34']:
            bad.append(f"{a['id']} pass flags differ")
    cons = model.constraints(p)
    t = res['tot']
    return dict(id=model.ID, ok=not bad and not cons, mismatches=bad, constraints=cons,
                line=f"front {t['front_pass']}/19 (saved {saved['tot']['front_pass']}), 3/4 {t['v34_pass']}/19 (saved {saved['tot']['v34_pass']})")


def main(ids):
    out = ["# E0 verification — recomputed from params.json\n", "| Model | Result | Recomputed vs saved | Problems |", "|---|---|---|---|"]
    for d in sorted(glob.glob(os.path.join(ROOT, 'models', 'M*'))):
        if not os.path.exists(os.path.join(d, 'E0_fit', 'params.json')):
            continue
        mid = os.path.basename(d)[:3]
        if ids and mid not in ids:
            continue
        r = check(d)
        out.append(f"| {r['id']} | {'✅ confirmed' if r['ok'] else '❌'} | {r['line']} | "
                   f"{'; '.join(r['mismatches'][:5] + r['constraints']) or 'none'} |")
        print(out[-1])
    open(os.path.join(HERE, 'verify_e0.md'), 'w', encoding='utf-8').write("\n".join(out) + "\n")


if __name__ == '__main__':
    main(sys.argv[1:])
