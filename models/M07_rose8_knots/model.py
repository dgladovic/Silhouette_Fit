"""
M07 — rose + 8θ harmonic base (1 + k cos4θ + c cos8θ)/(1 + k + c), k(z) and c(z) Catmull-Rom through 6 nodes,
radius knots every 10 mm + twist knots every 10 mm (Catmull-Rom). = M06 + the c(z) harmonic. docs/05_EXPERIMENTS.md §5.2.
Knot curves = value-only Catmull-Rom (`curves.catmull_keys`), kernel v1 decision (not Hermite with slopes).
"""
import numpy as np
from study import Shape, SMOOTH_W
import curves as C
import bases as B

ID = 'M07'
TITLE = 'rose + 8θ harmonic c(z) + 10 mm knots radius + 10 mm knots twist'
SOURCE = 'new model; settings inherit M05 (Grasshoper_full/), sections on the 10 mm knots'
SETTINGS = dict(N=22, H=3.0, placement='arc', target_w=9.0, sections=dict(mode='knots10'))

KZ = [0.0, 38.0, 76.0, 114.0, 152.0, 190.0]          # k / c nodes (same as M05 k)
ZK = [10.0 * i for i in range(20)]                   # radius / twist knots: z = 0, 10 ... 190

# start values: M05 kernel-v2 E0 fit (models/M05_rose_bezier/E0_fit/params.json) sampled at the knots, baked in
R0_0 = [81.5848, 91.3808, 99.1174, 104.8358, 109.0089, 112.0421, 114.0867, 115.0736, 114.8022, 113.0703,
        109.8489, 105.3741, 99.9753, 93.8301, 86.965, 79.3778, 71.0944, 62.1664, 52.6565, 42.6275]
TW_0 = [0.0, -0.622, 1.4523, 4.6074, 8.5969, 13.2887, 18.5848, 24.3963, 30.6321, 37.1914,
        43.96, 50.8065, 57.5808, 64.1154, 70.2272, 75.7241, 80.4121, 84.106, 86.6393, 87.8735]
K_0 = [0.21451, 0.20409, 0.2086, 0.18419, 0.22245, 0.17311]   # = M05 E0 k values
C_0 = [0.0] * 6

NR, NT, NK, NC = len(ZK), len(ZK) - 1, len(KZ), len(KZ)   # 20 + 19 + 6 + 6 = 51
ZCHK = np.arange(0, 190.5, 1.0)                           # constraint grid (1 mm)
W_VALID = 3000.0  # soft penalty on max rho - 1 > 0 (tip not outermost), per 10 mm band; added after the first E0 (see PROGRESS)


def unpack(p):
    p = np.asarray(p, float)
    i = 0
    r = p[i:i + NR]; i += NR
    tw = np.r_[0.0, p[i:i + NT]]; i += NT
    kv = p[i:i + NK]; i += NK
    cv = p[i:i + NC]
    return r, tw, kv, cv


NAMES = ([f'r@{z:.0f}' for z in ZK] + [f'tw@{z:.0f}' for z in ZK[1:]] + [f'k@{z:.0f}' for z in KZ] +
         [f'c@{z:.0f}' for z in KZ])
P0 = np.array(R0_0 + TW_0[1:] + K_0 + C_0, float)
LB = np.r_[np.full(NR, 20.0), np.full(NT, -30.0), np.full(NK, 0.0), np.full(NC, -0.08)]
UB = np.r_[np.full(NR, 160.0), np.full(NT, 150.0), np.full(NK, 0.45), np.full(NC, 0.08)]


def _rho(kv, cv, z):
    return B.rose8(C.catmull_keys(KZ, kv, z), C.catmull_keys(KZ, cv, z))


def shape(p):
    r, tw, kv, cv = unpack(p)
    return Shape(r0=lambda z: C.catmull_keys(ZK, r, z),
                 twist=lambda z: C.catmull_keys(ZK, tw, z),
                 rho=lambda z: _rho(kv, cv, z))


def penalty(p):
    r, tw, kv, cv = unpack(p)
    return np.r_[SMOOTH_W['mm'] * C.second_diff(r), SMOOTH_W['deg'] * C.second_diff(tw),
                 50 * np.minimum(np.asarray(kv) - 0.02, 0), SMOOTH_W['k'] * C.second_diff(kv),
                 SMOOTH_W['k'] * C.second_diff(cv), W_VALID * _valid_excess(kv, cv)]


def _valid_excess(kv, cv):
    """Max of (max_theta rho - 1, 0) per 10 mm band on the 1 mm grid (19 values); 0 while the tip is the outermost point."""
    ex = np.maximum(_rho(kv, cv, ZCHK).max(axis=1) - 1.0, 0.0)
    return np.array([ex[10 * i:10 * i + 11].max() for i in range(19)])


def constraints(p):
    r, tw, kv, cv = unpack(p)
    out = []
    rho = _rho(kv, cv, ZCHK)
    if rho.min() <= 0:
        out.append(f'section rho <= 0 (min {rho.min():.3f})')
    if rho.max() > 1.001:
        zi = int(np.argmax(rho.max(axis=1)))
        out.append(f'section rho > 1.001 (max {rho.max():.4f} at z = {ZCHK[zi]:.0f}, tip not outermost)')
    k = C.catmull_keys(KZ, kv, ZCHK)
    if k.min() < 0.02 or k.max() > 0.4:
        out.append(f'k(z) out of 0.02..0.4 ({k.min():.3f}..{k.max():.3f})')
    rr = C.catmull_keys(ZK, r, ZCHK)
    if rr.min() < 20.0:
        out.append(f'r0(z) below 20 mm ({rr.min():.1f})')
    return out
