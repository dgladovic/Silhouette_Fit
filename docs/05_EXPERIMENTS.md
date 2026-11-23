# 5 — Model study: which model setup fits the lamp best

Read this before creating, running or judging a model experiment.

**Status: PLAN — no code yet.** The user approves the plan, then the build starts (§5.10).

## 5.0 Decisions so far
| Date | Decision |
|---|---|
| 2026-11-23 | Segments: 10 mm (S01–S19). Pass targets as in `segments.json`. |
| 2026-11-23 | Targets: **front drawing** (`reference/fusion_rel_size_YZ.jpg`) + **3/4 drawing** (`reference/view34_drawing.png`). |
| 2026-11-23 | Scenarios 1 and 2 used the `bez_points` keyframe table for the radius. |
| 2026-11-23 | Swept parameters: triangle count, triangle width, triangle height, twist, radius, **+ section positions** (E6). |
| 2026-11-23 | Judge weights approved as proposed (§5.8). |
| 2026-11-23 | **Each scenario runs with its own historical settings** (triangles, placement, sections), see §5.4. |
| 2026-11-23 | **Every model folder (and the kernel) keeps its own `PROGRESS.md`**: history of every change, run and result (§5.7). |
| 2026-11-23 | Fusion task F1 is run **manually by the user** before the build (`fusion_runs/README.md`). A Fusion MCP is installed; Claude uses it read-only unless told otherwise. |

---

## 5.1 Geometry options (how the shade surface is built)

Separate from the *model* (§5.2), which decides base shape, radius and twist. The geometry only decides how
the ribs/wall are made from it. Rib **paths** are identical in all options; what changes is the outline offset,
the look, and how it is built and printed.

| # | Geometry | How | Outline offset over the bare base | + | − |
|---|---|---|---|---|---|
| G1 | **Triangle wedges** (current) | each tooth = solid triangle lofted through the sections; 22 per quarter → 88 bodies | ≈ H − sagitta ≈ 2.7 mm | Fusion-native, editable, what all fits use | no inner wall (teeth touch only at points), so it needs a shell for printing; slow with many teeth |
| G2 | **Pleated wall mesh** (`LampWall`) | base offset by a triangle wave + wall thickness → STL | ≈ rib height (1.5 mm) | any rib count, printable, fast | mesh, not editable BRep |
| G3 | **Single closed-profile loft** | whole toothed outline as one closed sketch per section, one loft (`loft_all_profiles`, `../BaseScript`) | like G1 | one Fusion solid | 88–180 teeth × many sections: slow, lofts may fail |
| G4 | **Smooth body + rib features** | loft the smooth base, sweep ribs along twisted paths | like G1 | classic CAD | 88–180 sweeps: heavy, fragile |
| G5 | **Rounded pleats** (G2 variant) | sine-shaped teeth (`PTS_PER_RIB ≥ 6`) | < rib height | matches the photos | — |

**Study uses G1.** The final print geometry is chosen after the judge; only the outline offset needs recalibrating.

---

## 5.2 Models

A model = **base shape** + **radius curve r0(z)** + **twist curve** (+ base-shape curves such as lobe depth k(z)).

### The user's scenarios (code in the parent folder `../`)
| ID | Folder name | Base | Radius r0(z) | Twist | Reference code |
|---|---|---|---|---|---|
| **M01** | `M01_spline_cubic` | custom spline: `r_mults` × r0 at cumulative `phi_increments`, 0–45° mirrored to 90°, degree-5 control-point spline (`create_profile_spline2`) | `bez_points` keyframes (t, r) every 0.1, Catmull-Rom (`smooth_spline_interpolation`) | cubic S-curve `calculate_bezier_twist`: fit `k1`, `k2`, max angle | `../BaseScript` |
| **M02** | `M02_spline_beztwist` | custom spline | `bez_points` keyframes | higher-order Bézier (t, deg), 5–7 points (`calculate_bezier_twist2`; designer tool `../Grasshoper_full/test_bez_twist.py`) | `../Grasshoper_full` |
| **M03** | `M03_spline_bez2d` | custom spline | 2D Bézier (r, z)(t), degree 6 (`calculate_2d_bezier_profile_7`; designer tool `../Grasshoper/test_bez.py`) | cubic S-curve **evaluated at the Bézier parameter t**, not at height | `../FulLTextureLamp` |
| **M04** | `M04_spline_keyframes` | custom spline | keyframe table, starts at 11 keys (t = 0 … 1 step 0.1) | keyframe table (`angle_points`), Catmull-Rom | `../BaseScript`, `../FulLTextureLamp/prave vrednost bezier.txt` |
| **M05** | `M05_rose_bezier` | 4-petal rose with k(z) | 8-point 2D Bézier | 5-point Bézier | `Grasshoper_full/` here (**the active fit**) |

