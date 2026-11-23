# M03 — scenario 3: custom spline base + 2D Bézier radius + cubic twist at the Bézier t

## Definition
| Part | Representation | Parameters |
|---|---|---|
| Base | the custom spline (`r_mults` / `phi_increments`, degree-5 control-point spline, 0–45° mirrored), **fixed over height** (`bases.custom_spline()`) | 0 |
| Radius r0(z) | degree-6 2D Bézier (r, z)(t), 7 control points (`calculate_2d_bezier_profile_7`); P0 z = 0 and P6 z = 190 fixed, inner points free in (r, z); r0(z) looked up by height (`curves.BezierRZ`) | 12 |
| Twist | `calculate_bezier_twist` cubic (k1, k2, max angle), **evaluated at the Bézier parameter t of the radius curve**: twist(z) = cubic(t(z)). The radius control points therefore also reshape the twist over height | 3 |
| **Total** | | **15** |

Own settings (`../FulLTextureLamp`): N = 23 per quarter, H = 2.0 mm (`scale_perp` 0.20 cm), equal angle with a half
tooth at 0° (`generate_polar_triangles_by_count`), 30 sections uniform in Bézier t (t = i/29).
Base: the script in `../` now draws the rose; the user's scenario says the custom spline, so M03 uses it (docs/05 §5.4).
Start: the script's control points P0 (80, 0), P1 (92.5, 10), P2 (106, 25), P3 (102, 35), P4 (140, 50), P5 (115, 120),
P6 (43, 190); k1 = 0, k2 = 0.80, max 90°. Penalty 20·min(Δz_controls, 0); constraint: z(t) monotone.
Start scores: front 0/19, 3/4 1/19, ribs 20.6 mm (the designer's values are far from the drawing; the twist rises
too early because t runs fast through the lower part of the curve).

## Hypothesis (written before running)
- Same base and same twist family as M01; the differences are the radius (one global degree-6 Bézier instead of
  11 local keys) and that the twist is read at t, not z/190. The t(z) map is a reparametrisation the radius points
  control, so the twist is effectively more flexible than M01's (≈ 3 + some of the 10 inner coordinates), but it is
  **coupled to the outline**: every move that reshapes the twist also reshapes r0.
- Outline: a 7-point Bézier can follow the bulge and neck but not the rounded rim flare (S01–S03) and probably not
  the shoulder/neck curvature change as well as 11 keys. Expect the outline to be a bit worse than M01.
- Ribs: the extra twist freedom through t(z) should help the waist/shoulder (S09–S17) somewhat versus M01, but the
  coupling means the optimiser trades outline against ribs. Net: about M01's level, front ≈ 2–5/19.
- 3/4 (held out): ≈ 10–14/19, like M01 (same base).
- Risk: the start is very far (ribs 20 mm); the fit may stop in a local minimum or hit the nfev cap.
- Locality (E4b/E5b): low for both curves, ≈ 0.2–0.35 (all parameters are global).
- E6: 30 sections uniform in t are dense; as built ≈ exact. Bézier-t sections bunch where dz/dt is small.

## Conclusions (after running)
Kernel **v2** (multi-start E0 + coarse first fit stage, `models/_common/PROGRESS.md` "kernel v2"). E0–E6 and
`summary.json` re-run by the orchestrator under v2. All numbers as built (30 Bézier-t sections) unless noted.

**E0 fit** — front **14/19**, 3/4 **13/19**; outline max 0.81 mm, ribs **0.48 mm / 92 %** ≤ 1 mm, 3/4 mean 0.75 mm
(exact: 14/19, 13/19, outline max 0.78). 15 params, cost 84.5, 59 s, best start pool:M05_E0, no cap hit, constraints OK.
Start costs: own start 84.6, M05_E0 84.5, M02_X1c 85.2, M01_E0 186.3. Three of the four starts reach the same
minimum, so the v1 result (6/19) was a stall of the fine-step fit, not the start: v2's coarse stage
(diff_step 1e-2) is what fixed it. Fitted: P0 (80.8, 0), P1 (90.1, 4.3), P2 (148.7, 62.1), P3 (102.5, 91.3),
P4 (123.0, 114.4), P5 (69.0, 163.9), P6 (43.7, 190); k1 −0.16, k2 0.90, max 88.8°.

**E1 triangle count** (N 12/16/22/23/30/45) — ribs unchanged (0.48 mm); outline bias −0.49 / −0.20 / −0.02 / 0 / +0.08 /
+0.15 mm. Front 6/11/14/14/14/13, 3/4 8/10/12/13/12/12. N 22–30 is flat; the own N = 23 is at the optimum.

**E2 width × placement** — angle_half fill 0.5→1.0: outline +0.11 → 0 mm, front 13–14/19, 3/4 11–13/19. Arc placement:
outline max 0.67–0.73 (better rim), front 13–14/19, but 3/4 drops to 8–10/19. The own setting (angle_half, f = 1) is best.

**E3 triangle height** — 1 : 1 outline shift (H 1.5 → −0.50 mm, H 3 → +1.00 mm). Front 3 / **14** / 0 / 0 / 0 for
H 1.5 / 2 / 3 / 4 / 5: the fitted radius is tuned to H 2.0; 0.5 mm off loses almost every segment.

