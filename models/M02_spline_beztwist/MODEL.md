# M02 — scenario 2: custom spline base + keyframe radius + higher-order Bézier twist

## Definition
| Part | Representation | Parameters |
|---|---|---|
| Base | the custom spline (`r_mults` / `phi_increments`, degree-5 control-point spline, 0–45° mirrored), **fixed over height** (same as M01) | 0 |
| Radius r0(z) | `bez_points` keyframes at t = 0, 0.1 … 1 (t = z/190), Catmull-Rom (`smooth_spline_interpolation`), bounds 20..200 mm, smoothness `SMOOTH_W['mm']` × 2nd difference (same as M01) | 11 |
| Twist | 5-point Bézier (t, deg), `calculate_bezier_twist2` lookup at t = z/190. P0 = (0, 0) fixed; T1–T3 free t (0..1) and angle; T4 at t = 1, angle free. Penalty 200 · min(diff(t), 0) | 7 |
| **Total** | | **18** |

Own settings (`../Grasshoper_full`): N = 22, H = 3.0 mm (`scale_perp` 0.3 cm), equal arc length with a 9 mm target
(`generate_arc_normal`), 15 uniform sections.
Start: radius = `../BaseScript` `bez_points` (M01's start); twist = `../Grasshoper_full` `twist_points`
(0, 0), (0.289, −0.7), (0.604, 59.0), (0.827, 78.4), (1, 90). Start (as built): front 1/19, 3/4 5/19, ribs 2.20 mm.
Pure-Python curves in `model.py` (`py_r0`, `py_twist`) agree with the numpy ones to < 1e-6 (self-test: `python models/M02_spline_beztwist/model.py`).

Difference from M01: only the twist representation (5-point Bézier, 7 params, instead of the 3-param cubic) and the
build settings (H 3.0 vs 2.4, arc vs angle placement, 15 vs 11 sections).

## Hypothesis (written before running)
- The radius and base are the same as M01, so the outline should behave like M01's after the fit (outline passes in
  the bulge S04–S08, fails at the rim S01–S03 and the neck S18–S19). H = 3.0 instead of 2.4 adds ~0.6 mm offset, but the
  radius keys absorb it (H and r0 are interchangeable for the outline, `02_PARAMETERS.md` §2.3).
- The 5-point Bézier twist has more freedom than the cubic (inner point t positions move), so the ribs should
  improve over M01 (M01: 0.67 mm mean, 80 % ≤ 1 mm, rib failures S07–S19). I expect gains in the waist S08–S12,
  where the twist rate changes fastest.
- The ribs in the shoulder/neck (S12–S19) will still fail in part: the base can't change lobe depth with height, so
  rib positions inside a lobe drift, and a global Bézier can't add local twist there without moving the waist.
- Locality: radius keys same as M01 (~0.6); twist low (~0.2–0.3), every control point moves the whole height.
- Expected: front ≈ 4–8/19 (more than M01's 3/19), 3/4 ≈ 12–15/19.

## Conclusions (after running) — kernel v2 (current)

**E0** (v2 multi-start; best start `pool:M01_E0`, cost 101.6; own start 217.3, M05_E0 101.8, M02_X1c 101.7, so three
different starts land in the same minimum): front **12/19**, 3/4 **15/19**, ribs 0.52 mm mean / 89 % ≤ 1 mm, 3/4 mean 0.78 mm,
outline max 2.08 mm (S01). Exact curves: 12/19, 11/19. 18 params, 50 s, no cap hit, constraints OK.
Fitted twist: T1 (0.000, −8.8°), T2 (0.456, 10.1°), T3 (0.522, 63.7°), T4 90.5°. That is a small back-twist low down,
then a steep S between z ≈ 80 and 110. Radius keys are within 1 mm of the v1 fit.

- **E1 triangle count**: N 16 → 12/19, 3/4 12/19 (bias −0.16 mm); N 12 → 10/19, 8/19 (−0.30 mm); N 30/45 → 11/19, 15/19 (+0.10/+0.17).
  Ribs unchanged (0.52). The own N = 22 is the best level.
- **E2 width × placement**: fill 0.5 → 1.0 moves the outline by ≤ 0.13 mm (11–12/19 front, 15–16/19 3/4). Angle placement at f 1.0 gives the
  same 12/19 and 15/19, but outline max 2.34 vs 2.08 mm. Small lever.
- **E3 triangle height**: outline shifts 1:1 (H 2.0 → −1.00 mm, H 4.0 → +1.00 mm), every other level gives 0/19 front. The radius is fitted
  for H = 3.0.
- **E4 twist**: ×0.97 / ×1.03 → ribs +0.82 / +0.79 mm, front 12 → 4 / 3, 3/4 15 → 7 / 8. Very sensitive (≈ 0.27 mm rib per 1 %).
  Bumps: locality **0.38**, median achieved 0.27 of 1° (M01 0.21). A +1° bump at one knot spreads over the whole height.
- **E5 radius**: ±1 mm → 0/19 front, 3/4 0 / 6 (bias ±0.95 mm). The outline has no slack. Bumps: locality **0.63**, achieved 0.49 of 1 mm
  (same keys as M01).
- **E6 sections**: own 15 uniform: loft deviation max 1.09 / mean 0.13 mm, in S01–S03 (1.09/0.65/0.43) and S17–S19 (0.24/0.47/0.82);
  S04–S16 ≤ 0.14. 20 adaptive: max 0.08 mm (buildability gate OK). Front 9–13/19 across all levels; 8 sections cost 3 segments.
  adaptive 15 drops to 9/19, adaptive 11 reaches 13/19, so ±1–3 segments sit right at the pass threshold.

**Segments (E0, as built)**
- Front pass: S02, S04–S07, S12–S18 (12). Fail: S01 (rim outline 2.08), S03 (outline 0.48), S08–S11 (waist ribs 0.72 / 1.14 / 0.84 / 0.62 mm,
  73–78 % ≤ 1 mm; S11 outline 0.48), S19 (neck outline 1.29).
- 3/4 pass: S05–S19 (15). Fail: S01–S04 (rim, 3/4 mean 2.98 / 1.68 / 1.50 / 0.85).

**Main limitation**
- **Waist ribs S08–S11 (twist + base)**: the S-curve's steepest part sits here. One global 5-point Bézier sets the waist rate together
  with the shoulder (E4b locality 0.38), and the fixed-over-height base can't shift ribs within a lobe.
- **Rim S01–S03 and neck S19 (radius)**: keys every 19 mm can't follow the rounded rim corner (kernel's known S01 limit) or the neck flare.
  This is also where the 15-section loft deviates most.