**M04 refinement rule** (the "add keys where a segment needs it" idea, made repeatable): after E0, add one key
(radius *and* twist) at the centre of the worst failing segment and refit. Repeat until no segment improves by more
than 0.1 mm, or 20 keys. Record every round.

The custom spline's valley (`r_mult = 0.681` at 45°) is close to a rose with k ≈ 0.19, so M01–M04 and M05 have
similar bases. They differ in the shape between tip and valley, and M01–M04 keep the base shape constant over height.

### New models
| ID | Folder name | Base | Radius | Twist | Hypothesis — why it should work |
|---|---|---|---|---|---|
| **M06** | `M06_rose_knots` | rose, k(z) | Hermite knots every 10 mm | Hermite knots every 10 mm | M04's idea on the segment grid: every segment can be fixed alone. Risk: fits drawing noise |
| **M07** | `M07_rose8_knots` | rose + 8θ harmonic: `1 + k·cos4θ + c·cos8θ`, c(z) | knots | knots | the top photo shows sharper creases than a rose; the worst ribs (x0 = ±41) run near creases |
| **M08** | `M08_superformula_knots` | superformula, 4-fold (`n1`, `n2` per height) | knots | knots | one family from round to star-shaped; shows which base the drawing wants |
| **M09** | `M09_rose_logistic` | rose, constant k | 2D Bézier | logistic S-curve, 3 params (total, centre z, width) | minimal baseline: if it scores close to M06, the extra knots are fitting noise |
| **M10** | `M10_rose_ribangle` | rose, k(z) | knots | rib lean angle α(z) knots; twist = ∫ tan α / r dz | the drawing shows rib lean directly; fitting α is less tangled with the radius |

---

## 5.3 Six swept parameters (one at a time, the other five fixed at the E0 fit)

| Exp | Parameter | Levels | What it tells us |
|---|---|---|---|
| **E1** | triangle count N per quarter | 12, 16, 22, 30, 45 | outline shift + scallop ripple per segment; neck tooth width |
| **E2** | triangle width (fill factor f = W / W_packed) × **placement rule** | f = 0.5, 0.7, 0.85, 1.0 × {equal arc length, equal angle with half tooth at 0° (`generate_shell_triangles_by_count`)} | gaps → outline shift; whether your old angle placement differs from the arc placement |
| **E3** | triangle height H | 1.5, 2, 3, 4, 5 mm | outline shift (expected 1:1, `02_PARAMETERS.md` §2.2) |
| **E4** | twist | (a) whole curve × 0.94 / 0.97 / 1.03 / 1.06 · (b) +1° bump at each 10 mm knot | (a) global sensitivity · (b) **19 × 19 influence map** |
| **E5** | radius r0 | (a) whole curve ± 1 / ± 2 mm · (b) +1 mm bump at each 10 mm knot | same as E4, for the radius |
| **E6** | **sections** (the base profiles that get lofted) | count {8, 11, 15, 20, 30, 39} × placement {uniform in z, uniform in Bézier t (as in M03), on the 10 mm knots, denser where twist/curvature is high} | how far the Fusion loft drifts from the exact curves between sections, per segment; and which placement needs the fewest sections |

**E4b / E5b — bumps through the model's own parameters.** The bump is the smallest change *of that model's
parameters* that best produces a +1° (+1 mm) bump at one knot. It is a linear least-squares fit on the curve, not on
the drawing. Knot models can do it locally. Global-Bézier, keyframe-every-19-mm or 3-parameter models can't, and the
map shows how far their change spills. This is the "can this model fix one segment?" test.

