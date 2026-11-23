"""
M01 — scenario 1: custom spline base + bez_points keyframe radius + 2-parameter cubic twist.
Settings and start values from ../BaseScript (docs/05_EXPERIMENTS.md §5.2, §5.4).
"""
import numpy as np
from study import Shape, SMOOTH_W
import curves as C
import bases as B

ID = 'M01'
TITLE = 'custom spline base + keyframe radius + cubic twist (k1, k2, max angle)'
SOURCE = '../BaseScript (bez_points, generate_shell_triangles_by_count, 11 sections); twist = calculate_bezier_twist'
SETTINGS = dict(N=22, H=2.4, placement='angle_half', target_w=9.0, sections=dict(mode='uniform_z', count=11))

KT = [i / 10 for i in range(11)]                                     # keyframe t = z / 190
R0 = [81, 98, 109.0, 114.0, 114.2, 110.4, 103.2, 92.4, 78.4, 62.0, 44.0]   # ../BaseScript bez_points
TW0 = [0.0, 0.95, 90.0]                                              # k1, k2, max angle (calculate_bezier_twist)

NAMES = [f'r@t{t:.1f}' for t in KT] + ['k1', 'k2', 'max_angle']
P0 = np.array(R0 + TW0, float)
LB = np.r_[np.full(11, 20.0), -1.0, -1.0, 45.0]
UB = np.r_[np.full(11, 200.0), 2.0, 2.0, 135.0]


def shape(p):
    p = np.asarray(p, float); r, (k1, k2, mx) = p[:11], p[11:14]
    return Shape(r0=lambda z: C.catmull_keys(KT, r, np.asarray(z) / 190.0),
                 twist=lambda z: C.cubic_twist(np.asarray(z) / 190.0, k1, k2, mx),
                 rho=lambda z: B.custom_spline())


def penalty(p):
    return SMOOTH_W['mm'] * C.second_diff(np.asarray(p)[:11])


def constraints(p):
    r = C.catmull_keys(KT, np.asarray(p)[:11], np.linspace(0, 1, 381))
    return [] if r.min() > 10 else [f'r0 too small ({r.min():.1f} mm)']
