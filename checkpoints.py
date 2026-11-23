"""
10 mm checkpoints: does the model hit the drawing?

1. Trace drawn rib lines upward from the bottom rim (many start points across the front).
2. For each traced rib, the model rib starting at the same point (same local angle θ0) is
   x(z) = r0(z) * rho(θ0, k(z)) * cos(θ0 + twist(z))     (front view, camera at -Y)
3. Compare every 10 mm: rib x-position error (mm) and silhouette error (mm).

Run:  python checkpoints.py            -> evaluates the current fit (fit_result.txt)
Used by fit_ribs.py as the objective.
"""
import os
import numpy as np
import cv2
import model as m
import measure_canvas as mc

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = cv2.imread(mc.IMG, 0)
_f = IMG.astype(np.float32) / 255
_gx = cv2.Sobel(_f, cv2.CV_32F, 1, 0, ksize=3); _gy = cv2.Sobel(_f, cv2.CV_32F, 0, 1, ksize=3)
_k = (15, 15)
_Jxx = cv2.GaussianBlur(_gx * _gx, _k, 0); _Jyy = cv2.GaussianBlur(_gy * _gy, _k, 0); _Jxy = cv2.GaussianBlur(_gx * _gy, _k, 0)
ANG = 0.5 * np.arctan2(2 * _Jxy, _Jxx - _Jyy) + np.pi / 2
COH = np.sqrt((_Jxx - _Jyy) ** 2 + 4 * _Jxy ** 2) / (_Jxx + _Jyy + 1e-9)
DARK = cv2.GaussianBlur(255 - IMG, (5, 1), 0).astype(float)
SIL = np.loadtxt(os.path.join(HERE, 'silhouette_front.csv'), delimiter=',', skiprows=1)
S_OF_Z = lambda z: np.interp(z, SIL[:, 0], (SIL[:, 1] + SIL[:, 2]) / 2)
CHECK_Z = np.arange(10.0, 190.0, 10.0)


def trace(x_mm_start, z_start=2.0, snap=2):
    """Follow one drawn line upward. Returns (z_mm, x_mm) arrays; stops when the line is lost
    or when it reaches the outline (where it disappears behind a lobe)."""
    x = mc.COL0 + x_mm_start / mc.SX
    row0 = int(round(float(mc.z_to_row(z_start))))
    # snap start onto the nearest line
    lo = int(x) - 6; c = np.argmax(DARK[row0, lo:lo + 13]) + lo; x = float(c)
    zs, xs, lost = [], [], 0
    for row in range(row0, 3, -1):
        xi = int(round(x))
        if xi < 3 or xi >= IMG.shape[1] - 3:
            break
        a = ANG[row, xi]
        dxdrow = np.cos(a) / np.sin(a) if abs(np.sin(a)) > 0.15 else 0.0
        x_pred = x - dxdrow
        lo, hi = int(round(x_pred)) - snap, int(round(x_pred)) + snap + 1
        win = DARK[row - 1, max(lo, 0):hi]
        if win.size and win.max() > 60:
            x = 0.5 * x_pred + 0.5 * (np.argmax(win) + max(lo, 0)); lost = 0
        else:
            x = x_pred; lost += 1
            if lost > 15:
                break
        z = float(mc.row_to_z(row - 1)); xm = (x - mc.COL0) * mc.SX
        if abs(xm) > S_OF_Z(z) - 3.0:          # reached the outline -> rib goes behind
            break
        # lines merging (crease): another dark line centre within 4 px -> the trace may switch lines here
        xi = int(round(x)); seg = DARK[row - 1, max(xi - 8, 0):xi + 9]
        peaks = np.sum((seg[1:-1] > 60) & (seg[1:-1] >= seg[:-2]) & (seg[1:-1] > seg[2:]))
        if peaks > 2:
            break                                # stop: from here on the trace is not trustworthy
        zs.append(z); xs.append(xm)
    return np.array(zs), np.array(xs)


def trace_all(starts=np.arange(-70.0, 71.0, 10.0)):
    out = []
    for x0 in starts:
        zt, xt = trace(x0)
        if len(zt):
            out.append(((float(xt[0]), float(zt[0])), zt, xt))   # start = where the trace really starts
    return out


def _arc_table(section):
    if section not in m._tables:
        cur = m.SECTION; m.set_section(section); m.set_section(cur)
    return m._tables[section][3]                                        # arc length S(θ) over 0..90°


