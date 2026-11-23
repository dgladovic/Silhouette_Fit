# 3 — Segments: finding and fixing one height band at a time

Read this when a height band is wrong, before any fit, and before accepting a result.
Machine-readable definitions, targets and tolerances: **`segments.json`** (tools read it; change the numbers there).

---

## 3.1 Why segments

Today the fit is one global problem. Every Bézier control point moves the whole height, so fixing the waist
can quietly break the neck. Segments give:
1. **Diagnosis**: every metric is reported per segment, so it is obvious *where* the model fails.
2. **Local fixes**: each segment is controlled by its own nearby knots (§3.5), so a fix stays local.
3. **Parallel work**: segments that share no knots can be fitted at the same time by different agents.
4. **Partial rebuilds** in Fusion: regenerate only the bodies of the segment that changed (§3.7, proposed).

---

## 3.2 Definition — 19 segments of 10 mm

`S01` = 0–10 mm, `S02` = 10–20 mm, …, `S19` = 180–190 mm. **Zones** are only names for groups of
segments, used when talking about the shape:

| Zone | Segments | z mm | In the drawing | Twist there | Main risk |
|---|---|---|---|---|---|
| **foot** | S01–S03 | 0 – 30 | bottom rim, fast flare 83 → 107 mm half-width | 0° → 4° | outline is blind to twist here (rotation ≈ 0°), so twist comes from ribs only |
| **lower bulge** | S04–S08 | 30 – 80 | widest point (112.7 mm at z ≈ 55) | 4° → 30° | rib traces start to run into the outline on the right side |
| **waist** | S09–S12 | 80 – 120 | outline plateau ~91 mm at z ≈ 100 – 120, where the upper lobe crosses over the lower one | 30° → 58° (45° at z = 102) | outline is most sensitive to twist (0.9 mm/°); worst errors today |
| **shoulder** | S13–S16 | 120 – 160 | outline narrows 91 → 73 mm | 58° → 80° | fewer traced ribs reach this high |
| **neck** | S17–S19 | 160 – 190 | top rim, 73 → 46 mm | 80° → 89° | outline blind to twist again; spiky teeth (W ≈ 3 mm) |

Note: the plateau at the waist comes from the **twist**, not from the radius. The fitted r0 is one smooth
bulge (114 → 97 mm across the waist). The outline flattens because the lobes are turned ~45° there
(outline factor g ≈ 0.80, see `01_MODEL_AND_METHODS.md` §1.6).

The foot (fluted cylinder under the shade) is **not** a segment yet. It is not modelled or scored.

---

## 3.3 Metrics and acceptance

Per segment (all in mm unless noted):

| Metric | Meaning | Source |
|---|---|---|
| `sil_max` | max \|model − drawn\| front outline half-width, every 1 mm | `silhouette_front.csv` |
| `sil_bias` | mean signed outline error (+ = model too wide) | same |
| `rib_mean` | mean \|x-error\| of model ribs vs the 15 traced drawn ribs, every 2 mm, visible side only | `checkpoints.py` tracer |
| `rib_within_1mm` | % of rib checkpoints within 1 mm | same |
| `rib_max` | worst rib checkpoint (+ which rib) | same |
| `v34_mean` | mean 3/4-view outline error in the image rows that map into the segment | `views/fit_view34.py` (per-segment split: to build) |

**Targets** (confirmed by the user 2026-11-23; in `segments.json`): `sil_max ≤ 0.75`, `|sil_bias| ≤ 0.30`,
`rib_mean ≤ 0.75`, `rib_within_1mm ≥ 80 %`, `v34_mean ≤ 0.75`.

**Regression rule.** A change is accepted only if **no other segment** gets worse by more than
0.10 mm (`sil_max`, `rib_mean`, `v34_mean`) or 3 points (`rib_within_1mm`). Every report shows **all segments,
before → after**. Use a compact table with one row per segment, and mark only the changes.

With 10 mm segments, the upper segments have few rib checkpoints (30 – 40 each; 15 ribs, but many are hidden behind
lobes). One bad trace can swing `within_1mm` by 3 points there. Check `checkpoints.png` before trusting a single
segment's rib numbers.

---

## 3.4 Status

*Baseline 2026-11-23 — active fit = joint two-view fit (commit 1e8223d).* Update this table whenever the active fit
changes. `rib_max` shows the rib's start x0 (mm) in brackets.

