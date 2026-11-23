"""
Fit BEZIER_CONTROL_POINTS (profile) and twist_points (twist) so the generated lamp
matches the canvas silhouette (reference/1.jpg) and the rib direction on the canvas.

Run:  python fit.py [n_profile_points] [n_twist_points]
Outputs (in this folder):
  fit_result.txt           - the values to paste + error table
  overlay_front.png        - model drawn over the canvas
  error_plot.png           - silhouette / twist / rib-slope curves
  Grasshoper_full/         - ready Fusion script with the fitted values
"""
import sys, os, re, shutil
import numpy as np
from scipy.optimize import least_squares
import cv2
import model as m

HERE = os.path.dirname(os.path.abspath(__file__))
WALL = '--wall' in sys.argv          # fit the LampWall continuous pleated wall instead of the triangle wedges
_nums = [a for a in sys.argv[1:] if not a.startswith('--')]
N_PROF = int(_nums[0]) if len(_nums) > 0 else 8
N_TW = int(_nums[1]) if len(_nums) > 1 else 5
OUT = os.path.join(HERE, 'LampWall', 'fit') if WALL else HERE
_opts = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)
EXPERIMENT = 'out' in _opts          # --out=folder : write results there only, don't touch the Fusion scripts
if EXPERIMENT:
    OUT = os.path.join(HERE, _opts['out'])
if 'section' in _opts:               # --section=rose:0.2  or  --section=circles:0.5  (constant section)
    kind, p = _opts['section'].split(':')
    m.set_section((kind, float(p)))
    m.K_OF_Z = None
if 'ktop' in _opts:                  # --ktop=0.15 [--kfrom=120] [--kbase=0.2] : lobe depth changes towards the rim
    m.LOBE_DEPTH = (float(_opts.get('kbase', 0.2)), float(_opts['ktop']), float(_opts.get('kfrom', 120)))
    m.K_OF_Z = m.k_top_blend(*m.LOBE_DEPTH)
LOBE = m.LOBE_DEPTH if m.K_OF_Z else (m.SECTION[1], m.SECTION[1], m.HEIGHT)   # what the scripts get
if WALL:
    m.GEOMETRY = 'wall'
    # use the rib settings currently in lamp_wall.py (edit them there, then refit)
    _lw = open(os.path.join(HERE, 'LampWall', 'lamp_wall.py'), encoding='utf-8').read()
    m.WALL_RIBS_PER_QUARTER = int(re.search(r"RIBS_PER_QUARTER = (\d+)", _lw).group(1))
    m.WALL_RIB_HEIGHT = float(re.search(r"RIB_HEIGHT = ([\d.]+)", _lw).group(1))
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------ canvas data
import measure_canvas as mc                     # Fusion canvas calibration (from fusion_dump.txt)
CANVAS = mc.IMG

sil = np.loadtxt(os.path.join(HERE, 'silhouette_front.csv'), delimiter=',', skiprows=1)
rib = np.loadtxt(os.path.join(HERE, 'rib_slope_center.csv'), delimiter=',', skiprows=1)
Z = np.arange(0.0, m.HEIGHT + 0.01, 2.0)
S_target = np.interp(Z, sil[:, 0], (sil[:, 1] + sil[:, 2]) / 2)
Zr = Z[(Z > 4) & (Z < m.HEIGHT - 4)]
slope_target = np.interp(Zr, rib[:, 0], rib[:, 1])
W_SLOPE = 25.0   # 0.04 slope error ~ 1 mm

# ------------------------------------------------------------ parameterisation
def unpack(x):
    # profile: P0=(r,0), interior (r,z) sorted by z, Plast=(r,190)
    k = 0
    prof = [(x[k], 0.0)]; k += 1
    inner = []
    for _ in range(N_PROF - 2):
        inner.append((x[k], x[k + 1])); k += 2
    prof += inner
    prof.append((x[k], m.HEIGHT)); k += 1
    # twist: (0,0), interior (t,deg), (1, end)
    tw = [(0.0, 0.0)]
    for _ in range(N_TW - 2):
        tw.append((x[k], x[k + 1])); k += 2
    tw.append((1.0, x[k])); k += 1
    return prof, tw