def model_rib(prof, twist_fn, start, z):
    """Model rib through bottom-rim point x0 on the front. Ribs keep their ARC-LENGTH position inside
    their quarter (like the triangles / LampWall pleats), so they slide in angle when the lobe depth changes."""
    x0_mm, zs0 = start if isinstance(start, tuple) else (start, 0.0)
    th = np.radians(np.linspace(-180, 0, 20001))                       # front half (y < 0) at the start height
    r00 = m.profile_r(prof, zs0); rot0 = np.radians(twist_fn(zs0 / m.HEIGHT))
    sec0 = m.section_at(zs0)
    xs0 = r00 * m.rho_fn(th - rot0, sec0) * np.cos(th)
    i = np.argmin(np.abs(xs0 - x0_mm))
    theta0 = th[i] - rot0                                                # local angle at z = 0
    q = np.floor(theta0 / (np.pi / 2)); local = theta0 - q * np.pi / 2
    S0 = _arc_table(sec0)
    f0 = np.interp(local, m._TH, S0) / S0[-1]                            # arc-length fraction in its quarter
    z = np.asarray(z, float)
    r0 = m.profile_r(prof, z); rot = np.radians(twist_fn(z / m.HEIGHT))
    xs, vis = np.empty(len(z)), np.empty(len(z), bool)
    for j, zz in enumerate(z):
        sec = m.section_at(zz)
        S = _arc_table(sec)
        th_l = np.interp(f0 * S[-1], S, m._TH) + q * np.pi / 2
        rho = m.rho_fn(np.array([th_l]), sec)[0]
        phi = th_l + rot[j]
        xs[j] = r0[j] * rho * np.cos(phi); vis[j] = np.sin(phi) < 0
    return xs, vis                                                       # x, visible (front side)


def evaluate(prof, twist_fn, traces, verbose=True, label=''):
    """Table of errors at every 10 mm. Returns (rib errors list, silhouette errors)."""
    full = m.silhouettes(prof, twist_fn, CHECK_Z)[0]
    sil_err = full - S_OF_Z(CHECK_Z)
    rows, all_err = [], []
    for x0, zt, xt in traces:
        if len(zt) < 30:
            continue
        zc = CHECK_Z[(CHECK_Z >= zt.min()) & (CHECK_Z <= zt.max())]
        xm, vis = model_rib(prof, twist_fn, x0, zc)
        xd = np.interp(zc, zt[::-1] if zt[0] > zt[-1] else zt, xt[::-1] if zt[0] > zt[-1] else xt)
        e = np.where(vis, xm - xd, np.nan)
        rows.append((x0, zc, e)); all_err += list(e[np.isfinite(e)])
    all_err = np.array(all_err)
    if verbose:
        print(f"\n=== {label} ===")
        print("height  silhouette  | rib x-error (mm) for ribs starting at x0 = ...")
        print("  z mm   err mm     | " + " ".join(f"{x0[0]:+5.0f}" for x0, _, _ in rows))
        for j, z in enumerate(CHECK_Z):
            cells = []
            for x0, zc, e in rows:
                k = np.where(zc == z)[0]
                cells.append(f"{e[k[0]]:+5.1f}" if len(k) and np.isfinite(e[k[0]]) else "    .")
            print(f"{z:6.0f}   {sil_err[j]:+6.2f}     | " + " ".join(cells))
        print(f"rib error: mean |e| {np.mean(np.abs(all_err)):.2f} mm, RMS {np.sqrt(np.mean(all_err**2)):.2f} mm, "
              f"max {np.max(np.abs(all_err)):.2f} mm, checkpoints within 1 mm: "
              f"{np.mean(np.abs(all_err) <= 1.0)*100:.0f}%  ({len(all_err)} checkpoints)")
        print(f"silhouette: max |e| {np.max(np.abs(sil_err)):.2f} mm")
    return rows, all_err, sil_err


def draw(prof, twist_fn, traces, path):
    vis = cv2.cvtColor(IMG, cv2.COLOR_GRAY2BGR)
    vis = (vis * 0.45 + 255 * 0.55).astype(np.uint8)
    zz = np.linspace(0, m.HEIGHT, 400)
    px = lambda x, z: (int(round(mc.COL0 + x / mc.SX)), int(round(float(mc.z_to_row(z)))))
    for x0, zt, xt in traces:
        if len(zt) < 30:
            continue
        cv2.polylines(vis, [np.array([px(a, b) for a, b in zip(xt, zt)], np.int32)], False, (0, 160, 0), 2, cv2.LINE_AA)
        xm, v = model_rib(prof, twist_fn, x0, zz)
        for i in range(len(zz) - 1):
            if v[i] and v[i + 1]:
                cv2.line(vis, px(xm[i], zz[i]), px(xm[i + 1], zz[i + 1]), (0, 0, 220), 1, cv2.LINE_AA)
    for z in CHECK_Z:
        r = int(round(float(mc.z_to_row(z))))
        cv2.line(vis, (0, r), (25, r), (120, 120, 120), 2)
    cv2.putText(vis, "green = traced drawing ribs   red = model ribs from the same start   ticks = 10 mm checkpoints",
                (20, 1740), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (30, 30, 30), 2, cv2.LINE_AA)
    cv2.imwrite(path, vis)


if __name__ == '__main__':
    from render_folds import read_fit
    prof, tw = read_fit()
    fn = lambda t: m.twist_deg(tw, t)
    tr = trace_all()
    evaluate(prof, fn, tr, label='current fit (Grasshoper_full)')
    draw(prof, fn, tr, os.path.join(HERE, 'checkpoints.png'))
