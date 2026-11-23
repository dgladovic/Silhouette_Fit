# M01 — scenario 1: custom spline base + keyframe radius + cubic twist

## Definition
| Part | Representation | Parameters |
|---|---|---|
| Base | the custom spline (`r_mults` / `phi_increments`, degree-5 control-point spline, 0–45° mirrored), **fixed over height** | 0 |
| Radius r0(z) | `bez_points` keyframes at t = 0, 0.1 … 1 (t = z/190), Catmull-Rom (`smooth_spline_interpolation`) | 11 |
| Twist | `calculate_bezier_twist`: 90°-style cubic, free k1, k2, max angle, at t = z/190 | 3 |
| **Total** | | **14** |

Own settings (`../BaseScript`): N = 22, H = 2.4 mm, equal angle with a half tooth at 0°, 11 uniform sections
(= on the keyframes). Start: BaseScript's `bez_points`, k1 = 0, k2 = 0.95, 90°.
Gate C: the kernel reproduces the BaseScript Fusion build (F1-4) within 0.05 mm mean / 0.2 mm max.

## Hypothesis (written before running)
- The radius keys are flexible enough for the outline (11 keys ≈ one per 19 mm).
- The **2-parameter cubic twist is too stiff**: one S-curve shape for the whole height. Expect the ribs to fail in
  several bands (waist and neck), and the outline to fail at the waist, where it is most twist-sensitive.
- The base can't change lobe depth with height. Rib positions inside a lobe will drift where the drawing's lobes
  get shallower or deeper.
- Locality: radius keys medium (Catmull-Rom reaches ~4 keys); twist ≈ 0 (3 global parameters).
- Expected: front ≈ 4–7/19.

## Conclusions (after running, kernel v1, 2026-11-23)

**E0 (as built): front 3/19, 3/4 14/19** · ribs 0.67 mm mean, 80 % ≤ 1 mm · outline max 2.30 mm · 3/4 mean 0.75 mm.
Start (BaseScript values): front 2/19, ribs 1.38 mm. The fit mostly fixed the twist (k1 0 → 0.001, k2 0.95 → 0.90, max 90 → 89.0°).
- **Lower half: best ribs of any model so far** (S01–S08 rib mean 0.13–0.61 mm, S01–S05 100 % ≤ 1 mm).
  But **S07–S19 fail on ribs** (54–78 % ≤ 1 mm, 0.96–1.29 mm above z = 80): one 3-parameter S-curve can't follow the twist
  both below and above the waist.
- Outline: rim/foot S01–S03 too wide (+1.66/+0.78/+0.46 bias) and neck S18–S19 too wide (+0.58/+1.11). 11 radius keys can't
  bend tightly enough at the ends. Mid-height outline is fine.
- **Held-out 3/4 view: 14/19, best so far** (M05: 7/19). The stiff model can't chase the front drawing's details, and the
  custom spline base may also suit the 3/4 view better. Open question for the judge.
- E1: N changes the outline −0.47 … +0.17 mm. Ribs unchanged. E2: fill/placement ≤ 0.13 mm.
- E3: H = 2.0 is better than its own 2.4 (outline −0.40 → 3/4 15/19, outline max 1.90): the historical tooth height
  was slightly too big for the drawing with this radius.
- E4: twist bump locality **0.21**, achieved 0.15 of 1°. A 3-parameter curve has no local control at all.
- E5: radius keys locality 0.63 (Catmull-Rom keys reach ~2 keys either side), achieved 0.49 of 1 mm.
- E6: equal-angle teeth at **8 sections deviate up to 1.72 mm** from the exact curves (0.26 at 20, 0.05 at 39). The
  historical 11 sections are borderline. More sections don't change the pass count, though.

**Hypothesis check**: right that the cubic twist is too stiff (upper half ribs fail) and on locality. Wrong on the outline:
the radius keys are *not* enough at the rim and neck ends. Surprise: best held-out 3/4 view.
**Main limitation: twist (3 global parameters).**


## Final round — kernel v3 (2026-11-24): orientation offset + pool round 2
These are the numbers the judge uses. The conclusions above were written under kernel v1/v2, without the free orientation offset.

| | value |
|---|---|
| Rank / score | **4 / 10**, 0.623 |
| Front (as built) | **10/19** `···████····██████··` |
| 3/4 held out | **13/19** `······█████████████` |
| Ribs | 0.43 mm mean, 92 % ≤ 1 mm |
| 3/4 mean / outline max | 0.83 mm / 2.09 mm |
| Fit cost (best of 14 starts) | 91.1 from `pool:M01_E0` |
| Orientation offset | -1.45° |
| Locality twist / radius | 0.26 / 0.63 |
| Parameters | 15 (incl. the offset) |
| Buildable | yes (loft deviation 0.04 mm, best placement ≤ 39 sections) |
