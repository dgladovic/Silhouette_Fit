# M07 — rose + 8θ harmonic base + 10 mm knots for radius and twist

## Definition
| Part | Representation | Parameters |
|---|---|---|
| Base | `(1 + k cos4θ + c cos8θ)/(1 + k + c)` (`bases.rose8`); lobe depth k(z) and harmonic c(z) each Catmull-Rom through 6 nodes (z = 0, 38 … 190) | 6 + 6 |
| Radius r0(z) | value knots every 10 mm (z = 0, 10 … 190), Catmull-Rom (`curves.catmull_keys`) | 20 |
| Twist | value knots every 10 mm, Catmull-Rom, twist(0) = 0 fixed | 19 |
| **Total** | | **51** |

Penalties: `SMOOTH_W` × 2nd difference of the r (0.05/mm), twist (0.05/°), k (2.0) and c (2.0) knots; k soft floor
`50·min(k − 0.02, 0)` (as M05/M06). Bounds: r 20–160 mm, twist −30…150°, k 0–0.45, **c −0.08…0.08**.
Constraints: the section stays valid on `bases.TH` at every z (1 mm grid): ρ > 0 and max ρ ≤ 1.001 (the tip at θ = 0
stays the outermost point); k(z) in 0.02–0.4; r0 ≥ 20 mm. Note: at k ≈ 0.2 the tip stops being the maximum for
c < ≈ −k/4 = −0.05, so the lower part of the c range is only reachable as an invalid section (reported, not penalised).

What c does (corrected after E0; the first version of this paragraph had the crease direction backwards, which
the hypothesis below inherited): ρ'' = −16k cos4θ − 64c cos8θ, so the curvature at the tip is −16k − 64c and in the
valley +16k − 64c. **c < 0** flattens and broadens the tip/flank (ρ(22.5°) 0.816 → 0.873 at k = 0.225, c = −0.037)
and makes the valley **narrower, deeper and sharper**: a crease. **c > 0** gives a pointier tip and a flatter, broader valley.

Settings (inherit M05, docs/05 §5.4): N = 22, H = 3 mm, equal arc length (9 mm target), **20 sections on the 10 mm knots**.
Start values: the M05 kernel-v2 E0 fit sampled at the knots (r0, twist), M05's fitted k values, c = 0, baked into
`model.py`. So the start is M06's representation with c = 0 (front 0/19, 3/4 8/19 as built: the twist(0) = 0 clamp at
the rim shifts the anchored ribs, as in M06).

Direct comparisons: **M06** (identical except c, 45 params) isolates the 8θ harmonic; **M05** has the same base family
(c = 0) with global Bézier curves (27 params).

## Hypothesis (written before running)
- c(z) will be used, and mostly **positive** (sharper creases, as the top photo suggests), ≈ +0.02…+0.05, largest in the
  waist/shoulder (z ≈ 70–130 mm) where the rib errors in M06 had mixed signs across one segment.
- Effect on the front: small but real. Changing the lobe shape moves ribs near the crease relative to ribs near the tip,
  which is the one thing M06's radius/twist knots could not do. Expect the waist rib means (S08–S12) to drop by
  0.1–0.3 mm vs M06 and front **6–9/19** (M06 5/19, M05 5/19). Cost below M06's 194.8.
- The neck (S13–S19) stays limited by the fixed rim twist (twist(0) = 0 with value-only Catmull-Rom), as in M06; c can't
  fix a common rib shift.
- 3/4 (held out): about the same as M06 (≈ 9–11/19). c changes the section, which also changes the 3/4 outline, so a
  noise-fitting c would show up there as a regression in the waist.
- Outline: c changes the tip radius relative to r0 only through the normalisation (ρ(0) = 1 stays), so outline bias
  barely changes; S01 still fails (rim corner, kernel known limit).
- Locality E4b/E5b ≈ M06 (0.9+); E6 same end-interval loft deviation as M06 (≈ 0.7 mm at S01/S19) → buildability gate fails
  for the same reason.

## Changes after the first fit (details in `PROGRESS.md`)
1. First E0: c(190) ran to the −0.08 bound (c/k = −0.48). The tip was no longer the outermost point for z = 175–190
   (max ρ 1.034), so the constraint failed. Saved in `E0_fit_first_invalid/` (cost 73.0, front 11/19, 3/4 6/19).
2. Added a soft validity penalty: `W_VALID · max(max_θ ρ − 1, 0)` per 10 mm band. W_VALID = 300 still left
   max ρ 1.0025 at z = 190 (`E0_fit_second_w300/`, cost 73.9, front 10, 3/4 11). **W_VALID = 3000** gives a valid
   section (excess 0.00009). That is the accepted E0: cost 74.9. Nothing else changed (bounds, start, settings, other penalties).

## Conclusions (after running)
All numbers are kernel v2 (multi-start E0, 3 stages), as built unless marked.

