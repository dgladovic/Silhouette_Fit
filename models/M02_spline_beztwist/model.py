"""
M02 — scenario 2: custom spline base + bez_points keyframe radius + higher-order Bézier twist (t, deg).
Base and radius identical to M01; only the twist representation differs (calculate_bezier_twist2).
Settings from ../Grasshoper_full (docs/05_EXPERIMENTS.md §5.2, §5.4).

Self-test (numpy vs pure-Python curves):  python models/M02_spline_beztwist/model.py
"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_common'))   # for the self-test
from study import Shape, SMOOTH_W
import curves as C
import bases as B

ID = 'M02'
TITLE = 'custom spline base + keyframe radius + 5-point Bezier twist (t, deg)'
SOURCE = ('../Grasshoper_full (generate_arc_normal N 22, scale_perp 0.3 cm, target_width 0.9 cm, 15 sections; '
          'twist = calculate_bezier_twist2 twist_points); radius start = ../BaseScript bez_points')
SETTINGS = dict(N=22, H=3.0, placement='arc', target_w=9.0, sections=dict(mode='uniform_z', count=15))

KT = [i / 10 for i in range(11)]                                          # keyframe t = z / 190
R0 = [81, 98, 109.0, 114.0, 114.2, 110.4, 103.2, 92.4, 78.4, 62.0, 44.0]    # ../BaseScript bez_points (= M01 start)
TW0 = [(0.000, 0.0), (0.289, -0.7), (0.604, 59.0), (0.827, 78.4), (1.000, 90.0)]   # ../Grasshoper_full twist_points
N_TW = len(TW0)                                                           # 5 control points (quartic Bézier)


def pack(r, tw):
    return np.array(list(r) + [v for q in tw[1:-1] for v in q] + [tw[-1][1]], float)


def unpack(p):
    p = list(map(float, p))
    r = p[:11]; k = 11
    tw = [(0.0, 0.0)]
    for _ in range(N_TW - 2):
        tw.append((p[k], p[k + 1])); k += 2
    tw.append((1.0, p[k]))
    return r, tw


NAMES = [f'r@t{t:.1f}' for t in KT] + [f'T{i}.{c}' for i in range(1, N_TW - 1) for c in ('t', 'deg')] + [f'T{N_TW-1}.deg']
P0 = pack(R0, TW0)
LB = np.r_[np.full(11, 20.0), np.tile([0.0, -90.0], N_TW - 2), 45.0]
UB = np.r_[np.full(11, 200.0), np.tile([1.0, 180.0], N_TW - 2), 135.0]


def shape(p):
    r, tw = unpack(p)
    r = np.asarray(r); bt = C.BezierTwist(tw)
    return Shape(r0=lambda z: C.catmull_keys(KT, r, np.asarray(z) / 190.0),
                 twist=lambda z: bt(np.asarray(z) / 190.0),
                 rho=lambda z: B.custom_spline())


def penalty(p):
    r, tw = unpack(p)
    ts = [q[0] for q in tw]
    return np.r_[SMOOTH_W['mm'] * C.second_diff(r), 200 * np.minimum(np.diff(ts), 0)]


def constraints(p):
    r, tw = unpack(p)
    out = []
    rr = C.catmull_keys(KT, r, np.linspace(0, 1, 381))
    if rr.min() <= 10:
        out.append(f'r0 too small ({rr.min():.1f} mm)')
    ts = [q[0] for q in tw]
    if min(ts) < 0 or max(ts) > 1 or np.any(np.diff(ts) < 0):
        out.append('twist t outside 0..1 or decreasing')
    return out


# ------------------------------------------------------------------ pure-Python curves (no numpy, for Fusion)
def py_r0(z, r):
    """Catmull-Rom through (KT, r) at t = z/190, same as smooth_spline_interpolation / curves.catmull_keys."""
    t = z / 190.0; n = len(KT)
    if t <= KT[0]:
        return r[0]
    if t >= KT[-1]:
        return r[-1]
    i = 0
    while i < n - 2 and t > KT[i + 1]:
        i += 1
    p0, p1, p2, p3 = r[max(i - 1, 0)], r[i], r[i + 1], r[min(i + 2, n - 1)]
    u = (t - KT[i]) / (KT[i + 1] - KT[i])
    return 0.5 * (2 * p1 + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u ** 2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3)


def py_twist(z, tw, steps=2000):
    """calculate_bezier_twist2 lookup (LUT over the Bézier parameter, linear between LUT points), t = z/190.
    steps = 2000 to match curves.BezierTwist (the user's script uses 100)."""
    tt = z / 190.0; n = len(tw) - 1
    lut = []
    for s in range(steps + 1):
        u = s / steps; x = y = 0.0
        for i, (px, py) in enumerate(tw):
            b = math.comb(n, i) * (1 - u) ** (n - i) * u ** i
            x += b * px; y += b * py
        lut.append((x, y))
    if tt <= lut[0][0]:
        return lut[0][1]
    for (x0, y0), (x1, y1) in zip(lut[:-1], lut[1:]):
        if x0 <= tt <= x1:
            return y0 if x1 == x0 else y0 + (tt - x0) / (x1 - x0) * (y1 - y0)
    return lut[-1][1]


def _selftest(p=None):
    p = P0 if p is None else p
    sh = shape(p); r, tw = unpack(p)
    Z = np.linspace(0, 190, 96)
    dr = max(abs(py_r0(float(z), r) - float(sh.r0(z))) for z in Z)
    dt = max(abs(py_twist(float(z), tw) - float(sh.twist(z))) for z in Z)
    return dr, dt


if __name__ == '__main__':
    import os, sys, json
    for lab, p in (('P0', P0),):
        dr, dt = _selftest(p)
        print(f'{lab}: max |numpy - pure| r0 {dr:.2e} mm, twist {dt:.2e} deg ->', 'OK' if max(dr, dt) < 1e-6 else 'FAIL')
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'E0_fit', 'params.json')
    if os.path.exists(f):
        dr, dt = _selftest(np.array(json.load(open(f))['values']))
        print(f'E0: max |numpy - pure| r0 {dr:.2e} mm, twist {dt:.2e} deg ->', 'OK' if max(dr, dt) < 1e-6 else 'FAIL')