def residuals(x):
    prof, tw = unpack(x)
    fn = lambda t: m.twist_deg(tw, t)
    full, _, _, _, _ = m.silhouettes(prof, fn, Z)
    slope = m.center_rib_slope(prof, fn, Zr)
    res = [full - S_target, W_SLOPE * (slope - slope_target)]
    # keep control points ordered (z for profile, t for twist) so the curves stay single valued
    zs = [p[1] for p in prof]; ts = [p[0] for p in tw]
    res.append(20 * np.minimum(np.diff(zs), 0))
    res.append(200 * np.minimum(np.diff(ts), 0))
    return np.concatenate(res)


def initial_guess():
    x = [82.0]
    zin = np.linspace(0, m.HEIGHT, N_PROF)[1:-1]
    rin = 80 + 40 * np.sin(np.pi * zin / 190 * 0.85)
    for r, z in zip(rin, zin):
        x += [r, z]
    x += [43.0]
    for t in np.linspace(0, 1, N_TW)[1:-1]:
        x += [t, 90 * (3 * t * t - 2 * t ** 3)]
    x += [90.0]
    return np.array(x)


def fusion_list(name, pts, fmt):
    lines = [f"{name} = ["]
    for i, p in enumerate(pts):
        lines.append(f"    ({fmt.format(*p)}),  # P{i}")
    lines.append("]")
    return "\n".join(lines)


