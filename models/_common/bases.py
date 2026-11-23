"""
Base shapes (cross-sections), one quarter, local angle θ in 0..90° (petal tip at θ = 0).
Every function returns ρ(θ) on the grid TH, shape (nz, NTH) or (1, NTH); the section radius is r0(z)·ρ(θ).

  rose(k)            (1 + k cos4θ) / (1 + k)                              M05, M06, M09, M10
  rose8(k, c)        (1 + k cos4θ + c cos8θ) / (1 + k + c)                M07
  superformula(n1,n2) (|cos θ'|^n2 + |sin θ'|^n2)^(-1/n1), θ' = θ + 45°, normalised to 1 at the tip   M08
  custom_spline()    the user's degree-5 control-point spline from r_mults / phi_increments,
                     0–45° mirrored to 90° (create_profile_spline2)        M01–M04
"""
import numpy as np

NTH = 1501
TH = np.linspace(0.0, np.pi / 2, NTH)

# ../BaseScript (and every custom-spline script): polar definition 0-45°
R_MULTS = [1.0, 1.003, 0.985, 0.929, 0.862, 0.807, 0.741, 0.713, 0.6843, 0.681]
PHI_INC = [0.0, 4.060, 6.9, 5.734, 5.018, 2.676, 4.097, 3.114, 7.699, 5.702]


def _col(v):
    return np.atleast_1d(np.asarray(v, float))[:, None]


def rose(k):
    k = _col(k)
    return (1 + k * np.cos(4 * TH)) / (1 + k)


def rose8(k, c):
    k, c = _col(k), _col(c)
    return (1 + k * np.cos(4 * TH) + c * np.cos(8 * TH)) / (1 + k + c)


def superformula(n1, n2):
    n1, n2 = _col(n1), _col(n2)
    t = TH + np.pi / 4
    r = (np.abs(np.cos(t)) ** n2 + np.abs(np.sin(t)) ** n2) ** (-1.0 / n1)
    tip = (2 * (np.sqrt(0.5)) ** n2) ** (-1.0 / n1)
    return r / tip


def bspline_clamped(ctrl, degree=5, n=6001):
    """Clamped uniform B-spline through control points (Fusion sketchControlPointSplines)."""
    from scipy.interpolate import BSpline
    ctrl = np.asarray(ctrl, float)
    m = len(ctrl)
    inner = np.linspace(0, 1, m - degree + 1)[1:-1]
    knots = np.r_[np.zeros(degree + 1), inner, np.ones(degree + 1)]
    return BSpline(knots, ctrl, degree)(np.linspace(0, 1, n))


def custom_spline_points(r_mults=R_MULTS, phi_inc=PHI_INC):
    pol = []
    a = 0.0
    for r, d in zip(r_mults, phi_inc):
        a = min(a + d, 45.0)
        pol.append((r, a))
        if a >= 45.0:
            break
    pol = pol + [(r, 90.0 - a) for r, a in reversed(pol[:-1])]
    return np.array([(r * np.cos(np.radians(a)), r * np.sin(np.radians(a))) for r, a in pol])


_custom = {}


def custom_spline(r_mults=R_MULTS, phi_inc=PHI_INC, degree=5):
    key = (tuple(r_mults), tuple(phi_inc), degree)
    if key not in _custom:
        c = bspline_clamped(custom_spline_points(r_mults, phi_inc), degree)
        th = np.arctan2(c[:, 1], c[:, 0]); rr = np.hypot(c[:, 0], c[:, 1])
        o = np.argsort(th)
        _custom[key] = np.interp(TH, th[o], rr[o])[None, :]
    return _custom[key]


def arc_table(rho):
    """Cumulative arc length of the unit section over TH, same shape as rho."""
    x, y = rho * np.cos(TH), rho * np.sin(TH)
    ds = np.hypot(np.diff(x, axis=-1), np.diff(y, axis=-1))
    return np.concatenate([np.zeros(rho.shape[:-1] + (1,)), np.cumsum(ds, axis=-1)], axis=-1)