**Hypothesis check**
- Outline like M01: **held** (S04–S07 pass; S01, S03, S19 fail; H 3.0 absorbed by the radius keys).
- Ribs better than M01 thanks to the higher-order twist: **held** (0.52 vs M01's 0.67 mm; 89 vs 80 % ≤ 1 mm). But the gain came in the
  **shoulder/neck S11–S18** (1.1–1.5 → 0.35–0.62 mm), not at the waist as predicted. The waist S08–S10 stays failed.
- "Shoulder/neck ribs will still fail": **wrong**. They pass.
- Locality: twist 0.38 (expected 0.2–0.3, a little better), radius 0.63: **held**.
- Front 4–8/19: **exceeded** (12/19). 3/4 12–15/19: held (15/19).

**Against M01** (v2: front 3/19, 3/4 13/19, ribs 0.67 mm): same base and radius. The 5-point Bézier fixes what the cubic couldn't: it
needs T2 and T3 close together in t (0.46 / 0.52) for a steep S at z ≈ 80–110 after a slight back-twist. A 3-parameter cubic can't make
that shape. The v1 X1b check showed that M01's settings alone don't explain the gap.

## Superseded (kernel v1)
_The conclusions below are from kernel v1 (single-start E0, which stalled at front 4/19). They are kept for the record and replaced by the
kernel v2 section above._


**E0 (protocol fit, historical start)**: front **4/19** (S02, S04, S05, S06), 3/4 **13/19**, ribs 0.76 mm mean / 78 % ≤ 1 mm,
3/4 mean 0.77 mm, outline max 2.24 mm (S01). Exact curves: also 4/19 and 13/19. 18 params, 29 s, nfev 18, no cap hit,
constraints OK. The fit hardly moved the twist (T2 59.0 → 60.9°, T3 78.4 → 81.5°): stage 1 stopped on `xtol` with
first-order optimality 1.1e3, so this is an early stop, not a minimum.

- **E1 triangle count**: N 16 gives front 5/19, 3/4 14/19 (outline bias −0.16 mm); N 12 −0.30 mm, N 45 +0.17 mm. Ribs unchanged
  (0.76). Small lever; the radius keys absorb it after a refit.
- **E2 width × placement**: arc f 0.5 → 1.0 shifts the outline by only 0.13 mm (3/19 → 4/19). Angle placement at f 1.0 gives the
  same 4/19, 13/19, but outline max 2.50 vs 2.24 mm (bias range −0.14..+0.27). Placement doesn't change the ribs here.
- **E3 triangle height**: outline shifts 1:1 (H 2.0 → −1.00 mm, H 4.0 → +1.00 mm), every non-own level drops to 0/19 front. The fitted
  radius is tied to H = 3.0; H isn't a free lever after the fit.
- **E4 twist**: ×0.97 / ×1.03 → ribs +0.79 / +0.49 mm and 3/4 13 → 5 / 9 passing: very sensitive (≈ 0.25 mm rib per 1 %).
  Bumps: locality **0.38** (M01 0.21), median achieved 0.29 of 1°. Better than the cubic, but a +1° bump still spreads over the
  whole height (the best knots are near the top, 0.55–0.65, where T4 is free).
- **E5 radius**: ±1 mm → 0/19 front (outline bias ±0.95 mm); the outline has no slack. Bumps: locality **0.63**, achieved 0.49 of 1 mm,
  identical to M01 (same keys).
- **E6 sections**: own 15 uniform: loft deviation max 1.07 / mean 0.13 mm, concentrated in S01–S03 (1.07/0.63/0.39) and S17–S19
  (0.24/0.48/0.82); S04–S16 ≤ 0.12. 20 uniform: max 0.25; adaptive 20: max 0.08. Pass counts change by at most 1 (3–4/19 front).
  Sections don't limit this model; the curves do.

**Extra check X1** (`X1_vs_M01/`, not part of E0–E6; same kernel `study.fit`):
- E0 params scored with M01's settings → 2/19, 15/19; M02 refitted with M01's settings → **3/19, 14/19, ribs 0.67 mm = exactly M01's E0**.
  So from the historical start the 5-point Bézier gives nothing over the cubic.
- M02 refitted from M01's E0 curves (cubic degree-elevated into 5 Bézier points) → **front 13/19, 3/4 13/19, ribs 0.52 mm / 89 %**,
  cost 102.8 vs 223.5. Twist: T1 (0.006, −9.1°), T2 (0.463, 11.7°), T3 (0.528, 64.4°), T4 90.4°. That is a slight back-twist low down
  and a steep S between z ≈ 80 and 110. Ribs S11–S17 drop from 1.25–1.50 to 0.37–0.63 mm. Still fails: S01 (rim), S08–S10 (waist ribs
  0.71/1.15/0.85 mm), S18–S19 (neck outline).
- Restarting from its own E0 doesn't escape (cost 193, 4/19). So the result depends on the start.

**Which segments pass (E0, as built)**: front S02, S04–S06 · 3/4 S04–S07, S11–S19. Fails: S01 everywhere (the rim corner, kernel known limit);
S03 outline 0.46 mm; S07–S10 ribs (55–75 % ≤ 1 mm); S11–S19 ribs 1.1–1.5 mm mean; S19 outline 1.33 mm.

**Where the model is limited and why**
- **Twist, through the fit and not the representation**: the shoulder/neck rib failures (S11–S19) are twist failures. X1c shows the
  5-point Bézier can fix them (13/19), but the protocol fit from the Grasshoper_full start doesn't find that basin.
- **Waist S08–S10**: these fail in every variant (rib 0.6–1.15 mm). The twist rate there is coupled to the S-curve shape above and below.
  The base can't change lobe depth with height either. Probably base + twist together.
- **Rim S01 and neck S19 outline**: radius keys every 19 mm can't follow the rounded rim corner or the neck flare. That's the radius
  (and the kernel's known S01 limit).

**Hypothesis check**
- Outline like M01: **held** (S04–S06 pass, S01/S03/S19 fail; H 3.0 absorbed by the radius keys).
- Ribs better than M01: **not held under the protocol** (0.76 vs 0.67 mm; X1b shows the gap is the settings, not the twist).
  **Held in principle**: X1c reaches 0.52 mm and fixes S11–S17. The gain shows up in the shoulder/neck, not at the waist as I expected.
- Shoulder/neck ribs still fail: held for E0, wrong for X1c (they pass there).
- Locality: twist 0.38 (expected 0.2–0.3, slightly better), radius 0.63 (held).
- Front 4–8/19: E0 4/19 (low end); 3/4 13/19 (held).

**Against M01**: same base, same radius. Under the protocol the higher-order twist doesn't fix what the cubic couldn't
(4/19 vs 3/19, the gap is from the settings). The representation itself can do it (13/19 from a better start). The cubic has no shape that
reaches it: the fitted twist needs T2 and T3 close in t (0.46/0.53), which a 3-parameter cubic can't produce.


## Final round — kernel v3 (2026-11-24): orientation offset + pool round 2
These are the numbers the judge uses. The conclusions above were written under kernel v1/v2, without the free orientation offset.

| | value |
|---|---|
| Rank / score | **2 / 10**, 0.702 |
| Front (as built) | **14/19** `·██████···████████·` |
| 3/4 held out | **13/19** `······█████████████` |
| Ribs | 0.47 mm mean, 91 % ≤ 1 mm |
| 3/4 mean / outline max | 0.78 mm / 2.00 mm |
| Fit cost (best of 14 starts) | 94.3 from `pool:M01_E0` |
| Orientation offset | -1.66° |
| Locality twist / radius | 0.41 / 0.63 |
| Parameters | 19 (incl. the offset) |
| Buildable | yes (loft deviation 0.04 mm, best placement ≤ 39 sections) |
