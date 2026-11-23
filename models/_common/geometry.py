"""
Geometry kernel: sections, teeth (triangle ribs), outline, rib paths, loft simulator.

A *shape* (returned by a model's curves(p)) has:
    shape.r0(z)    petal-tip radius mm            shape.twist(z)  rotation deg
    shape.rho(z)   base ρ(θ) on bases.TH, (nz|1, NTH)
    shape.zt(u)    optional: height at curve parameter u in 0..1 (for 'bezier_t' sections)
*settings*: dict(N, H, placement 'arc'|'angle_half', target_w (mm), fill (1.0), sections=dict(mode, count | z))

World frame: Z up, front camera at -Y shows X. One quarter = local θ 0..90°, rotated by twist.
"""
import numpy as np
from scipy.interpolate import CubicSpline
from bases import TH, arc_table

HEIGHT = 190.0
QROT = [np.array([[c, -s], [s, c]]) for c, s in ((1, 0), (0, 1), (-1, 0), (0, -1))]   # 0, 90, 180, 270°


class Tables:
    def __init__(self, shape, Z):
        Z = np.atleast_1d(np.asarray(Z, float))
        self.Z = Z
        self.r0 = np.asarray(shape.r0(Z), float) * np.ones_like(Z)
        self.rot = np.asarray(shape.twist(Z), float) * np.ones_like(Z)
        rho = np.asarray(shape.rho(Z), float)
        self.rho = np.broadcast_to(rho, (len(Z), rho.shape[-1])) if rho.shape[0] == 1 else rho
        S = arc_table(rho)
        self.S = np.broadcast_to(S, (len(Z), S.shape[-1])) if S.shape[0] == 1 else S


# ------------------------------------------------------------------------------------------------ teeth
def _teeth_local(r0, rho, S, st):
    """(N, 7, 2) local points: p1, 4 base-arc points, p2, apex."""
    N, H = int(st['N']), float(st['H'])
    f = float(st.get('fill', 1.0))
    u6 = np.linspace(0, 1, 6)
    if st.get('placement', 'arc') == 'arc':
        L = r0 * S[-1]
        Wt = float(st.get('target_w', 9.0))
        if L < N * Wt:
            W, g = L / N, 0.0
        else:
            W, g = Wt, (L - N * Wt) / (N - 1)
        Wf = f * W
        s = (np.arange(N) * (W + g) + (W - Wf) / 2)[:, None] + Wf * u6[None, :]
        th = np.interp(s / r0, S, TH)
    else:                                                   # 'angle_half': W = 90°/(N-0.5), half tooth at 0°
        Wd = (np.pi / 2) / (N - 0.5)
        a0 = np.r_[0.0, Wd / 2 + np.arange(N - 1) * Wd]
        w = np.r_[Wd / 2, np.full(N - 1, Wd)]
        a0 = a0 + np.r_[0.0, (w[1:] - f * w[1:]) / 2]
        th = a0[:, None] + (f * w)[:, None] * u6[None, :]
    rr = r0 * np.interp(th, TH, rho)
    P = np.stack([rr * np.cos(th), rr * np.sin(th)], -1)               # (N, 6, 2)
    d = P[:, -1] - P[:, 0]
    d = d / np.linalg.norm(d, axis=1, keepdims=True)
    apex = (P[:, 0] + P[:, -1]) / 2 + H * np.stack([d[:, 1], -d[:, 0]], -1)
    if st.get('placement', 'arc') != 'arc':
        apex[0] = P[0, 0] + H * np.array([1.0, 0.0])                  # half tooth: tip pushed straight out at 0°
    return np.concatenate([P, apex[:, None]], 1)


def teeth_world(tb, st):
    """(nz, N, 7, 2) world points of ONE quarter at every height of the Tables."""
    out = []
    for i in range(len(tb.Z)):
        P = _teeth_local(tb.r0[i], tb.rho[i], tb.S[i], st)
        a = np.radians(tb.rot[i]); c, s = np.cos(a), np.sin(a)
        out.append(P @ np.array([[c, s], [-s, c]]))
    return np.array(out)


