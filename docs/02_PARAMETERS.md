# 2 — Parameters and what they do

Read this before changing any parameter, or deciding which one to change.
Rule: if an effect you need is not in this file, **probe it and add a row**. Don't guess.

---

## 2.1 Catalogue

Names are the same in `model.py` (Python replica) and the Fusion scripts unless noted.

### Shape curves (fitted)
| Parameter | Where | Now | Support | Constraint |
|---|---|---|---|---|
| `BEZIER_CONTROL_POINTS` — r0(z) profile | Fusion scripts; `fit_ribs_result.json` | 8 points (r, z) | **global** (degree-7 Bézier) | z(t) monotone increasing; P0 at z = 0, P7 at z = 190 |
| `twist_points` — twist(t), t = z/190 | `calculate_bezier_twist2` | 5 points (t, deg), 0° → 88.6° | **global** (degree-4 Bézier) | t in 0..1 and increasing; P0 = (0, 0) |
| `LOBE_DEPTH_Z / LOBE_DEPTH_K` — k(z) | `shape_ratio_at` | 6 nodes every 38 mm, k 0.17 – 0.23 | local (Catmull-Rom: a node acts on 2 intervals each side) | k > 0.02 |

### Ribs (design choices, not fitted)
| Parameter | Fusion name | `model.py` | Now |
|---|---|---|---|
| Triangles per quarter | `TOTAL` / `num_triangles` | `N_TRI` | 22 |
| Target base width | `target_width` (cm) | `TRI_W` (mm) | 0.9 cm = 9 mm (**inactive**, §2.2) |
| Apex height | `scale_perp` (cm) | `TRI_H` (mm) | 0.3 cm = 3 mm |
| Placement | `generate_arc_normal` | `slice_points` | by arc length, equal gaps |

### Build (Fusion only)
| Parameter | Where | Now | Effect |
|---|---|---|---|
| `num_sections` | `run()` in Fusion scripts | 15 (every 13.57 mm) | how closely the loft follows the curves between sections. `model.py` evaluates the exact curves; DumpCanvas showed ≤ 0.05 mm difference at 15 |
| `max_height_cm` | `run()` | 190.0 (really mm) | shade height |

### LampWall (secondary geometry, `LampWall/lamp_wall.py`)
`PROFILE_POINTS` (own refit), `TWIST_POINTS`, `LOBE_DEPTH` (copied from the active fit), `RIBS_PER_QUARTER = 45`,
`RIB_HEIGHT = 1.5`, `WALL = 1.2`, `DZ = 1.0`, `PTS_PER_RIB = 2`.

### Calibration (not design — only change after DumpCanvas)
`measure_canvas.py`: `W_MM, H_MM, PLANE_Z, V_OFF`. `views/view34/camera.json`: 3/4 camera.

---

## 2.2 Triangle size and count → silhouette  (measured 2026-11-23, active fit)

Method: `model.py` triangle geometry, full 4-quarter outline every 0.5 mm over 0–190 mm, one parameter changed
at a time, compared with the baseline and with the bare rose (no triangles).

### Finding 1 — the triangles are never 9 mm wide
`target_width` only applies if `N × target_width ≤ L` (quarter arc length). Here `22 × 9 = 198 mm`, but
L = r0 × 1.50 ≤ 173 mm. So the fallback (`W = L/N`, no gaps) is active at **100 % of heights**:

| z mm | 0 | 40 | 80 | 120 | 160 | 190 |
|---|---|---|---|---|---|---|
| r0 mm | 81.7 | 109.3 | 113.9 | 99.8 | 71.3 | 42.8 |
| quarter arc L mm | 123.6 | 164.4 | 171.2 | 148.6 | 108.1 | 64.3 |
| **real triangle width W = L/22** | 5.6 | 7.5 | 7.8 | 6.8 | 4.9 | **2.9** |

Because the apex height is a fixed 3 mm, the tooth shape changes with height: H/W = 0.38 at the bulge,
**1.03 at the neck** (spiky).

### Finding 2 — apex height (`scale_perp`) shifts the outline 1 : 1 and does nothing else
| TRI_H | 1.5 | 2.0 | **3.0** | 4.0 | 5.0 |
|---|---|---|---|---|---|
| outline shift (mean, min–max over height) | −1.50 | −1.00 | 0 | +1.00 | +1.99 |
| scallop ripple (peak-to-peak) | 0.34 | — | 0.35 | — | 0.36 |

- Uniform over the whole height (±0.01 mm). Rib paths are unaffected.
- **It is perfectly interchangeable with r0 for the outline.** If you change H by Δ, the profile must shrink by ~Δ
  (or re-run the outline fit). Otherwise the whole shade grows.

### Finding 3 — target width (`target_width`) does nothing at N = 22
| TRI_W | 5 | 7 | **9** | 12 |
|---|---|---|---|---|
| outline shift (mean / max) | +0.08 / 0.26 | +0.01 / 0.08 | 0 | 0 / 0 |

