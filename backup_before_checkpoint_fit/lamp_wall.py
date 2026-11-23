"""
Continuous pleated-wall lamp shade -> STL (pure Python, no numpy: runs inside Fusion too).

Cross-section at height z (local angle θ, before twist):
    rose:   r(θ) = r0(z) * (1 + k*cos 4θ) / (1 + k),  k = k(z) from LOBE_DEPTH
    pleats: the rose is offset along its outward normal by RIB_HEIGHT * w,
            w = triangle wave with RIBS_PER_QUARTER teeth per quarter, spaced by ARC LENGTH
            (w = 0 at the start of each quarter, 1 at each tooth tip)
    twist:  whole section rotated by twist(z)
r0(z) and twist(z) are the same Bezier curves as Grasshoper_full (PROFILE_POINTS, TWIST_POINTS).

Standalone:  python lamp_wall.py            -> lamp_wall.stl next to this file
"""
import math, os, struct

# ------------------------------------------------------------------ PARAMETERS
PROFILE_POINTS = [            # (radius mm, height mm) - from fit.py --wall
    (81.1, 0.0), (125.8, 34.6), (112.0, 75.4), (132.6, 75.4), (106.4, 120.5), (97.6, 120.5), (108.5, 126.5), (44.2, 190.0),
]
TWIST_POINTS = [              # (height fraction, degrees)
    (0.000, 0.0), (0.030, 7.5), (0.235, -19.0), (0.628, 78.5), (1.000, 84.6),
]
HEIGHT = 190.0                # mm
SHAPE_RATIO = 0.20            # b/a of the 4-petal rose (used only if LOBE_DEPTH is None)
LOBE_DEPTH = (0.2, 0.15, 120.0)  # (k below z_from, k at the rim, z_from mm): lobes get shallower towards the rim
RIBS_PER_QUARTER = 45         # 180 ribs around
RIB_HEIGHT = 1.5              # mm, tooth height outward from the rose
WALL = 1.2                    # mm wall thickness (inner skin = outer moved inward), 0 = surface only
DZ = 1.0                      # mm between rings
PTS_PER_RIB = 2               # 2 = sharp triangle teeth (valley + tip); 6+ = smoother

# ------------------------------------------------------------------ curves
def _bezier(pts, u):
    n = len(pts) - 1
    x = y = 0.0
    for i, (px, py) in enumerate(pts):
        w = math.comb(n, i) * (1 - u) ** (n - i) * u ** i
        x += w * px; y += w * py
    return x, y


def _lut(pts, key, val, steps=4000):
    c = sorted((_bezier(pts, s / steps) for s in range(steps + 1)), key=lambda p: p[key])
    ks = [p[key] for p in c]; vs = [p[val] for p in c]
    def f(q):
        if q <= ks[0]: return vs[0]
        if q >= ks[-1]: return vs[-1]
        lo, hi = 0, len(ks) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if ks[mid] <= q: lo = mid
            else: hi = mid
        t = (q - ks[lo]) / (ks[hi] - ks[lo]) if ks[hi] > ks[lo] else 0.0
        return vs[lo] + t * (vs[hi] - vs[lo])
    return f


# ------------------------------------------------------------------ cross-section (unit r0)
def _unit_section(n_per_quarter, pts_per_rib, k):
    """Points of the pleated section for r0 = 1 as (θ_local, rose_x, rose_y, nx, ny, w) for one turn."""
    # arc length of one quarter of the rose
    M = 4000
    th = [0.5 * math.pi * i / M for i in range(M + 1)]
    xy = [((1 + k * math.cos(4 * t)) / (1 + k) * math.cos(t), (1 + k * math.cos(4 * t)) / (1 + k) * math.sin(t)) for t in th]
    s = [0.0]
    for i in range(1, M + 1):
        s.append(s[-1] + math.hypot(xy[i][0] - xy[i - 1][0], xy[i][1] - xy[i - 1][1]))
    L = s[-1]

    def theta_at(frac):          # arc-length fraction of a quarter -> θ
        target = frac * L
        lo, hi = 0, M
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if s[mid] <= target: lo = mid
            else: hi = mid
        t = (target - s[lo]) / (s[hi] - s[lo]) if s[hi] > s[lo] else 0.0
        return th[lo] + t * (th[hi] - th[lo])

    out = []
    per_q = n_per_quarter * pts_per_rib
    for q in range(4):
        for j in range(per_q):
            frac = j / per_q
            phase = frac * n_per_quarter                       # rib index + fraction
            w = 1.0 - 2.0 * abs((phase % 1.0) - 0.5)           # 0 valley, 1 tip
            t = theta_at(frac) + 0.5 * math.pi * q
            rho = (1 + k * math.cos(4 * t)) / (1 + k)
            drho = -4 * k * math.sin(4 * t) / (1 + k)
            x, y = rho * math.cos(t), rho * math.sin(t)
            dx = drho * math.cos(t) - rho * math.sin(t)
            dy = drho * math.sin(t) + rho * math.cos(t)
            l = math.hypot(dx, dy)
            out.append((x, y, dy / l, -dx / l, w))
    return out


