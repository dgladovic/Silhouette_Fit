"""
Joint fit to BOTH drawings:
  front drawing : outline every 2 mm + 15 traced ribs every 4 mm   (same as fit_ribs.py)
  3/4 drawing   : left/right outline edge every 4 px row (shade only), camera free
Model: triangle geometry (Grasshoper_full) - all 4 quarters for the 3/4 view.
Starts from fit_ribs_result.json + views/view34/camera.json.
Writes views/view34/joint_result.json (same keys as fit_ribs_result.json + camera).

Run: python views/fit_joint.py            (then: python views/fit_joint.py --apply  to make it the current fit)
"""
import os, sys, json
import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, HERE)
APPLY = '--apply' in sys.argv
sys.argv = [sys.argv[0], '5', 'soft_l1']          # fit_ribs reads argv at import
import model as m
import checkpoints as cp
import fit_ribs as fr
import fit_view34 as v34

OUT = os.path.join(HERE, 'view34')
W34 = 1.0                                          # weight of the 3/4 outline (mm residuals)
ROWS = np.arange(44, v34.ROW_CUT - 4, 4)
DRAW_L = np.array([np.nonzero(v34.IMG_MASK[r])[0].min() for r in ROWS], float)
DRAW_R = np.array([np.nonzero(v34.IMG_MASK[r])[0].max() for r in ROWS], float)
ZP = np.arange(0.0, 190.01, 0.5)


def model_points(prof, fn):
    """All triangle points (4 quarters) of the shade, world mm, shape (N, 3)."""
    r0 = m.profile_r(prof, ZP); rot = fn(ZP / m.HEIGHT)
    pts = []
    for z, r, a in zip(ZP, r0, rot):
        m.set_section(m.section_at(z))
        for q in range(4):
            P = m.slice_points(r, a + 90 * q).reshape(-1, 2)
            pts.append(np.c_[P, np.full(len(P), z)])
    return np.concatenate(pts)


def view34_residual(prof, fn, cam):
    uv = v34.project(model_points(prof, fn), list(cam) + [1])
    rows = np.round(uv[:, 1]).astype(int); cols = uv[:, 0]
    ok = (rows >= 0) & (rows < v34.H)
    lo = np.full(v34.H, np.inf); hi = np.full(v34.H, -np.inf)
    np.minimum.at(lo, rows[ok], cols[ok]); np.maximum.at(hi, rows[ok], cols[ok])
    ml, mr = lo[ROWS], hi[ROWS]
    s = cam[2]
    rl = np.where(np.isfinite(ml), (DRAW_L - ml) / s, 5.0)   # + = model sticks out on the left
    rr = np.where(np.isfinite(mr), (mr - DRAW_R) / s, 5.0)   # + = model sticks out on the right
    return np.r_[rl, rr]


NX = None


def residuals(x):
    xm, cam = x[:NX], x[NX:]
    prof, fn, tw, kv = fr.apply(xm)
    return np.r_[fr.residuals(xm), W34 * view34_residual(prof, fn, cam)]


def main():
    global NX
    d = json.load(open(os.path.join(ROOT, 'fit_ribs_result.json')))
    prof = [tuple(p) for p in d['BEZIER_CONTROL_POINTS']]; tw = [tuple(p) for p in d['twist_points']]
    kv = d['LOBE_DEPTH_K']
    cam = json.load(open(os.path.join(OUT, 'camera.json')))['camera']
    xm0 = fr.x_from(prof, tw, kv); NX = len(xm0)
    x0 = np.r_[xm0, cam[:6]]
    lb = np.full(len(x0), -np.inf); ub = np.full(len(x0), np.inf)
    k0 = 2 + 2 * (fr.N_PROF - 2)
    for j in range(fr.N_TW - 2):
        lb[k0 + 2 * j], ub[k0 + 2 * j] = 0.0, 1.0
    lb[-1], ub[-1] = 0.0, 0.01                     # invD (perspective) >= 0
    x0 = np.clip(x0, lb + 1e-9, ub - 1e-9)

    def summary(x, label):
        prof, fn, tw, kv = fr.apply(x[:NX])
        rows, err, sil = cp.evaluate(prof, fn, fr.TRACES, verbose=False)
        r34 = view34_residual(prof, fn, x[NX:])
        print(f"{label}: front outline max {np.abs(sil).max():.2f} mm | ribs mean {np.mean(np.abs(err)):.2f} mm, "
              f"{np.mean(np.abs(err) <= 1)*100:.0f}% within 1 mm | 3/4 outline mean {np.mean(np.abs(r34)):.2f} mm, "
              f"max {np.abs(r34).max():.2f} mm", flush=True)
        return prof, tw, kv, err, sil, r34

    summary(x0, 'BEFORE')
    r = least_squares(residuals, x0, bounds=(lb, ub), x_scale='jac', diff_step=1e-4, loss='soft_l1', f_scale=1.5,
                      xtol=1e-10, ftol=1e-9, max_nfev=300, verbose=1)
    prof, tw, kv, err, sil, r34 = summary(r.x, 'AFTER ')
    cam = list(map(float, r.x[NX:])) + [1]
    out = {'BEZIER_CONTROL_POINTS': [list(map(float, p)) for p in prof],
           'twist_points': [list(map(float, p)) for p in tw],
           'LOBE_DEPTH_Z': m.K_NODES_Z, 'LOBE_DEPTH_K': [float(v) for v in kv], 'camera34': cam,
           'rib_mean_abs_mm': float(np.mean(np.abs(err))), 'rib_max_mm': float(np.max(np.abs(err))),
           'within_1mm_pct': float(np.mean(np.abs(err) <= 1) * 100), 'sil_max_mm': float(np.max(np.abs(sil))),
           'view34_mean_mm': float(np.mean(np.abs(r34))), 'view34_max_mm': float(np.max(np.abs(r34)))}
    json.dump(out, open(os.path.join(OUT, 'joint_result.json'), 'w'), indent=1)
    print(json.dumps({k: out[k] for k in out if k.endswith('mm') or k.endswith('pct')}, indent=1))


def apply_joint():
    """Make the joint fit the current one: copy into fit_ribs_result.json and write all Fusion scripts."""
    import shutil, subprocess
    shutil.copy(os.path.join(ROOT, 'fit_ribs_result.json'), os.path.join(ROOT, 'fit_ribs_result_front_only.json'))
    d = json.load(open(os.path.join(OUT, 'joint_result.json')))
    json.dump(d, open(os.path.join(ROOT, 'fit_ribs_result.json'), 'w'), indent=1)
    subprocess.run([sys.executable, 'apply_ribs_fit.py'], cwd=ROOT, check=True)
    print('joint fit applied (previous front-only fit saved as fit_ribs_result_front_only.json)')


if __name__ == '__main__':
    if APPLY:
        apply_joint()
    else:
        main()
