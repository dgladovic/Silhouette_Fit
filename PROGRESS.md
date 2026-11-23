# Silhouette Fit — progress notes

Goal: find the curve parameters for the generative lamp shade so the model generated in Fusion 360
matches the reference drawing (front + right view canvases) — outline **and** the twist of the ribs.

Shade height is 190 mm (the shade only, not the base). The lamp has 4-fold symmetry (4 lobes),
so the front and right views show the same outline.

> **Reference docs** (2026-11-23): `CLAUDE.md` → `docs/01_MODEL_AND_METHODS.md` (model + fit methods),
> `docs/02_PARAMETERS.md` (what each parameter does, incl. triangle size/count), `docs/03_SEGMENTS.md`
> (segments S1–S5, targets, status), `docs/04_AGENT_WORKFLOW.md` (multi-agent loop, phase plan).
> This file stays the running log + current best numbers.

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
| **Active fit** | **joint fit to both drawings** (`fit_ribs_result.json`; front-only kept as `fit_ribs_result_front_only.json`) |
| Outline vs front canvas (every 2 mm) | max 1.24 mm (triangles), 0.26 mm (LampWall) |
| Drawn ribs vs model ribs, every 10 mm (15 traced ribs, 190 checkpoints) | mean 0.82 mm, 73 % within 1 mm, worst 4.3 mm |
| Outline vs 3/4 drawing | mean 0.70 mm, max 3.3 mm |
| Twist | 0° → 88.6° |

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
- **Second view** — done and applied, see "3/4 view check" below.
- **Verify in Fusion** with `Grasshoper_TwoTriangles` and the original drawing as canvas (not re-scaled).
  If the canvas is re-imported or re-scaled, run DumpCanvas and update `measure_canvas.py` first.
- The 3/4 drawing shows the base slightly off the shade axis (~1.7 mm) — the base is excluded from scoring.

## 3/4 view check (`reference/view34_drawing.png`, scripts in `views/`)

The drawing is a near-orthographic view from ~22° above (vertical base sides stay parallel).

1. **Camera only, shape unchanged** (`python views/fit_view34.py`): fits rotation, elevation, scale,
   position and mild perspective (camera ≈ 4.5 m away). Shade outline error: **mean 0.62 mm, 95 % 2.1 mm,
   max 2.95 mm** (LampWall geometry). Independent confirmation that profile + twist + lobe depth are right.
   Result: `views/view34/camera.json`, overlay `views/view34/overlay_camera_only.png`.
2. **Joint fit to both drawings** (`python views/fit_joint.py`): front outline + 10 mm rib checkpoints +
   3/4 outline (row-by-row edges, triangle geometry, all 4 quarters), camera free.

| | Front outline max | Ribs mean / within 1 mm | 3/4 outline mean / max |
|---|---|---|---|
| Current scripts (front-only fit) | 0.68 mm | 0.78 mm / 74 % | 1.22 / 5.66 mm |
| Joint fit (`views/view34/joint_result.json`) | 1.23 mm | 0.82 mm / 73 % | 0.70 / 3.32 mm |

The joint fit halves the 3/4 error but loosens the front outline by ~0.5 mm. **It is now the active fit**
(applied with `python views/fit_joint.py --apply`; the front-only fit is kept as
`fit_ribs_result_front_only.json` — copy it back to `fit_ribs_result.json` and run `apply_ribs_fit.py` to return). Comparison picture: `views/view34/compare_current_vs_joint.png`.

Ideas: weight the two views differently (`W34` in `fit_joint.py`); the two drawings may simply not be
100 % consistent with each other (both are illustrations).

- The FulLTextureLamp script used the S-curve twist (`k1 = 0, k2 = 0.8`) on the *profile Bezier parameter*
  instead of the height; its hand-tuned angles agree with the fitted twist within ~2° at every 10 %.

---

## Model study (docs/05_EXPERIMENTS.md) — completed 2026-11-24

10 model setups (the user's scenarios M01–M05 + new M06–M10) × E0 fit + E1–E6 sweeps, shared kernel `models/_common/`
(v3), every model with its own `PROGRESS.md` history. Results: `judge/RESULTS.md`, local page `judge/results.html`.

| Rank | Model | Front / 3/4 (of 19) | Ribs | Params |
|---|---|---|---|---|
| 1 | M03 custom spline + 2D Bézier radius + cubic twist at Bézier t | 14 / 14 | 0.43 mm, 92 % ≤ 1 mm | 16 |
| 2 | M02 custom spline + keyframe radius + 5-pt Bézier twist | 14 / 13 | 0.47 mm, 91 % | 19 |
| 3 | M07 rose + 8θ harmonic + 10 mm knots | 13 / 13 | 0.43 mm, 90 % | 52 |
| — | (before the study, active fit M05, same scoring) | 4 / — | 0.82 mm | 27 |

Findings: base shape decides most (custom spline / rose+8θ ≫ plain rose); the drawn lamp is rotated ≈ −1.4° (free
orientation offset); twist is the most sensitive parameter; triangle count/width/height and sections mostly shift the
outline. Still failing: S01 rim edge and parts of the waist S08–S11.
**Not yet done:** the active fit (`fit_ribs_result.json`, Fusion scripts in the repo root) is unchanged — still M05.
Next: Fusion build F2 of the top 2 (`fusion_runs/README.md`), then the user picks the model.