**E6 needs a loft simulator.** `model.py` evaluates the exact curves at every height. Fusion only uses them **at the
sections** and interpolates in between. The simulator interpolates every triangle vertex through the sections with
a smooth spline in z, like the loft does. It must be checked against Fusion once (§5.10, Fusion task F1).
Expectation: at 15 uniform sections, DumpCanvas already showed ≤ 0.05 mm, so E6 should matter mainly at low
section counts, at the rim flare (S01–S03) and where twist is fastest (S08–S12). In the user's older scripts the
sections sat exactly on the keyframes (11 sections, keys every 0.1). There, the loft *was* the interpolation, so
E6 shows how much that choice changed the shape.

Every experiment reports per segment (S01–S19): Δ outline (max, bias), Δ ribs (mean, within 1 mm), Δ 3/4 outline.
Known couplings (`02_PARAMETERS.md` §2.3): H and r0 are interchangeable for the outline; twist and r0 trade off
through g. So the sweeps give **sensitivities**. The best combination always comes from the E0 fit, never from
picking each sweep's best level.

---

## 5.4 Fitting protocol (E0), identical for every model

- Fit on the **front** target only: outline every 2 mm + traced ribs every 4 mm. Same weights, same loss
  (`soft_l1`, f_scale 1.5), same smoothness penalty (2nd difference of knot/key values), same `max_nfev` cap.
- **3/4 target is held out**: scoring only. (M05 is refitted under this protocol; today's active fit also used the 3/4 view.)
- **Each model uses its own settings** (user decision). Historical ones come from the user's scripts; new models
  inherit M05's:

  | Model | Settings taken from | N / quarter | H (`scale_perp`) | Placement | Sections | Section heights | Twist evaluated at |
  |---|---|---|---|---|---|---|---|
  | M01 | `../BaseScript` | 22 | 2.4 mm | equal angle, half tooth at 0° (`generate_shell_triangles_by_count`) | 11 | uniform z (= on the keyframes) | z / 190 |
  | M02 | `../Grasshoper_full` | 22 | 3.0 mm | equal arc length, 9 mm target (`generate_arc_normal`) | 15 | uniform z | z / 190 |
  | M03 | `../FulLTextureLamp` | 23 | 2.0 mm | equal angle, half tooth (`generate_polar_triangles_by_count`) | 30 | uniform in Bézier t | Bézier t |
  | M04 | `../BaseScript` | 22 | 2.4 mm | equal angle, half tooth | 11 + one per added key | on the keyframes | z / 190 |
  | M05 | `Grasshoper_full/` (here) | 22 | 3.0 mm | equal arc length, 9 mm target | 15 | uniform z | z / 190 |
  | M06–M10 | inherit M05 | 22 | 3.0 mm | equal arc length | 20 | on the 10 mm knots | z / 190 |

  The base shapes follow the user's scenario description, even where the script in `../` has since been switched
  to the rose (`../FulLTextureLamp`, `../Grasshoper_full`).
- **Fit on the exact curves**, then **score "as built"**: the same parameters run through the loft simulator at the
  model's own sections. The judge uses the as-built numbers; the exact-curve numbers are shown beside them, so it is
  visible when only the section count is holding a model back.
- Sweep levels E1–E6 always include the model's own setting as the baseline level (for example, M03 sweeps N
  around 23 and H around 2.0 mm).
- Start values: the historical numbers from the user's scripts (M01–M04) or the active fit (M05). New models start
  from M05's curves sampled onto their parameters.
- Output: `params.json`, per-segment `metrics.json` (front + 3/4), overlays, fit time, parameter count, constraint check.

---

## 5.5 Targets, noise floor, rib count (done once, before any model)

| Item | How | Why |
|---|---|---|
| Front target | `reference/fusion_rel_size_YZ.jpg`, calibration from `measure_canvas.py` (Fusion canvas), outline + traced ribs | fitting |
| 3/4 target | `reference/view34_drawing.png`, camera from `views/view34/camera.json`, outline per row | held-out scoring |
| 3/4 per segment | each image row is scored in the segment of the z of the **model point that forms the outline in that row** | per-segment 3/4 numbers |
| **Outline noise floor** | a 4-fold shape seen from the front is 180°-symmetric, so the left and right half-widths must be equal at every z. Their difference (after centring) = drawing noise | sets what "within target" can realistically mean |
| **Rib noise floor** | trace every rib with 3 tracer settings; the spread = tracer noise | same, for ribs |
| **Rib count** | count line peaks along rows near the centre, convert to ribs per quarter with the arc length | the right N for the final look (E1 context) |