It only becomes active when `N × W < L` somewhere. For example, W = 5 mm opens gaps below z ≈ 150 mm.
Rule: keep `TRI_W ≥ L_max / N` (≥ 7.9 mm at N = 22) for touching triangles; go below that only on purpose.

### Finding 4 — triangle count (`N`) controls the scalloping and slightly shifts the outline
"Offset" = model outline minus bare-rose outline. "Ripple" = peak-to-peak variation of that offset over the height
(it comes from apexes and valleys sweeping past the silhouette as the shade twists).

| N per quarter | 12 | 16 | **22** | 30 | 45 |
|---|---|---|---|---|---|
| width at bulge / neck mm | 9.0 / 5.4 | 9.0 / 4.0 | 7.8 / 2.9 | 5.8 / 2.1 | 3.8 / 1.4 |
| mean offset over bare rose mm | 2.42 | 2.56 | 2.74 | 2.86 | 2.94 |
| outline shift vs N = 22 (min / max) mm | −0.94 / −0.01 | −0.49 / +0.15 | 0 | −0.02 / +0.35 | +0.07 / +0.38 |
| scallop ripple mm | 0.91 | 0.62 | 0.35 | 0.19 | 0.09 |

- Ripple falls roughly as **1/N²**. At N = 22 it is 0.35 mm, small next to the current fit errors (up to 1.2 mm).
- Offset rises with N toward H (= 3 mm): narrower triangles lose less to the sagitta of the arc under the chord.
- **Rib paths do not depend on N** (arc-fraction placement), so the rib checkpoint fit is unaffected. Changing N
  needs only a small outline refit (≤ 0.4 mm).
- What N mostly changes is the **look**: rib density. LampWall uses 45/quarter. The drawing's real rib count has
  not been measured yet (Phase 1). At N ≥ 30 the neck teeth become very narrow (≤ 2 mm wide, 3 mm tall), which is a
  risk for Fusion lofts and printing.

### Cheat-sheet
| Change | Outline | Rib paths | Look | Required follow-up |
|---|---|---|---|---|
| `scale_perp` +Δ | +Δ everywhere | none | deeper ribs | profile −Δ (or outline refit) |
| `target_width` (while inactive) | none | none | none | — |
| `target_width` below L/N | small, uneven (gaps appear) | none | gaps between ribs | outline refit |
| `N` up | +0.1…0.4 mm, less ripple | none | denser, finer ribs | outline refit; check neck tooth width |
| `N` down | −0.2…0.9 mm, more ripple | none | coarser ribs | outline refit |

Ideas not yet tried: make the apex height proportional to the width (`H = c·W`) so the tooth shape stays the same
from bulge to neck.

---

## 2.3 Base curves → silhouette and ribs

| Parameter | Outline effect | Rib-path effect | Notes |
|---|---|---|---|
| r0(z) | × g(k, twist) — ~0.8 to 1.0 mm per mm | small (ribs scale with r0) | Bézier = global: moving one point moves every height |
| twist(z) | up to **0.9 mm per degree** near 45° (z ≈ 102); ~0 near 0°/90° (foot, neck) | **main driver**: a rib's sideways position ≈ R·Δtwist (~1.9 mm per degree at R = 110 mm) | outline is blind to twist at the foot and the neck |
| k(z) | small: g(45°) = 0.811 / 0.794 / 0.783 for k = 0.15 / 0.20 / 0.25 | shifts ribs sideways inside a lobe (changes the arc-fraction → angle mapping) | trades off locally against twist |

Outline width factor g(k, rotation) — the full table is in `01_MODEL_AND_METHODS.md` §1.6.

**Known couplings (degeneracies)**
1. r0 ↔ `scale_perp`: identical for the outline.
2. r0 ↔ twist ↔ k: the outline only sees `r0 · g(k, twist)`. Ribs and the 3/4 view are needed to separate them.
3. twist ↔ k on the ribs: a local k change can imitate a small twist change for ribs near the lobe flanks.

---

## 2.4 Sensitivity matrix — to be filled in Phase 1

Effect of a small step in each parameter on each segment's metrics (`docs/03_SEGMENTS.md`). One row per
parameter, produced by `lamp-probe` agents (results in `work/probes/<param>/`).

| Parameter | Step | Δ sil bias S01…S19 (mm) | Δ rib mean S01…S19 (mm) | Δ 3/4 mean (mm) | Spill (segments affected) | Linear? |
|---|---|---|---|---|---|---|
| profile P1 … P6 (r and z each) | | | | | | |
| twist P1 … P3 (t and deg), P4 deg | | | | | | |
| k node 0 … 5 | | | | | | |
| `scale_perp`, `N`, `target_width` | | done (§2.2) | none | | all segments | yes |
