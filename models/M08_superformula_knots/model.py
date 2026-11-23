"""
M08 — superformula base, 4-fold, with n1(z), n2(z) + radius knots every 10 mm + twist knots every 10 mm (Catmull-Rom).
One base family from rose-like (n2 -> 2, small n1) to star-like (large n2: pointed tips). docs/05_EXPERIMENTS.md §5.2.
Base: bases.superformula(n1, n2) = (|cos θ'|^n2 + |sin θ'|^n2)^(-1/n1), θ' = θ + 45°, normalised to 1 at the tip.
n1(z), n2(z): value-only Catmull-Rom through 6 nodes (z = 0, 38 ... 190), as M05's k(z).
"""
import numpy as np
from study import Shape, SMOOTH_W
import curves as C
import bases as B

ID = 'M08'
TITLE = 'superformula n1(z), n2(z) + 10 mm knots radius + 10 mm knots twist'
SOURCE = 'new model; settings inherit M05 (Grasshoper_full/), sections on the 10 mm knots'
SETTINGS = dict(N=22, H=3.0, placement='arc', target_w=9.0, sections=dict(mode='knots10'))

KZ = [0.0, 38.0, 76.0, 114.0, 152.0, 190.0]          # base-shape nodes (same heights as M05's k nodes)
ZK = [10.0 * i for i in range(20)]                   # radius / twist knots: z = 0, 10 ... 190

# start values, baked in:
#  r0, twist: M05 E0 fit (kernel v2, models/M05_rose_bezier/E0_fit/params.json) sampled at the knots
#  n1, n2: least-squares fit of the superformula to the rose with M05's mean k(z) = 0.2029 (max |Δρ| 0.0031,
#          rms 0.0015); n1 sits on its lower bound 0.3 (unbounded optimum n1 0.294, n2 2.353, max |Δρ| 0.0034 - the
#          bounded point is as good), used at all 6 nodes.
R0_0 = [81.5848, 91.3808, 99.1174, 104.8358, 109.0089, 112.0421, 114.0867, 115.0736, 114.8022, 113.0703,
        109.8489, 105.3741, 99.9753, 93.8301, 86.965, 79.3778, 71.0944, 62.1664, 52.6565, 42.6275]
TW_0 = [0.0, -0.622, 1.4523, 4.6074, 8.5969, 13.2887, 18.5848, 24.3963, 30.6321, 37.1914,
        43.96, 50.8065, 57.5808, 64.1154, 70.2272, 75.7241, 80.4121, 84.106, 86.6393, 87.8735]
N1_0 = [0.3] * 6
N2_0 = [2.36030324] * 6

SMOOTH_N = 0.2       # smoothness weight per unit of n1 / n2 (orchestrator's choice: units differ from k)
RHO_MIN = 0.3        # valley must stay above this (constraint) -> soft floor in the penalty
NR, NT, NN = len(ZK), len(ZK) - 1, len(KZ)            # 20 + 19 + 6 + 6 = 51


def unpack(p):
    p = np.asarray(p, float)
    r = p[:NR]
    tw = np.r_[0.0, p[NR:NR + NT]]
    n1 = p[NR + NT:NR + NT + NN]
    n2 = p[NR + NT + NN:NR + NT + 2 * NN]
    return r, tw, n1, n2


NAMES = ([f'r@{z:.0f}' for z in ZK] + [f'tw@{z:.0f}' for z in ZK[1:]] +
         [f'n1@{z:.0f}' for z in KZ] + [f'n2@{z:.0f}' for z in KZ])
P0 = np.array(R0_0 + TW_0[1:] + N1_0 + N2_0, float)
LB = np.r_[np.full(NR, 20.0), np.full(NT, -30.0), np.full(NN, 0.3), np.full(NN, 2.05)]
UB = np.r_[np.full(NR, 160.0), np.full(NT, 150.0), np.full(NN, 30.0), np.full(NN, 30.0)]


def _n(n1, n2, z):
    return C.catmull_keys(KZ, n1, z), C.catmull_keys(KZ, n2, z)


def shape(p):
    r, tw, n1, n2 = unpack(p)
    return Shape(r0=lambda z: C.catmull_keys(ZK, r, z),
                 twist=lambda z: C.catmull_keys(ZK, tw, z),
                 rho=lambda z: B.superformula(*_n(n1, n2, z)))


def _valley(n1, n2):
    """ρ at the valley (θ = 45°): 2^(-(n2/2 - 1)/n1)."""
    return 2.0 ** (-(np.asarray(n2) / 2.0 - 1.0) / np.asarray(n1))


def penalty(p):
    r, tw, n1, n2 = unpack(p)
    return np.r_[SMOOTH_W['mm'] * C.second_diff(r), SMOOTH_W['deg'] * C.second_diff(tw),
                 SMOOTH_N * C.second_diff(n1), SMOOTH_N * C.second_diff(n2),
                 50 * np.minimum(_valley(n1, n2) - (RHO_MIN + 0.02), 0)]


def constraints(p):
    r, tw, n1, n2 = unpack(p)
    out = []
    z = np.arange(0, 190.5, 1.0)
    a, b = _n(n1, n2, z)
    if a.min() <= 0.0 or b.min() <= 2.0:      # node values are bounded; between nodes only the physical limits matter
        out.append(f'n1(z) <= 0 or n2(z) <= 2 between nodes (n1 min {a.min():.3f}, n2 min {b.min():.3f})')
    else:
        rho = B.superformula(a, b)
        if rho.max() > 1.001:
            out.append(f'rho max {rho.max():.4f} > 1.001 (tip not outermost)')
        if rho.min() <= RHO_MIN:
            out.append(f'rho min {rho.min():.3f} <= {RHO_MIN}')
    rr = C.catmull_keys(ZK, r, z)
    if rr.min() < 20.0:
        out.append(f'r0(z) below 20 mm ({rr.min():.1f})')
    return out
