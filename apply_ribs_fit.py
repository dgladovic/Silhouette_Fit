"""
Write the checkpoint fit (fit_ribs_result.json) into all scripts:
  Grasshoper_full, Grasshoper_TwoTriangles : profile, twist, lobe depth curve (shape_ratio_at)
  LampWall/lamp_wall.py                     : same twist + lobe depth, profile refitted for the 1.5 mm pleats
Also writes fit_result.txt + lobe_depth.json so the check scripts (expected_triangles, render_folds, ...) use it.
Run: python apply_ribs_fit.py
"""
import os, re, json
import numpy as np
from scipy.optimize import least_squares
import model as m
import checkpoints as cp

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, 'fit_ribs_result.json')))
prof = [tuple(p) for p in d['BEZIER_CONTROL_POINTS']]
tw = [tuple(p) for p in d['twist_points']]
KZ, KV = d['LOBE_DEPTH_Z'], d['LOBE_DEPTH_K']
json.dump({'z': KZ, 'k': KV}, open(os.path.join(HERE, 'lobe_depth.json'), 'w'))
m.K_OF_Z = m.catmull_rom(KZ, KV)
fn = lambda t: m.twist_deg(tw, t)

prof_txt = "BEZIER_CONTROL_POINTS = [\n" + "\n".join(f"    ({r:.2f}, {z:.2f}),  # P{i}" for i, (r, z) in enumerate(prof)) + "\n]"
tw_lines = "\n".join(f"        [{t:.4f}, {a:.2f}]," for t, a in tw)
lobe_block = (
    "# --- LOBE DEPTH (shape_ratio) BY HEIGHT - from fit_ribs.py (10 mm checkpoint fit) ---\n"
    f"LOBE_DEPTH_Z = {[round(z, 1) for z in KZ]}   # mm\n"
    f"LOBE_DEPTH_K = {[round(k, 4) for k in KV]}\n\n"
    "def shape_ratio_at(z_mm, max_height=190.0):\n"
    "    zs, vs = LOBE_DEPTH_Z, LOBE_DEPTH_K\n"
    "    if z_mm <= zs[0]: return vs[0]\n"
    "    if z_mm >= zs[-1]: return vs[-1]\n"
    "    i = max(j for j in range(len(zs) - 1) if zs[j] <= z_mm)\n"
    "    t = (z_mm - zs[i]) / (zs[i + 1] - zs[i])\n"
    "    p0 = vs[max(i - 1, 0)]; p1 = vs[i]; p2 = vs[i + 1]; p3 = vs[min(i + 2, len(vs) - 1)]\n"
    "    return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t\n"
    "                  + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)\n"
    "# --- END LOBE DEPTH ---\n\n")


def patch_triangle_script(path):
    code = open(path, encoding='utf-8').read()
    code = re.sub(r"\nBEZIER_CONTROL_POINTS = \[.*?\n\]", lambda _: "\n" + prof_txt, code, count=1, flags=re.S)
    code = re.sub(r"twist_points = \[.*?\n    \]", lambda _: "twist_points = [\n" + tw_lines + "\n    ]", code, count=1, flags=re.S)
    code = re.sub(r"# --- LOBE DEPTH.*?# --- END LOBE DEPTH ---\n\n", lambda _: lobe_block, code, count=1, flags=re.S)
    assert "LOBE_DEPTH_K = " in code and "shape_ratio = shape_ratio_at(z_cm)" in code and "calculate_bezier_twist2(z_cm" in code
    open(path, 'w', encoding='utf-8').write(code)


for p in ('Grasshoper_full/Grasshoper_full.py', 'Grasshoper_TwoTriangles/Grasshoper_TwoTriangles.py'):
    patch_triangle_script(os.path.join(HERE, p))

# fit_result.txt for the check scripts (read_fit format)
full = m.silhouettes(prof, fn, cp.CHECK_Z)[0]
open(os.path.join(HERE, 'fit_result.txt'), 'w', encoding='utf-8').write(
    "From fit_ribs.py (checkpoint fit)\n\n" + prof_txt.replace("),  # P", "),  # P") + "\n\ntwist_points = [\n" +
    "\n".join(f"    [{t:.4f}, {a:.2f}]," for t, a in tw) + "\n]\n")

# ---------------- LampWall: same twist + lobe depth, refit only the profile for the pleated wall
lw_path = os.path.join(HERE, 'LampWall', 'lamp_wall.py')
lw = open(lw_path, encoding='utf-8').read()
m.GEOMETRY = 'wall'
m.WALL_RIBS_PER_QUARTER = int(re.search(r"RIBS_PER_QUARTER = (\d+)", lw).group(1))
m.WALL_RIB_HEIGHT = float(re.search(r"RIB_HEIGHT = ([\d.]+)", lw).group(1))
Z = np.arange(0.0, 190.01, 2.0); S = cp.S_OF_Z(Z)


def unpack(x):
    pts = [(x[0], 0.0)] + [(x[1 + 2 * i], x[2 + 2 * i]) for i in range(len(prof) - 2)] + [(x[-1], m.HEIGHT)]
    return pts


x0 = np.array([prof[0][0]] + [v for p in prof[1:-1] for v in p] + [prof[-1][0]])
res = lambda x: np.r_[m.silhouettes(unpack(x), fn, Z)[0] - S, 20 * np.minimum(np.diff([p[1] for p in unpack(x)]), 0),
                      0.05 * (x - x0)]                     # stay close to the triangle-fit profile
r = least_squares(res, x0, x_scale='jac', diff_step=1e-4, max_nfev=300)
wprof = unpack(r.x)
werr = m.silhouettes(wprof, fn, Z)[0] - S
lw = re.sub(r"PROFILE_POINTS = \[.*?\n\]", lambda _: "PROFILE_POINTS = [            # (radius mm, height mm) - wall fit\n    " +
            ", ".join(f"({a:.2f}, {b:.2f})" for a, b in wprof) + ",\n]", lw, count=1, flags=re.S)
lw = re.sub(r"TWIST_POINTS = \[.*?\n\]", lambda _: "TWIST_POINTS = [              # (height fraction, degrees)\n    " +
            ", ".join(f"({a:.4f}, {b:.2f})" for a, b in tw) + ",\n]", lw, count=1, flags=re.S)
lw = re.sub(r"LOBE_DEPTH = [^\n]*", "LOBE_DEPTH = [" + ", ".join(f"({a:.1f}, {b:.4f})" for a, b in zip(KZ, KV)) +
            "]  # (z mm, k): lobe depth curve", lw, count=1)
open(lw_path, 'w', encoding='utf-8').write(lw)
print(f"scripts updated; wall outline RMS {np.sqrt(np.mean(werr**2)):.2f} mm, max {np.abs(werr).max():.2f} mm")