def main():
    x0 = initial_guess()
    best = None
    for attempt in range(3):
        start = x0 if best is None else best.x + np.random.default_rng(attempt).normal(0, 1.0, len(x0)) * 0.5
        r = least_squares(residuals, start, x_scale='jac', max_nfev=4000)
        if best is None or r.cost < best.cost:
            best = r
    prof, tw = unpack(best.x)
    fn = lambda t: m.twist_deg(tw, t)

    full, qf, qr, r0, rot = m.silhouettes(prof, fn, Z)
    slope = m.center_rib_slope(prof, fn, Zr)
    err = full - S_target
    # check with the actual 15 Fusion sections (loft = smooth interpolation between them)
    zs = m.section_heights()
    sec = m.silhouettes(prof, fn, zs)[0]
    sec_err = sec - np.interp(zs, Z, S_target)

    # --------------------------------------------------- text report
    prof_txt = fusion_list("BEZIER_CONTROL_POINTS", prof, "{:.1f}, {:.1f}")
    tw_txt = "twist_points = [\n" + "\n".join(f"    [{t:.3f}, {a:.1f}]," for t, a in tw) + "\n]"
    rep = [f"Profile points: {N_PROF}, twist points: {N_TW}",
           f"Silhouette error: RMS {np.sqrt(np.mean(err**2)):.2f} mm, max {np.abs(err).max():.2f} mm",
           f"At the 15 Fusion sections: max {np.abs(sec_err).max():.2f} mm",
           f"Rib slope RMS error: {np.sqrt(np.mean((slope-slope_target)**2)):.3f}",
           f"Twist at top: {tw[-1][1]:.1f} deg",
           f"Lobe depth (shape_ratio): {LOBE[0]:.2f} below {LOBE[2]:.0f} mm -> {LOBE[1]:.2f} at the rim",
           "", prof_txt, "", tw_txt, "",
           "   z  canvas  model  error   r0    twist  quarterFront quarterRight"]
    for i in range(0, len(Z), 5):
        rep.append(f"{Z[i]:5.0f} {S_target[i]:6.1f} {full[i]:6.1f} {err[i]:+6.2f} {r0[i]:6.1f} {rot[i]:6.1f} {qf[i]:8.1f} {qr[i]:10.1f}")
    rep_s = "\n".join(rep)
    open(os.path.join(OUT, 'fit_result.txt'), 'w', encoding='utf-8').write(rep_s)
    print(rep_s)

    # --------------------------------------------------- overlay on canvas
    img = cv2.imread(CANVAS)
    img = (img * 0.55 + 255 * 0.45).astype(np.uint8)     # fade canvas
    to_px = lambda x_mm, z_mm: (int(round(mc.COL0 + x_mm / mc.SX)), int(round(float(mc.z_to_row(z_mm)))))
    for sgn in (1, -1):
        pts = np.array([to_px(sgn * f, z) for f, z in zip(full, Z)], np.int32)
        cv2.polylines(img, [pts], False, (0, 0, 230), 3, cv2.LINE_AA)
    # front-facing ribs of the model (world angle in (-180, 0) = facing the front camera)
    zz = np.linspace(0, m.HEIGHT, 200)
    rr, aa = m.profile_r(prof, zz), fn(zz / m.HEIGHT)
    for k in range(0, 360, 6):
        th = np.radians(k)
        rho = (1 + m.SHAPE_RATIO * np.cos(4 * th)) / (1 + m.SHAPE_RATIO)
        w = th + np.radians(aa)
        x, y = rr * rho * np.cos(w), rr * rho * np.sin(w)
        vis = y < 0
        col = (0, 160, 0) if k % 90 == 0 else (200, 120, 0)
        thick = 4 if k % 90 == 0 else 1
        for i in range(len(zz) - 1):
            if vis[i] and vis[i + 1]:
                cv2.line(img, to_px(x[i], zz[i]), to_px(x[i + 1], zz[i + 1]), col, thick, cv2.LINE_AA)
    for zsec in zs:
        cv2.line(img, to_px(-130, zsec), to_px(-118, zsec), (120, 120, 120), 2)
    cv2.putText(img, "red = model silhouette   green = first triangle (petal tip)   blue = ribs", (20, 1740),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (40, 40, 40), 2, cv2.LINE_AA)
    cv2.imwrite(os.path.join(OUT, 'overlay_front.png'), img)

    # --------------------------------------------------- plots
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(15, 6))
    ax[0].plot(S_target, Z, 'k', lw=2, label='canvas'); ax[0].plot(full, Z, 'r--', label='model (full lamp)')
    ax[0].plot(qr, Z, 'b:', label='quarter, right view'); ax[0].plot(qf, Z, 'g:', label='quarter, front view')
    ax[0].plot(r0, Z, color='0.6', label='r0 (petal tip)')
    ax[0].plot([p[0] for p in prof], [p[1] for p in prof], 'x-', color='0.7', lw=0.8, label='control cage')
    ax[0].set_xlabel('radius mm'); ax[0].set_ylabel('z mm'); ax[0].legend(fontsize=8); ax[0].set_title('Silhouette')
    ax[0].grid(alpha=.3); ax[0].set_aspect('equal')
    ax[1].plot(rot, Z, 'r'); ax[1].plot([a for t, a in tw], [t * m.HEIGHT for t, a in tw], 'x:', color='0.6')
    ax[1].set_xlabel('twist deg'); ax[1].set_title('Twist'); ax[1].grid(alpha=.3)
    ax[2].plot(slope_target, Zr, 'k', label='canvas'); ax[2].plot(slope, Zr, 'r--', label='model')
    ax[2].set_xlabel('rib dx/dz at centre'); ax[2].set_title('Rib direction'); ax[2].legend(); ax[2].grid(alpha=.3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'error_plot.png'), dpi=110)

    if EXPERIMENT:
        return
    if WALL:   # write the fitted curves into LampWall/lamp_wall.py
        path = os.path.join(HERE, 'LampWall', 'lamp_wall.py')
        code = open(path, encoding='utf-8').read()
        p_txt = "PROFILE_POINTS = [            # (radius mm, height mm) - from fit.py --wall\n    " + \
                ", ".join(f"({r:.1f}, {z:.1f})" for r, z in prof) + ",\n]"
        t_txt = "TWIST_POINTS = [              # (height fraction, degrees)\n    " + \
                ", ".join(f"({t:.3f}, {a:.1f})" for t, a in tw) + ",\n]"
        code = re.sub(r"PROFILE_POINTS = \[.*?\n\]", lambda _: p_txt, code, count=1, flags=re.S)
        code = re.sub(r"TWIST_POINTS = \[.*?\n\]", lambda _: t_txt, code, count=1, flags=re.S)
        code = re.sub(r"RIBS_PER_QUARTER = \d+", f"RIBS_PER_QUARTER = {m.WALL_RIBS_PER_QUARTER}", code, count=1)
        code = re.sub(r"RIB_HEIGHT = [\d.]+", f"RIB_HEIGHT = {m.WALL_RIB_HEIGHT}", code, count=1)
        code = re.sub(r"LOBE_DEPTH = \([^)]*\)", f"LOBE_DEPTH = ({LOBE[0]}, {LOBE[1]}, {LOBE[2]})", code, count=1)
        assert f"LOBE_DEPTH = ({LOBE[0]}" in code
        open(path, 'w', encoding='utf-8').write(code)
        return

    # --------------------------------------------------- Fusion scripts (triangle versions)
    lobe_block = (
        "# --- LOBE DEPTH (shape_ratio) BY HEIGHT - from fit.py ---\n"
        f"LOBE_DEPTH_BASE = {LOBE[0]}   # below LOBE_DEPTH_FROM\n"
        f"LOBE_DEPTH_TOP = {LOBE[1]}    # at the top rim\n"
        f"LOBE_DEPTH_FROM = {LOBE[2]}   # mm, where the change starts (smooth step to the rim)\n\n"
        "def shape_ratio_at(z_mm, max_height=190.0):\n"
        "    t = min(max((z_mm - LOBE_DEPTH_FROM) / (max_height - LOBE_DEPTH_FROM), 0.0), 1.0)\n"
        "    return LOBE_DEPTH_BASE + (LOBE_DEPTH_TOP - LOBE_DEPTH_BASE) * t * t * (3 - 2 * t)\n"
        "# --- END LOBE DEPTH ---\n\n")

    def patch(code):
        code = re.sub(r"\nBEZIER_CONTROL_POINTS = \[.*?\n\]", lambda _: "\n" + prof_txt, code, count=1, flags=re.S)
        code = re.sub(r"twist_points = \[.*?\n    \]",
                      lambda _: "twist_points = [\n" + "\n".join(f"        [{t:.3f}, {a:.1f}]," for t, a in tw) + "\n    ]",
                      code, count=1, flags=re.S)
        code = code.replace("rot = calculate_bezier_twist(z_cm / max_height_cm)",
                            "rot = calculate_bezier_twist2(z_cm / max_height_cm)  # fitted twist (fit.py)")
        if "# --- LOBE DEPTH" in code:
            code = re.sub(r"# --- LOBE DEPTH.*?# --- END LOBE DEPTH ---\n\n", lambda _: lobe_block, code, count=1, flags=re.S)
        else:
            code = code.replace("\nBEZIER_CONTROL_POINTS = [", "\n" + lobe_block + "BEZIER_CONTROL_POINTS = [", 1)
        if "shape_ratio = shape_ratio_at(z_cm)" not in code:
            code = re.sub(r"\n(\s*)(current_a = [^\n]*\(1\.0 \+ shape_ratio\))",
                          lambda mm: f"\n{mm.group(1)}shape_ratio = shape_ratio_at(z_cm)  # lobe depth at this height\n"
                                     f"{mm.group(1)}{mm.group(2)}", code, count=1)
        assert "calculate_bezier_twist2(z_cm" in code and "shape_ratio = shape_ratio_at(z_cm)" in code
        return code

    src = os.path.join(os.path.dirname(HERE), 'Grasshoper_full')
    dst = os.path.join(HERE, 'Grasshoper_full')
    os.makedirs(dst, exist_ok=True)
    for f in ('ClosedProfile.py', 'ScriptIcon.svg', 'Grasshoper_full.manifest'):
        shutil.copy(os.path.join(src, f), dst)
    code = patch(open(os.path.join(src, 'Grasshoper_full.py'), encoding='utf-8').read())
    open(os.path.join(dst, 'Grasshoper_full.py'), 'w', encoding='utf-8').write(code)
    two = os.path.join(HERE, 'Grasshoper_TwoTriangles', 'Grasshoper_TwoTriangles.py')
    if os.path.exists(two):
        code = patch(open(two, encoding='utf-8').read())
        open(two, 'w', encoding='utf-8').write(code)


if __name__ == '__main__':
    main()
