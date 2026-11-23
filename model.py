"""
Python replica of Grasshoper_full.py geometry (no Fusion needed).

Units: mm and degrees, same as BEZIER_CONTROL_POINTS / twist_points in the Fusion script.
Coordinate system: Z up, front view looks along +Y (shows X), right view looks along -X (shows Y).
"""
import math, os
import numpy as np

HEIGHT = 190.0          # max_height_cm in the script (really mm)
SHAPE_RATIO = 0.20      # b/a of the polar rose r = a + b*cos(4θ)
N_TRI = 22              # TOTAL triangles per quarter
TRI_W = 9.0             # target_width 0.9 cm
TRI_H = 3.0             # scale_perp 0.3 cm
NUM_SECTIONS = 15

# ---------------------------------------------------------------- curves
def bezier(points, u):
    """General Bezier, points = [(x, y), ...], u array in [0, 1]."""
    p = np.asarray(points, float)
    n = len(p) - 1
    u = np.asarray(u, float)[:, None]
    w = np.stack([math.comb(n, i) * (1 - u[:, 0]) ** (n - i) * u[:, 0] ** i for i in range(n + 1)], 1)
    return w @ p


def profile_r(points, z):
    """r0(z) exactly like find_t_for_height + calculate_dynamic_bezier (points are (r, z))."""
    c = bezier(points, np.linspace(0, 1, 4001))
    order = np.argsort(c[:, 1])
    return np.interp(z, c[order, 1], c[order, 0])


def twist_deg(points, t):
    """calculate_bezier_twist2: points are (t, deg) with t in 0..1."""
    c = bezier(points, np.linspace(0, 1, 2001))
    order = np.argsort(c[:, 0])
    return np.interp(t, c[order, 0], c[order, 1])


def twist_cubic(t, k1=0.0, k2=0.95, max_angle=90.0):
    """calculate_bezier_twist (the old 2-parameter version)."""
    t = np.asarray(t, float)
    return max_angle * (3 * (1 - t) ** 2 * t * k1 + 3 * (1 - t) * t ** 2 * k2 + t ** 3)


# ---------------------------------------------------------------- one slice
# Cross-section shape r/r0 as a function of local angle θ (petal tips at 0, 90, 180, 270 deg):
#   ('rose', k)    : (1 + k cos 4θ) / (1 + k)              -- Grasshoper_full (round valleys)
#   ('circles', d) : union of 4 circles, centres at distance d, radius 1-d  (star nozzle: round lobes, sharp creases)
SECTION = ('rose', SHAPE_RATIO)


def rho_fn(th, section=None):
    kind, p = section or SECTION
    th = np.asarray(th, float)
    if kind == 'rose':
        return (1 + p * np.cos(4 * th)) / (1 + p)
    if kind == 'circles':
        d, c = p, 1.0 - p
        best = np.full(th.shape, -np.inf)
        for alpha in (0.0, 0.5 * np.pi, np.pi, 1.5 * np.pi):
            D = th - alpha
            disc = c * c - (d * np.sin(D)) ** 2
            r = np.where(disc >= 0, d * np.cos(D) + np.sqrt(np.maximum(disc, 0)), -np.inf)
            best = np.maximum(best, r)
        return best
    raise ValueError(kind)


def drho_fn(th, section=None, h=1e-5):
    return (rho_fn(np.asarray(th) + h, section) - rho_fn(np.asarray(th) - h, section)) / (2 * h)


_TH = np.radians(np.linspace(0, 90, 1501))


_tables = {}


def set_section(section):
    """Switch the cross-section shape everywhere in the model (tables cached per section)."""
    global SECTION, _RHO, _UX, _UY, _S_UNIT
    SECTION = section
    if len(_tables) > 4000:          # keep memory bounded during long fits
        _tables.clear()
    if section not in _tables:
        rho = rho_fn(_TH)
        ux, uy = rho * np.cos(_TH), rho * np.sin(_TH)
        _tables[section] = (rho, ux, uy, np.r_[0, np.cumsum(np.hypot(np.diff(ux), np.diff(uy)))])
    _RHO, _UX, _UY, _S_UNIT = _tables[section]


set_section(SECTION)

def section_at(z):
    return ('rose', round(float(K_OF_Z(z)), 6)) if K_OF_Z else SECTION


K_NODES_Z = [0.0, 38.0, 76.0, 114.0, 152.0, 190.0]   # heights of the lobe-depth control values


def catmull_rom(nodes_z, values):
    """Smooth curve through (nodes_z, values) (Catmull-Rom, clamped ends). Same maths in the Fusion scripts."""
    zs, vs = list(nodes_z), list(values)
    def f(z):
        z = float(z)
        if z <= zs[0]: return vs[0]
        if z >= zs[-1]: return vs[-1]
        i = max(j for j in range(len(zs) - 1) if zs[j] <= z)
        t = (z - zs[i]) / (zs[i + 1] - zs[i])
        p0 = vs[max(i - 1, 0)]; p1 = vs[i]; p2 = vs[i + 1]; p3 = vs[min(i + 2, len(vs) - 1)]
        return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)
    return f


def k_top_blend(k_base, k_top, z_from):
    """k = k_base below z_from, smooth (smoothstep) change to k_top at the rim."""
    def f(z):
        t = np.clip((np.asarray(z, float) - z_from) / (HEIGHT - z_from), 0, 1)
        return k_base + (k_top - k_base) * t * t * (3 - 2 * t)
    return f


