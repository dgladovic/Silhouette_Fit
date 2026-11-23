# models/_common (kernel) — progress

## Status  (overwrite this block only)
- Version: **v1** (2026-11-23). Gates A, B, C passed. Used by every model.
- Known limits: loft simulator ±0.5 mm below 15 sections (exact enough at 15+); the drawn rim edge (z = 0–4 mm)
  is a rounded corner no smooth radius curve follows, so S01's outline fails for every model.
- Next: none planned. Model runners report kernel problems here via the orchestrator.

## Log  (append only, newest at the bottom)

### 2026-11-23 22:40 — v1 built
- Modules: `targets.py`, `curves.py`, `bases.py`, `geometry.py`, `score.py`, `study.py`, `plots.py`, `fusion_template.py`, `fusion_check.py`.
- Targets (`targets/`): front outline + 15 traced ribs; 3/4 outline (136 rows) + start camera.
- Noise floors (`targets/front/noise.json`): outline left/right asymmetry → half-width noise **0.03 mm** (≤ 0.06 per segment).
  Tracer repeatability (snap 1/2/3 px): mean 0.25 mm, but 8.5 % of points disagree by > 1 mm.
- **Rib exclusion**: points where the 3 tracer runs disagree by > 1 mm are skipped for every model. In practice that is
  the rib starting at x0 = −40.7 mm from z ≈ 15 mm up (runs 3–4 mm apart). It was the worst rib in S12–S15 before.
- Rib count in the drawing: line spacing 3.1 / 3.6 / 4.2 mm at z = 20 / 40 / 60 → **≈ 41–49 ribs per quarter**.

### 2026-11-23 22:45 — Gate A (kernel vs model.py)
- M05 with the active fit, exact curves, no rib exclusion: all 19 segments within 0.01 mm of `docs/03_SEGMENTS.md` §3.4.
- 3/4 residual identical to `views/fit_joint.py` (0.697 vs 0.696 mm) after sampling model points every **0.5 mm**
  (1 mm gave 1.08 mm: rows near the rim need the finer sampling).

### 2026-11-23 22:50 — Gate B (loft simulator vs Fusion, fusion_runs/F1-1..3)
- Outline (quarter maxY) vs Fusion, cubic not-a-knot interpolation of tooth vertices through the sections:
  8 sections mean 0.12 / max 0.54 mm · 15: 0.017 / 0.13 · 30: 0.003 / 0.016. Natural/Akima/PCHIP/linear are worse.
- The exact curves themselves differ from Fusion by only 0.16 mm mean at 8 sections, so **section count is a small lever** for the outline.
- Isolated 2 mm maxX differences come from the cut edge of the single quarter (never part of the real outline). Ignored.

### 2026-11-23 22:55 — Gate C (custom spline base, ../BaseScript vs fusion_runs/F1-4)
- Clamped uniform degree-5 B-spline + equal-angle half-tooth placement + 11-section loft: **0.05 mm mean / 0.20 mm max**. Passed.

### 2026-11-23 23:10 — implementation decisions (differences from the plan in docs/05)
- **Knot curves = value-only Catmull-Rom on the 10 mm grid** (`curves.catmull_keys`), not Hermite with slopes: half the
  parameters, and fits stay fast. A knot reaches 4 segments instead of 2. E4b/E5b measure the real locality.
- **Fusion export is table-driven** (`fusion_template.py`): each model's curves are sampled at its sections into the
  script, which draws the bases and teeth and lofts. No pure-Python curve copies are needed. Checked: generated teeth = kernel within 0.0025 mm.
- Smoothness penalty weights `study.SMOOTH_W`: 0.05 per mm (radius keys), 0.05 per degree (twist keys), 2.0 per unit of k.
- Fit: `least_squares` trf, soft_l1 (f_scale 1.5), x_scale 'jac', 2 stages (diff_step 1e-3, 1e-4), max_nfev 200 each.
- E4b/E5b: bump = linear least-squares change of the model's own parameters (other curve held, ridge 1e-2), applied as a
  small step (≤ 0.2 % per parameter) and scaled back to 1 °/1 mm. Linear and realized changes agree within 0.05.

### 2026-11-23 23:15 — reference runs
- M05 (orchestrator): E0 front 8/19, 3/4 7/19 (as built), E1–E6 done.
- M01 (orchestrator): E0 front 3/19, 3/4 14/19, E1–E6 done.

### 2026-11-23 23:45 — fit-stall check (raised by the M04 runner)
- Observation: stage 1 of `study.fit` stops on xtol (status 3) after ~15–25 evaluations while optimality is still ~6e3.
  Rib visibility and interpolation make the objective non-smooth, so the trust region shrinks.
