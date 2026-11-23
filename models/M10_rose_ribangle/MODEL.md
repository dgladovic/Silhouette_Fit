# M10 — rose base + 10 mm knots for radius and rib lean angle (twist integrated)

## Definition
| Part | Representation | Parameters |
|---|---|---|
| Base | 4-petal rose `(1 + k cos4θ)/(1 + k)`, lobe depth k(z) Catmull-Rom through 6 nodes (z = 0, 38 … 190), as M05/M06 | 6 |
| Radius r0(z) | value knots every 10 mm (z = 0, 10 … 190), Catmull-Rom (`curves.catmull_keys`) | 20 |
| Rib lean angle α(z) | value knots every 10 mm, Catmull-Rom, degrees from vertical (+ = today's twist direction) | 20 |
| Twist | **derived**: `twist(z) = (180/π) ∫₀^z tan α(z') / r0(z') dz'` (turning rate of a point at the petal-tip radius), cumulative trapezoid on a 0.25 mm grid, linear interpolation in between; twist(0) = 0 by construction | 0 |
| **Total** | | **46** |

Penalties: `SMOOTH_W` × 2nd difference of the r (0.05/mm), α (0.05/°) and k (2.0) knots; k soft floor
`50·min(k − 0.02, 0)` (as M05). Bounds: r 20–160 mm, α −30…75°, k 0–0.45. Constraints: k(z) in 0.02–0.4, r0 ≥ 20 mm,
|α(z)| ≤ 80°. Cost of one `shape(p)` incl. the integral: ~0.13 ms.

Settings (inherit M05, docs/05 §5.4): N = 22, H = 3 mm, equal arc length (9 mm target), **20 sections on the 10 mm knots**.

Start values (baked into `model.py`): the M05 kernel-v2 E0 curves. r0 at the knots; α = atan(r0 · dtwist/dz · π/180) at
the knots; k = M05's fitted k. M05's twist drops 1° within the first 4 mm (slope → −∞ at z = 0, sampled α(0) = −66°),
so α(0) is clipped to the bound −30°. The rebuilt twist matches M05 within **0.60°** (max at z = 10; a constant −0.48°
offset above z = 20). Unclipped it would be 4.1° off; a least-squares α projection gets 0.45° (only at z ≈ 1 mm), and the
kernel's `pool:M05` start does that projection anyway. r0 matches within 0.85 mm (end intervals S01/S19).
Start score as built: front 0/19, 3/4 8/19, ribs 1.26 mm (the rim-twist offset shifts every rib, as in M06).

Direct comparison: **M06** has the same base, radius knots, settings and protocol; only the twist is represented by
19 twist knots instead of 20 α knots (45 → 46 parameters). M05 is the source of the start.

## Hypothesis (written before running)
- **Fit quality**: α(0) is free, so M10 can make the rim dip that M06's fixed twist(0) knot could not (M06 diagnostic with
  twist(0) free: cost 159). But a 10 mm Catmull-Rom α ramp from −30° only reaches about −0.5° of dip, not M05's −1°.
  Expect cost between M06's 194.8 and M05's 163.8 (≈ 170–185), front 5–7/19, 3/4 9–10/19. Waist ribs S08–S12 stay limited
  by the base (mixed-sign rib errors, M06 finding), not by the twist representation.
- **Conditioning**: α at one knot changes the twist at every height above it, so the Jacobian is "triangular" and the
  ribs (which see twist differences, i.e. local α) are directly addressed. Expect a similar or slightly lower nfev than
  M06 and the same minimum from all 4 starts; no large gain in cost from the reparametrisation alone.
- **E4b locality** (twist bump made of α knots): a +1° hat on the twist needs α up below the knot and down above it,
  spread by Catmull-Rom over 3–4 knots → locality lower than M06's 0.93, ≈ 0.7–0.85, achieved bump ≤ 0.9.
- **E5b locality** (radius bump, twist held): r0 enters the twist through 1/r0, so α has to compensate; locality ≈ M06
  (0.9+), radius knots are the same.
