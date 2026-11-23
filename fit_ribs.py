"""
Fit profile + twist + lobe depth k(z) so that the model hits the drawing at the checkpoints:
  - silhouette (every 2 mm)
  - 15 traced drawing ribs: model rib from the same start must stay on the drawn rib (every 4 mm)
Prints the 10 mm checkpoint table before and after, saves fit_ribs_result.txt + checkpoints_fitted.png.

Run: python fit_ribs.py
"""
import os, sys, json
import numpy as np
from scipy.optimize import least_squares
import model as m
import checkpoints as cp
from render_folds import read_fit

HERE = os.path.dirname(os.path.abspath(__file__))
N_PROF = 8
N_TW = int(sys.argv[1]) if len(sys.argv) > 1 else 5
LOSS = sys.argv[2] if len(sys.argv) > 2 else 'soft_l1'
OUT_TAG = sys.argv[3] if len(sys.argv) > 3 else ''
KZ = m.K_NODES_Z
Z_SIL = np.arange(0.0, 190.01, 2.0)
S_TARGET = cp.S_OF_Z(Z_SIL)
W_SIL = 2.0

TRACES = [t for t in cp.trace_all() if len(t[1]) >= 30]
RIB_SAMPLES = []
for x0, zt, xt in TRACES:
    o = np.argsort(zt)
    zs = np.arange(4.0, zt.max() - 5.0, 4.0)
    RIB_SAMPLES.append((x0, zs, np.interp(zs, zt[o], xt[o])))


def unpack(x):
    k = 0
    prof = [(x[k], 0.0)]; k += 1
    for _ in range(N_PROF - 2):
        prof.append((x[k], x[k + 1])); k += 2
    prof.append((x[k], m.HEIGHT)); k += 1
    tw = [(0.0, 0.0)]
    for _ in range(N_TW - 2):
        tw.append((x[k], x[k + 1])); k += 2
    tw.append((1.0, x[k])); k += 1
    kv = list(x[k:k + len(KZ)])
    return prof, tw, kv


def apply(x):
    prof, tw, kv = unpack(x)
    m.K_OF_Z = m.catmull_rom(KZ, kv)
    return prof, (lambda t: m.twist_deg(tw, t)), tw, kv


def residuals(x):
    prof, fn, tw, kv = apply(x)
    res = [W_SIL * (m.silhouettes(prof, fn, Z_SIL)[0] - S_TARGET)]
    for x0, zs, xd in RIB_SAMPLES:
        xm, vis = cp.model_rib(prof, fn, x0, zs)
        res.append(np.where(vis, xm - xd, 0.0))
    zs_ = [p[1] for p in prof]; ts = [p[0] for p in tw]
    res.append(20 * np.minimum(np.diff(zs_), 0)); res.append(200 * np.minimum(np.diff(ts), 0))
    res.append(50 * np.minimum(np.array(kv) - 0.02, 0))          # keep lobe depth positive
    res.append(2.0 * np.diff(kv, 2))                              # gentle smoothness on k(z)
    return np.concatenate(res)


def x_from(prof, tw, kv):
    x = [prof[0][0]]
    for r, z in prof[1:-1]:
        x += [r, z]
    x += [prof[-1][0]]
    for t, a in tw[1:-1]:
        x += [t, a]
    x += [tw[-1][1]]
    return np.array(x + list(kv), float)


def main():
    prev = os.path.join(HERE, 'fit_ribs_result.json')
    if os.path.exists(prev):                     # continue from the last checkpoint fit
        d = json.load(open(prev))
        prof = [tuple(p) for p in d['BEZIER_CONTROL_POINTS']]; kv0 = d['LOBE_DEPTH_K']
        tw = [tuple(p) for p in d['twist_points']]
        if len(tw) != N_TW:                      # resample twist into N_TW control points
            ts = np.linspace(0, 1, N_TW); ang = m.twist_deg(tw, ts)
            tw = [(float(t), float(a)) for t, a in zip(ts, ang)]
    else:
        prof, tw = read_fit()
        kv0 = [float(m.K_OF_Z(z)) if m.K_OF_Z else 0.2 for z in KZ]
    x0 = x_from(prof, tw, kv0)
    p, fn, _, _ = apply(x0)
    cp.evaluate(p, fn, TRACES, label='BEFORE (current scripts)')

    # hard limits: twist control-point t values must stay in 0..1 (Fusion's twist lookup needs that)
    lb = np.full(len(x0), -np.inf); ub = np.full(len(x0), np.inf)
    k0 = 2 + 2 * (N_PROF - 2)
    for j in range(N_TW - 2):
        lb[k0 + 2 * j], ub[k0 + 2 * j] = 0.0, 1.0
    x0 = np.clip(x0, lb + 1e-6, ub - 1e-6)
    best = None
    for diff in (1e-3, 1e-4):
        r = least_squares(residuals, x0 if best is None else best.x, bounds=(lb, ub), x_scale='jac', diff_step=diff, loss=LOSS, f_scale=1.5,
                          xtol=1e-12, ftol=1e-10, gtol=1e-10, max_nfev=400, verbose=1)
        if best is None or r.cost < best.cost:
            best = r
    r = best
    prof, fn, tw, kv = apply(r.x)
    rows, err, sil = cp.evaluate(prof, fn, TRACES, label='AFTER (profile + twist + lobe depth fitted to checkpoints)')
    out = {'BEZIER_CONTROL_POINTS': [list(map(float, p)) for p in prof],
           'twist_points': [list(map(float, p)) for p in tw],
           'LOBE_DEPTH_Z': KZ, 'LOBE_DEPTH_K': [float(v) for v in kv],
           'rib_mean_abs_mm': float(np.mean(np.abs(err))), 'rib_max_mm': float(np.max(np.abs(err))),
           'within_1mm_pct': float(np.mean(np.abs(err) <= 1) * 100), 'sil_max_mm': float(np.max(np.abs(sil)))}
    json.dump(out, open(os.path.join(HERE, f'fit_ribs_result{OUT_TAG}.json'), 'w'), indent=1)
    print({k: out[k] for k in ('rib_mean_abs_mm', 'rib_max_mm', 'within_1mm_pct', 'sil_max_mm')})
    try:
        cp.draw(prof, fn, TRACES, os.path.join(HERE, f'checkpoints_fitted{OUT_TAG}.png'))
    except Exception as e:
        import traceback; traceback.print_exc()


if __name__ == '__main__':
    main()
