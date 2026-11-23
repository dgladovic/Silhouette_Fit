"""
M09 — minimal baseline: rose with ONE constant lobe depth k, 8-point 2D Bézier radius (as M05), 3-parameter logistic twist.
docs/05_EXPERIMENTS.md §5.2 (new models). Settings inherit M05 (N 22, H 3, arc 9 mm, 15 uniform sections).
Question: if this scores close to the knot models, their extra parameters are fitting drawing noise.
"""
import numpy as np
from study import Shape
import curves as C
import bases as B

ID = 'M09'
TITLE = 'rose (constant k) + 2D Bezier radius + logistic twist'
SOURCE = 'new model; settings inherit M05 (Grasshoper_full/ in this repo), M05 own sections (15 uniform z)'
SETTINGS = dict(N=22, H=3.0, placement='arc', target_w=9.0, sections=dict(mode='uniform_z', count=15))

N_PROF = 8

# start values (baked from M05 E0, kernel v2, models/M05_rose_bezier/E0_fit/params.json):
# radius points = M05's fitted 2D Bezier points (unpacked with M05.unpack)
PROF0 = [(81.58480359538704, 0.0), (113.610178831613, 30.04059529851807), (109.47589465256692, 40.68777443339416),
         (120.86307518345146, 81.72942150263599), (128.84820716739907, 86.49430780375154),
         (90.09837331404844, 115.13137807986058), (118.6161732495087, 115.99903285689209), (42.62748444429606, 190.0)]
# k = mean of M05's six fitted k(z) node values
K0 = 0.20115766665286786
# logistic (total, centre, width): least squares on M05's E0 twist at z = 0..190 step 1 mm
# (rms 0.93 deg, max |d| 2.26 deg at z = 14 mm, where M05's Bezier twist dips to -0.6 deg)
LOG0 = [88.67558910559536, 102.35814459119267, 34.624612805135634]


def pack(prof, k, lg):
    x = [prof[0][0]] + [v for p in prof[1:-1] for v in p] + [prof[-1][0]]
    return np.array(x + [k] + list(lg), float)


def unpack(x):
    x = list(map(float, x))
    prof = [(x[0], 0.0)]; j = 1
    for _ in range(N_PROF - 2):
        prof.append((x[j], x[j + 1])); j += 2
    prof.append((x[j], 190.0)); j += 1
    return prof, x[j], x[j + 1:j + 4]


NAMES = (['P0.r'] + [f'P{i}.{c}' for i in range(1, N_PROF - 1) for c in 'rz'] + [f'P{N_PROF-1}.r'] +
         ['k', 'tw.total', 'tw.centre', 'tw.width'])
P0 = pack(PROF0, K0, LOG0)
LB = np.full(len(P0), -np.inf); UB = np.full(len(P0), np.inf)
_j = 2 + 2 * (N_PROF - 2)                       # index of k
LB[_j:_j + 4] = [0.05, 45.0, 20.0, 3.0]
UB[_j:_j + 4] = [0.40, 135.0, 170.0, 80.0]


def shape(p):
    prof, k, (tot, cen, wid) = unpack(p)
    bz = C.BezierRZ(prof)
    rho = B.rose(k)
    return Shape(r0=bz.r, twist=lambda z: C.logistic_twist(z, tot, cen, wid),
                 rho=lambda z: rho, zt=bz.z_of_t)            # (1, NTH): constant over height, kernel broadcasts


def penalty(p):
    prof, _, _ = unpack(p)
    zs = [q[1] for q in prof]
    return 20 * np.minimum(np.diff(zs), 0)        # same soft monotone-z penalty as M05 (no knot values to smooth)


def constraints(p):
    prof, k, lg = unpack(p)
    out = []
    if not C.BezierRZ(prof).monotone():
        out.append('profile z(t) not monotone')
    if not 0.05 <= k <= 0.4:
        out.append(f'k out of 0.05..0.4 ({k:.3f})')
    return out
