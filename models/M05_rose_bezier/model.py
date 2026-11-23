"""
M05 — rose base with lobe depth k(z), 8-point 2D Bézier radius, 5-point Bézier twist.
= Grasshoper_full in this repo (the active fit before the study). docs/05_EXPERIMENTS.md §5.2.
"""
import numpy as np
from study import Shape
import curves as C
import bases as B

ID = 'M05'
TITLE = 'rose k(z) + 2D Bezier radius + Bezier twist'
SOURCE = 'Grasshoper_full/ (this repo)'
SETTINGS = dict(N=22, H=3.0, placement='arc', target_w=9.0, sections=dict(mode='uniform_z', count=15))

KZ = [0.0, 38.0, 76.0, 114.0, 152.0, 190.0]
N_PROF, N_TW = 8, 5

# start values: the active fit (joint two-view fit, commit 1e8223d)
PROF0 = [(81.67181042970066, 0.0), (112.48223927577794, 32.18512798926261), (107.25694524168713, 34.294432676281055),
         (120.77968823240195, 67.83766926380636), (128.43525210140578, 85.45624970264477), (90.9427838413748, 115.12390707375792),
         (118.80905277143538, 116.07817526836186), (42.83343037250626, 190.0)]
TW0 = [(0.0, 0.0), (1.7417933965843367e-05, -6.1652418613822455), (0.3965471346999638, 0.8281938405570629),
       (0.6538277056571102, 82.79893575241452), (1.0, 88.58118275910391)]
K0 = [0.2235862152310918, 0.20925091785018549, 0.21028615553324329, 0.1716731781566505, 0.2285983698737901, 0.20048178556239893]


def pack(prof, tw, kv):
    x = [prof[0][0]] + [v for p in prof[1:-1] for v in p] + [prof[-1][0]]
    x += [v for p in tw[1:-1] for v in p] + [tw[-1][1]]
    return np.array(x + list(kv), float)


def unpack(x):
    x = list(x); k = 0
    prof = [(x[0], 0.0)]; k = 1
    for _ in range(N_PROF - 2):
        prof.append((x[k], x[k + 1])); k += 2
    prof.append((x[k], 190.0)); k += 1
    tw = [(0.0, 0.0)]
    for _ in range(N_TW - 2):
        tw.append((x[k], x[k + 1])); k += 2
    tw.append((1.0, x[k])); k += 1
    return prof, tw, x[k:k + len(KZ)]


NAMES = (['P0.r'] + [f'P{i}.{c}' for i in range(1, N_PROF - 1) for c in 'rz'] + [f'P{N_PROF-1}.r'] +
         [f'T{i}.{c}' for i in range(1, N_TW - 1) for c in ('t', 'deg')] + [f'T{N_TW-1}.deg'] + [f'k@{z:.0f}' for z in KZ])
P0 = pack(PROF0, TW0, K0)
LB = np.full(len(P0), -np.inf); UB = np.full(len(P0), np.inf)
_k = 2 + 2 * (N_PROF - 2)
for j in range(N_TW - 2):
    LB[_k + 2 * j], UB[_k + 2 * j] = 0.0, 1.0


def shape(p):
    prof, tw, kv = unpack(p)
    bz = C.BezierRZ(prof); bt = C.BezierTwist(tw)
    return Shape(r0=bz.r, twist=lambda z: bt(np.asarray(z) / 190.0),
                 rho=lambda z: B.rose(C.catmull_keys(KZ, kv, z)), zt=bz.z_of_t)


def penalty(p):
    prof, tw, kv = unpack(p)
    zs = [q[1] for q in prof]; ts = [q[0] for q in tw]
    return np.r_[20 * np.minimum(np.diff(zs), 0), 200 * np.minimum(np.diff(ts), 0),
                 50 * np.minimum(np.array(kv) - 0.02, 0), 2.0 * C.second_diff(kv)]


def constraints(p):
    prof, tw, kv = unpack(p)
    out = []
    if not C.BezierRZ(prof).monotone():
        out.append('profile z(t) not monotone')
    ts = [q[0] for q in tw]
    if min(ts) < 0 or max(ts) > 1 or np.any(np.diff(ts) < 0):
        out.append('twist t outside 0..1 or decreasing')
    k = C.catmull_keys(KZ, kv, np.arange(0, 190.5, 1.0))
    if k.min() < 0.02 or k.max() > 0.4:
        out.append(f'k(z) out of 0.02..0.4 ({k.min():.3f}..{k.max():.3f})')
    return out
