"""
Render the fitted model in front view with hidden surfaces removed and draw its fold lines
(depth jumps = where one lobe passes behind another) on top of the canvas.
Compares the model's real fold lines with the dark fold lines of the drawing.

Run after fit.py:  python render_folds.py
Output: folds_overlay.png
"""
import os, re, ast
import numpy as np
import cv2
import model as m
import measure_canvas as mc

HERE = os.path.dirname(os.path.abspath(__file__))


def read_fit(folder=None):
    txt = open(os.path.join(folder or HERE, 'fit_result.txt'), encoding='utf-8').read()
    pblock = re.search(r"BEZIER_CONTROL_POINTS = \[(.*?)\n\]", txt, re.S).group(1)
    tblock = re.search(r"twist_points = \[(.*?)\n\]", txt, re.S).group(1)
    prof = [tuple(map(float, p)) for p in re.findall(r"\(([-\d.]+), ([-\d.]+)\)", pblock)]
    tw = [tuple(map(float, p)) for p in re.findall(r"\[([-\d.]+), ([-\d.]+)\]", tblock)]
    return prof, tw


def depth_render(prof, tw, offset_deg=0.0):
    img = cv2.imread(mc.IMG, 0)
    H, W = img.shape
    depth = np.full((H, W), np.inf, np.float32)
    theta_id = np.full((H, W), np.nan, np.float32)
    zz = np.linspace(0, m.HEIGHT, 1300)
    r0 = m.profile_r(prof, zz)
    rot = m.twist_deg(tw, zz / m.HEIGHT) + offset_deg
    th = np.radians(np.linspace(0, 360, 6000, endpoint=False))
    for z, r, a in zip(zz, r0, rot):
        rho = m.rho_fn(th, m.section_at(z))      # lobe depth at this height
        w = th + np.radians(a)
        x = r * rho * np.cos(w); y = r * rho * np.sin(w)
        col = np.round(mc.COL0 + x / mc.SX).astype(int)
        row = int(round(float(mc.z_to_row(z))))
        for dr in (0, 1):                       # 2-pixel tall stripes to avoid gaps
            rr = row + dr
            if 0 <= rr < H:
                ok = (col >= 0) & (col < W)
                c, d, t = col[ok], y[ok], np.degrees(th[ok])
                order = np.argsort(-d)          # far first, near last -> near wins
                depth[rr, c[order]] = d[order]
                theta_id[rr, c[order]] = t[order]
    return img, depth, theta_id


def main(offset_deg=0.0, out='folds_overlay.png'):
    prof, tw = read_fit()
    img, depth, theta_id = depth_render(prof, tw, offset_deg)
    # fold lines: depth jump between neighbouring pixels
    d = np.where(np.isfinite(depth), depth, 1e3)
    jump = np.maximum(np.abs(np.diff(d, axis=1, prepend=d[:, :1])), np.abs(np.diff(d, axis=0, prepend=d[:1])))
    edges = (jump > 8) & np.isfinite(depth)
    edges = cv2.dilate(edges.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    # petal tips (local theta = 0, 90, 180, 270) that are visible
    tip = np.isfinite(theta_id) & (np.abs(((theta_id + 45) % 90) - 45) < 0.35)
    tip = cv2.dilate(tip.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0

    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    vis = (vis * 0.6 + 255 * 0.4).astype(np.uint8)
    vis[tip] = (0, 170, 0)
    vis[edges] = (0, 0, 230)
    cv2.putText(vis, "red = model fold lines (hidden-line render)   green = petal tips", (20, 1740),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (40, 40, 40), 2, cv2.LINE_AA)
    cv2.imwrite(os.path.join(HERE, out), vis)
    return vis


if __name__ == '__main__':
    import sys
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 0.0)