- E4a/E5a/E1–E3 sensitivities ≈ M06 (they don't depend on representation). E6 shows the same S01/S19 end-interval loft
  deviation as M06 (same knots10 Catmull-Rom radius), ≈ 0.7 mm, so the buildability gate likely fails again.
- Smoothness: integrating α smooths the twist (one order smoother than the α knots), so fewer twist inflections than M06.

## Conclusions (after running)
All numbers are kernel v2 (multi-start E0, 3 stages), as built unless marked. M05 / M06 numbers are their kernel-v2 E0s.
No change to `model.py` after the first fit.

**E0.** Front **5/19** (S03–S07), 3/4 **11/19**, exact curves 5/19 / 11/19. Ribs 0.68 mm / 78 % ≤ 1 mm, outline max
2.56 mm (S01), 3/4 mean 0.91 mm. **Cost 169.0** (data 166.3 + penalty 2.75), best from the own start; the 3 pool starts end
at 175.4 / 175.9 / 170.4. nfev 15 per stage, no cap hit, constraints OK, 116 s. α(0) sits at its bound −30°, but
relaxing the bound to −70° and refitting does not move it (cost 169.0): not bound-limited. The fitted twist dips to
−1.17° at z = 5 mm and is back to −0.57° at z = 10: the rim dip M06 could not make.

**E1 (N).** N = 12/16/22 front 5/19, N = 30/45 4/19; 3/4 best at the own N = 22 (11/19). Outline bias −0.31 (N 12) …
+0.19 mm (N 45); ribs unchanged. Same as M05/M06.

**E2 (fill × placement).** Arc f = 1.0 (own) best on the front (5/19); lower fill +0.05…+0.13 mm bias, front 4/19.
Angle-half placement: front 4/19, ribs +0.03 mm, but 3/4 12–13/19 (outline max 2.95 at S01). Small lever.

**E3 (H).** Outline shifts 1:1 (−1.50 … +2.00 mm); only H = 3.0 passes any front segment. Ribs unchanged.

**E4 (twist).** ×0.97 / ×1.03 → ribs +0.73 / +0.61 mm, front 3/19; ×0.94 / ×1.06 → +1.89 / +1.65 mm (= M06).
**E4b locality 0.77, achieved bump 0.68 of 1°** (M06 0.93 / 0.89, M05 0.37). See the influence map note below.

**E5 (radius).** ±1 mm → front 0/19 (bias ±0.95), ribs +0.26 / +0.10 mm. **E5b locality 0.96**, achieved 0.89 of 1 mm
(= M06: the radius knots are identical; the twist change that 1/r0 would cause is compensated by α).

**E6 (sections).** knots10 (own) = uniform 20: loft deviation max **0.72 mm** / mean 0.050; interior S02–S18 ≤ 0.06 mm,
**S01 0.60, S19 0.72 mm** (Catmull-Rom end intervals of r0, as M06). Adaptive 20: 0.40 mm, uniform 39: 0.08 mm.
Pass counts move only 4–6 / 10–13 since S01/S19 fail anyway. Buildability gate (best ≤ 20 sections ≤ 0.3 mm) **fails** (0.40).

### E4b influence map: what locality means for an angle model
A +1° hat on the twist at knot z_k (0 at z_k ± 10) is the integral of a +/− pair: α up in [z_k − 10, z_k], α down in
[z_k, z_k + 10]. A single α knot change does not do this; it adds a **step** to the twist that persists all the way to the
top (twist is cumulative). So the least-squares bump uses an alternating chain of α knot changes that cancels the step
above and below. With Catmull-Rom α (one knot reaches 4 intervals) that cancellation is imperfect: each bump row reads
≈ 0.51 / 0.51 in its two own segments, then 0.09 / 0.04 / 0.02 / 0.01 decaying on both sides (fully regular from 20 to
170 mm), and the peak only reaches 0.68°. The knot at z = 0 gives 0 (twist(0) = 0 fixed by the integral), the end knot
190 reaches 1.06 (no cancellation needed above). Read the other way, the natural local edit in M10 is not a twist bump
but a **rib-angle bump**: one α knot changes the twist slope over ±20 mm and shifts everything above by a constant,
which the outline sees as a shift of the lobe phase in every segment above. For the ribs (which are compared relative
to their drawn start near the rim) a lower-z α change moves all ribs above, so "fix one segment" means "fix α locally
and accept/compensate the phase above".

### Segments
- Front pass: S03–S07 (same set as M05 and M06). Fail: S01 (rim outline +1.38 mm bias, kernel known limit), S02 (bias
  +0.34), S08–S19 on **ribs** (S08 0.82 / 70 %, S09 1.33, S10 1.07, S11 0.88 / 62 %, S12–S19 0.85–1.05 mm, 44–76 %).
  Outline (max ≤ 0.75, |bias| ≤ 0.3) passes S03–S18 (largest S10/S11 max 0.57/0.62, S16 bias +0.27); S01, S02, S19 (+0.41) fail.
- 3/4 pass: S02, S06, S07, S11, S12, S14–S19 (11). Fail: S01 (2.06), S03–S05 (0.92–1.01), S08–S10 (1.15 / 1.94 / 1.61), S13.

### Compared with M06 (same base, radius knots, settings; twist knots instead of α knots)
- **Fits better**: cost 169.0 vs 194.8 (−13 %), ribs 0.68 vs 0.75 mm, 3/4 11/19 vs 10/19, mean 0.91 vs 0.95 mm; front
  equal (5/19). The gain is in the upper ribs S11–S19 (M06 1.03–1.39 → M10 0.85–1.05 mm), exactly the region M06 lost
  through its fixed twist(0) knot: α(0) free lets M10 make the −1° rim dip, so the twist relative to the rib starts is
  right. Waist S09/S10 ribs are slightly worse than M06 (1.33 / 1.07 vs 1.20 / 0.97): the mixed-sign rib errors
  (base limit, M06 finding) remain. Against M05 (cost 163.8, ribs 0.68, 3/4 9/19): equal ribs, better 3/4, cost +3 %.
- **Not better conditioned**: same nfev (15 per stage vs 13–15), but the column-normalised Jacobian condition number is
  35 vs M06's 6.6 (cumulative α columns are correlated), and the starts spread 169.0–175.9 against M06's 194.8–195.1. The
  lower cost comes from the reachable rim dip, not from easier fitting. Fit time 116 vs 145 s.
- **Smoother twist**: 3 twist inflections vs M06's 8 (integration smooths the knot wiggle); r0 6 vs 4 (judge smoothness
  0.25 vs 0.18; M05 1.0).
