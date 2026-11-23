"""
Targets: the two drawings every model is fitted to / scored against (docs/05_EXPERIMENTS.md §5.5).

front  : outline half-width per z (mm) + traced rib lines (z, x mm)       -> fitting
view34 : drawn outline left/right column per image row + start camera   -> held-out scoring

`python models/_common/targets.py` (re)builds targets/front/*, targets/view34/* and the noise floors.
Everything else only *loads* the cached files, so all models use identical targets.
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TDIR = os.path.join(ROOT, 'targets')
sys.path.insert(0, ROOT)

ROW_CUT = 590            # 3/4 drawing: rows below belong to the foot (not scored)
V34_ROWS_STEP = 4


# ----------------------------------------------------------------------------------------------- loaders
_cache = {}


def front():
    """dict: z (mm, 0..190), half (mean half-width), left, right, ribs [(x0, z0, z[], x[])], calib"""
    if 'front' not in _cache:
        d = os.path.join(TDIR, 'front')
        o = np.loadtxt(os.path.join(d, 'outline.csv'), delimiter=',', skiprows=1)
        ribs = json.load(open(os.path.join(d, 'ribs.json')))
        cal = json.load(open(os.path.join(d, 'calibration.json')))
        _cache['front'] = dict(
            z=o[:, 0], left=o[:, 1], right=o[:, 2], half=(o[:, 1] + o[:, 2]) / 2,
            ribs=[(r['x0'], r['z0'], np.array(r['z']), np.array(r['x']), np.array(r['spread'])) for r in ribs['ribs']],
            max_spread=ribs['max_spread_mm'], calib=cal)
    return _cache['front']


def half_width(z):
    f = front()
    return np.interp(z, f['z'], f['half'])


def view34():
    """dict: rows, L, R (drawing outline columns), camera (7 values), H, W"""
    if 'v34' not in _cache:
        d = os.path.join(TDIR, 'view34')
        o = np.loadtxt(os.path.join(d, 'outline.csv'), delimiter=',', skiprows=1)
        cam = json.load(open(os.path.join(d, 'camera.json')))['camera']
        meta = json.load(open(os.path.join(d, 'meta.json')))
        _cache['v34'] = dict(rows=o[:, 0].astype(int), L=o[:, 1], R=o[:, 2], camera=cam, H=meta['H'], W=meta['W'])
    return _cache['v34']


# ----------------------------------------------------------------------------------------------- builders
def build():
    import cv2
    import measure_canvas as mc
    import checkpoints as cp

    # ---- front -------------------------------------------------------------------------------
    fd = os.path.join(TDIR, 'front'); os.makedirs(fd, exist_ok=True)
    sil = np.loadtxt(os.path.join(ROOT, 'silhouette_front.csv'), delimiter=',', skiprows=1)
    np.savetxt(os.path.join(fd, 'outline.csv'), sil, delimiter=',', header='z_mm,left_mm,right_mm', fmt='%.3f', comments='')
    json.dump(dict(source='reference/fusion_rel_size_YZ.jpg (Fusion canvas rel_size, YZ plane)',
                   mm_per_px_x=mc.SX, mm_per_px_z=mc.SZ, axis_col_px=mc.COL0, W_MM=mc.W_MM, H_MM=mc.H_MM,
                   PLANE_Z=mc.PLANE_Z, V_OFF=mc.V_OFF, mirrored='canvas mirrored left-right vs the original drawing',
                   note='z(row) = PLANE_Z + V_OFF + H_MM*(1-(row+0.5)/H_PX)'),
              open(os.path.join(fd, 'calibration.json'), 'w'), indent=1)
    traces = [t for t in cp.trace_all() if len(t[1]) >= 30]
    ribs = []
    for (x0, z0), zt, xt in traces:
        o = np.argsort(zt)
        # tracer repeatability along this rib (snap 1/2/3 px): unreliable where the runs disagree by > 1 mm
        runs = []
        for snap in (1, 2, 3):
            zz, xx = cp.trace(x0, snap=snap)
            if len(zz) > 10:
                oo = np.argsort(zz); runs.append((zz[oo], xx[oo]))
        zs = zt[o]
        X = np.array([np.where(zs <= r[0].max(), np.interp(zs, r[0], r[1]), np.nan) for r in runs])
        spread = np.nanmax(X, 0) - np.nanmin(X, 0)
        spread = np.where(np.isfinite(spread), spread, 99.0)
        ribs.append(dict(x0=float(x0), z0=float(z0), z=[round(float(v), 3) for v in zs], x=[round(float(v), 3) for v in xt[o]],
                         spread=[round(float(v), 3) for v in spread]))
    json.dump(dict(note='traced drawing ribs (checkpoints.trace_all, >= 30 points); start (x0, z0) on the bottom rim. '
                        'spread = disagreement of tracer runs (snap 1/2/3 px); scoring skips points with spread > 1 mm',
                   max_spread_mm=1.0, ribs=ribs), open(os.path.join(fd, 'ribs.json'), 'w'))

    # ---- noise floors ------------------------------------------------------------------------
    noise = {}
    z, L, R = sil[:, 0], sil[:, 1], sil[:, 2]
    d = L - R                                   # a 4-fold shape seen from the front is 180° symmetric -> L == R
    d_c = d - d.mean()                          # remove a constant axis offset (calibration)
    seg = {}
    for j in range(19):
        s = (z >= 10 * j) & (z < 10 * j + 10)
        seg[f"S{j+1:02d}"] = round(float(np.abs(d_c[s]).mean() / 2), 3)    # /2: error of the mean half-width
    noise['outline'] = dict(axis_offset_mm=round(float(d.mean() / 2), 3),
                            lr_asym_mean_abs_mm=round(float(np.abs(d_c).mean()), 3),
                            lr_asym_p95_mm=round(float(np.percentile(np.abs(d_c), 95)), 3),
                            half_width_noise_mean_mm=round(float(np.abs(d_c).mean() / 2), 3),
                            per_segment_half_width_noise_mm=seg)
    # rib tracer repeatability: same start, snap 1 / 2 / 3 px
    spreads = []
    for (x0, z0), zt, xt in traces:
        runs = []
        for snap in (1, 2, 3):
            zz, xx = cp.trace(x0, snap=snap)
            if len(zz) > 10:
                o = np.argsort(zz); runs.append((zz[o], xx[o]))
        if len(runs) < 2:
            continue
        top = min(r[0].max() for r in runs)
        zs = np.arange(4.0, top, 2.0)
        X = np.array([np.interp(zs, r[0], r[1]) for r in runs])
        spreads += list(X.max(0) - X.min(0))
    spreads = np.array(spreads)
    noise['ribs'] = dict(tracer_spread_mean_mm=round(float(spreads.mean()), 3),
                         tracer_spread_p95_mm=round(float(np.percentile(spreads, 95)), 3),
                         frac_spread_over_1mm=round(float(np.mean(spreads > 1.0)), 3))
    # rib count: dark-line peaks along rows close to the centre column
    IMG = cv2.imread(mc.IMG, 0)
    counts = []
    import model as mdl
    for zz in (20.0, 40.0, 60.0):
        row = int(round(float(mc.z_to_row(zz))))
        prof = (255 - IMG[row - 1:row + 2].astype(float)).mean(0)
        c0 = int(mc.COL0); half = int(25 / mc.SX)
        p = prof[c0 - half:c0 + half]
        pk = np.sum((p[1:-1] > 60) & (p[1:-1] >= p[:-2]) & (p[1:-1] > p[2:]))
        spacing = 50.0 / max(pk, 1)                                     # mm per rib, along x at the centre
        counts.append(dict(z=zz, peaks_in_50mm=int(pk), spacing_mm=round(spacing, 3)))
    noise['rib_count'] = dict(samples=counts, note='ribs per quarter = quarter arc length / spacing; see study log')
    json.dump(noise, open(os.path.join(fd, 'noise.json'), 'w'), indent=1)

    # ---- view34 ------------------------------------------------------------------------------
    vd = os.path.join(TDIR, 'view34'); os.makedirs(vd, exist_ok=True)
    src = cv2.imread(os.path.join(vd, 'image.png'), cv2.IMREAD_UNCHANGED)
    if src.shape[2] == 4:
        a = src[:, :, 3:4].astype(float) / 255
        src = (src[:, :, :3] * a + 255 * (1 - a)).astype(np.uint8)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    H, W = gray.shape
    dark = (gray < 140).astype(np.uint8)
    closed = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    ff = closed.copy(); cv2.floodFill(ff, np.zeros((H + 2, W + 2), np.uint8), (0, 0), 2)
    mask = (ff != 2).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask)
    mask = (lab == 1 + np.argmax(st[1:, 4])).astype(np.uint8)
    rows = np.arange(44, ROW_CUT - 4, V34_ROWS_STEP)
    out = np.array([(r, np.nonzero(mask[r])[0].min(), np.nonzero(mask[r])[0].max()) for r in rows], float)
    np.savetxt(os.path.join(vd, 'outline.csv'), out, delimiter=',', header='row,left_col,right_col', fmt='%.1f', comments='')
    json.dump(dict(H=H, W=W, row_cut=ROW_CUT, note='mask = largest dark-closed blob (same as views/fit_view34.py)'),
              open(os.path.join(vd, 'meta.json'), 'w'), indent=1)
    print(json.dumps(noise, indent=1))
    print(f"front: {len(ribs)} ribs; view34: {len(out)} rows")


if __name__ == '__main__':
    build()