def build_rings(p=None, inner_offset=None):
    """List of rings; each ring = list of (x, y, z) points (one full turn).
    inner_offset=None -> pleated outer skin; a number -> smooth rose moved inward by that many mm."""
    p = p or {}
    prof = p.get('PROFILE_POINTS', PROFILE_POINTS); tw = p.get('TWIST_POINTS', TWIST_POINTS)
    H = p.get('HEIGHT', HEIGHT); k = p.get('SHAPE_RATIO', SHAPE_RATIO)
    nq = p.get('RIBS_PER_QUARTER', RIBS_PER_QUARTER); h = p.get('RIB_HEIGHT', RIB_HEIGHT)
    dz = p.get('DZ', DZ); ppr = p.get('PTS_PER_RIB', PTS_PER_RIB)
    lobe = p.get('LOBE_DEPTH', LOBE_DEPTH)
    r_of_z = _lut(prof, 1, 0)
    tw_of_t = _lut(tw, 0, 1)
    sections = {}

    def k_at(z):
        if not lobe:
            return k
        if isinstance(lobe[0], (tuple, list)):          # [(z, k), ...] -> smooth Catmull-Rom curve
            zs = [a for a, _ in lobe]; vs = [b for _, b in lobe]
            if z <= zs[0]: return vs[0]
            if z >= zs[-1]: return vs[-1]
            i = max(j for j in range(len(zs) - 1) if zs[j] <= z)
            t = (z - zs[i]) / (zs[i + 1] - zs[i])
            p0 = vs[max(i - 1, 0)]; p1 = vs[i]; p2 = vs[i + 1]; p3 = vs[min(i + 2, len(vs) - 1)]
            return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)
        k0, k1, z0 = lobe                                 # (k below z0, k at rim, z0) smooth step
        t = min(max((z - z0) / (H - z0), 0.0), 1.0)
        return k0 + (k1 - k0) * t * t * (3 - 2 * t)

    nz = max(2, int(round(H / dz)) + 1)
    rings = []
    for i in range(nz):
        z = H * i / (nz - 1)
        kz = round(k_at(z), 4)
        if kz not in sections:
            sections[kz] = _unit_section(nq, ppr, kz)
        sec = sections[kz]
        r0 = r_of_z(z)
        a = math.radians(tw_of_t(z / H))
        ca, sa = math.cos(a), math.sin(a)
        ring = []
        for (x, y, nx, ny, w) in sec:
            off = h * w if inner_offset is None else -inner_offset
            px = r0 * x + off * nx
            py = r0 * y + off * ny
            ring.append((px * ca - py * sa, px * sa + py * ca, z))
        rings.append(ring)
    return rings


# ------------------------------------------------------------------ mesh + STL
def _tri_normal(a, b, c):
    ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    l = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    return nx / l, ny / l, nz / l


def build_triangles(p=None):
    p = p or {}
    wall = p.get('WALL', WALL)
    outer = build_rings(p)
    n = len(outer[0])
    tris = []

    def skin(rings, flip):
        for i in range(len(rings) - 1):
            A, B = rings[i], rings[i + 1]
            for j in range(n):
                j2 = (j + 1) % n
                t1, t2 = (A[j], A[j2], B[j2]), (A[j], B[j2], B[j])
                if flip:
                    t1, t2 = (t1[0], t1[2], t1[1]), (t2[0], t2[2], t2[1])
                tris.append(t1); tris.append(t2)

    skin(outer, False)
    if wall > 0:
        # inner skin = smooth rose moved inward by WALL (pleats only on the outside -> always a valid solid;
        # for vase-mode printing the slicer only uses the outer skin anyway)
        inner = build_rings(p, inner_offset=wall)
        skin(inner, True)
        for ring_o, ring_i, top in ((outer[0], inner[0], False), (outer[-1], inner[-1], True)):
            for j in range(n):            # close bottom and top rims
                j2 = (j + 1) % n
                t1, t2 = (ring_o[j], ring_i[j2], ring_o[j2]), (ring_o[j], ring_i[j], ring_i[j2])
                if top:
                    t1, t2 = (t1[0], t1[2], t1[1]), (t2[0], t2[2], t2[1])
                tris.append(t1); tris.append(t2)
    return tris


def write_stl(path, tris):
    with open(path, 'wb') as f:
        f.write(b'lamp_wall'.ljust(80, b' '))
        f.write(struct.pack('<I', len(tris)))
        for a, b, c in tris:
            f.write(struct.pack('<12fH', *_tri_normal(a, b, c), *a, *b, *c, 0))
    return path


def generate(path=None, params=None):
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lamp_wall.stl')
    tris = build_triangles(params)
    write_stl(path, tris)
    return path, len(tris)


if __name__ == '__main__':
    import time
    t0 = time.time()
    path, n = generate()
    print(f"{path}: {n} triangles, {os.path.getsize(path)/1e6:.1f} MB, {time.time()-t0:.1f}s")
