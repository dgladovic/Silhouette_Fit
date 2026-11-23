"""
Second view check: does the fitted lamp match the 3/4 drawing (reference/view34_drawing.png)?

The drawing is an orthographic view from above (vertical base sides stay parallel). Camera unknowns:
  az   rotation of the lamp about Z (deg)       el  elevation of the view (deg)
  s    scale (px per mm)                        cx, cy  image position of the axis at z = 0 (px)
  mirror  +1 / -1 (drawing may be mirrored)
Model: LampWall rings (current fitted profile, twist, lobe depth, 1.5 mm pleats) + base cylinder
(radius 39.45 mm, 70 mm tall, measured on the front drawing).

Fits the camera only (shape fixed), then reports the outline error every 10 px row and saves overlays.
Run: python views/fit_view34.py
"""
import os, sys, json
import numpy as np
import cv2
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'LampWall'))
import lamp_wall as lw

OUT = os.path.join(HERE, 'view34')
os.makedirs(OUT, exist_ok=True)
BASE_R, BASE_H = 39.45, 70.0

# ------------------------------------------------------------ drawing outline
src = cv2.imread(os.path.join(ROOT, 'reference', 'view34_drawing.png'), cv2.IMREAD_UNCHANGED)
if src.shape[2] == 4:
    a = src[:, :, 3:4].astype(float) / 255
    src = (src[:, :, :3] * a + 255 * (1 - a)).astype(np.uint8)
