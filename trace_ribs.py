"""
Follow single rib lines of the DRAWING upward from a start point at the bottom rim, and compare
them with the model's triangle paths (front view, the camera-side copies Q3a and Q4a).

Tracing: step one row up at a time, predict x with the local line direction (structure tensor),
then snap to the centre of the nearest dark line within a few pixels.
Output: trace_ribs.png  + printed deviation table (mm)
"""
import os
import numpy as np
import cv2
import model as m
import measure_canvas as mc
from render_folds import read_fit

HERE = os.path.dirname(os.path.abspath(__file__))
img = cv2.imread(mc.IMG, 0)
f = img.astype(np.float32) / 255
gx = cv2.Sobel(f, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(f, cv2.CV_32F, 0, 1, ksize=3)
k = (15, 15)
Jxx = cv2.GaussianBlur(gx * gx, k, 0); Jyy = cv2.GaussianBlur(gy * gy, k, 0); Jxy = cv2.GaussianBlur(gx * gy, k, 0)
ANG = 0.5 * np.arctan2(2 * Jxy, Jxx - Jyy) + np.pi / 2          # line direction
DARK = cv2.GaussianBlur(255 - img, (5, 1), 0).astype(float)


def trace(x_start, row_start, row_end, snap=3):
    x = float(x_start); pts = []
    for row in range(row_start, row_end, -1):
        xi = int(round(x))
        if xi < 2 or xi >= img.shape[1] - 2:
            break
        a = ANG[row, xi]
        dxdrow = np.cos(a) / np.sin(a) if abs(np.sin(a)) > 0.15 else 0.0   # x change per row DOWN
        x_pred = x - dxdrow                                             # moving one row up
        lo, hi = int(round(x_pred)) - snap, int(round(x_pred)) + snap + 1
        win = DARK[row - 1, max(lo, 0):hi]
        if win.max() > 60:
            c = np.argmax(win) + max(lo, 0)
            x = 0.5 * x_pred + 0.5 * c
        else:
            x = x_pred
        pts.append((x, row - 1))
    return np.array(pts)


def main():
    prof, tw = read_fit()
    zz = np.linspace(0, m.HEIGHT, 600)
    r0 = m.profile_r(prof, zz); rot = m.twist_deg(tw, zz / m.HEIGHT)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    vis = (vis * 0.5 + 255 * 0.5).astype(np.uint8)
    rows = []
    for q, name, col in ((2, 'Q3a (left edge start)', (220, 120, 0)), (3, 'Q4a (centre start)', (180, 0, 180))):
        P = np.array([m.slice_points(r, a + 90 * q)[0, 6] for r, a in zip(r0, rot)])
        xm = mc.COL0 + P[:, 0] / mc.SX
        rm = mc.z_to_row(zz)
        facing = P[:, 1] < 0
        # trace the drawn rib starting where the model triangle starts (a few rows above the rim)
        i0 = np.argmin(abs(zz - 3))
        T = trace(xm[i0], int(round(rm[i0])), 5)
        for i in range(len(zz) - 1):
            if facing[i]:
                cv2.line(vis, (int(xm[i]), int(rm[i])), (int(xm[i + 1]), int(rm[i + 1])), col, 4, cv2.LINE_AA)
        cv2.polylines(vis, [T.astype(np.int32)], False, (0, 170, 0), 2, cv2.LINE_AA)
        # deviation in mm along height
        zt = mc.row_to_z(T[:, 1])
        xt = (T[:, 0] - mc.COL0) * mc.SX
        print(f"\n{name}: model path vs traced drawing rib (front view)")
        print("   z   model_x  drawn_x   diff_mm  model on camera side")
        for zq in range(5, 190, 15):
            j = np.argmin(abs(zt - zq)); i = np.argmin(abs(zz - zq))
            if abs(zt[j] - zq) < 2:
                print(f"{zq:5d} {P[i,0]:8.1f} {xt[j]:8.1f} {xt[j]-P[i,0]:+8.1f}   {facing[i]}")
    cv2.putText(vis, "thick = model first triangle (camera side)   green = traced drawing rib from same start",
                (20, 1740), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 2, cv2.LINE_AA)
    cv2.imwrite(os.path.join(HERE, 'trace_ribs.png'), vis)


if __name__ == '__main__':
    main()
