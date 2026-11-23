"""
Per-segment scoring against both targets (docs/03_SEGMENTS.md §3.3, docs/05_EXPERIMENTS.md §5.4-5.5).

evaluate(shape, settings, built=True, camera=None)  -> full result (19-segment table, totals, camera)
fit_residuals(shape, settings)                       -> residual vector of the E0 protocol (front only, exact curves)
"""
import os, json
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import least_squares
import targets as T
import geometry as G

ROOT = T.ROOT
SEGS = json.load(open(os.path.join(ROOT, 'segments.json')))
TGT = SEGS['targets']
SEG_EDGES = [(s['id'], s['z0'], s['z1']) for s in SEGS['segments']]

Z_SCORE = np.arange(0.0, 190.01, 1.0)       # outline scoring
Z_FIT = np.arange(0.0, 190.01, 2.0)         # outline fitting
Z_34 = np.arange(0.0, 190.01, 0.5)          # 3/4 model points (0.5 mm: rows near the rim need it)
W_SIL = 2.0


def seg_index(z):
    return np.clip((np.asarray(z) // 10).astype(int), 0, 18)


# ------------------------------------------------------------------------------------------------ ribs
def _rib_set(step, start, top_margin, exclude):
    """Checkpoints per drawn rib: list of (x0, z0, zc, xd, ok)."""
    f = T.front()
    out = []
    for x0, z0, zt, xt, sp in f['ribs']:
        zc = np.arange(start, zt.max() - top_margin, step)
        ok = np.ones(len(zc), bool)
        if exclude:
            ok = np.interp(zc, zt, sp) <= f['max_spread']
        out.append((x0, z0, zc, np.interp(zc, zt, xt), ok))
    return out


_RIBS = {}


def rib_set(kind='score', exclude=True):
    key = (kind, exclude)
    if key not in _RIBS:
        _RIBS[key] = _rib_set(2.0, 2.0, 1.0, exclude) if kind == 'score' else _rib_set(4.0, 4.0, 5.0, exclude)
    return _RIBS[key]


def model_ribs(shape, st, ribs, built):
    """x of the model rib at each checkpoint + visibility, per drawn rib."""
    allz = np.unique(np.concatenate([r[2] for r in ribs]))
    if built:
        zs = G.section_heights(shape, st)
        tb = G.Tables(shape, zs)
    else:
        tb = G.Tables(shape, allz)
    out = []
    for x0, z0, zc, xd, ok in ribs:
        q, inv = G.rib_start(shape, st, x0, z0)
        x, y = G.rib_xy(tb, st, q, inv)
        if built:
            sx, sy = CubicSpline(tb.Z, x), CubicSpline(tb.Z, y)
            xm, ym = sx(zc), sy(zc)
        else:
            idx = np.searchsorted(allz, zc)
            xm, ym = x[idx], y[idx]
        out.append((xm, ym < 0))
    return out


# ------------------------------------------------------------------------------------------------ 3/4 view
def project(P, cam):
    """cam = [az, el, s, cx, cy, invD, mirror] (same as views/fit_view34.py)."""
    az, el, s, cx, cy, invD, mir = cam
    a, e = np.radians(az), np.radians(el)
    x1 = P[..., 0] * np.cos(a) - P[..., 1] * np.sin(a)
    y1 = P[..., 0] * np.sin(a) + P[..., 1] * np.cos(a)
    zc = P[..., 2] - 95.0
    depth = y1 * np.cos(e) - zc * np.sin(e)
    f = 1.0 / (1.0 + invD * depth)
    u = x1 * mir * f
    v = (P[..., 2] * np.cos(e) + y1 * np.sin(e) - 95.0 * np.cos(e)) * f + 95.0 * np.cos(e)
    return np.stack([cx + s * u, cy - s * v], -1)


def points3d(shape, st, built):
    P = G.points(shape, Z_34, st, built)                      # (nz, N, 7, 2)
    A = G.all_quarters(P.reshape(len(Z_34), -1, 2))           # (nz, 4M, 2)
    zz = np.broadcast_to(Z_34[:, None], A.shape[:2])
    return np.concatenate([A, zz[..., None]], -1).reshape(-1, 3)


def v34_edges(P3, cam):
    v = T.view34()
    uv = project(P3, cam)
    rows = np.round(uv[:, 1]).astype(int); cols = uv[:, 0]
    ok = (rows >= 0) & (rows < v['H'])
    rows, cols, zz = rows[ok], cols[ok], P3[ok, 2]
    res = {}
    for side, key in (('L', cols), ('R', -cols)):
        o = np.lexsort((key, rows))
        r_s = rows[o]
        u, first = np.unique(r_s, return_index=True)
        col = dict(zip(u, cols[o][first])); zof = dict(zip(u, zz[o][first]))
        res[side] = (np.array([col.get(r, np.nan) for r in v['rows']]), np.array([zof.get(r, np.nan) for r in v['rows']]))
    return res


def v34_residual(P3, cam):
    v = T.view34(); s = cam[2]
    e = v34_edges(P3, cam)
    rl = (v['L'] - e['L'][0]) / s                  # + = model sticks out on the left
    rr = (e['R'][0] - v['R']) / s
    rl = np.where(np.isfinite(rl), rl, 5.0); rr = np.where(np.isfinite(rr), rr, 5.0)
    return np.r_[rl, rr], np.r_[e['L'][1], e['R'][1]]


def fit_camera(P3, cam0=None):
    cam0 = list(cam0 or T.view34()['camera'])
    mir = cam0[6]
    lb = [-np.inf] * 5 + [0.0]; ub = [np.inf] * 5 + [0.01]
    x0 = np.clip(cam0[:6], np.array(lb) + 1e-9, np.array(ub) - 1e-9)
    r = least_squares(lambda c: v34_residual(P3, list(c) + [mir])[0], x0, bounds=(lb, ub),
                      x_scale=[1, 1, 0.01, 1, 1, 1e-4], diff_step=1e-4, max_nfev=200)
    return list(map(float, r.x)) + [mir]


# ------------------------------------------------------------------------------------------------ evaluate
def evaluate(shape, st, built=True, camera=None, fit_cam=False, exclude=True):
    pts = G.points(shape, Z_SCORE, st, built)
    sil = G.full_outline(pts) - T.half_width(Z_SCORE)
    ribs = rib_set('score', exclude)
    mr = model_ribs(shape, st, ribs, built)
    rz, re, rx0 = [], [], []
    for (x0, z0, zc, xd, ok), (xm, vis) in zip(ribs, mr):
        m = ok & vis
        rz += list(zc[m]); re += list((xm - xd)[m]); rx0 += [x0] * int(m.sum())
    rz, re, rx0 = np.array(rz), np.array(re), np.array(rx0)
    P3 = points3d(shape, st, built)
    if camera is None or fit_cam:
        camera = fit_camera(P3, camera)
    v34, vz = v34_residual(P3, camera)
    seg = []
    for sid, z0, z1 in SEG_EDGES:
        s = sil[(Z_SCORE >= z0) & (Z_SCORE <= z1)]
        rm = (rz >= z0) & (rz < z1)
        r = re[rm]
        vm = (vz >= z0) & (vz < z1) & np.isfinite(vz)
        row = dict(id=sid, sil_max=float(np.abs(s).max()), sil_bias=float(s.mean()),
                   rib_mean=float(np.abs(r).mean()) if len(r) else None,
                   within1=float(np.mean(np.abs(r) <= 1) * 100) if len(r) else None,
                   rib_max=float(np.abs(r).max()) if len(r) else None,
                   rib_max_x0=float(rx0[rm][np.argmax(np.abs(r))]) if len(r) else None, n_rib=int(len(r)),
                   v34_mean=float(np.abs(v34[vm]).mean()) if vm.any() else None, n_v34=int(vm.sum()))
        row['pass_front'] = bool(row['sil_max'] <= TGT['sil_max_mm'] and abs(row['sil_bias']) <= TGT['sil_bias_abs_mm']
                                 and (row['rib_mean'] is None or (row['rib_mean'] <= TGT['rib_mean_mm']
                                                                  and row['within1'] >= TGT['rib_within_1mm_pct'])))
        row['pass_v34'] = bool(row['v34_mean'] is not None and row['v34_mean'] <= TGT['v34_mean_mm'])
        seg.append(row)
    tot = dict(front_pass=sum(r['pass_front'] for r in seg), v34_pass=sum(r['pass_v34'] for r in seg),
               sil_max=float(np.abs(sil).max()), rib_mean=float(np.abs(re).mean()),
               within1=float(np.mean(np.abs(re) <= 1) * 100), rib_max=float(np.abs(re).max()),
               v34_mean=float(np.abs(v34).mean()), v34_max=float(np.abs(v34).max()), n_rib=int(len(re)))
    return dict(seg=seg, tot=tot, camera=camera, built=built, sil=sil, rib=(rz, re, rx0), v34=(v34, vz))


def fit_residuals(shape, st):
    """E0 protocol: front outline every 2 mm (x W_SIL) + drawn ribs every 4 mm, exact curves, unreliable ribs skipped."""
    pts = G.points(shape, Z_FIT, st, built=False)
    res = [W_SIL * (G.full_outline(pts) - T.half_width(Z_FIT))]
    ribs = rib_set('fit', True)
    for (x0, z0, zc, xd, ok), (xm, vis) in zip(ribs, model_ribs(shape, st, ribs, built=False)):
        res.append(np.where(ok & vis, xm - xd, 0.0))
    return np.concatenate(res)


def table(res, cols=('sil_max', 'sil_bias', 'rib_mean', 'within1', 'v34_mean')):
    fmt = lambda v, k: '—' if v is None else (f"{v:.0f} %" if k == 'within1' else f"{v:+.2f}" if k == 'sil_bias' else f"{v:.2f}")
    lines = ["| Seg | " + " | ".join(cols) + " | front | 3/4 |", "|---|" + "---|" * (len(cols) + 2)]
    for r in res['seg']:
        lines.append(f"| {r['id']} | " + " | ".join(fmt(r[c], c) for c in cols) +
                     f" | {'✅' if r['pass_front'] else '❌'} | {'✅' if r['pass_v34'] else '❌'} |")
    t = res['tot']
    lines.append(f"\n**front {t['front_pass']}/19 · 3/4 {t['v34_pass']}/19** · outline max {t['sil_max']:.2f} mm · "
                 f"ribs mean {t['rib_mean']:.2f} mm, {t['within1']:.0f} % ≤ 1 mm · 3/4 mean {t['v34_mean']:.2f} mm")
    return "\n".join(lines)