- Locality: radius identical (0.96); twist 0.77 vs 0.93 (cumulative, see above).

### Where the model is limited
- **Base** for the waist ribs S08–S10 (same mixed-sign per-rib errors as M06; no twist/radius curve can fix them).
- **Radius end intervals** for buildability (S01/S19 loft 0.6–0.7 mm, Catmull-Rom end knots), and the rim corner S01.
- Twist is no longer the limit at the rim (M06's problem) but its locality is lower by construction.

### Did the hypothesis hold?
- Cost 170–185: **better** than expected (169.0, the dip reached −1.17°, not −0.5°). Front 5–7/19: yes (5). 3/4 9–10/19:
  exceeded (11).
- Waist limited by the base: yes.
- Conditioning "similar nfev, same minimum from all starts": nfev yes; same minimum **no** (spread 7 cost units),
  condition number worse than M06.
- E4b 0.7–0.85: yes (0.77, achieved 0.68). E5b 0.9+: yes (0.96).
- E6 end-interval loft deviation ≈ 0.7 mm, gate fails: yes (0.72; 0.40 best at 20 sections).
- Smoother twist than M06: yes (3 vs 8 inflections).


## Final round — kernel v3 (2026-11-24): orientation offset + pool round 2
These are the numbers the judge uses. The conclusions above were written under kernel v1/v2, without the free orientation offset.

| | value |
|---|---|
| Rank / score | **8 / 10**, 0.453 |
| Front (as built) | **5/19** `··█████············` |
| 3/4 held out | **10/19** `·█····█···██·██████` |
| Ribs | 0.66 mm mean, 78 % ≤ 1 mm |
| 3/4 mean / outline max | 0.94 mm / 2.48 mm |
| Fit cost (best of 14 starts) | 159.8 from `pool:M01_E0` |
| Orientation offset | -0.77° |
| Locality twist / radius | 0.79 / 0.96 |
| Parameters | 47 (incl. the offset) |
| Buildable | yes (loft deviation 0.06 mm, best placement ≤ 39 sections) |