# Lobe depth (rose k) that changes with height: K_OF_Z(z_mm) -> k.  None = constant SECTION.
# Design default (ktop_experiment.py): 0.20 below 120 mm, smoothly to 0.15 at the rim.
LOBE_DEPTH = (0.20, 0.15, 120.0)          # (k_base, k_top, z_from)
K_OF_Z = k_top_blend(*LOBE_DEPTH)
# Current design: lobe depth curve from the 10 mm checkpoint fit (apply_ribs_fit.py -> lobe_depth.json)
_ld = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lobe_depth.json')
if os.path.exists(_ld):
    import json as _json
    _d = _json.load(open(_ld))
    K_OF_Z = catmull_rom(_d['z'], _d['k'])


def slice_points(r0, rot):
    """All triangle points of one quarter slice (generate_arc_normal), world XY in mm.
    Returns array (N_TRI, 7, 2): p1, 4 base-arc points, p2, apex."""
    L = r0 * _S_UNIT[-1]
    if L < N_TRI * TRI_W:
        W, g = L / N_TRI, 0.0
    else:
        W, g = TRI_W, (L - N_TRI * TRI_W) / (N_TRI - 1)
    s0 = np.arange(N_TRI) * (W + g)
    s = s0[:, None] + W * np.linspace(0, 1, 6)[None, :]          # p1, 4 arc pts, p2
    th = np.interp(s / r0, _S_UNIT, _TH)
    rho = rho_fn(th)
    a = th + math.radians(rot)
    P = np.stack([r0 * rho * np.cos(a), r0 * rho * np.sin(a)], -1)  # (N,6,2)
    d = P[:, -1] - P[:, 0]
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    apex = (P[:, 0] + P[:, -1]) / 2 + TRI_H * np.stack([d[:, 1], -d[:, 0]], -1)
    return np.concatenate([P, apex[:, None]], 1)


GEOMETRY = 'triangles'   # 'triangles' = Grasshoper_full wedges, 'wall' = LampWall continuous pleats
WALL_RIBS_PER_QUARTER = 45
WALL_RIB_HEIGHT = 1.5
_wall_cache = {}


def wall_points(r0, rot):
    """Outer pleated wall section of ONE quarter (same maths as LampWall/lamp_wall.py), world XY mm."""
    key = (WALL_RIBS_PER_QUARTER, WALL_RIB_HEIGHT, SECTION)
    if key not in _wall_cache:
        nq = WALL_RIBS_PER_QUARTER
        frac = np.arange(nq * 2 + 1) / (nq * 2)                 # valleys and tips
        th = np.interp(frac * _S_UNIT[-1], _S_UNIT, _TH)
        w = 1 - 2 * np.abs((frac * nq) % 1.0 - 0.5)
        rho = rho_fn(th)
        drho = drho_fn(th)
        dx = drho * np.cos(th) - rho * np.sin(th); dy = drho * np.sin(th) + rho * np.cos(th)
        l = np.hypot(dx, dy)
        _wall_cache[key] = (th, rho, dy / l, -dx / l, w)
    th, rho, nx, ny, w = _wall_cache[key]
    px = r0 * rho * np.cos(th) + WALL_RIB_HEIGHT * w * nx
    py = r0 * rho * np.sin(th) + WALL_RIB_HEIGHT * w * ny
    a = math.radians(rot)
    return np.stack([px * math.cos(a) - py * math.sin(a), px * math.sin(a) + py * math.cos(a)], -1)


def extents(r0, rot):
    """Silhouette half-widths at one height.
    full_front : max X of the full lamp (4 quarters) = what the canvas shows (all 4 sides equal)
    q_front    : max X of the single generated quarter (front view of what the script makes)
    q_right    : max Y of the single generated quarter (right view)"""
    P = wall_points(r0, rot) if GEOMETRY == 'wall' else slice_points(r0, rot).reshape(-1, 2)
    q_front, q_right = P[:, 0].max(), P[:, 1].max()
    full = max(q_front, P[:, 1].max(), (-P[:, 0]).max(), (-P[:, 1]).max())
    return full, q_front, q_right


def silhouettes(profile_pts, twist_fn, z):
    r0 = profile_r(profile_pts, z)
    rot = twist_fn(z / HEIGHT)
    base = SECTION
    out = []
    for zi, r, a in zip(np.atleast_1d(z), r0, rot):
        if K_OF_Z:
            set_section(section_at(zi))
        out.append(extents(r, a))
    if K_OF_Z:
        set_section(base)
    out = np.array(out)
    return out[:, 0], out[:, 1], out[:, 2], r0, rot


def center_rib_slope(profile_pts, twist_fn, z, dz=0.5):
    """dx/dz of the rib passing through the front-facing centre line (world angle -90°)."""
    r0 = profile_r(profile_pts, z)
    rot = twist_fn(z / HEIGHT)
    drot = (twist_fn(np.clip(z + dz, 0, HEIGHT) / HEIGHT) - twist_fn(np.clip(z - dz, 0, HEIGHT) / HEIGHT)) / (
        np.clip(z + dz, 0, HEIGHT) - np.clip(z - dz, 0, HEIGHT))
    if K_OF_Z:   # x = 0 on the front -> dx/dz = R * rot' exactly, R = section radius there
        rho = np.array([rho_fn(np.radians(-90.0 - a), section_at(zi)) for a, zi in zip(np.atleast_1d(rot), np.atleast_1d(z))])
    else:
        rho = rho_fn(np.radians(-90.0 - rot))      # section radius of the point facing the camera
    return r0 * rho * np.radians(drot)


def section_heights():
    return np.array([(i / (NUM_SECTIONS - 1)) * HEIGHT for i in range(NUM_SECTIONS)])
