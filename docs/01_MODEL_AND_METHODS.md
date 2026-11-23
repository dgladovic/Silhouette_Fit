# 1 — The model and how it is fitted

Read this before touching geometry, curves or fitting code.
Numbers marked *snapshot* go stale — the live values are in `fit_ribs_result.json`.

---

## 1.1 What we are modelling

A 3D-printed lamp shade: **4 lobes that twist ~90° from bottom to top**, covered in fine ribs, sitting on a
fluted cylinder foot. References in `reference/`:

| File | What it is | Used for |
|---|---|---|
| `fusion_rel_size_YZ.jpg` (= `1.jpg`, `fusion_rel_size1_XZ.jpg`) | Front line drawing, the canvas in Fusion | **Main target**: outline + rib paths |
| `view34_drawing.png` (= `5.png`) | 3/4 drawing from ~22° above | Second, independent projection |
| `top_view_insta.webp` | Photo looking down into the top rim | Cross-section shape check (qualitative) |
| `2.webp`, `3.jpg`, `4.jpg`, `6.png` | Product photos | Visual sanity only (perspective, not measurable) |

- **Shade height = 190 mm** (the shade only). The foot is not modelled or scored yet (it sits ~1.7 mm off-axis in the 3/4 drawing).
- **4-fold symmetry** → the front and right views show the same outline. `Grasshoper_full` builds **one quarter**;
  the other three are copies.

---

## 1.2 The base (cross-section)

At every height the cross-section is a **4-petal polar rose**:

```
r(θ) = a + b·cos 4θ ,   a = r0 / (1 + k),   b = a·k          → r(0°) = r0  (petal tip)
     = r0 · (1 + k·cos 4θ) / (1 + k)                            valleys at r0·(1−k)/(1+k)
```

| Symbol | Meaning | Typical |
|---|---|---|
| `r0` | petal-tip radius (outermost point of the bare rose) | 43 – 114 mm |
| `k` | lobe depth (`shape_ratio`). 0 = circle. Valley/tip ratio = (1−k)/(1+k) | 0.17 – 0.23 (k = 0.2 → valleys at 0.667·r0) |
| `θ` | local angle; petal tips at 0°, 90°, 180°, 270° before twist | |

In Fusion: `create_polar_rose_spline()` in `ClosedProfile.py` — a fitted spline through 51 points over 0–90°
(one quarter), drawn as a construction line. The ribs are built on it (§1.4).

**Shapes tested** (`section_experiment.py`, results in `experiments/summary.txt`):

| Base shape | Outline RMS | Rib-angle error over whole drawing |
|---|---|---|
| rose k = 0.12 | 0.30 mm | 3.64° |
| **rose k = 0.20** | **0.10 mm** | **1.68°** ← chosen |
| rose k = 0.28 | 0.16 mm | 2.80° |
| "star nozzle" (union of 4 circles) d = 0.3 / 0.4 / 0.5 | 0.12 – 0.22 mm | 3.1 – 6.0° |

Open question: the top-view photo shows **sharper creases** between lobes than a pure rose has.
Candidate: one extra harmonic `r ∝ 1 + a·cos4θ + c·cos8θ` (not tried yet).

---

## 1.3 How the base changes along the height — three curves

The whole shade = the base, re-sized, re-shaped and rotated at every height `z` (0–190 mm):

| Curve | What it controls | Representation (now) | Where | Evaluated by |
|---|---|---|---|---|
| **r0(z)** — profile | size of the base | 8-point Bézier in (r mm, z mm), degree 7 | `BEZIER_CONTROL_POINTS` | `find_t_for_height` (bisection on z) → `calculate_dynamic_bezier` |
| **k(z)** — lobe depth | how deep the lobes are | Catmull-Rom through 6 values at z = 0, 38, 76, 114, 152, 190 | `LOBE_DEPTH_Z / LOBE_DEPTH_K` | `shape_ratio_at(z)` |
| **twist(z)** — rotation | rotation of the whole base about Z | 5-point Bézier in (t = z/190, degrees) | `twist_points` | `calculate_bezier_twist2(t)` (lookup table) |

Important properties:
- The two Bézier curves have **global support**: moving one control point changes the curve at *every* height.
  That is why a fix in one height band currently disturbs the others. See `docs/03_SEGMENTS.md` §3.5 for the proposed fix.
- Fusion constraints: profile z(t) must increase monotonically (bisection lookup); twist t values must stay in 0..1 and increase.

*Snapshot (2026-11-23, joint fit)* — values at the segment knots, plus the drawn outline half-width:

| z mm | r0 mm | k | twist ° | drawn half-width mm |
|---|---|---|---|---|
| 0 | 81.7 | 0.224 | 0.0 | 82.7 |
| 15 | 95.0 | 0.218 | −0.1 | 97.8 |
| 30 | 104.9 | 0.212 | 4.3 | 107.0 |
| 55 | 113.3 | 0.211 | 15.7 | 112.7 |
| 80 | 113.9 | 0.207 | 30.5 | 106.1 |
| 102 | 108.2 | 0.178 | **45.1** | 90.2 |
| 125 | 96.9 | 0.184 | 60.6 | 91.2 |
| 142 | 85.7 | 0.217 | 71.2 | 84.7 |
| 160 | 71.3 | 0.228 | 80.4 | 72.9 |
| 175 | 57.7 | 0.214 | 85.8 | 60.1 |
| 190 | 42.8 | 0.200 | 88.6 | 45.6 |

