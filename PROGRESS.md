# Silhouette Fit — progress notes

Goal: find the curve parameters for the generative lamp shade so the model generated in Fusion 360
matches the reference drawing (front + right view canvases) — outline **and** the twist of the ribs.

Shade height is 190 mm (the shade only, not the base). The lamp has 4-fold symmetry (4 lobes),
so the front and right views show the same outline.

---

## How the model works (same maths as the Fusion scripts)

At every height `z` (0–190 mm) the cross-section is a 4-petal rose, scaled and rotated:

```
r(θ)  = r0(z) · (1 + k(z)·cos 4θ) / (1 + k(z))      r0 = petal-tip radius, k = lobe depth (shape_ratio)
twist = twist(z / 190)                                 whole section rotated about Z
```

- `r0(z)` — Bezier `BEZIER_CONTROL_POINTS` (radius mm, height mm), evaluated by height.
- `twist(t)` — Bezier `twist_points` (height fraction, degrees), via `calculate_bezier_twist2`.
- `k(z)` — lobe depth curve `LOBE_DEPTH_Z / LOBE_DEPTH_K` (Catmull-Rom through 6 values), `shape_ratio_at(z)`.
- Ribs: triangles (Grasshoper_full: 22 per quarter, 9 mm wide, 3 mm tall) or a continuous pleated wall
  (LampWall: 45 ribs per quarter, 1.5 mm tall). Ribs keep their **arc-length** position inside their quarter.

`model.py` is a Python replica of this geometry. It has been checked against Fusion: the bodies sliced in
Fusion (DumpCanvas) match the Python outline within 0.05 mm, and Fusion's own `calculate_bezier_twist2`
and `shape_ratio_at` give the model's values within 0.01°.

---

## Current status (best result so far)

| Check | Result |
|---|---|
| Outline vs canvas (every 2 mm) | max 0.68 mm (triangles), 0.39 mm (LampWall) |
| Drawn ribs vs model ribs, every 10 mm (15 traced ribs, 190 checkpoints) | mean 0.78 mm, 74 % within 1 mm, worst 4.5 mm |
| Twist | 0° → 89.1° (close to the hand-tuned 87° in `FulLTextureLamp/prave vrednost bezier.txt`) |
| Lobe depth k(z) at z = 0/38/76/114/152/190 | 0.223 / 0.204 / 0.210 / 0.206 / 0.248 / 0.211 |

Full per-rib table: `checkpoints_report.txt`. Picture: `checkpoints.png` (green = drawn rib, red = model rib).

Not yet verified in Fusion with these exact values (last Fusion check was on an earlier fit).

---

## Scripts

| File | What it does |
|---|---|
| `Grasshoper_full/` | Fusion script: the quarter lamp with triangle ribs — **current fitted values** |
| `Grasshoper_TwoTriangles/` | Fusion debug script: only the first + last triangle of each of the 4 quarters |
| `LampWall/` | Fusion script + `lamp_wall.py`: continuous pleated wall → STL → inserted as mesh. Standalone: `python lamp_wall.py` |
| `DumpCanvas/` | Fusion script: writes `fusion_dump.txt` (canvas placement/scale + real body outline every 5 mm) |
| `model.py` | Python replica of the geometry (section, twist, lobe depth, triangles / wall) |
| `measure_canvas.py` | Canvas → mm calibration (from `fusion_dump.txt`), writes `silhouette_front.csv`, `rib_slope_center.csv` |
| `checkpoints.py` | Traces drawn ribs, prints the **10 mm checkpoint table** for the current fit |
| `fit_ribs.py` | Main fitter: profile + twist + lobe depth vs outline and traced ribs → `fit_ribs_result.json` |
| `apply_ribs_fit.py` | Writes `fit_ribs_result.json` into all three Fusion scripts (+ refits the LampWall profile) |
| `fit.py` | Older fitter: outline + centre-line rib slope only (`--wall`, `--section=`, `--ktop=`, `--out=`) |
| `expected_triangles.py` | Where the TwoTriangles bodies should land in front/right view |
| `render_folds.py`, `rib_error_map.py`, `trace_ribs.py` | Diagnostics: fold lines, rib-angle error map, single-rib traces |
| `section_experiment.py`, `ktop_experiment.py` | Experiments on the cross-section shape (results in `experiments/`) |

Typical loop:

```bash
python checkpoints.py        # evaluate current values every 10 mm
python fit_ribs.py           # fit again (continues from fit_ribs_result.json)
python apply_ribs_fit.py     # write the result into the Fusion scripts
python expected_triangles.py # images to compare with Fusion
```

---

## What was tried (in order) and what we learned

1. **Outline-only fit (constant k = 0.2).** Outline fitted to 0.1 mm, twist from the rib slope on the
   centre line. Outline was great, but outline alone cannot separate profile from twist from section shape.
2. **Front view of a single quarter is misleading.** The generated quarter turns away from the front
   camera; only the right view (or 4 quarters) shows the full outline.
3. **Canvas calibration.** The Fusion canvases were 226.75 × 260.08 mm — 2.2 % squeezed horizontally.
   Recalibrated from `fusion_dump.txt` (`measure_canvas.py`). The canvases are also mirrored left–right
   (negative scale) compared with the original drawing.
4. **Fold lines.** Hidden-line render of the model puts its folds on the drawing's folds within ~1 mm.
   A rib (or the first triangle) is *not* supposed to follow the outline or fold — it leaves the outline as
   the lobe twists (the drawing's own ribs do the same).
5. **Cross-section shape test** (`section_experiment.py`): rose k = 0.12 / 0.20 / 0.28 and "star nozzle"
   (union of 4 circles) d = 0.3 / 0.4 / 0.5. Rose k = 0.20 was best; star nozzle 2–4× worse.
6. **Lobe depth towards the rim** (`ktop_experiment.py`): 0.20 → 0.15 above 120 mm helped the top band.
7. **10 mm checkpoint fit** (`checkpoints.py`, `fit_ribs.py`): trace 15 drawn ribs from the bottom rim,
   require the model rib from the same start to stay on it. Fitting profile + twist + 6-point lobe depth
   together: rib error 2.68 mm → 0.78 mm, within-1 mm 18 % → 74 %.
   Fixes along the way: tracer limited to 2 px/row (no line hopping), model rib starts exactly at the
   traced start point, twist control-point t kept in 0..1 (Fusion's lookup needs that).

## Open issues / what to try next

- **Remaining rib errors of 2–3 mm** around z = 70–130 mm on the ribs starting at x0 ≈ −71, 0, +20 mm,
  while neighbours are within 1 mm. Either the drawing is not exact there (it is an illustration) or the
  model misses something. Ideas:
  - rib spacing not uniform in arc length (e.g. equal angle, or denser near the creases);
  - section not exactly a rose: try `r = 1 + a·cos4θ + b·cos8θ` (one extra harmonic) fitted with the ribs;
  - more lobe-depth nodes (8–10) or a 7-point twist (tried once: tiny gain).
- **Second view (3/4 perspective drawing `reference/view34_drawing.png`)** — independent check of the
  model from another angle (see section below).
- **Verify in Fusion** with `Grasshoper_TwoTriangles` and the original drawing as canvas (not re-scaled).
  If the canvas is re-imported or re-scaled, run DumpCanvas and update `measure_canvas.py` first.
- The FulLTextureLamp script used the S-curve twist (`k1 = 0, k2 = 0.8`) on the *profile Bezier parameter*
  instead of the height; its hand-tuned angles agree with the fitted twist within ~2° at every 10 %.
