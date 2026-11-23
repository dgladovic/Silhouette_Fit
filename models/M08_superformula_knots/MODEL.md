# M08 — superformula base n1(z), n2(z) + 10 mm knots for radius and twist

## Definition
| Part | Representation | Parameters |
|---|---|---|
| Base | 4-fold superformula `(|cos θ'|^n2 + |sin θ'|^n2)^(-1/n1)`, θ' = θ + 45°, normalised to 1 at the tip (`bases.superformula`); n1(z) and n2(z) each Catmull-Rom through 6 nodes (z = 0, 38 … 190) | 6 + 6 |
| Radius r0(z) | value knots every 10 mm (z = 0, 10 … 190), Catmull-Rom (`curves.catmull_keys`) | 20 |
| Twist | value knots every 10 mm, Catmull-Rom, twist(0) = 0 fixed | 19 |
| **Total** | | **51** |

Penalties: `SMOOTH_W` × 2nd difference of the r (0.05/mm) and twist (0.05/°) knots; **0.2 × 2nd difference of n1 and of n2**
(orchestrator's weight, because n1/n2 have other units than k); soft floor `50·min(ρ_valley − 0.32, 0)` on the node valley
depth ρ(45°) = 2^(−(n2/2 − 1)/n1). Bounds: r 20–160 mm, twist −30…150°, n1 0.3–30, n2 2.05–30.
Constraints: ρ ≤ 1.001 everywhere (tip outermost), ρ > 0.3, n1(z) > 0 and n2(z) > 2 between nodes, r0 ≥ 20 mm.

What the family can do: the valley depth is fixed by (n2/2 − 1)/n1. For n2 → 2 (with small n1) the shape is rose-like and
only the depth is free. Raising n2 at a constant depth makes the **tips pointed and the valleys rounder and wider**
(star-like). It cannot make the valleys sharper than the tips (n2 < 2 turns the tip into a minimum).

Settings (inherit M05, docs/05 §5.4): N = 22, H = 3 mm, equal arc length (9 mm target), **20 sections on the 10 mm knots**.

Start values (baked into `model.py`): r0 and twist = M05 E0 fit (kernel v2) sampled at the knots. n1, n2 = least-squares
fit of the superformula to the rose with M05's mean k(z) = 0.2029: **n1 = 0.30 (lower bound), n2 = 2.360**, at all 6 nodes.
**How well the superformula mimics the rose: max |Δρ| = 0.0031** (at the valley, 45°; ≈ 0.35 mm at r0 = 115 mm), rms 0.0015.
The unbounded optimum (n1 0.294, n2 2.353) is no better (0.0034). So the start base equals M05's within ~0.3 mm.
Start score (P0): exact front 0/19, 3/4 9/19, ribs 1.20 mm; as built front 0/19, 3/4 7/19 (the S01 twist effect M06
documented: fixed twist(0) = 0 knots can't make M05's rim dip).

Direct comparisons: **M06** (same curves and settings, rose k(z) base, 45 params) isolates the base family;
**M05** (rose, Bézier curves); **M01–M04** (custom spline base, constant over height).

## Hypothesis (written before running)
- The base family contains the rose (within 0.003 in ρ), so E0 will be at least as good as M06 (cost ≤ 194.8, front
  ≥ 5/19). The extra shape freedom will be used, but modestly: I expect n2 to rise to ≈ 2.5–4 in some heights
  (slightly pointed tips / rounder valleys), not a star (n2 ≫ 5).
- Front ≈ 5–7/19, 3/4 ≈ 9–11/19. The waist S08–S12 will still fail on ribs: M06 showed mixed-sign rib errors inside one
  segment; a symmetric lobe-shape change can spread ribs differently between tip and valley, so it may fix some of it,
  but not all.
- The neck S12–S19 ribs stay limited by the fixed twist(0) = 0 (as in M06).
- Locality E4b/E5b ≈ 0.9 (same knot curves as M06). E6: the same end-interval loft deviation as M06 (≈ 0.7 mm in
  S01/S19), so the buildability gate likely fails again.
- If the fit drives n2 to large values somewhere, that height wants pointed tips (custom-spline-like flat shoulders);
  if it stays at n2 ≈ 2.05–2.4, the rose is already the right family and the lobe shape is not the limit.

## Conclusions (after running)
All numbers kernel v2 (multi-start E0, 3 stages), as built unless marked. M06 = `models/M06_rose_knots` (same curves and
settings, rose base): front 5/19, 3/4 10/19, ribs 0.75 mm, cost 194.8. M05: front 5/19, 3/4 9/19, ribs 0.68, cost 163.8.

**E0.** Front **6/19** (S02–S07), 3/4 **8/19**, exact 6/19 / 8/19. Ribs 0.79 mm / 74 % ≤ 1 mm, outline max 2.35 mm (S01),
3/4 mean 0.97 mm. Cost **209.1** (all 4 starts 209.1–211.6: stable; best start pool:M05_E0), no cap hit, constraints OK,
214 s. Front count +1 vs M06 is within the ±2 optimiser-noise band; by cost and rib mean M08 is slightly **worse** than M06.

**Fitted base.** n1 = 0.300 / 0.306 / 0.300 / 0.394 / 0.335 / 0.311, n2 = 2.361 / 2.352 / 2.356 / 2.397 / 2.420 / 2.304
at z = 0 / 38 / 76 / 114 / 152 / 190. The fit barely leaves the rose-matched start (n1 0.30, n2 2.36). Valley-equivalent
lobe depth k = 0.205 / 0.197 / 0.203 / 0.173 / 0.214 / 0.167, the same as M06's fitted k (0.204 / 0.196 / 0.201 / 0.170 /
0.205 / 0.167). The only thing the fit uses is the depth; it chooses **no sharpening** at any height.

