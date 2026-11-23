"""
M06 — rose base with lobe depth k(z) + radius knots every 10 mm + twist knots every 10 mm (Catmull-Rom).
M04's "keys where needed" idea on the 10 mm segment grid. docs/05_EXPERIMENTS.md §5.2.
Knot curves = value-only Catmull-Rom (`curves.catmull_keys`), kernel v1 decision (not Hermite with slopes).
"""
import numpy as np
from study import Shape, SMOOTH_W
import curves as C
import bases as B

ID = 'M06'
TITLE = 'rose k(z) + 10 mm knots radius + 10 mm knots twist'
SOURCE = 'new model; settings inherit M05 (Grasshoper_full/), sections on the 10 mm knots'
SETTINGS = dict(N=22, H=3.0, placement='arc', target_w=9.0, sections=dict(mode='knots10'))

KZ = [0.0, 38.0, 76.0, 114.0, 152.0, 190.0]          # lobe-depth nodes (same as M05)
ZK = [10.0 * i for i in range(20)]                   # radius / twist knots: z = 0, 10 ... 190

# start values: M05 E0 fit (models/M05_rose_bezier/E0_fit/params.json) sampled at the knots, baked in
R0_0 = [82.1608, 91.4151, 99.0617, 104.8012, 108.9784, 111.9959, 113.9907, 114.891, 114.5344, 112.7817,
        109.6299, 105.2612, 99.9316, 93.8046, 86.9331, 79.3394, 71.0599, 62.1475, 52.6617, 42.6612]
TW_0 = [0.0, -1.0587, 1.0368, 4.2436, 8.2841, 13.0177, 18.3446, 24.177, 30.4256, 36.9927,
        43.7668, 50.6198, 57.4053, 63.9595, 70.1048, 75.656, 80.429, 84.2517, 86.9739, 88.4761]
K_0 = [0.22389, 0.2074, 0.21155, 0.17727, 0.22276, 0.18165]

NR, NT, NK = len(ZK), len(ZK) - 1, len(KZ)            # 20 + 19 + 6 = 45


def unpack(p):
    p = np.asarray(p, float)
    r = p[:NR]
    tw = np.r_[0.0, p[NR:NR + NT]]
    kv = p[NR + NT:NR + NT + NK]
    return r, tw, kv


NAMES = [f'r@{z:.0f}' for z in ZK] + [f'tw@{z:.0f}' for z in ZK[1:]] + [f'k@{z:.0f}' for z in KZ]
P0 = np.array(R0_0 + TW_0[1:] + K_0, float)
LB = np.r_[np.full(NR, 20.0), np.full(NT, -30.0), np.full(NK, 0.0)]
UB = np.r_[np.full(NR, 160.0), np.full(NT, 150.0), np.full(NK, 0.45)]


def shape(p):
    r, tw, kv = unpack(p)
    return Shape(r0=lambda z: C.catmull_keys(ZK, r, z),
                 twist=lambda z: C.catmull_keys(ZK, tw, z),
                 rho=lambda z: B.rose(C.catmull_keys(KZ, kv, z)))


def penalty(p):
    r, tw, kv = unpack(p)
    return np.r_[SMOOTH_W['mm'] * C.second_diff(r), SMOOTH_W['deg'] * C.second_diff(tw),
                 50 * np.minimum(np.asarray(kv) - 0.02, 0), SMOOTH_W['k'] * C.second_diff(kv)]


def constraints(p):
    r, tw, kv = unpack(p)
    out = []
    z = np.arange(0, 190.5, 1.0)
    k = C.catmull_keys(KZ, kv, z)
    if k.min() < 0.02 or k.max() > 0.4:
        out.append(f'k(z) out of 0.02..0.4 ({k.min():.3f}..{k.max():.3f})')
    rr = C.catmull_keys(ZK, r, z)
    if rr.min() < 20.0:
        out.append(f'r0(z) below 20 mm ({rr.min():.1f})')
    return out
