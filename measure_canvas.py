"""
Measure the canvas drawing in Fusion's own coordinates.

Calibration is taken from fusion_dump.txt (DumpCanvas script), canvas 'rel_size' (YZ plane):
  plane origin z = 60 mm, transform Matrix2D [-22.67524, 0, 11.33762 | 0, 26.008172, -13.004086] (cm)
  -> horizontal: 226.7524 mm over the image width, centred on the Z axis
  -> vertical:   260.08172 mm over the image height, image bottom at z = -70.04 mm
If you move/rescale the canvas in Fusion, re-run DumpCanvas and update the numbers below.

Writes silhouette_front.csv and rib_slope_center.csv (used by fit.py).
"""
import os
import numpy as np
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, 'reference', 'fusion_rel_size_YZ.jpg')

W_MM, H_MM = 226.7524, 260.08172       # canvas size in Fusion
PLANE_Z, V_OFF = 60.0, -130.04086      # plane origin z, transform v offset (mm)

im = cv2.imread(IMG, 0)
H_PX, W_PX = im.shape
SX = W_MM / W_PX                       # mm per pixel horizontally
SZ = H_MM / H_PX                       # mm per pixel vertically
COL0 = W_PX / 2 - 0.5                  # pixel column on the Z axis


def col_to_mm(c):
    return (np.asarray(c, float) - COL0) * SX


def row_to_z(r):
    return PLANE_Z + V_OFF + H_MM * (1 - (np.asarray(r, float) + 0.5) / H_PX)


def z_to_row(z):
    return (1 - (np.asarray(z, float) - PLANE_Z - V_OFF) / H_MM) * H_PX - 0.5


def main():
    dark = im < 128
    # shade = rows above the bottom rim line, below the top rim line
    rows = range(1, 1290)
    out = []
    for y in rows:
        xs = np.where(dark[y])[0]
        out.append((row_to_z(y), -col_to_mm(xs.min()), col_to_mm(xs.max())))
    out = np.array(out[::-1])
    np.savetxt(os.path.join(HERE, 'silhouette_front.csv'), out, delimiter=',',
               header='z_mm,left_mm,right_mm', fmt='%.3f', comments='')

    # rib direction along the axis column (structure tensor), converted to mm/mm
    f = im.astype(np.float32) / 255
    gx = cv2.Sobel(f, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(f, cv2.CV_32F, 0, 1, ksize=3)
    k = (41, 41)
    Jxx = cv2.GaussianBlur(gx * gx, k, 0); Jyy = cv2.GaussianBlur(gy * gy, k, 0); Jxy = cv2.GaussianBlur(gx * gy, k, 0)
    ang = 0.5 * np.arctan2(2 * Jxy, Jxx - Jyy)
    c = int(round(COL0 - 1))           # drawing axis column
    res = []
    for y in range(1288, 0, -1):
        L = ang[y, c - 20:c + 21].mean() + np.pi / 2
        slope_px = -np.cos(L) / np.sin(L)          # d(col)/d(-row)
        res.append((row_to_z(y), slope_px * SX / SZ))
    np.savetxt(os.path.join(HERE, 'rib_slope_center.csv'), np.array(res), delimiter=',',
               header='z_mm,dx_dz', fmt='%.4f', comments='')
    print(f"mm/px: horizontal {SX:.5f}, vertical {SZ:.5f}")
    print(f"shade bottom z={out[0,0]:.2f}  top z={out[-1,0]:.2f}")
    print(f"bottom half-width {out[0,1:].mean():.2f} mm, top {out[-1,1:].mean():.2f} mm, "
          f"max {out[:,1:].mean(1).max():.2f} mm, left/right offset {np.mean(out[:,2]-out[:,1]):+.2f} mm")


if __name__ == '__main__':
    main()