**E4 twist** — ×0.97 / ×1.03: rib mean +0.83 / +0.79 mm, front 4 / 4/19 (×1.03 keeps 3/4 13/19). ×0.94 / ×1.06: ribs
+2.0 mm. Bumps: locality **0.37**, median achieved 0.24 of 1°. No local twist control (3 global params + t(z)).

**E5 radius** — ±1 mm offset: front 0/19 both ways (outline bias ±0.95 mm; −1 mm also +0.31 mm ribs). Bumps: locality
**0.39**, median achieved 0.26 of 1 mm. A 1 mm local change spreads over ~5–6 segments.

**E6 sections** — Bézier-t: max loft deviation 0.63 / 0.39 / 0.24 / 0.15 / 0.05 / 0.02 mm at 8/11/15/20/30/39; adaptive
20 → 0.09, uniform-z 20 → 0.36 mm (the steeper v2 curve needs better-placed sections). Pass counts stay 13–15/19 front,
12–14/19 3/4 at every level. Buildability gate (best placement ≤ 20 sections): 0.09 mm → **buildable**.

### Segments, limits, hypothesis (kernel v2)
- **Front pass (14)**: S02–S07, S12–S19. **Fail (5)**: S01 (rim outline max 0.81 / bias +0.55, the rounded drawn rim
  edge that fails for every model); S08–S11, the **waist**: S08 within-1 mm 77 %, S09 ribs 1.00 mm / 71 %, S10 ribs
  0.72 / 78 %, S11 outline bias −0.54 / max 0.78.
- **3/4 pass (13)**: S04–S12, S14, S15, S17, S18. **Fail**: S01–S03 (rim, 0.98–1.62 mm), S13 0.76, S16 0.78, S19 0.96.
- **Main limitation: the twist at the waist (S08–S11)**, with the radius trading against it. A 3 % twist change costs
  ~0.8 mm of rib and a 1° bump can't be made locally (0.24 achieved, locality 0.37). The radius is coupled to the
  twist through t(z): S11's outline bias −0.54 mm is where the optimiser pulled r0 in to keep the waist ribs. The fixed
  base (no lobe-depth change) adds nothing to tune there either. Rim (S01) is a drawing-edge limit, not the model.
- **What t(z) does**: t leads z/190 in the lower half (t = 0.22 at z 30, 0.31 at 50, 0.51 at 90; z/190 = 0.16, 0.26,
  0.47), so the same cubic rises earlier: twist 4.3° / 12.8° / 36.7° at z 30 / 50 / 90 vs 0.7° / 7.9° / 32.3° for the
  same (k1, k2, max) at z/190. That front-loading is the extra twist freedom the radius points give the cubic.
- **vs M01 (v2: front 3/19, 3/4 13/19, ribs 0.67 mm, outline max 2.27 mm)**: same base, same twist formula, keyframe
  radius at z/190. M03 is far better on the front (14 vs 3/19): shoulder/neck ribs S12–S19 0.38–0.68 mm vs 1.00–1.29,
  rim and neck outline 0.81 / 0.13 mm vs 2.27 / ≈1.35. The two twists differ by only 1–2° (M03 lower from z 30 to 150,
  both ≈ 89° at the top), and that small difference is worth ~0.6 mm of rib: M01's cubic at z/190 can't make that
  shape, M03's cubic at t(z) can. 3/4 is equal (13/19). Locality: M03 twist 0.37 vs M01 0.21, radius 0.39 vs 0.63.
- **Hypothesis**: mostly wrong, in M03's favour. Held: locality low (0.37–0.39, just above the predicted 0.2–0.35),
  3/4 within the 10–14 guess (13), the start was far and could stall (it did under v1). Wrong: I expected the coupled
  twist to give only "about M01's level, front 2–5/19" and an outline worse than M01; under v2 the t(z) coupling is a
  real advantage (front 14/19, ribs 0.48 mm) and the outline is better than M01's. I also expected E6 as built ≈ exact
  at all counts; with the v2 curve, uniform-z sections need ≥ 30 (0.24 mm) while Bézier-t/adaptive reach ≤ 0.15 mm at 20.

### Superseded (kernel v1)
Kernel v1. All numbers as built (30 Bézier-t sections) unless noted; exact curves give front 6/19, 3/4 11/19.

**E0 fit** — front **6/19** (S03–S08), 3/4 **10/19** (S04–S08, S14–S18); outline max 1.02 mm, ribs 0.64 mm / 83 % ≤ 1 mm,
3/4 mean 0.76 mm. 15 params, 25 s, nfev 19, cap not hit, constraints OK. Start was front 0/19, ribs 20.6 mm.
Fitted: P0 (81.7, 0), P1 (94.8, 11.7), P2 (124.0, 37.6), P3 (117.5, 74.6), P4 (122.2, 95.6), P5 (104.9, 128.1),
P6 (43.9, 190); k1 −0.08, k2 0.46, max 93.1°. The designer's P4 (140, 50) bulge moved up and in.

