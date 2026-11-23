# M06 — rose base + 10 mm knots for radius and twist

## Definition
| Part | Representation | Parameters |
|---|---|---|
| Base | 4-petal rose `(1 + k cos4θ)/(1 + k)`, lobe depth k(z) Catmull-Rom through 6 nodes (z = 0, 38 … 190), as M05 | 6 |
| Radius r0(z) | value knots every 10 mm (z = 0, 10 … 190), Catmull-Rom (`curves.catmull_keys`) | 20 |
| Twist | value knots every 10 mm, Catmull-Rom, twist(0) = 0 fixed | 19 |
| **Total** | | **45** |

Penalties: `SMOOTH_W` × 2nd difference of the r (0.05/mm), twist (0.05/°) and k (2.0) knots; k soft floor
`50·min(k − 0.02, 0)` (as M05). Bounds: r 20–160 mm, twist −30…150°, k 0–0.45. Constraints: k(z) in 0.02–0.4, r0 ≥ 20 mm.
Knot curves are value-only Catmull-Rom (kernel v1 decision), not Hermite with slopes: one knot reaches 4 segments.

Settings (inherit M05, docs/05 §5.4): N = 22, H = 3 mm, equal arc length (9 mm target), **20 sections on the 10 mm knots**.
Start values: the M05 E0 fit sampled at the knots (r0, twist) and M05's fitted k values, baked into `model.py`.
The start equals M05's curves within 0.02 mm / 0.12° in S02–S18; only S01 (twist 1.0°, r 0.76 mm) and S19 (r 0.77 mm) differ.
Because ribs are anchored at their drawn start near the rim, that 1° in S01 doubles the start rib error (1.6 vs 0.71 mm).

Direct comparison: **M05** has the same base, settings (except 15 uniform sections) and protocol; only the curve
representation differs (27 → 45 parameters).

## Hypothesis (written before running)
- The fit will beat M05 on the front: ribs and outline in the waist S08–S12 should improve, because a twist knot can
  add local twist there without disturbing the bulge and shoulder. Expect front ≈ 11–14/19 (M05: 8/19).
- S01 will still fail on the outline (rounded rim corner, kernel known limit). Some neck segments (S16–S19) may stay
  limited by the rib traces and the fixed-k rose, not by the curves.
- Locality (E4b/E5b) will be high, ≈ 0.6–0.8: a Catmull-Rom knot reaches 4 segments but most of its effect lies in the 2
  adjacent ones (M05: twist 0.26).
- The 3/4 view (held out) will **not** improve in proportion, and may get slightly worse in some segments: the extra
  twist/radius freedom will partly fit front-drawing noise (rib tracer noise ~0.25 mm, outliers > 1 mm). Expect 3/4
  ≈ 6–10/19 (M05: 7/19).
- 20 sections on the knots: the loft passes exactly through the knot values, so as-built ≈ exact (≤ 0.1 mm);
  E6 should show uniform_z 20 ≈ knots10.
- Main remaining limit: the base (rose with only 6 k nodes) where the drawing's lobe shape differs from a rose.
- Note: kernel v1's sweeps E4a ×0.94 and E3/E5a offsets will behave like M05 (global sensitivities don't depend on representation).

## Conclusions (after running)
All numbers are kernel v2 (multi-start E0, 3 stages), as built unless marked. M05 numbers are its kernel-v2 E0
(`models/M05_rose_bezier/E0_fit/metrics.json`: front 5/19, 3/4 9/19, cost 163.8). A first E0 on kernel v1 (front 4/19,
3/4 8/19, cost 202.8) is superseded and logged in `PROGRESS.md`.

**E0.** Front **5/19** (S03–S07), 3/4 **10/19**, exact curves 6/19 / 9/19. Ribs 0.75 mm / 75 % ≤ 1 mm, outline max
2.36 mm (S01), 3/4 mean 0.95 mm. All 4 starts (own, pool M01/M05/M02) end at cost 194.8–195.1, so this is a stable
minimum, not a start artefact; no cap hit (nfev ≤ 15 per stage), constraints OK, 145 s.
M05 under the same protocol: front 5/19 (also S03–S07), 3/4 9/19, ribs 0.68 mm / 81 %, **cost 163.8 < M06's 194.8**
although M06 has 45 vs 27 parameters and its knots can reproduce M05's curves in S02–S18 within 0.02 mm.

**E1 (N).** N = 16 gives front 6/19, N = 22 (own) 5/19, N = 30/45 give 3/4 11/19 and 12/19 but front 4/19. Outline bias
shifts −0.30 (N 12) … +0.18 mm (N 45); ribs unchanged. Same picture as M05.

**E2 (fill × placement).** Arc f = 1.0 (own) is best on the front (5/19). Lower fill adds +0.05…+0.13 mm bias.
Angle-half placement: ribs −0.01 mm, outline max 2.73, front 4/19. Small lever.

**E3 (H).** Outline shifts 1:1 (−1.50 … +2.00 mm); only H = 3.0 (the fitted one) passes any front segment. Ribs unchanged.

**E4 (twist).** ×0.97 / ×1.03 → ribs +0.69 / +0.51 mm, front 3/19; ×0.94 / ×1.06 → ribs +1.9 / +1.5 mm.
**E4b locality 0.93** (achieved bump 0.89 of 1°; knot z = 0 is fixed, so its row is 0). M05: 0.37 (summary, kernel v1).

**E5 (radius).** ±1 mm → front 0/19 (outline bias ±0.94), ribs +0.27 / +0.06 mm. **E5b locality 0.96**
(achieved 0.89 of 1 mm). M05: 0.58.