GRAY = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
H, W = GRAY.shape
dark = (GRAY < 140).astype(np.uint8)
closed = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
ff = closed.copy(); cv2.floodFill(ff, np.zeros((H + 2, W + 2), np.uint8), (0, 0), 2)
mask = (ff != 2).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(mask)
IMG_MASK = (lab == 1 + np.argmax(st[1:, 4])).astype(np.uint8)
IMG_EDGE = cv2.morphologyEx(IMG_MASK, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
DT_IMG = cv2.distanceTransform(1 - IMG_EDGE, cv2.DIST_L2, 3)

# ------------------------------------------------------------ model geometry (world mm)
RINGS = np.array(lw.build_rings({'DZ': 2.0, 'PTS_PER_RIB': 2}))            # (nz, npts, 3)
nb = 240
tb = np.linspace(0, 2 * np.pi, nb, endpoint=False)
BASE = np.array([[[BASE_R * np.cos(t), BASE_R * np.sin(t), z] for t in tb] for z in (-BASE_H, -BASE_H / 2, 0.0)])


def quads(rings):
    a, b = rings[:-1], rings[1:]
    a2, b2 = np.roll(a, -1, axis=1), np.roll(b, -1, axis=1)
    return np.stack([a, a2, b2, b], axis=2).reshape(-1, 4, 3)


QUADS = np.concatenate([quads(RINGS), quads(BASE)])
CAPS = [BASE[0], RINGS[0]]          # filled discs (base bottom, shade bottom)
ROW_CUT = 590                       # drawing rows below this belong to the base


def project(P, cam):
    """cam = [az, el, s, cx, cy, invD, mirror]; invD = 1 / camera distance (mm), 0 = orthographic."""
    az, el, s, cx, cy, invD, mir = cam
    a, e = np.radians(az), np.radians(el)
    x1 = P[..., 0] * np.cos(a) - P[..., 1] * np.sin(a)
    y1 = P[..., 0] * np.sin(a) + P[..., 1] * np.cos(a)
    zc = P[..., 2] - 95.0                                  # perspective centred at mid shade height
    depth = y1 * np.cos(e) - zc * np.sin(e)                # + = away from the camera
    f = 1.0 / (1.0 + invD * depth)
    u = x1 * mir * f
    v = (P[..., 2] * np.cos(e) + y1 * np.sin(e) - 95.0 * np.cos(e)) * f + 95.0 * np.cos(e)
    return np.stack([cx + s * u, cy - s * v], -1)


def render(cam):
    m = np.zeros((H, W), np.uint8)
    q = np.round(project(QUADS, cam) * 4).astype(np.int32)
    cv2.fillPoly(m, list(q), 1, shift=2)
    for c in CAPS:
        cv2.fillPoly(m, [np.round(project(c, cam) * 4).astype(np.int32)], 1, shift=2)
    # make it a solid silhouette: close pixel gaps between thin quads, then fill enclosed holes
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    ff = m.copy(); cv2.floodFill(ff, np.zeros((H + 2, W + 2), np.uint8), (0, 0), 2)
    return (ff != 2).astype(np.uint8)


def cost(cam, detail=False):
    m = render(cam)
    edge = cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    if edge.sum() == 0:
        return 1e6
    dt_m = cv2.distanceTransform(1 - edge, cv2.DIST_L2, 3)
    edge[ROW_CUT:] = 0                                     # score the shade only (base is approximate)
    d1 = DT_IMG[edge > 0]; d2 = dt_m[:ROW_CUT][IMG_EDGE[:ROW_CUT] > 0]
    c = 0.5 * (d1.mean() + d2.mean())
    if detail:
        inter = (m & IMG_MASK).sum(); union = (m | IMG_MASK).sum()
        return c, inter / union, m, d1, d2
    return c


def fit_camera(perspective=True):
    best = None
    for mir in (1, -1):
        for az in range(0, 90, 6):
            for el in (12, 17, 22):
                cam0 = [az, el, 2.5, 345.5, 533.0, 0.0]
                f = lambda p: cost(list(p) + [mir])
                c = f(cam0)
                if best is None or c < best[0]:
                    best = (c, cam0, mir)
    c, cam0, mir = best
    print(f"coarse: az {cam0[0]} el {cam0[1]} mirror {mir}  outline dist {c:.2f} px")
    # orthographic first (invD fixed 0), then optionally free perspective
    f5 = lambda p: cost(list(p) + [0.0, mir])
    r = minimize(f5, cam0[:5], method='Nelder-Mead', options={'xatol': 0.005, 'fatol': 0.0005, 'maxiter': 3000})
    r = minimize(f5, r.x, method='Nelder-Mead', options={'xatol': 0.005, 'fatol': 0.0005, 'maxiter': 3000})
    cam = list(r.x) + [0.0, mir]
    if perspective:
        sc = np.array([1, 1, 0.01, 1, 1, 1e-4])            # scale the simplex: invD ~ 1e-3
        f6 = lambda q: cost(list(q * sc) + [mir])
        r = minimize(f6, np.array(cam[:6]) / sc + np.r_[0, 0, 0, 0, 0, 2.0], method='Nelder-Mead',
                     options={'xatol': 0.005, 'fatol': 0.0005, 'maxiter': 4000})
        r = minimize(f6, r.x, method='Nelder-Mead', options={'xatol': 0.005, 'fatol': 0.0005, 'maxiter': 4000})
        cam_p = list(r.x * sc) + [mir]
        if cost(cam_p) < cost(cam):
            cam = cam_p
    return cam


def report(cam, tag):
    c, iou, m, d1, d2 = cost(cam, detail=True)
    s = cam[2]
    dist = f"{1/cam[5]:.0f} mm" if cam[5] > 1e-6 else "orthographic"
    print(f"[{tag}] az {cam[0]:.2f}  el {cam[1]:.2f}  scale {s:.4f} px/mm  centre ({cam[3]:.1f},{cam[4]:.1f})  camera {dist}  mirror {cam[6]}")
    print(f"   outline distance mean {c:.2f} px = {c/s:.2f} mm, 95% {np.percentile(np.r_[d1,d2],95)/s:.2f} mm, "
          f"max {max(d1.max(), d2.max())/s:.2f} mm, IoU {iou:.4f}")
    # per-row outline error (left / right edge), every 25 px
    print("   row   drawing L/R    model L/R    error L/R (mm)")
    for y in range(40, ROW_CUT, 25):
        a = np.nonzero(IMG_MASK[y])[0]; b = np.nonzero(m[y])[0]
        if len(a) and len(b):
            print(f"   {y:4d}  {a.min():4d} {a.max():4d}   {b.min():4d} {b.max():4d}   {(a.min()-b.min())/s:+5.2f} {(b.max()-a.max())/s:+5.2f}")
    vis = cv2.cvtColor(GRAY, cv2.COLOR_GRAY2BGR)
    vis = (vis * 0.55 + 255 * 0.45).astype(np.uint8)
    edge = cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    vis[edge > 0] = (0, 0, 230)
    cv2.imwrite(os.path.join(OUT, f'overlay_{tag}.png'), vis)
    return c, iou


if __name__ == '__main__':
    cam = fit_camera()
    c, iou = report(cam, 'camera_only')
    json.dump({'camera': [float(v) for v in cam], 'outline_mean_px': float(c), 'iou': float(iou)}, open(os.path.join(OUT, 'camera.json'), 'w'), indent=1)