**Diagnostics (scratch, logged in PROGRESS).**
- n2 scan at the E0 curves with the valley depth held: data cost n2 2.1 → 123.6, 2.2 → 109.4, **2.36 → 105.0**, 2.7 →
  155.9, 3 → 223.9, 4 → 442, 6 → 728, 10 → 1008 (ribs 0.78 → 3.40 mm). Pointed tips are strongly rejected; the family's
  best is the most rose-like member, which at this depth coincides with the n1 ≥ 0.3 bound (n2 below it is worse anyway).
- M06's own E0 curves with the superformula matched to M06's k: data cost 105.5 vs M06 97.4. The 0.003 ρ difference
  (≈ 0.35 mm at the valley) between the best superformula and the rose is worth ≈ 8 cost units: the drawing prefers the
  rose's exact lobe profile to every superformula member. That explains cost 209 vs 195.
- Custom spline (M01–M04 base): best superformula max |Δρ| 0.024, best rose 0.021. The custom spline has a flatter tip
  (ρ = 0.994 at 5°) and a flat, wide valley with steeper flanks. The superformula on the n2 > 2 branch can only make the
  tip *sharper* and the valley rounder, which is the opposite direction.

**E1 (N).** N = 16 and 22 (own) give front 6/19; N = 12 / 30 / 45 give 4/19. 3/4 best at N = 16 / 30 (10/19).
Outline bias −0.31 (N 12) … +0.19 mm (N 45); ribs unchanged. Same picture as M05/M06.

**E2 (fill × placement).** Arc f = 1.0 (own) is best on the front (6/19); lower fill adds +0.05 … +0.13 mm bias and loses
1–2 segments. Angle-half: front 4/19, 3/4 10–11/19, outline max 2.74 (S01). Small lever.

**E3 (H).** 1:1 outline shift (−1.50 … +2.00 mm); only H = 3.0 passes any front segment. Ribs unchanged.

**E4 (twist).** ×0.97 / ×1.03 → ribs +0.65 / +0.49 mm, front 4/19; ×0.94 / ×1.06 → +1.82 / +1.47 mm.
**E4b locality 0.93** (achieved 0.89 of 1°), identical to M06 (same knot curves). M05 0.37.