**E1 triangle count** (N 12/16/22/23/30/45) — ribs unchanged (0.64 mm); outline bias −0.49 mm at N 12, −0.20 at 16,
+0.08 at 30, +0.15 at 45. Front 2/5/6/6/6/6, 3/4 9/11/9/10/10/10. N ≥ 22 is flat; 23 is fine.

**E2 width × placement** — angle_half fill 0.5→1.0 shifts the outline by ≤ +0.19 mm, front stays 6/19. Arc placement
gives front 7/19 (outline max 1.02 → 0.80–0.89 mm, the S01 rim), but 3/4 drops to 8–10/19. Placement is a small lever.

**E3 triangle height** — 1 : 1 outline shift (H 1.5 → −0.50 mm, H 3 → +1.00 mm). H 2.0 is the only level with ≥ 6/19
front; H 1.5 gives 3/19 front but 12/19 3/4 (the 3/4 view wants the outline ~0.3–0.5 mm smaller in S09–S13).

**E4 twist** — ×0.97 / ×1.03 raise rib mean by +0.72 / +0.60 mm and drop front to 4 / 3/19 (×1.03 gives 3/4 14/19).
Very sensitive: 3 % of twist ≈ 1 mm of rib. Bumps: locality **0.39**, median achieved 0.26 of 1° — the 3 twist
parameters plus the t(z) map can't make a local bump; the end knots are slightly better (0.54–0.73).

**E5 radius** — ±1 mm offset: front 0/19 both ways, outline bias ±0.95 mm. Bumps: locality **0.40**, median achieved
0.32 of 1 mm (best at the rim, 1.12 at z = 0, locality 0.78). Global Bézier: a 1 mm bump spreads over ~6 segments.

**E6 sections** — the loft is never the problem here: Bézier-t 30 → 0.00 mm, uniform-z 11 → 0.04 mm, 8 sections
≤ 0.28 mm. The smooth 7-point Bézier is easy to loft. Pass counts 6–7/19 at every count and placement.

### Segments, limits, hypothesis
- **Pass front**: S03–S08. **Fail**: S01–S02 (rim outline: S01 max 1.02 / bias +0.68, S02 bias +0.33 — the rounded drawn
  rim edge, same for every model); S09–S19 on **ribs** (rib mean 0.68–1.58 mm, within-1 mm 28–85 %; S12–S13 also
  outline bias +0.39/+0.14). Worst: S18–S19 (ribs 1.31 / 1.58 mm, 28–32 % within 1 mm).
- **Limiting part: the twist.** The outline is good from S02 up (max ≤ 0.50 mm, S03–S19 all ≤ 0.5). The ribs fail
  from the waist up because the twist is a 3-parameter cubic; reading it at Bézier t only adds a mild reparametrisation
  (t(z) is nearly linear above z ≈ 40 mm: t = 0.38 at 50, 0.66 at 100, 0.88 at 150). The fitted twist is within
  1–4° of M01's over the whole height (93° vs 89° at the top). The fixed base can't help either (no lobe-depth change).
- **vs M01** (same base, same twist formula, keyframe radius at z/190): M03 is better, front 6 vs 3/19, outline max
  1.02 vs 2.30 mm (S01 rim 1.02 vs 2.30, neck S18–S19 0.27/0.29 vs 0.87/1.35), shoulder ribs S11–S16 0.71–0.89 vs
  1.02–1.29 mm. 3/4 is worse (10 vs 14/19: S09–S13 0.77–0.96 mm vs M01's 0.34–1.13). M03 has 15 params vs 14, and
  better locality (0.39 vs M01's 0.21 twist / 0.63 radius — radius locality is worse, twist better through t(z)).
  The gain is mostly the smoother, better-placed rim/neck radius plus small twist shifts, not a new twist shape.
- **Hypothesis**: partly held. Correct: twist is the limit (ribs fail S09–S19), locality is low (0.39–0.40, close to the
  predicted 0.2–0.35 band), E6 shows as built ≈ exact. Wrong: the outline was *better* than M01, not worse (the
  7-point Bézier follows the rim and neck better than 11 Catmull-Rom keys), and front 6/19 beat the 2–5/19 guess.
  3/4 10/19 is at the low end of the 10–14 guess. The start was far (ribs 20.6 mm) but the fit converged without a cap.


## Final round — kernel v3 (2026-11-24): orientation offset + pool round 2
These are the numbers the judge uses. The conclusions above were written under kernel v1/v2, without the free orientation offset.

| | value |
|---|---|
| Rank / score | **1 / 10**, 0.706 |
| Front (as built) | **14/19** `·██████····████████` |
| 3/4 held out | **14/19** `····██████████████·` |
| Ribs | 0.43 mm mean, 92 % ≤ 1 mm |
| 3/4 mean / outline max | 0.74 mm / 0.76 mm |
| Fit cost (best of 14 starts) | 72.9 from `pool:M07_E0v2` |
| Orientation offset | -1.33° |
| Locality twist / radius | 0.42 / 0.41 |
| Parameters | 16 (incl. the offset) |
| Buildable | yes (loft deviation 0.00 mm, best placement ≤ 39 sections) |
