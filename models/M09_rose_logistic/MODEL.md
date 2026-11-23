# M09 — rose (constant k) + 2D Bézier radius + logistic twist (minimal baseline)

## Definition
| Part | Representation | Parameters |
|---|---|---|
| Base | 4-petal rose `(1 + k cos4θ)/(1 + k)`, **one constant k** over height (`bases.rose(k)`), bounds 0.05..0.4 | 1 |
| Radius r0(z) | 8-point 2D Bézier (r, z), P0 at z = 0, P7 at z = 190 (`curves.BezierRZ`), exactly as M05; penalty 20·min(Δz, 0), monotone constraint | 14 |
| Twist | logistic S-curve `curves.logistic_twist(z, total, centre, width)`, z in mm, normalised to 0 at z = 0 and `total` at z = 190; bounds total 45..135°, centre 20..170 mm, width 3..80 mm | 3 |
| **Total** | | **18** |

Settings (inherit M05): N = 22, H = 3 mm, equal arc length (9 mm target), 15 uniform-z sections (M05's own).
Start values (baked into `model.py`): radius points = M05 E0 (kernel v2); k = mean of M05's six fitted k nodes = 0.201;
logistic = least squares on M05's E0 twist (z = 0..190, 1 mm): total 88.68°, centre 102.4 mm, width 34.6 mm.
Match: rms 0.93°, **max |Δ| 2.26° at z = 14 mm** (M05's Bézier twist dips to −0.6° near the rim; a logistic is monotone).
Start score (as built): front 1/19, 3/4 7/19, ribs 1.44 mm / 45 % — the start is clearly off before refitting
(the twist sensitivity is ~0.7 mm rib mean per 3 % twist, see M05 E4).

Purpose: the deliberately minimal baseline. Same radius representation and settings as M05, so M09 vs M05 isolates what
k(z) (6 → 1 params) and the 5-point Bézier twist (7 → 3 params) buy.

## Hypothesis (written before running)
- M09 will land **close to M05** (front 5/19 under v2): within ±2 segments, which is optimiser noise. M05's fitted k(z)
  only varies 0.17–0.22 and its twist is already almost a monotone S-curve, so the extra 9 parameters buy little.
- Rib mean will be slightly worse than M05 (0.68 mm) — expect 0.70–0.80 mm — mainly in the waist S08–S12 and the neck
  S16–S19, where the symmetric logistic cannot make the twist rate different below and above the centre.
- The bulge S02–S07 passes (it passes for every rose model; mostly outline + small twist).
- It will **not** reach M03 (14/19) or M02 (12/19): those have a custom base and different twist parametrisations.
  If M09 does come close to them, the base shape is not what limits the rose models.
- 3/4 view: similar to M05 (≈ 8–10/19).
- Locality: twist ≈ 0.2 (3 global parameters, the bump can only shift centre/width), radius ≈ 0.5–0.6 (same Bézier as M05).
- E6: sections are not a lever (≤ 0.15 mm loft deviation at 8+ sections, as M05).

## Conclusions (after running, kernel v2, 2026-11-23)

**E0 (as built): front 2/19, 3/4 9/19** · ribs 1.10 mm mean, 56 % ≤ 1 mm · outline max 1.49 mm (rim S01) · 3/4 mean 0.96 mm · cost 327.0.
Front strip `....YY.............`, 3/4 strip `..YYYY....Y...Y.YYY`. Best start: pool M01_E0 (327.0; own 330.5, M05 330.2, M02 X1c 339.1).
Fitted: k = 0.195, total 88.6°, centre 100.6 mm, width 36.2 mm. A stall check (restart + 3 extra starts) lands in the same
basin (326.8–329.6, rib 1.10 mm), so this is the model's real minimum.
- **The outline is fine almost everywhere** (|bias| ≤ 0.38 mm except S01 +0.90 rim edge and S10 −0.58): the Bézier radius
  is the same as M05's and does its job. **Every failure except S01 is a rib failure**: S02–S04 (1.03–1.25 mm) and
  S07–S19 (0.85–1.64 mm, 34–56 % ≤ 1 mm). Only S05–S06, where the logistic passes through M05's twist, pass.
- E1 triangle count: N 12 → 45 shifts the outline −0.31 → +0.18 mm, ribs unchanged; front 1–2/19 at every level (same as M05).
- E2 width/placement: fill 0.5 +0.13 mm outline; equal-angle placement changes the ribs by 0.00 mm (constant k: rose
  placement cannot shift ribs relative to M05's +0.03) and the outline up to +0.33 mm at single segments.
- E3 height: 1.00 mm outline per mm, uniform; any H ≠ 3 drops the front to 0–1/19 (radius fitted for H = 3).
- E4 twist: ×0.97 / ×1.03 → ribs 1.54 / 1.40 mm (+0.59 / +0.40). 1-knot bumps: **locality 0.21**, median achieved bump
  0.15 of 1° (M05 0.37 / 0.25): 3 global parameters can only slide or stretch the S-curve.
- E5 radius: ±1 mm → bias ±0.95 mm, front 0–1/19. 1-knot bumps: **locality 0.57**, achieved 0.52 of 1 mm (= M05's 0.58: same Bézier).
- E6 sections: loft deviation at 15 uniform sections max 0.49 mm, **all in S01** (S01 0.49, S02 0.17, rest ≤ 0.07): the fit put
  two Bézier points close to the rim (P1 z = 15, P2 z = 25, r 93 → 126), a sharp rim flare 15 sections can't follow. 20 Bézier-t
  sections: 0.09 mm (gate passed, buildable). The pass counts don't move (front 2/19 at every count and placement).

**Comparison with M05 (same radius and settings, 27 vs 18 params)**: M05 front 5/19, ribs 0.68 mm / 81 %, cost 163.8 →
M09 front 2/19, ribs 1.10 mm / 56 %, cost 327.0. The 3/4 view is equal (9/19; 0.93 vs 0.96 mm). Swapping parts on the
fixed curves (exact, front camera) splits the cost of the reduction:
- **constant k instead of k(z)** (M05 E0, k := 0.201): rib 0.67 → 0.86 mm, front 5 → 2; the damage is in S10–S17 (+0.2..0.5 mm).
  M05's k(z) varies only 0.17–0.22, yet that small variation moves ribs inside the lobe by up to 0.5 mm.
- **logistic instead of the 5-pt Bézier twist**: M09 E0 with M05's twist swapped in → rib 1.10 → 0.87 mm. The logistic can't
  make the slightly negative twist near the rim (M05 −0.6° at z = 10, M09 +1.8°) and is symmetric about its centre, so the
  rate below and above the waist are tied. 1° at r ≈ 110 mm moves a rib ≈ 1.9 mm, so a 2° shape error is fatal for ribs.
- So both extra pieces of M05 are real, not noise: each is worth ≈ 0.2 mm of rib mean. The 9 extra parameters buy 3
  front segments and 25 % more rib points within 1 mm, at the same 3/4 score.

**Comparison with M01 / M03 (3-parameter cubic twist on the fixed custom base)**: M01 (14 params) ribs 0.67 mm, front 3/19;
M03 (15 params) ribs 0.49 mm, front 14/19. With about as many parameters, M09's rose + logistic is clearly worse on ribs
(1.10 mm). The cubic `max·(3(1−t)²t·k1 + 3(1−t)t²·k2 + t³)` is asymmetric (k1 ≈ 0 gives a flat start, k2 sets the top),
which the logistic can't do; and the custom spline base fixes the rib position inside the lobe better than a constant-k rose.
M03 shows a minimal twist works when it is the *right* 3-parameter family (and evaluated at Bézier t).

**Where it fails and why**: front fails S01 (rim edge, outline, every model) and S02–S04, S07–S19 (ribs). Limited by the
**twist family first** (wrong shape near the rim and asymmetric rate), **the constant base second** (S10–S17 ribs).
The radius is not the limit (outline passes everywhere except S01/S10).

**Hypothesis check**: wrong on the main claim. M09 is not close to M05: ribs 1.10 vs 0.68 mm, front 2 vs 5/19 (just outside
the ±2 optimiser-noise band, and the rib gap is far larger than noise). The extra parameters of M05 fit real shape, not drawing noise. Right on: the bulge passing (partly,
S05–S06 only), not reaching M02/M03, 3/4 similar to M05 (9/19), twist locality low (0.21), radius locality like M05 (0.57),
E6 not a lever for the pass count. Wrong on the rib mean (expected 0.70–0.80) and on S02–S04, which fail on the near-rim twist.


## Final round — kernel v3 (2026-11-24): orientation offset + pool round 2
These are the numbers the judge uses. The conclusions above were written under kernel v1/v2, without the free orientation offset.

| | value |
|---|---|
| Rank / score | **10 / 10**, 0.353 |
| Front (as built) | **1/19** `····█··············` |
| 3/4 held out | **7/19** `·██···█····█····███` |
| Ribs | 0.97 mm mean, 62 % ≤ 1 mm |
| 3/4 mean / outline max | 0.85 mm / 0.99 mm |
| Fit cost (best of 14 starts) | 262.1 from `pool:M01_E0v2` |
| Orientation offset | -1.28° |
| Locality twist / radius | 0.27 / 0.57 |
| Parameters | 19 (incl. the offset) |
| Buildable | yes (loft deviation 0.00 mm, best placement ≤ 39 sections) |