**E5 (radius).** ±1 mm → front 0/19 (bias ±0.94), ribs +0.24 / +0.06 mm. **E5b locality 0.96** (= M06). M05 0.58.

**E6 (sections).** knots10 (own) = uniform 20: loft deviation max **0.72 mm** / mean 0.052 (S01/S19 end intervals, the
Catmull-Rom end effect M06 documented). Adaptive 20: 0.44; uniform 39: 0.08 mm. Pass counts move only 5–6 front,
6–11 3/4. Buildability gate (loft_dev_20 0.44 > 0.3) **fails**, as M06.

### Segments
- Front pass: S02–S07. Fail: S01 (rim outline +1.19 bias, kernel known limit), S08–S19 on **ribs** (S08 0.82 / 62 %,
  S09 1.28, S10 1.05, S11 1.14, S12–S19 1.15–1.44 mm). Outline passes S02–S18 except S15/S16 (bias +0.28/+0.30 borderline);
  S19 bias +0.41.
- 3/4 pass: S02, S04, S05, S11, S12, S14, S18, S19. Worst S01 2.36, S09 2.22, S10 1.82, S08 1.44 mm.
- Rib means per segment are 0.01–0.13 mm above M06's in S06–S19 (e.g. S09 1.28 vs 1.20, S12 1.36 vs 1.23): the base
  freedom did not buy anything in the waist or neck.

### Where the model is limited
- **Twist** (ribs S08–S19): same as M06, fixed twist(0) = 0 with value-only Catmull-Rom can't make the rim dip
  (rib anchoring), and mixed-sign rib errors within a segment (waist) aren't a curve problem.
- **Base**: not via sharpness. The superformula family's extra freedom points the wrong way for this drawing (pointed
  tips); its best member is a slightly worse rose. The custom-spline models M02 (12/19, cost 102) and M03 (14/19, 84.5)
  do much better with a base that differs from both the rose and the superformula by ≈ 0.02 in ρ in the *other*
  direction (flatter tip, flat valley, steeper flanks). That is the base direction worth exploring (M07's cos 8θ term with
  c < 0 flattens tip and valley).
- **Radius**: not a limit (outline S02–S18 passes or is borderline).

### Did the hypothesis hold?
- "At least as good as M06": **no** by cost (209.1 vs 194.8) and ribs (0.79 vs 0.75); front 6 vs 5 is noise. Reason: the
  family contains the rose only to 0.003 in ρ, and the drawing resolves that.
- "n2 rises modestly to 2.5–4": **no**; n2 stays 2.30–2.42 everywhere. The answer to "which crease shape does the drawing
  want" is: **rounder than any superformula, i.e. rose-like or flatter (custom-spline-like), never star-like.**
- Front 5–7 / 3/4 9–11: front yes (6), 3/4 slightly below (8). Waist fails: yes. Neck limited by fixed twist(0): yes.
- Locality ≈ 0.9: yes (0.93 / 0.96). E6 end-interval deviation as M06: yes (0.72 mm, gate fails).



## Final round — kernel v3 (2026-11-24): orientation offset + pool round 2
These are the numbers the judge uses. The conclusions above were written under kernel v1/v2, without the free orientation offset.

| | value |
|---|---|
| Rank / score | **9 / 10**, 0.452 |
| Front (as built) | **5/19** `··█████············` |
| 3/4 held out | **10/19** `·█···██···██··█████` |
| Ribs | 0.71 mm mean, 75 % ≤ 1 mm |
| 3/4 mean / outline max | 0.98 mm / 2.54 mm |
| Fit cost (best of 14 starts) | 175.6 from `pool:M05_E0v2` |
| Orientation offset | -1.13° |
| Locality twist / radius | 0.96 / 0.96 |
| Parameters | 52 (incl. the offset) |
| Buildable | yes (loft deviation 0.08 mm, best placement ≤ 39 sections) |