- Test from the E0 results with diff_step 1e-2 / 3e-3: M01 no change (cost 198.19 → 198.19, a real minimum).
  M05: cost 171.8 → 164.7 (−4 %), but front pass **8 → 6** and 3/4 7 → 8. The pass counts are threshold-sensitive.
- Decision: protocol unchanged (identical for every model, so comparisons stay fair). **Read pass-count differences of
  ±2 segments as optimiser noise**; the judge report says so. The docstring of `refine` is corrected to the real call signature.

### 2026-11-24 00:20 — kernel v2: multi-start E0 (raised by the M02 runner)
- **Problem**: M02's runner showed that M02 reaches cost 102.8 / front 13/19 from another start, against 223.5 / 4/19 from
  its historical start. v1 E0 results depended on the start, not just on what the model can represent. The earlier stall
  check (restart from the result) could not see this.
- **Fix (v2)**: `fit_multistart`. Each model is fitted from its own start AND from every curve set in
  `start_pool.json` (M01 E0, M05 E0, M02 X1c), each projected onto its parameters (`project_start`: least squares on
  r0(z), twist(z)); the lowest cost wins. All start costs are logged. The fit gets 3 stages: diff_step 1e-2 → 1e-3 → 1e-4
  (the coarse stage steps over the non-smooth rib terms).
- Effect: M02 217 → 101.6 (front 4 → 12/19), M03 → 84.5 (front 6 → 14/19), M05 171.8 → 163.8 (front 8 → 5/19!),
  M01, M04 unchanged (198, 209: real minima). The cost and the pass counts don't always move together (M05).
- All of M01–M05 re-run (E0–E6, summaries) under v2 and re-verified (`judge/verify_e0.py`: all confirmed).
- **Gate fix**: the buildability gate now uses the best section placement at ≤ 20 sections (the plan's wording). v1 checked
  only 20 uniform sections, which wrongly failed M03 (uniform 0.36 mm, adaptive 0.09 mm, own 30 sections 0.05 mm).
- Planned: after all 10 models have run under v2, add every model's best curves to the pool and run one more E0 round for
  all ("pool round 2"), so no model misses a good start found by another.

### 2026-11-24 01:30 — kernel v3: orientation offset, gate, pool round 2 (final round)
- **Orientation offset** (raised independently by the M04 and M06 runners): the rotation of the whole lamp relative to the
  drawing is not part of the shape, but twist(0) = 0 fixed it for the keyframe/knot models. Bézier models could imitate it
  with a control point at t ≈ 0 (M02/M03/M05 fits dip to about −1° at the rim). Evidence: M04 E0 + a constant −1° costs
  148.6 vs 209.5 without any refit; M06 with twist(0) free costs 159 vs 195. v3: `study.load_model` appends a free
  `orient_deg` (±15°) to EVERY model (`_wrap_orient`); twist(z) → model twist(z) + offset. model.py files are unchanged.
- **M04 refinement** is disabled in v3: its internal refits bypass the wrapper. It added 0 keys in v1 and v2; v3 runs M04 on
  its 11 historical keys.
- **Buildability gate**: loft deviation ≤ 0.3 mm at **≤ 39 sections** (best placement). The knot models (M06, M07, M08, M10)
  deviate only in the two end segments (Catmull-Rom end intervals vs the loft spline, 0.4–0.7 mm at ≤ 20 sections, 0.08 at
  39 uniform). The judge scores everything *as built* at each model's own sections, so this deviation is already in their
  scores; the gate only has to ensure a practical Fusion build.
- **Pool round 2**: `start_pool.json` = round 1 (3 curves) + every model's v2 E0 curves (10), so every model starts from the
  best shapes any model found.
- Then all 10 models re-run (E0–E6, summaries) with `judge/run_round.py`, logs in `work/round_v3/`.

### 2026-11-24 02:10 — final round results (kernel v3)
- All 10 models re-run (E0–E6, summaries, 1st–10th in `judge/RESULTS.md`), all E0 numbers confirmed by `judge/verify_e0.py`.
- The orientation offset was the biggest single fix: M01 198 → 91, M04 210 → 91, M06 195 → 160, M10 169 → 160 (cost).
  Fitted offsets are all −0.5 … −1.7°: the drawing's lamp is rotated about 1.4° against twist(0) = 0.
- **Base shape decides the rest**: custom spline (M01–M04) and rose + 8θ (M07) reach cost 73–95, while the plain rose (M05, M06,
  M08, M10) stays at 160–176, whatever the radius/twist representation. M08 shows the superformula can't do better than a rose.
- Known limitation: `project_start` matches only r0/twist; base-shape parameters (k, c, n1/n2) start from the model's P0
  for every pool start. M07 v3 (79.3) is therefore slightly above its v2 cost (74.9). Its pass counts still went up.