If a noise floor is near or above a target, flag it to the user. The target can't be met reliably there.

---

## 5.6 Shared kernel `models/_common/` (spec)

| Module | Contents |
|---|---|
| `targets.py` | load both targets + calibration/camera; outline, ribs, 3/4 mask; segment mapping |
| `curves.py` | 2D Bézier (r, z) with z-inversion · Bézier (t, deg) lookup · keyframes + Catmull-Rom (identical to `smooth_spline_interpolation`) · Hermite knots · logistic · rib-angle integral |
| `bases.py` | rose · rose + 8θ · superformula · custom spline (degree-5 control-point B-spline from `r_mults`/`phi_increments`, mirrored) — each with arc-length tables |
| `geometry.py` | sections; tooth placement (arc / angle-half-start / fill factor); outline extents (front, 4 quarters); rib paths; **loft simulator** (E6) |
| `score.py` | per-segment metrics from `segments.json`: front outline, ribs, 3/4 outline |
| `fit.py` | the E0 protocol (§5.4) |
| `sweeps.py` | E1–E6 runners, incl. the bump projection (E4b/E5b) |
| `plots.py` | overlays on both targets, Δ-vs-z curves, influence heat maps, segment pass/fail strips |
| `fusion_template.py` | one Fusion script template; each model plugs in its curve functions |

**Model interface** (`models/Mxx/model.py`, the only model-specific code): parameter names + start values + bounds,
`curves(params) → r0(z), twist(z), base(θ, z)`, `constraints(params)`, and **pure-Python versions of the curves**.
Fusion's Python has no numpy. The numpy and pure versions are cross-checked to be equal.

**Gate A**: M05 run through the kernel must reproduce `03_SEGMENTS.md` §3.4 within 0.02 mm before any model agent starts.

---

## 5.7 Directory layout

```
targets/                         the 2 images (README inside)
  front/                         image + calibration.json + outline.csv + ribs.json + noise.json
  view34/                        image + camera.json + outline.csv
fusion_runs/                     Fusion ground truth: DumpCanvas outputs from the user's manual builds (README inside)
models/
  README.md                      index: one line per model + status
  _common/                       shared kernel (§5.6)
    PROGRESS.md                  kernel version log: every change, which models it affects, re-runs triggered
  M01_spline_cubic/
    PROGRESS.md                  history + progress of THIS model (template below)
    MODEL.md                     definition, parameters, hypothesis (before), conclusions (after)
    model.py                     model-specific curves + parameters
    fusion/                      generated Fusion script + manifest
    E0_fit/                      run.py, params.json, metrics.json, overlays
    E1_tri_count/  E2_tri_width/  E3_tri_height/  E4_twist/  E5_radius/  E6_sections/
                                 each: run.py, results.json, plots
    summary.json                 what the judge reads
  M02_spline_beztwist/ … M10_rose_ribangle/
judge/
  judge.py                       reads every models/*/summary.json
  RESULTS.md                     ranking + per-segment tables (also published as a results page)
```
The old `experiments/` folder stays frozen.

### `PROGRESS.md` — one per model folder (and one for the kernel)
Rules: **append only**. Never rewrite or delete an old entry; correct it with a new one. One entry for every change
to `model.py` or the parameters, every experiment run (also failed and re-run ones), and every kernel change that
affects the model. The status block at the top is the only part that gets overwritten.

```markdown
# M01_spline_cubic — progress

## Status  (overwrite this block only)
- State: not started | E0 done | E1–E6 done | verified | judged | rejected
- Best E0 (as built): front x/19 pass, 3/4 x/19 pass, params n, kernel v<k>
- Next: …

## Log  (append only, newest at the bottom)
### 2026-11-24 14:05 — E0 fit, kernel v1
- What: first fit, historical start values from ../BaseScript
- Changed: k1 0 → 0.07, k2 0.95 → 0.88, max angle 90 → 88.9; 11 radius keys (see E0_fit/params.json)
- Result: front 6/19, 3/4 9/19; worst S09 (rib 1.9 mm); fit 4 min, cap not hit
- Command: python models/M01_spline_cubic/E0_fit/run.py
- Notes / decisions: …
```

---

## 5.8 Judge (decided before any result is seen)