def all_quarters(P):
    """(..., M, 2) -> (..., 4M, 2): the 4 copies of the quarter."""
    return np.concatenate([P @ R.T for R in QROT], axis=-2)


def full_outline(P):
    """front outline half-width of the full 4-quarter lamp (4-fold -> max |x|, |y| of one quarter)."""
    Q = P.reshape(P.shape[0], -1, 2)
    return np.abs(Q).max(axis=(1, 2))


def quarter_extents(P):
    Q = P.reshape(P.shape[0], -1, 2)
    return Q[..., 0].max(1), Q[..., 1].max(1), Q[..., 0].min(1), Q[..., 1].min(1)


# ------------------------------------------------------------------------------------------------ sections + loft
def section_heights(shape, st):
    sec = st.get('sections', dict(mode='uniform_z', count=15))
    mode = sec.get('mode', 'uniform_z')
    if mode == 'list':
        return np.unique(np.clip(np.asarray(sec['z'], float), 0, HEIGHT))
    n = int(sec.get('count', 15))
    if mode == 'uniform_z':
        return np.linspace(0, HEIGHT, n)
    if mode == 'knots10':
        return np.arange(0, HEIGHT + 1e-9, 10.0)
    if mode == 'bezier_t':
        if not hasattr(shape, 'zt'):
            raise ValueError('model has no curve parameter for bezier_t sections')
        return np.clip(np.asarray(shape.zt(np.linspace(0, 1, n)), float), 0, HEIGHT)
    if mode == 'adaptive':                                  # denser where twist turns fast / profile bends
        z = np.linspace(0, HEIGHT, 381)
        tw = np.gradient(shape.twist(z), z); r = shape.r0(z)
        curv = np.abs(np.gradient(np.gradient(r, z), z))
        dens = 1.0 + np.abs(tw) / (np.abs(tw).mean() + 1e-9) + curv / (curv.mean() + 1e-9)
        cdf = np.r_[0, np.cumsum((dens[1:] + dens[:-1]) / 2 * np.diff(z))]
        return np.interp(np.linspace(0, cdf[-1], n), cdf, z)
    raise ValueError(mode)


def points(shape, Z, st, built=True):
    """(nz, N, 7, 2) quarter points at heights Z; built=True -> loft-simulated through the sections."""
    Z = np.atleast_1d(np.asarray(Z, float))
    if not built:
        return teeth_world(Tables(shape, Z), st)
    zs = section_heights(shape, st)
    Ps = teeth_world(Tables(shape, zs), st)
    return CubicSpline(zs, Ps, axis=0)(np.clip(Z, zs[0], zs[-1]))


# ------------------------------------------------------------------------------------------------ ribs
def rib_start(shape, st, x0, z0):
    """Invariant of the model rib through the drawn start point (x0 mm, z0 mm) on the front side.
    'arc' placement: arc-length fraction inside its quarter; 'angle_half': local angle."""
    tb = Tables(shape, [z0])
    th = np.radians(np.linspace(-180, 0, 20001))
    rot0 = np.radians(tb.rot[0])
    loc = np.mod(th - rot0, np.pi / 2)
    xs = tb.r0[0] * np.interp(loc, TH, tb.rho[0]) * np.cos(th)
    i = np.argmin(np.abs(xs - x0))
    theta0 = th[i] - rot0
    q = np.floor(theta0 / (np.pi / 2)); local = theta0 - q * np.pi / 2
    if st.get('placement', 'arc') == 'arc':
        return q, float(np.interp(local, TH, tb.S[0]) / tb.S[0][-1])
    return q, float(local)


def rib_xy(tb, st, q, inv):
    xs, ys = np.empty(len(tb.Z)), np.empty(len(tb.Z))
    arc = st.get('placement', 'arc') == 'arc'
    for j in range(len(tb.Z)):
        th_l = np.interp(inv * tb.S[j][-1], tb.S[j], TH) if arc else inv
        rho = np.interp(th_l, TH, tb.rho[j])
        phi = th_l + q * np.pi / 2 + np.radians(tb.rot[j])
        xs[j] = tb.r0[j] * rho * np.cos(phi); ys[j] = tb.r0[j] * rho * np.sin(phi)
    return xs, ys