**E0.** Front **10/19**, 3/4 **12/19**; exact curves 11/19 / 13/19. Cost **74.9** (M06 194.8, M05 163.8). Ribs
0.43 mm / 88 % ≤ 1 mm (M06 0.75 / 75 %, M05 0.68 / 81 %). Outline max 1.03 mm (S01), 3/4 mean 1.11 mm. All 4 starts
end at 74.9–82.9 (best pool:M05_E0), so this is a stable minimum. Constraints OK, 197 s, no cap hit.
Fitted c at z = 0/38/76/114/152/190: −0.042 / −0.034 / −0.037 / −0.016 / −0.007 / −0.046 (held at the validity limit
−k/4 at the neck). k: 0.241 / 0.241 / 0.225 / 0.202 / 0.200 / 0.178.

**E1 (N).** N = 16–45: front 10/19; N = 12: 8/19. 3/4 is 6 / 10 / 12 / 12 / 11 for N 12 / 16 / 22 / 30 / 45. Outline
bias moves −0.24 (N 12) to +0.17 mm (N 45); ribs are unchanged. N = 22 (own) is as good as any level.

**E2 (fill × placement).** Arc fill 0.5–1.0 adds only +0.04 to +0.12 mm bias, with the same pass counts. **Angle-half
placement: ribs +0.28 mm, front 7/19** (in M06 it was −0.05 mm). The c(z) base was fitted together with the arc placement,
so rib placement and lobe shape are coupled: c moves ribs around the lobe, and so does the placement rule.

**E3 (H).** The outline shifts 1:1 (−1.50 to +2.00 mm). Only H = 3.0 (the fitted value) passes anything. Ribs unchanged.

**E4 (twist).** ×0.97 / ×1.03 → ribs +0.94 / +0.77 mm, front 5/19. ×0.94 / ×1.06 → +2.17 / +1.87 mm, front 3/19.
**E4b locality 0.93** (achieved bump 0.89 of 1°), the same as M06.

**E5 (radius).** ±1 mm → front 0/19 (outline bias ±0.95), ribs +0.47 / +0.30 mm. **E5b locality 0.96** (0.89 of 1 mm).

**E6 (sections).** Own knots10 (= uniform 20): loft deviation max **0.89 mm** / mean 0.057. S02–S18 ≤ 0.05 mm, but
**S01 0.89 and S19 0.72 mm**: the Catmull-Rom end intervals, the same cause as M06. Adaptive 20: 0.52 mm (front 12/19);
adaptive/uniform 30: 0.12 / 0.43; 39: 0.04–0.09. Pass counts stay at 10–12 / 10–13 for every level, because S01 and S19
fail anyway. Buildability gate (≤ 0.3 mm at ≤ 20 sections) **fails** (0.52 mm), as for M06. Adding a section at z ≈ 5 and
z ≈ 185 mm, or 30 adaptive sections, would fix it.

### Segments (E0, as built)
- Front pass: S02–S07, S12–S14, S18 (10). Fail:
  - S01: outline max 1.03, bias +0.55. Rim corner, kernel known limit.
  - S19: outline bias +0.39.
  - S08–S11 and S15–S17: rib **within-1 mm share** only (67–75 %). Rib means are 0.49–0.66, except S09 at 1.05; the
    outline passes.

  The fails come from a few whole ribs that are > 1 mm off: x0 = −49, 0 and +41 in S07–S11, x0 = ±9 in S10–S16, and
  x0 = −20 in S15–S18. The kernel excludes only x0 = −40.7. x0 = +40.6 runs −7.6 mm off in S09–S13; it is kept, as the
  protocol requires.
- 3/4 pass: S05–S16 (12). Fail: S01–S04 (3.03 / 1.83 / 1.86 / 0.84) and S17–S19 (0.85 / 1.76 / 3.68). In S19, one row at
  z = 189.5 (top-left rim edge) is 27.7 mm off. Without that row S19 is 1.93.

### Compared with M06 (same representation without c) and M05
- **The 8θ harmonic is the biggest single improvement in the rose family so far.** Same knots, settings and protocol
  as M06, with 6 more parameters: cost 194.8 → 74.9, front 5 → 10, 3/4 10 → 12, ribs 0.75 → 0.43 mm.
- Where it helps, front rib mean M06 → M07:
  - waist: S10 0.97 → 0.58, S11 1.03 → 0.65, S12 1.23 → 0.60
  - neck: S13–S19 1.10–1.39 → 0.45–0.66
  - rim: S01–S05 0.26–0.47 → 0.14–0.30
  - smallest gain at S08/S09: 0.75 → 0.61, 1.20 → 1.05

  New front passes: S02, S12–S14 and S18. Outline max 2.36 → 1.03 mm.