| Criterion | Measure | Score 0–1 | Weight (proposed) |
|---|---|---|---|
| **Fit** | segments passing front outline + ribs (E0, as built) | passing / 19 | 0.35 |
| **Held-out** | segments with 3/4 mean ≤ 0.75 mm (E0, as built) | passing / 19 | 0.30 |
| **Locality** | share of a 1-knot bump's effect that stays in its 2 segments (E4b + E5b) | mean share | 0.15 |
| **Simplicity** | number of fitted parameters p | 1 / (1 + p/30) | 0.10 |
| **Smoothness** | wiggles in r0 / twist / base curves (curvature sign changes beyond the drawing's own) | 1 − normalised penalty | 0.10 |
| **Buildability** | constraints pass, loft simulator OK at ≤ 20 sections, (Fusion build for the top 2) | **gate**: fail = not ranked | — |

Ties within 0.02 → the simpler model wins. The raw numbers are always shown next to the score.

Results page: ranking table, a 19-segment pass/fail strip per model (front and 3/4), influence maps, E1–E6
sensitivity summaries, and overlays of the top 2 models on both targets.

---

## 5.9 Agents for the study

| Agent | Job | Writes to |
|---|---|---|
| orchestrator (main session) | kernel, targets, noise floor, Gate A, M05, judge, results page | `models/_common/`, `targets/`, `models/M05_*`, `judge/`, docs |
| **`model-runner`** (`.claude/agents/model-runner.md`) × 1 per model | `model.py` + Fusion script, E0–E6, `MODEL.md` conclusions, `summary.json` | its own `models/Mxx_*/` only |
| `fit-verifier` | recompute each model's E0 numbers from its `params.json` | `work/verify/` |

Model runners never edit `_common/`. Kernel bugs are reported to the orchestrator, fixed once, and the affected
models are re-run.

---

## 5.10 Execution plan (after the plan is approved)

| Step | What | Who | Gate |
|---|---|---|---|
| 0 | Fusion task **F1** (`fusion_runs/README.md`): Grasshoper_full at 8 / 15 / 30 sections + `../BaseScript` as-is, DumpCanvas after each | user, **before** the build | the 4 dump files are in `fusion_runs/` |
| 1 | `targets/` (both), noise floors, rib count | orchestrator | noise floors written to `targets/README.md` |
| 2 | `models/_common/` kernel + `PROGRESS.md` (v1) | orchestrator | — |
| 3 | M05 through the kernel (exact + as built) | orchestrator | **Gate A**: exact reproduces §3.4 within 0.02 mm · **Gate B**: as built at 8/15/30 sections matches the F1 dumps within 0.1 mm |
| 4 | M01 historical (`../BaseScript` values, 11 sections) through the kernel | orchestrator | **Gate C**: matches the F1 BaseScript dump within 0.1 mm. This checks the custom spline base, angle placement and the sparse loft together. If it fails: fix the kernel, or mark M01–M04 "approx." |
| 5 | Batch 1: M01, M02, M03, M04 | 4 × `model-runner` in parallel | each E0 checked by `fit-verifier` |
| 6 | Batch 2: M06, M07, M08 · then batch 3: M09, M10 | `model-runner` | same |
| 7 | Judge + results page | orchestrator | — |
| 8 | Fusion task **F2** (user): build the top 2 models | user | buildability gate |
| 9 | User picks the model → segment-fitting loop (`04_AGENT_WORKFLOW.md`) | all | — |

Rough size: 10 fits (+ M04 refinement rounds) and ~90 evaluations per model (cheap). There are 10 model-runner
runs + verifiers; fits are the slow part.

---

## 5.11 Risks

| Risk | Mitigation |
|---|---|
| Knot models (M06–M08, M10) fit the illustration's noise | smoothness penalty; 3/4 held out; noise floor known |
| Fusion's degree-5 control-point spline (custom base) isn't reproduced exactly in Python | F1 check; until then, mark M01–M04 base as "approx." |
| Loft simulator ≠ Fusion loft | F1 check; E6 provisional until then |
| Bad rib traces (x0 = ±41, −20) steer the fits | trace-quality check in step 1; exclusions listed, identical for all models |
| Kernel bug discovered mid-study | fixed once by the orchestrator; affected models re-run; noted in `models/README.md` |

---

## 5.12 Still open

Nothing on the plan itself. Waiting for: F1 dumps in `fusion_runs/`, then the user's "go" (after the restart that
loads the Fusion MCP).
