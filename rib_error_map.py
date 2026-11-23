"""
Error map: direction of the model's ribs vs direction of the drawing's lines at EVERY visible pixel.
The model ribs follow fixed local angle θ0 while the section scales by r0(z) and rotates by twist(z):
    x(z) = r0(z) * rho(θ0) * cos(θ0 + rot(z))  ->  dx/dz = r0' rho cos φ - r0 rho sin φ * rot'
Output: rib_error_map.png (red = model ribs turn more clockwise than drawing, blue = less), and stats.
"""
import os, sys
import numpy as np
import cv2
import model as m
import measure_canvas as mc
from render_folds import read_fit

HERE = os.path.dirname(os.path.abspath(__file__))


def drawing_angle(img):
    f = img.astype(np.float32) / 255
    gx = cv2.Sobel(f, cv2.CV_32F, 1, 0, ksize=3); gy = cv2.Sobel(f, cv2.CV_32F, 0, 1, ksize=3)
    k = (31, 31)
    Jxx = cv2.GaussianBlur(gx * gx, k, 0); Jyy = cv2.GaussianBlur(gy * gy, k, 0); Jxy = cv2.GaussianBlur(gx * gy, k, 0)
    ang = 0.5 * np.arctan2(2 * Jxy, Jxx - Jyy) + np.pi / 2           # line direction in image coords
    coh = np.sqrt((Jxx - Jyy) ** 2 + 4 * Jxy ** 2) / (Jxx + Jyy + 1e-9)
    # convert to slope dx_mm/dz_mm (image row grows downward)
    slope = -np.cos(ang) / np.where(np.abs(np.sin(ang)) < 1e-3, 1e-3, np.sin(ang)) * mc.SX / mc.SZ
    return slope, coh


def model_slope_field(prof, tw, H, W, section=None):
    """Depth render: per pixel keep nearest surface point, store the analytic rib slope dx/dz there."""
    depth = np.full((H, W), np.inf, np.float32)
    slope = np.full((H, W), np.nan, np.float32)
    zz = np.linspace(0, m.HEIGHT, 1300)
    r0 = m.profile_r(prof, zz); rot = np.radians(m.twist_deg(tw, zz / m.HEIGHT))
    dr0 = np.gradient(r0, zz); drot = np.gradient(rot, zz)
    th = np.radians(np.linspace(0, 360, 4000, endpoint=False))

    def sec_xy(z):
        rho = m.rho_fn(th, m.section_at(z))      # model section at this height (constant or K_OF_Z)
        return rho * np.cos(th), rho * np.sin(th)

    for z, r, a, dr, da in zip(zz, r0, rot, dr0, drot):
        sx, sy = sec_xy(z)
        ca, sa = np.cos(a), np.sin(a)
        x = r * (sx * ca - sy * sa); y = r * (sx * sa + sy * ca)
        # d/dz of x = dr*(sx ca - sy sa) + r*(-sx sa - sy ca)*da  (+ change of section shape with z)
        dxdz = dr * (sx * ca - sy * sa) + r * (-sx * sa - sy * ca) * da
        if m.K_OF_Z:
            e = 0.25
            sx2, sy2 = sec_xy(min(z + e, m.HEIGHT)); sx1, sy1 = sec_xy(max(z - e, 0))
            dz = min(z + e, m.HEIGHT) - max(z - e, 0)
            dxdz = dxdz + r * ((sx2 - sx1) * ca - (sy2 - sy1) * sa) / dz
        col = np.round(mc.COL0 + x / mc.SX).astype(int)
        row = int(round(float(mc.z_to_row(z))))
        for dr_ in (0, 1):
            rr = row + dr_
            ok = (col >= 0) & (col < W)
            c, d, s = col[ok], y[ok], dxdz[ok]
            o = np.argsort(-d)
            depth[rr, c[o]] = d[o]; slope[rr, c[o]] = s[o]
    return slope, depth


def main(out='rib_error_map.png', section=None, label='rose k=0.2', fit_dir=None):
    prof, tw = read_fit(fit_dir)
    img = cv2.imread(mc.IMG, 0)
    H, W = img.shape
    ds, coh = drawing_angle(img)
    ms, depth = model_slope_field(prof, tw, H, W, section)
    # angle difference in degrees (in the projected mm frame)
    err = np.degrees(np.arctan(ms) - np.arctan(ds))
    valid = np.isfinite(err) & (coh > 0.6)
    # stay away from outline/folds where the drawing direction is ambiguous
    d = np.where(np.isfinite(depth), depth, 1e3)
    jump = np.maximum(np.abs(np.diff(d, axis=1, prepend=d[:, :1])), np.abs(np.diff(d, axis=0, prepend=d[:1])))
    near_fold = cv2.dilate(((jump > 8) | ~np.isfinite(depth)).astype(np.uint8), np.ones((25, 25), np.uint8)) > 0
    valid &= ~near_fold
    e = err[valid]
    print(f"[{label}] pixels {e.size}, mean |angle error| {np.mean(np.abs(e)):.2f} deg, RMS {np.sqrt(np.mean(e**2)):.2f} deg")
    zrow = mc.row_to_z(np.nonzero(valid)[0])
    global LAST_BANDS
    LAST_BANDS = {z0: (e[(zrow >= z0) & (zrow < z0 + 20)].mean(), np.abs(e[(zrow >= z0) & (zrow < z0 + 20)]).mean())
                  for z0 in (120, 140, 160, 180)}
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    vis = (vis * 0.35 + 255 * 0.65).astype(np.uint8)
    lim = 10.0
    t = np.clip(err / lim, -1, 1)
    red = np.zeros_like(vis); red[..., 2] = 255
    blue = np.zeros_like(vis); blue[..., 0] = 255
    a = np.abs(t)[..., None]
    col = np.where((t > 0)[..., None], red, blue)
    mix = vis * (1 - 0.8 * np.nan_to_num(a)) + col * 0.8 * np.nan_to_num(a)
    mix = np.nan_to_num(mix)
    vis[valid] = mix[valid].astype(np.uint8)
    cv2.putText(vis, f"{label}: rib direction error, red/blue = +/-10 deg, mean {np.mean(np.abs(e)):.1f} deg",
                (20, 1740), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 2, cv2.LINE_AA)
    cv2.imwrite(os.path.join(fit_dir or HERE, out), vis)
    return np.mean(np.abs(e))


if __name__ == '__main__':
    main()