**E6 (sections).** knots10 (own) = uniform 20: loft deviation from the exact curves max **0.73 mm** / mean 0.053;
interior S02–S18 ≤ 0.08 mm, but **S01 0.66 and S19 0.73 mm**. Cause: the kernel's Catmull-Rom duplicates the end knot,
so the end intervals [0, 10] and [180, 190] bend differently from the smooth spline the loft draws through the same
knot values (r0 differs by up to 0.74 mm at z = 187, twist 0.33° at z = 3). 39 uniform sections bring it to 0.08 mm.
Front/3/4 pass counts barely move (5–6 / 8–11) because S01 and S19 fail anyway. The summary's buildability gate
(loft_dev_20 ≤ 0.3 mm) **fails** for this reason; M05 is 0.03 mm.

### Segments
- Front pass: S03–S07 (same as M05). Fail: S01 (rim outline, +1.26 mm bias, kernel known limit), S02 (outline bias
  +0.31), S08–S19 on **ribs** (S08 0.75 / 70 %, S09 1.20, S10 0.97, S11 1.03, S12–S19 1.10–1.39 mm). Outline (max ≤ 0.75,
  |bias| ≤ 0.3) passes S03–S18 except S15 (bias +0.31); S19 fails (+0.42).
- 3/4 pass: S04, S05, S11–S16, S18, S19 (10). Fail: S01–S03, S06–S10, S17. Worst S09 2.10, S10 1.66, S08 1.45 mm.

### Compared with M05 (same base and settings, only the curve representation differs)
- **Waist S08–S12: local control does not fix it.** Rib mean S08–S10 improves (0.94/1.46/1.19 → 0.75/1.20/0.97 mm) but
  S11/S12 get worse (0.98/1.00 → 1.03/1.23) and no waist segment passes. The signed per-rib errors in S09 have
  mixed signs across the width (x0 = −70: −1.6, −20: −1.3, 0: +2.8, +9: +0.5, +41: −4.6 mm). A twist or radius knot
  moves all ribs of a segment the same way, so it can't remove errors of opposite sign between neighbouring ribs.
  The waist limit is the **base** (how the ribs are distributed around a lobe: rose shape / arc placement), or the
  drawn rib traces themselves, not the radius or twist curves.
- **Upper ribs got worse** (S12–S19: 0.8–1.0 → 1.1–1.4 mm). Cause: twist(0) = 0 is fixed, the value-only Catmull-Rom
  cannot make M05's fast −0.9° dip at the rim (M05 twist(2.2 mm) = −0.94°, M06 −0.02°), and every rib is anchored at
  its drawn start z0 = 2.2 mm. The fit has to choose between the absolute twist (outline, 3/4) and the twist relative to
  the rim (ribs). Diagnostic (scratch, kernel-v1 protocol, not official): the same model with **twist(0) free** (46
  params) reaches cost 159 (below M05), front 6/19, 3/4 9/19, ribs 0.65 mm, twist(0) = −1.08°.
- **Locality is real**: 0.93 / 0.96 vs M05 0.37 / 0.58. Every segment can be moved alone; it just doesn't help where
  the error is not a common shift.
- **3/4 (held out)**: 10/19 vs 9/19, mean 0.95 vs 0.93 mm. It gets better in S04, S05, S11, S12, S15 and worse in
  S02, S07–S10 (S09 1.70 → 2.10). The waist is where M06 bought front-rib improvement with knot freedom, and there the
  held-out view gets worse: that is the drawing-noise fit the plan warned about, but it is local and small overall.
- Smoothness: r0 4 and twist 8 curvature sign changes (judge score 0.18; M05 0 / 0). The twist steps per 10 mm
  wiggle by ~0.6° (6.89 → 6.31° at 100–110 mm), invisible in the outline but counted by the judge.

### Did the hypothesis hold?
- Front 11–14/19: **no** (5/19, same as M05). Local twist/radius control is not what limits the waist.
- S01 fails: yes. Neck limited by ribs: yes, and worse than M05 because of the fixed rim twist.
- Locality 0.6–0.8: **exceeded** (0.93 / 0.96).
- 3/4 not improving in proportion: yes (10 vs 9, and worse exactly at the waist).
- As built ≈ exact on the knots: **no at the ends** (0.66 / 0.73 mm in S01 / S19, Catmull-Rom end intervals); yes inside.
- Base as the remaining limit: yes (mixed-sign rib errors in one segment).

### What would help (for the orchestrator, not done here)
Free twist(0) (or a knot at z = 5 mm); a not-a-knot/natural spline or extra sections at z = 5 and 185 mm to make the loft
follow the end intervals; a base with more freedom in the lobe shape (M07/M08) for the waist ribs.


## Final round — kernel v3 (2026-11-24): orientation offset + pool round 2
These are the numbers the judge uses. The conclusions above were written under kernel v1/v2, without the free orientation offset.

| | value |
|---|---|
| Rank / score | **7 / 10**, 0.488 |
| Front (as built) | **7/19** `·██████·······█····` |
| 3/4 held out | **10/19** `·█···██···██··█████` |
| Ribs | 0.66 mm mean, 78 % ≤ 1 mm |
| 3/4 mean / outline max | 0.94 mm / 2.49 mm |
| Fit cost (best of 14 starts) | 160.0 from `pool:M04_E0v2` |
| Orientation offset | -1.06° |
| Locality twist / radius | 0.96 / 0.96 |
| Parameters | 46 (incl. the offset) |
| Buildable | yes (loft deviation 0.06 mm, best placement ≤ 39 sections) |
