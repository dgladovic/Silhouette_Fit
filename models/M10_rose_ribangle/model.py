"""
M10 — rose base with lobe depth k(z) + radius knots every 10 mm + rib lean angle alpha(z) knots every 10 mm.
The twist is not a parameter: it is integrated from the rib lean angle the drawing shows directly,
    twist(z) = (180/pi) * integral_0^z tan(alpha(z')) / r0(z') dz'
= the turning rate of a point at the petal-tip radius r0. docs/05_EXPERIMENTS.md §5.2.
Knot curves = value-only Catmull-Rom (`curves.catmull_keys`), kernel v1 decision. twist(0) = 0 by construction,
but alpha(0) is free, so the rim may turn either way (M05's rim dip is reachable, unlike M06's fixed knot).
"""
import numpy as np
from study import Shape, SMOOTH_W
import curves as C
import bases as B

ID = 'M10'
TITLE = 'rose k(z) + 10 mm knots radius + 10 mm knots rib lean angle (twist = integral tan(alpha)/r0)'
SOURCE = 'new model; settings inherit M05 (Grasshoper_full/), sections on the 10 mm knots'
SETTINGS = dict(N=22, H=3.0, placement='arc', target_w=9.0, sections=dict(mode='knots10'))

KZ = [0.0, 38.0, 76.0, 114.0, 152.0, 190.0]          # lobe-depth nodes (same as M05/M06)
ZK = [10.0 * i for i in range(20)]                   # radius / alpha knots: z = 0, 10 ... 190
DZ = 0.25                                            # integration grid step (mm)
ZF = np.arange(0.0, 190.0 + 1e-9, DZ)                # fine grid for the twist integral

# start values: M05 kernel-v2 E0 fit (models/M05_rose_bezier/E0_fit/params.json), baked in.
# r0 at the knots; alpha = atan(r0 * dtwist/dz * pi/180) at the knots (dtwist/dz by np.gradient on a 0.25 mm grid),
# alpha(0) = -65.95 deg (M05's steep rim dip) clipped to the lower bound -30; k = M05's fitted k nodes.
# Rebuilt twist vs M05 twist: max 0.60 deg (z = 10), a constant -0.48 deg offset above z = 20 (the clipped rim dip).
R0_0 = [81.5848, 91.3808, 99.1174, 104.8358, 109.0089, 112.0421, 114.0867, 115.0736, 114.8022, 113.0703,
        109.8489, 105.3741, 99.9753, 93.8301, 86.965, 79.3778, 71.0944, 62.1664, 52.6565, 42.6275]
AL_0 = [-30.0, 12.3103, 24.8274, 33.3684, 39.6675, 44.4073, 47.9535, 50.4971, 52.1183, 52.8349,
        52.6359, 51.5049, 49.3887, 46.1415, 41.5382, 35.3717, 27.6416, 18.8094, 9.9245, 2.4078]
K_0 = [0.21451, 0.20409, 0.2086, 0.18419, 0.22245, 0.17311]

NR, NA, NK = len(ZK), len(ZK), len(KZ)               # 20 + 20 + 6 = 46


def unpack(p):
    p = np.asarray(p, float)
    return p[:NR], p[NR:NR + NA], p[NR + NA:NR + NA + NK]


def twist_table(r, al):
    """Cumulative twist (deg) on the fine grid ZF: cumulative trapezoid of tan(alpha)/r0."""
    a = np.radians(np.clip(C.catmull_keys(ZK, al, ZF), -85.0, 85.0))
    rr = np.maximum(C.catmull_keys(ZK, r, ZF), 1.0)
    f = np.tan(a) / rr
    return np.r_[0.0, np.cumsum(0.5 * (f[1:] + f[:-1]) * DZ)] * (180.0 / np.pi)


NAMES = [f'r@{z:.0f}' for z in ZK] + [f'alpha@{z:.0f}' for z in ZK] + [f'k@{z:.0f}' for z in KZ]
P0 = np.array(R0_0 + AL_0 + K_0, float)
LB = np.r_[np.full(NR, 20.0), np.full(NA, -30.0), np.full(NK, 0.0)]
UB = np.r_[np.full(NR, 160.0), np.full(NA, 75.0), np.full(NK, 0.45)]


def shape(p):
    r, al, kv = unpack(p)
    tw = twist_table(r, al)
    return Shape(r0=lambda z: C.catmull_keys(ZK, r, z),
                 twist=lambda z: np.interp(z, ZF, tw),
                 rho=lambda z: B.rose(C.catmull_keys(KZ, kv, z)))


def penalty(p):
    r, al, kv = unpack(p)
    return np.r_[SMOOTH_W['mm'] * C.second_diff(r), SMOOTH_W['deg'] * C.second_diff(al),
                 50 * np.minimum(np.asarray(kv) - 0.02, 0), SMOOTH_W['k'] * C.second_diff(kv)]


def constraints(p):
    r, al, kv = unpack(p)
    out = []
    z = np.arange(0, 190.5, 1.0)
    k = C.catmull_keys(KZ, kv, z)
    if k.min() < 0.02 or k.max() > 0.4:
        out.append(f'k(z) out of 0.02..0.4 ({k.min():.3f}..{k.max():.3f})')
    rr = C.catmull_keys(ZK, r, z)
    if rr.min() < 20.0:
        out.append(f'r0(z) below 20 mm ({rr.min():.1f})')
    aa = C.catmull_keys(ZK, al, z)
    if np.abs(aa).max() > 80.0:
        out.append(f'alpha(z) beyond +-80 deg ({aa.min():.1f}..{aa.max():.1f})')
    return out
