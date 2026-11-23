"""
Where the Grasshoper_TwoTriangles bodies should appear on the canvas, per Fusion view.
Draws the apex path of the first and last triangle of every quadrant over the ORIGINAL
(un-mirrored) drawing.  Solid = on the camera side, thin = behind the canvas plane.

Front view: camera at -Y, screen right = +X.   Right view: camera at +X, screen right = +Y.
Output: expected_front_view.png, expected_right_view.png
"""
import os
import numpy as np
import cv2
import model as m
import measure_canvas as mc
from render_folds import read_fit

HERE = os.path.dirname(os.path.abspath(__file__))
COLORS = [(0, 160, 0), (0, 0, 220), (220, 120, 0), (180, 0, 180)]   # Q1..Q4 (BGR)


def main():
    prof, tw = read_fit()
    zz = np.linspace(0, m.HEIGHT, 400)
    r0 = m.profile_r(prof, zz)
    rot = m.twist_deg(tw, zz / m.HEIGHT)
    apex = {}   # (q, which) -> (N,2) world xy
    def apex_pts(z, r, a):
        m.set_section(m.section_at(z))          # lobe depth at this height
        return m.slice_points(r, a)[[0, -1], 6]  # apex of tri 0 and last

    for q in range(4):
        P = np.array([apex_pts(z, r, a + 90 * q) for z, r, a in zip(zz, r0, rot)])
        apex[(q, 'first')] = P[:, 0]
        apex[(q, 'last')] = P[:, 1]

    base = cv2.imread(mc.IMG)
    base = (base * 0.5 + 255 * 0.5).astype(np.uint8)
    to_px = lambda s_mm, z: (int(round(mc.COL0 + s_mm / mc.SX)), int(round(float(mc.z_to_row(z)))))
    for view in ('front', 'right'):
        img = base.copy()
        for (q, which), P in apex.items():
            if view == 'front':
                s, facing = P[:, 0], P[:, 1] < 0      # screen x = X, visible if in front of the y=0 canvas
            else:
                s, facing = P[:, 1], P[:, 0] > 0      # screen x = Y, visible if in front of the x=0 canvas
            col = COLORS[q]
            for i in range(len(zz) - 1):
                thick = 5 if (facing[i] and facing[i + 1]) else 1
                cv2.line(img, to_px(s[i], zz[i]), to_px(s[i + 1], zz[i + 1]), col, thick, cv2.LINE_AA)
            # label at the bottom end
            x0, y0 = to_px(s[0], zz[0])
            cv2.putText(img, f"Q{q+1}{'a' if which == 'first' else 'b'}", (x0 - 20, y0 + 30 + 28 * (which == 'last')),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, col, 2, cv2.LINE_AA)
        cv2.putText(img, f"{view.upper()} VIEW - a = first triangle, b = last triangle, thick = camera side",
                    (20, 1700), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (30, 30, 30), 2, cv2.LINE_AA)
        cv2.putText(img, "canvas shown UN-mirrored (as in the original drawing)", (20, 1740),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.85, (30, 30, 30), 2, cv2.LINE_AA)
        cv2.imwrite(os.path.join(HERE, f'expected_{view}_view.png'), img)


if __name__ == '__main__':
    main()