Note that r0 ≠ drawn half-width: the outline also depends on rotation (§1.6) and on the triangles (+~2.7 mm, see `02_PARAMETERS.md`).

---

## 1.4 Ribs on top of the base

**Triangles** (`Grasshoper_full`, the primary geometry), per section and per quarter:
1. Measure the arc length `L` of the rose quarter.
2. Place `N = 22` triangles along it by **arc length** (`generate_arc_normal`). Base = rose arc between p1 and p2.
   Width = `target_width` (9 mm) with equal gaps — **or, if N·9 mm doesn't fit, W = L/N with no gaps**
   (this fallback is active at every height today; see `02_PARAMETERS.md` §2.2).
3. Apex = chord midpoint + `scale_perp` (3 mm) along the outward chord normal.
4. 15 sections (every 13.57 mm); each triangle is lofted through all sections → 22 wedge bodies per quarter.

**Consequence used by the fit:** a rib keeps its **arc-length fraction** inside its quarter at every height, so its
3D path depends only on r0(z), k(z) and twist(z) — not on N, width or height of the triangles.
That is what makes drawn ribs usable as checkpoints.

**LampWall** (`LampWall/lamp_wall.py`, secondary): continuous pleated wall, 45 ribs per quarter, 1.5 mm tall,
written as STL. Same twist and k(z); its profile is refitted by `apply_ribs_fit.py` because the pleats stick out less.

---

## 1.5 Coordinates, units, calibration

- Python: **mm and degrees**. Fusion API: cm — the scripts divide by 10. `max_height_cm = 190.0` is really mm (old name).
- Z up. **Front view**: camera at −Y, shows X. **Right view**: camera at +X, shows Y.
- The Fusion canvases are **mirrored left–right** compared with the original drawing.
- Canvas → mm calibration is in `measure_canvas.py`, taken from `fusion_dump.txt` (DumpCanvas script).
  The canvas was 226.75 × 260.08 mm (2.2 % squeezed horizontally). **If the canvas is moved or rescaled in Fusion:
  run DumpCanvas and update `measure_canvas.py` first**, or every measurement is wrong.
- `model.py` is the Python replica of the Fusion geometry. Verified: Fusion bodies sliced by DumpCanvas match it
  within 0.05 mm; Fusion's twist and k functions match within 0.01°.

---

## 1.6 How the profile is determined — methods

**Why the outline alone is not enough.** At height z the outline half-width is

```
outline(z) ≈ r0(z) · g( k(z), twist(z) mod 90° ) + triangle offset (~2.7 mm)
```

`g` = how wide the 4-lobed base looks from the front, depending on how far it has turned:

| rotation | 0° | 10° | 20° | 30° | 40° | 45° |
|---|---|---|---|---|---|---|
| g (k = 0.20) | 1.000 | 0.989 | 0.956 | 0.904 | 0.834 | 0.794 |

So the outline is up to **0.9 mm per degree of twist** (at r0 ≈ 110 mm, near 45°). Many combinations of r0, k
and twist draw the same outline. Each method below adds a constraint:

| # | Method | Script(s) | What it pins down | Status |
|---|---|---|---|---|
| 1 | Front outline, every 2 mm | `fit.py`, term in all fitters | r0, *given* twist and k | always a term |
| 2 | Rib slope on the centre line | `measure_canvas.py` → `rib_slope_center.csv`, `fit.py` | twist rate (dx/dz = R·dtwist/dz) | superseded by 4 |
| 3 | Base-shape test | `section_experiment.py`, `rib_error_map.py`, `ktop_experiment.py` | which base shape / k | done → rose k ≈ 0.2 |
| 4 | **Rib checkpoints**: trace 15 drawn ribs up from the rim; the model rib from the same start must stay on it | `checkpoints.py` (eval, 10 mm table), `fit_ribs.py` (fit, every 4 mm) | twist(z) and k(z) | main method |
| 5 | **3/4 view**: camera-only fit, then joint fit with 1 + 4 | `views/fit_view34.py`, `views/fit_joint.py` | breaks the remaining r0/k/twist trade-off | **active fit = joint** |
| 6 | Fusion check | `DumpCanvas/`, `Grasshoper_TwoTriangles/` + `expected_triangles.py` | Fusion builds what `model.py` says | last done on an earlier fit |

**Blind spots to keep in mind**
- The outline gives almost **no twist information near 0° and 90°** (g is flat there) → the foot (S01–S03) and the
  neck (S17–S19). There, twist comes from the ribs only.
- The outline is **most twist-sensitive near 45°** → z ≈ 102 mm, in the waist (S09–S12), which is also where the upper
  lobe crosses over the lower one. Expect this band to be the hardest.
- Traced ribs end where they go behind a lobe → fewer checkpoints above ~100 mm on the right-hand ribs.
- Both drawings are illustrations. There is a noise floor, and the two drawings may not agree 100 % with each other.

**Typical commands**
```bash
python checkpoints.py         # 10 mm table for the active fit + checkpoints.png
python fit_ribs.py            # front-only fit (outline + ribs), continues from fit_ribs_result.json
python views/fit_joint.py     # joint fit front + 3/4  (--apply to make it active)
python apply_ribs_fit.py      # write fit_ribs_result.json into all Fusion scripts + LampWall
python expected_triangles.py  # images to compare with the Fusion TwoTriangles build
```
