"""
M03 — scenario 3: custom spline base (fixed over height) + degree-6 2D Bezier radius (r, z)(t) + cubic twist
evaluated at the Bezier parameter t of the radius curve (not at height).
Settings and start values from ../FulLTextureLamp/FulLTextureLamp.py (docs/05_EXPERIMENTS.md §5.2, §5.4):
  calculate_2d_bezier_profile_7 (7 control points), calculate_bezier_twist (k1 = 0, k2 = 0.80, 90 deg),
  generate_polar_triangles_by_count (N = 23, scale_perp 0.20 cm = 2.0 mm, half tooth at 0 deg),
  30 sections at uniform Bezier t (t = i / 29).
The script in ../ now draws the rose base; the user's scenario says custom spline, so the custom spline is used.
"""
import math
import numpy as np
from study import Shape
import curves as C
import bases as B

ID = 'M03'
TITLE = 'custom spline base + 7-point 2D Bezier radius + cubic twist at Bezier t'
SOURCE = ('../FulLTextureLamp (calculate_2d_bezier_profile_7, calculate_bezier_twist at Bezier t, '
          'generate_polar_triangles_by_count N 23 / 0.20 cm, 30 sections uniform in t); base = custom spline per scenario')
SETTINGS = dict(N=23, H=2.0, placement='angle_half', target_w=9.0, sections=dict(mode='bezier_t', count=30))

N_PROF = 7
PROF0 = [(80.0, 0.0), (92.5, 10.0), (106.0, 25.0), (102.0, 35.0), (140.0, 50.0), (115.0, 120.0), (43.0, 190.0)]
TW0 = [0.0, 0.80, 90.0]                                   # k1, k2, max angle (calculate_bezier_twist)


def pack(prof, tw):
    return np.array([prof[0][0]] + [v for q in prof[1:-1] for v in q] + [prof[-1][0]] + list(tw), float)


def unpack(x):
    x = list(map(float, x))
    prof = [(x[0], 0.0)]; k = 1
    for _ in range(N_PROF - 2):
        prof.append((x[k], x[k + 1])); k += 2
    prof.append((x[k], 190.0)); k += 1
    return prof, x[k:k + 3]


NAMES = ['P0.r'] + [f'P{i}.{c}' for i in range(1, N_PROF - 1) for c in 'rz'] + [f'P{N_PROF-1}.r', 'k1', 'k2', 'max_angle']
P0 = pack(PROF0, TW0)
LB = np.r_[20.0, np.tile([20.0, 0.0], N_PROF - 2), 20.0, -1.0, -1.0, 45.0]
UB = np.r_[200.0, np.tile([200.0, 190.0], N_PROF - 2), 200.0, 2.0, 2.0, 135.0]


def shape(p):
    prof, (k1, k2, mx) = unpack(p)
    bz = C.BezierRZ(prof)
    return Shape(r0=bz.r, twist=lambda z: C.cubic_twist(bz.t(z), k1, k2, mx),
                 rho=lambda z: B.custom_spline(), zt=bz.z_of_t)


def penalty(p):
    prof, _ = unpack(p)
    return 20 * np.minimum(np.diff([q[1] for q in prof]), 0)


def constraints(p):
    prof, _ = unpack(p)
    bz = C.BezierRZ(prof)
    out = []
    if not bz.monotone():
        out.append('profile z(t) not monotone')
    r = bz.r(np.linspace(0, 190, 381))
    if r.min() < 10:
        out.append(f'r0 too small ({r.min():.1f} mm)')
    return out


# ------------------------------------------------------------------ pure-Python copies (Fusion has no numpy)
def bez_rz_pure(prof, t):
    """calculate_2d_bezier_profile_7: (r, z) at Bezier parameter t."""
    n = len(prof) - 1
    w = [math.comb(n, i) * (1 - t) ** (n - i) * t ** i for i in range(n + 1)]
    return sum(wi * q[0] for wi, q in zip(w, prof)), sum(wi * q[1] for wi, q in zip(w, prof))


def twist_pure(t, k1, k2, mx):
    """calculate_bezier_twist at Bezier parameter t."""
    return mx * (3 * (1 - t) ** 2 * t * k1 + 3 * (1 - t) * t ** 2 * k2 + t ** 3)


def section_pure(p, i, n=30):
    """(z, r0, twist) of section i as ../FulLTextureLamp computes it (t = i / (n - 1))."""
    prof, (k1, k2, mx) = unpack(p)
    t = i / (n - 1)
    r, z = bez_rz_pure(prof, t)
    return z, r, twist_pure(t, k1, k2, mx)


def self_test(p=None, tol=1e-6):
    """numpy curves (kernel) vs pure-Python curves at every section: max abs difference."""
    p = P0 if p is None else np.asarray(p, float)
    prof, (k1, k2, mx) = unpack(p)
    ts = np.linspace(0, 1, 30)
    c = C.bezier(prof, ts)
    tw = C.cubic_twist(ts, k1, k2, mx)
    d = 0.0
    for i, t in enumerate(ts):
        z, r, a = section_pure(p, i)
        d = max(d, abs(z - c[i, 1]), abs(r - c[i, 0]), abs(a - tw[i]))
    # the kernel's shape() looks t up by height (interpolated table): check it at the section heights too
    sh = shape(p)
    zs = c[:, 1]
    d_lookup = float(max(np.abs(sh.r0(zs) - c[:, 0]).max(), np.abs(sh.twist(zs) - tw).max()))
    return dict(exact_max=d, ok=d < tol, lookup_max=d_lookup)


if __name__ == '__main__':
    print(self_test())