- **Why it works.** In M06, one segment had rib errors of opposite sign across its width, which no twist or radius knot
  can fix. Changing the lobe shape moves the ribs near the tip relative to the ribs near the crease, because arc-length
  placement over a different ρ(θ) shifts their angles. That is exactly a mixed-sign correction. The neck also recovers:
  M06's rim-twist conflict (twist(0) fixed) was not the main neck limit. M07 has the same fixed twist(0) and reaches
  0.45–0.66 mm there.
- **Direction of c: negative everywhere** (c/k ≈ −0.15 at z = 0–76, −0.08 to −0.03 at the shoulder z = 114–152, and
  at the validity limit −0.26 at z = 190). Negative c flattens and broadens the tip and flank (ρ(22.5°) +0.06) and makes
  the valley narrower and sharper. So the drawing wants **fuller lobes with sharper creases**, as the top-view photo
  suggests, and the effect is strongest at the rim and the neck. At the neck the fit would go further than a valid
  section allows (max ρ > 1). A base that can sharpen the crease without lifting the flank above the tip (e.g. the
  superformula, M08) may gain more there.
- **3/4 (held out)** gets better in the middle and worse at the ends.
  - Better at the waist, where M06 was worst: S08–S10 1.45 / 2.10 / 1.66 → 0.43 / 0.35 / 0.45.
  - Worse at the rim (S01–S03 2.45 / 0.88 / 0.91 → 3.03 / 1.83 / 1.86) and the neck (S18–S19 0.60 / 0.62 → 1.76 /
    3.68 incl. the one rim row).

  The ends are where c is largest. There the front-fitted lobe shape does not match the 3/4 silhouette, which sees the
  section from another angle. That is either drawing-to-drawing inconsistency or c over-fitting the front at the ends.
  The first, invalid fit was even worse there (3/4 6/19).
- vs **M05** (Bézier curves, 27 params): cost 163.8 → 74.9, front 5 → 10, 3/4 9 → 12, ribs 0.68 → 0.43 mm. Locality
  0.37 / 0.58 → 0.93 / 0.96. M05 still has the better loft (0.03 mm) and smoothness (0 extra inflections; M07 r0 4 /
  twist 6, judge smoothness 0.22).

### Where the model is limited
- **Base** (main): the waist ribs x0 = −49 / 0 / +41 and the upper ribs ±9 / −20 stay > 1 mm off. c is pinned at the
  validity limit at the neck, and the 3/4 view disagrees with the lobe shape at the rim and the neck.
- **Radius:** not limiting (outline passes S02–S18 except a +0.39 bias in S19). S01 is the rim corner.
- **Twist:** not limiting in the fit. Locality is high, and the sweeps show the fit sits in a sharp minimum (±3 % twist
  costs 0.8–0.9 mm of rib error).
- **Build:** the Catmull-Rom end intervals give 0.7–0.9 mm loft deviation at S01/S19 with 20 sections on the knots.

### Did the hypothesis hold?
- c used: **yes**. Positive: **no, negative**. The hypothesis wrote "positive = sharper creases" from my wrong sign
  analysis (corrected in the definition). In substance, the creases did get sharper, but the lobes got fuller too.
  Largest in the waist: **no**; largest at the rim and the neck, near 0 at the shoulder.
- Waist ribs −0.1 to −0.3 mm vs M06: **yes, and more** (−0.14 to −0.63 in S08–S12). Front 6–9/19: **exceeded** (10/19).
  Cost below M06: yes (74.9 vs 194.8).
- Neck stays limited by the fixed rim twist: **no**. The neck ribs halved with the same twist(0) = 0.
- 3/4 ≈ M06 (9–11): 12/19, slightly better, but worse at the ends (rim/neck), where c is largest.
- Outline unchanged, S01 fails: S01 fails, yes. The outline actually improved (max 2.36 → 1.03).
- Locality ≈ M06, same E6 end-interval problem: **yes** (0.93 / 0.96; 0.89 / 0.72 mm at S01 / S19).


## Final round — kernel v3 (2026-11-24): orientation offset + pool round 2
These are the numbers the judge uses. The conclusions above were written under kernel v1/v2, without the free orientation offset.

| | value |
|---|---|
| Rank / score | **3 / 10**, 0.650 |
| Front (as built) | **13/19** `·███████·█████···█·` |
| 3/4 held out | **13/19** `···█████████████···` |
| Ribs | 0.43 mm mean, 90 % ≤ 1 mm |
| 3/4 mean / outline max | 0.91 mm / 1.73 mm |
| Fit cost (best of 14 starts) | 79.3 from `pool:M04_E0v2` |
| Orientation offset | -0.46° |
| Locality twist / radius | 0.96 / 0.96 |
| Parameters | 52 (incl. the offset) |
| Buildable | yes (loft deviation 0.02 mm, best placement ≤ 39 sections) |

M07 note: v3 cost 79.3 is above the v2 cost 74.9. The pool projection only matches radius and twist, so the fitted crease term c(z) starts from 0 for every pool start. The pass counts still improved (front 10 → 13). A start that also carries the base shape would probably lower it further.
