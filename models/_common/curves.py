"""
Curve families used by the models (docs/05_EXPERIMENTS.md §5.6). All vectorised (numpy), mm and degrees.
Each matches the maths of the user's Fusion scripts:
  bezier_rz        2D Bézier (r, z)(t), looked up by height         (Grasshoper_full, find_t_for_height)
  bezier_tdeg      Bézier (t, deg), looked up by t                   (calculate_bezier_twist2)
  cubic_twist      2-parameter cubic S-curve                         (calculate_bezier_twist)
  catmull_keys     keyframes (t, value), Catmull-Rom                 (smooth_spline_interpolation, shape_ratio_at)
  logistic_twist   3-parameter S-curve (new, M09)
"""
import math
import numpy as np

HEIGHT = 190.0


def bezier(points, u):
    p = np.asarray(points, float)
    n = len(p) - 1
    u = np.asarray(u, float)[:, None]
    w = np.stack([math.comb(n, i) * (1 - u[:, 0]) ** (n - i) * u[:, 0] ** i for i in range(n + 1)], 1)
    return w @ p


class BezierRZ:
    """r0(z) from a 2D Bézier in (r, z). Also gives t(z) (the Bézier parameter at height z) and z(t)."""

    def __init__(self, points, n=4001):
        self.points = [tuple(map(float, p)) for p in points]
        self.u = np.linspace(0, 1, n)
        c = bezier(self.points, self.u)
        self.r_u, self.z_u = c[:, 0], c[:, 1]
        o = np.argsort(self.z_u, kind='stable')
        self._z, self._r, self._t = self.z_u[o], self.r_u[o], self.u[o]

    def r(self, z):
        return np.interp(z, self._z, self._r)

    def t(self, z):
        return np.interp(z, self._z, self._t)

    def z_of_t(self, t):
        return np.interp(t, self.u, self.z_u)

    def monotone(self):
        return bool(np.all(np.diff(self.z_u) > 0))


class BezierTwist:
    """twist(t) from Bézier control points (t, deg); t in 0..1 (calculate_bezier_twist2 lookup)."""

    def __init__(self, points, n=2001):
        c = bezier(points, np.linspace(0, 1, n))
        o = np.argsort(c[:, 0], kind='stable')
        self._t, self._a = c[o, 0], c[o, 1]

    def __call__(self, t):
        return np.interp(t, self._t, self._a)


def cubic_twist(t, k1=0.0, k2=0.95, max_angle=90.0):
    t = np.asarray(t, float)
    return max_angle * (3 * (1 - t) ** 2 * t * k1 + 3 * (1 - t) * t ** 2 * k2 + t ** 3)


def catmull_keys(ts, vs, t):
    """Catmull-Rom through keyframes (ts increasing), exactly like smooth_spline_interpolation / shape_ratio_at
    (uniform-parameter Catmull-Rom per interval, ends clamped, value held outside the keys)."""
    ts = np.asarray(ts, float); vs = np.asarray(vs, float); t = np.asarray(t, float)
    n = len(ts)
    idx = np.clip(np.searchsorted(ts, t, side='left') - 1, 0, n - 2)
    p0 = vs[np.maximum(idx - 1, 0)]; p1 = vs[idx]; p2 = vs[idx + 1]; p3 = vs[np.minimum(idx + 2, n - 1)]
    span = ts[idx + 1] - ts[idx]
    lt = np.where(span > 0, (t - ts[idx]) / np.where(span > 0, span, 1), 0.0)
    val = 0.5 * (2 * p1 + (-p0 + p2) * lt + (2 * p0 - 5 * p1 + 4 * p2 - p3) * lt ** 2 + (-p0 + 3 * p1 - 3 * p2 + p3) * lt ** 3)
    val = np.where(t <= ts[0], vs[0], val)
    return np.where(t >= ts[-1], vs[-1], val)


def logistic_twist(z, total, centre, width, H=HEIGHT):
    s = lambda x: 1.0 / (1.0 + np.exp(-x))
    z = np.asarray(z, float)
    a, b = s((0 - centre) / width), s((H - centre) / width)
    return total * (s((z - centre) / width) - a) / (b - a)


def second_diff(v):
    v = np.asarray(v, float)
    return v[2:] - 2 * v[1:-1] + v[:-2] if len(v) > 2 else np.zeros(0)