| Seg | z mm | sil_max | sil_bias | rib_mean | within 1 mm | rib_max (x0) | checkpoints | Verdict |
|---|---|---|---|---|---|---|---|---|
| S01 | 0–10 | **1.55** | **+0.67** | 0.36 | 98 % | 1.15 (+70) | 60 | fail: outline (rim edge, z = 0–4 only) |
| S02 | 10–20 | 0.26 | −0.16 | 0.52 | 93 % | 1.27 (+70) | 75 | ✅ PASS |
| S03 | 20–30 | 0.35 | +0.13 | 0.25 | 99 % | 1.03 (+70) | 75 | ✅ PASS |
| S04 | 30–40 | 0.38 | **+0.34** | 0.40 | 93 % | 1.30 (+41) | 75 | fail: outline bias (marginal) |
| S05 | 40–50 | 0.31 | +0.18 | 0.59 | 86 % | 1.65 (+0) | 72 | ✅ PASS |
| S06 | 50–60 | 0.09 | −0.01 | 0.70 | 84 % | 1.95 (+0) | 69 | ✅ PASS |
| S07 | 60–70 | 0.40 | −0.22 | 0.73 | **77 %** | 2.14 (+0) | 65 | fail: ribs |
| S08 | 70–80 | **0.87** | **−0.62** | **1.04** | **66 %** | 3.23 (+41) | 61 | fail: outline + ribs |
| S09 | 80–90 | **1.24** | **−1.02** | **1.60** | **46 %** | 6.92 (+41) | 56 | fail: outline + ribs — **worst** |
| S10 | 90–100 | **1.24** | **−0.90** | **1.41** | **42 %** | 3.25 (+20) | 50 | fail: outline + ribs |
| S11 | 100–110 | **0.80** | **−0.62** | **1.20** | **44 %** | 2.53 (−71) | 45 | fail: outline + ribs |
| S12 | 110–120 | 0.39 | −0.30 | **1.19** | **59 %** | 3.23 (−41) | 41 | fail: ribs |
| S13 | 120–130 | 0.26 | −0.21 | **1.15** | **62 %** | 3.47 (−41) | 40 | fail: ribs |
| S14 | 130–140 | 0.35 | +0.09 | **0.93** | **62 %** | 3.30 (−41) | 40 | fail: ribs |
| S15 | 140–150 | 0.37 | +0.28 | **0.88** | **74 %** | 2.66 (−41) | 38 | fail: ribs |
| S16 | 150–160 | 0.50 | **+0.39** | **0.94** | **66 %** | 2.18 (−20) | 35 | fail: outline bias + ribs |
| S17 | 160–170 | 0.54 | **+0.50** | **0.92** | **62 %** | 2.45 (−20) | 32 | fail: outline bias + ribs |
| S18 | 170–180 | 0.47 | **+0.38** | **0.93** | **67 %** | 2.60 (−20) | 30 | fail: outline bias + ribs |
| S19 | 180–190 | 0.38 | +0.25 | **0.88** | **67 %** | 2.48 (−20) | 30 | fail: ribs |

**Summary: 4 / 19 pass.** The pattern:
- **S08–S11**: model outline too narrow (bias −0.6 to −1.0) *and* ribs off → points to twist (§3.6).
- **S12–S19**: outline fine, ribs consistently ~0.9 mm off. The rib from x0 = −41 is worst in S12–S15 and the one from
  x0 = −20 in S16–S19. Check whether those two traces are reliable before fitting.
- **S16–S18**: model outline too wide (+0.4 to +0.5).
- **S01**: only the very bottom edge (z = 0–4 mm). Likely the drawing's rim line, not the model.

Rib checkpoints here are every 2 mm (the 10 mm table in `checkpoints_report.txt` is a subset). Large `rib_max` values
near the outline (x0 = ±41) may be tracer errors where lines merge.

---

## 3.5 Parameter ownership

**Now (global curves)** — nothing is truly local:
| Curve | Local? |
|---|---|
| profile Bézier (8 pts) | no — every point moves all heights |
| twist Bézier (5 pts) | no — same |
| k Catmull-Rom (nodes at 0, 38, 76, 114, 152, 190) | partly — each node acts on ±2 intervals (~76 mm) |

**Proposed — knot curves on the 10 mm grid**
- Knots at every segment boundary: **0, 10, 20, …, 190** (20 knots).
- Each of r0(z), twist(z), k(z) becomes a **piecewise cubic Hermite** curve (value + slope at every knot).
  The piece inside one segment depends only on the two knots at its ends, so **moving one knot changes exactly the
  two segments that touch it** and nothing else.
- With value-only Catmull-Rom (slopes from neighbours), a knot reaches **4 segments**. That means fewer parameters
  but less local control. The model study (`docs/05_EXPERIMENTS.md`, M06) measures both.
- **Overfitting risk**: 20 knots × 3 curves can follow the illustration's noise. Always fit with a smoothness
  penalty (2nd difference of knot values), and judge on the 3/4 view as a held-out check.
- Parallel-safe: knots with **two knots between them** touch disjoint segments. For example, one agent on knots
  {30, 60, 90}, another on {120, 150, 180}. Never two agents on neighbouring knots.

---

## 3.6 Procedure — fixing one segment

1. **Confirm**: segment table + picture (`checkpoints.png`, outline overlay). Is it the model or the tracer?
2. **Diagnose**: from `02_PARAMETERS.md`, which parameter moves this metric the right way with the least spill?
   - outline bias with good ribs → r0 (or `scale_perp`, if the bias is the same in every segment)
   - ribs all off to one side → twist; ribs spread or squeezed inside a lobe → k
   - outline *and* ribs off where rotation is near 45° (S09–S12) → twist first (outline is most twist-sensitive there)
3. **Fit** only the knots that touch that segment (`segment-fitter`). Try 1–3 hypotheses in parallel if unsure.
4. **Verify** (`fit-verifier`): recompute from scratch, all segments, regression rule, Fusion constraints.
5. **Apply** (orchestrator only): back up → write the active fit → `apply_ribs_fit.py` → update §3.4 and `PROGRESS.md`.
6. **Fusion** (user): rebuild the segment (or all, until §3.7 exists), check against the canvas.

---

## 3.7 Fusion per-segment build (proposed)

- Sections on the 10 mm grid (20 sections: one per knot, which also lands on every segment boundary), optionally
  with an extra section at 5 mm inside each segment. Today it is 15 uniform sections every 13.57 mm.
- Script switch such as `BUILD_SEGMENTS = ['S09', 'S10']` builds bodies only between those sections, for quick checks.
- Risk: separate lofts meet with a tangent break at the boundary. Use segment builds for **checking**, and one
  full-height loft for the **final** build.
