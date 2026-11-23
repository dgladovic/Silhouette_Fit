# M04 — scenario 4: custom spline base + keyframe radius + keyframe twist, refined per segment

User's scenario 4: "a tool to save radius/height values; wherever a segment needed it, more points were added".

## Definition
| Part | Representation | Parameters |
|---|---|---|
| Base | the custom spline (`r_mults` / `phi_increments`, degree-5 control-point spline, 0–45° mirrored), **fixed over height** (`bases.custom_spline()`) | 0 |
| Radius r0(z) | keyframes (t, r), t = z/190, Catmull-Rom (`curves.catmull_keys` = `smooth_spline_interpolation`) | n keys |
| Twist | keyframes (t, deg) at the **same** key positions, Catmull-Rom; the key at t = 0 is fixed at 0° | n − 1 |
| **Total (start, 11 keys)** | | **21** (2n − 1; grows by 2 per added key, max 39 at 20 keys) |

Own settings (`../BaseScript`): N = 22, H = 2.4 mm, equal angle with a half tooth at 0° (`angle_half`), sections
= one on every key (`mode='list'`, z = 190·t). At 11 keys this is identical to M01's 11 uniform sections.
Start values: `bez_points` and `angle_points` from `../BaseScript/BaseScript.py` (11 keys, t = 0 … 1 step 0.1;
twist 0, 2.2, 8.26, 17.2, 28.2, 40.3, 52.6, 64.4, 74.8, 82.6, 90). The variant in
`../FulLTextureLamp/prave vrednost bezier.txt` differs only in r(0.6) 104.2, r(0.8) 79.0, twist(1.0) 87; not used.
Smoothness penalty: `SMOOTH_W['mm']` × 2nd difference of the radius keys, `SMOOTH_W['deg']` × 2nd difference of the
twist keys (over the key sequence, incl. the fixed 0 at t = 0).

**Refinement rule** (docs/05 §5.2), implemented in `model.refine()` (called by `study.run_E0`):
after the first fit, add ONE key (radius and twist) at the centre of the worst failing segment as built (the failing
segment with the largest rib_mean among those failing on ribs; if none fail on ribs, the largest sil_max; segments
whose centre already holds a key are skipped), refit from the current curves sampled at the new key set, repeat.
Stop when the targeted segment improves by ≤ 0.1 mm (that last key is removed again, it did not earn its place),
or at 20 keys. Every key also adds a section. Final keys: `E0_fit/keys.json` (loaded by `model.py` at import, so
E1–E6 and the summary use the refined model). `E0_fit/run.py` sets `M04_BASE_KEYS=1`, so a re-run of E0 always
starts from the 11 historical keys and repeats the refinement.

## Hypothesis (written before running)
- With 10 free twist keys instead of M01's 3-parameter cubic, the ribs should improve clearly over M01 (0.67 mm,
  front 3/19): the twist can bend locally at the waist and shoulder. Expect the first fit at ≈ 5–8/19 front.
- Refinement will add keys in the waist/shoulder bands (S09–S16), where M01's ribs were worst, and gain
  maybe 1–3 more segments before the 0.1 mm rule stops it; probably 2–5 keys added, not 9.
- The limit is the **fixed base**: the lobe shape cannot change with height, so rib positions inside a lobe drift
  where the drawing's lobes get shallower/deeper. Extra keys cannot fix that, which is why refinement stalls.
- S01 (rim corner) and the outline at the neck (S18–S19) will keep failing; a key at the rim cannot follow the
  drawn rounded corner, and sections on sparse keys add loft drift (±0.5 mm below 15 sections).
- 3/4: about as good as M01 (≈ 12–15/19), since the outline is mostly the radius.
- Locality (E4b/E5b): medium, ≈ 0.4–0.6 for both curves (Catmull-Rom over ~19 mm keys reaches ~4 keys);
  denser where keys were added.
- Expected E0 (as built): front ≈ 6–9/19, 3/4 ≈ 12–15/19.

## Conclusions (after running) — kernel v2
Kernel v2 (multi-start E0, 3 stages). All numbers as built (11 sections on the 11 keys) unless marked exact.
The coordinator re-ran E0 (including refinement) and E1–E6 under v2; I re-ran no experiments. The read-only checks
below only evaluate the cost of given curves (no fit, nothing written).

**E0 + refinement.** 4 starts: own start (P0) 209.6, M01 E0 209.5 (best), M05 E0 210.1, M02 X1c 209.7 (soft_l1
cost; caps not hit). **Front 3/19 (S04–S06), 3/4 13/19**, outline max 2.33, ribs 0.72 mm / 78 %, 3/4 mean 0.81
(exact: front 4/19, 3/4 13/19). Refinement round 1 added a key at z = 125 mm (S13, worst rib 1.35 mm). S13 improved
only 1.35 → 1.28 mm (gain 0.07 ≤ 0.1), so the key was removed and refinement stopped. **Keys added: 0**; the final
key set is the 11 historical keys (`E0_fit/keys.json`).

**E1 (N).** Ribs unchanged (0.72 mm at every N). N = 22 is best (front 3/19, 3/4 13/19). N = 12 shifts the outline
−0.47 mm (front 1/19, 3/4 8/19); N = 45 shifts it +0.17 mm (front 1/19, 3/4 9/19).
**E2 (fill × placement).** Fill 0.5 shifts the outline +0.12–0.13 mm (front 1/19). Arc f = 1.0: front 3/19,
**3/4 14/19**, outline max 2.33 → 2.07 (S01). Own angle_half f = 1.0: 3/19, 13/19.
**E3 (H).** 1:1 outline shift (−0.90 at 1.5 mm, +2.60 at 5 mm), ribs unchanged. H = 2.0 gives front 3/19,
3/4 14/19 (3/4 mean 0.68); H ≥ 3 → front 0/19.
**E4 (twist).** ×0.97 / ×1.03 add +0.77 / +0.52 mm to the ribs (3/4 5/19, 7/19). 1-key bumps: **locality 0.59**,
achieved 0.47 of 1° (the 19 mm key spacing can't make a 10 mm-wide bump).
**E5 (radius).** ±1 mm → outline bias ±0.95 mm (front 1/19 and 0/19). **Locality 0.63**, achieved 0.49 of 1 mm.
**E6 (sections).** Own 11 sections: loft deviation max 1.80 / mean 0.20 mm. 20 uniform 0.25 mm, 20 adaptive 0.05 mm
(buildability gate OK at 0.05). Front 3 → 4/19 at 15+ sections; 3/4 stays 13/19. The sections are not the limit.

**Segments.** Front passes S04–S06 only. Outline fails at S01–S03 (bias +0.46…+1.71) and S18–S19 (+0.59 / +1.08).
Ribs fail from S07 up (0.56 → 1.35 mm; S12–S19 1.07–1.35 mm). 3/4 fails at S01–S03 and S08–S10.

**Main limitation: the twist curve is stuck in the wrong basin. It is not the base** (this corrects my v1
conclusion). Read-only cost checks under M04's own settings:
- M02 E0 (same custom-spline base, kernel v2) reaches front 12/19 and ribs 0.35–0.61 mm in S12–S19. Its curves
  evaluated with M04's settings (H 2.4, angle_half, 11 sections) cost **147.3**, against M04's 209.5. The base
  can therefore fit much better.
- **The same M04 E0 curves with a constant −1° twist offset cost 148.6** (−0.5°: 165.8, −1.5°: 157.9, −2°: 219.8).
  No other change is needed. The missing freedom is a global rotation of the shade against the drawing.
- M04 fixes the twist at t = 0 to 0°. A global offset therefore needs all 10 twist keys to move together plus a
  0 → −1° ramp over 0–19 mm. M02 gets the same offset from a sharp drop near the rim (−1.6° by z = 2 mm).
  Sampled onto M04's keys, M02's twist misses that drop by up to 1.78° (1.33° even on a 10 mm grid), and the cost
  rises to 715 (598). That is why the M02 pool start (projected onto the keys) did not help.
- The fit and the one-key-at-a-time refinement never reach the offset direction from any of the 4 starts. Keys
  added in the failing rib bands (S16 in v1, S13 in v2) can't supply a global rotation.
- My v1 20-key probe (cost 183, S12–S19 ribs ≥ 1.07 mm) was single-start; it did not prove a base limit.

**Comparison with M01/M02 (same base, v2).** M01 (cubic twist, 14 params): front 3/19, 3/4 13/19, ribs 0.67 mm.
M02 (Bézier twist, 18): **front 12/19**, 3/4 15/19, ribs 0.52 mm. M04 (keys, 21): front 3/19, 3/4 13/19, ribs 0.72 mm.
M01 and M04 share the same basin, and their per-segment rib errors are within ±0.1 mm of each other. M02 escapes it
through its twist near the rim. So M04's extra twist freedom is in the wrong place: it is local in height, while the
missing freedom is global.

**Hypothesis check.**
- **Wrong:** I expected the ribs to beat M01 (0.72 vs 0.67 mm), 2–5 keys added (0 were), and front 6–9/19 (3/19).
- **Wrong:** I named the fixed base as the limit. The same base reaches 12/19 in M02, so it is not the limit.
- **Right:** the outline fails at S01 and S18–S19, 3/4 lands at 12–15/19 (13/19), and locality is 0.4–0.6
  (0.59 / 0.63).

**Open (for the orchestrator, not done here):** a free twist value at t = 0 (or one global rotation parameter), or
a pool start with the −1° offset, would very likely move M04 from cost 209 to ≤ 149. That changes the model spec,
which fixes twist(0) = 0, so it needs a decision before any re-run.

## Superseded (kernel v1)
Kernel v1. All numbers as built (11 sections on the 11 keys) unless marked exact.

**E0 + refinement.** Start (BaseScript keys): front 2/19, 3/4 11/19, ribs 1.63 mm. First fit (11 keys, 21 params,
nfev 13, cap not hit): **front 3/19 (S04–S06), 3/4 10/19**, outline max 2.28, ribs 0.71 mm / 78 %, 3/4 mean 0.99
(exact: front 3/19, 3/4 7/19). Refinement round 1 added a key at z = 155 mm (S16, worst rib 1.36 mm): S16 got
*worse* (1.36 → 1.46 mm) and 3/4 fell to 6/19, so the 0.1 mm rule stopped it and the key was removed.
**Keys added: 0** (final = the 11 historical key positions). Probe beyond the rule (logged, not the result):
20 keys on the 10 mm grid only reach front 4/19, ribs 0.70 mm, with S12–S19 ribs still 1.07–1.25 mm.

**E1 (N).** Ribs unchanged (0.71 mm at every N). N = 22/30 best (front 3/19, 3/4 10/19); N = 12 shifts the outline
−0.47 mm on average (front 1/19, 3/4 6/19), N = 45 +0.17 mm.
**E2 (fill × placement).** Small: fill 0.5 shifts the outline +0.12–0.13 mm; arc placement gives the same pass
counts (3/19, 11/19) and lowers the outline max 2.28 → 2.02 (S01 only).
**E3 (H).** Outline shifts 1:1 (−0.90 at 1.5 mm, +2.60 at 5 mm), ribs unchanged. H = 2.0–2.4 best; H ≥ 3 → 0/19 front.
**E4 (twist).** Very sensitive: ×0.97 / ×1.03 raise ribs by +0.77 / +0.52 mm. 1-knot bumps: locality share
**0.59** (M01 cubic twist: 0.21), achieved 0.47 of 1° (the 19 mm key spacing cannot make a 10 mm bump).
**E5 (radius).** ±1 mm → outline bias ±0.95, front 1/19 and 0/19. Locality **0.63** (same as M01: same radius keys).
**E6 (sections).** Own 11 sections: loft deviation max 1.88 / mean 0.20 mm (rim and neck). 20 uniform: 0.26 mm,
20 adaptive: 0.05 mm. Front pass changes by ≤ 1 segment (3 → 4/19 at 15–20 sections); the sections are not the limit.

**Segments.** Front passes S04, S05, S06 only. Outline fails at S01–S03 (rim corner, +0.5…+1.7 mm bias) and
S18–S19 (+0.6/+1.1 mm bias). Ribs fail from S07 up (0.56 → 1.36 mm); S12–S19 are 1.2–1.4 mm everywhere.
3/4 fails at S01–S04, S08–S10, S12–S13.

**Where the model is limited: the base.** Free twist keys reach the same cost basin as M01's 3-parameter cubic
(cost 210 vs 198; M01's curves sampled on M04 keys refit to 210), and neither an extra key at S16 nor 20 keys
move the S12–S19 ribs below 1.07 mm. Rib positions inside a lobe are set by the fixed custom-spline cross-section,
and one twist value per height cannot put all ribs of a lobe right at once. The radius keys are fine for the outline
in S04–S17; S01–S03 and S18–S19 are the rim/neck ends, where keys 19 mm apart and the sparse loft can't follow.

**Comparison with M01/M02 (same base).** M01 (cubic twist, 14 params): front 3/19, 3/4 14/19, ribs 0.67.
M02 (Bézier twist, 18 params): front 4/19, 3/4 13/19, ribs 0.76. M04 (keys, 21 params): front 3/19, 3/4 10/19,
ribs 0.71. More twist freedom does not help the front fit, and it costs 3/4 (held-out): the free keys follow the
front drawing a little more closely at the expense of the other view. Per-segment rib errors of the three are within
±0.15 mm of each other in every segment: the shared base dominates.

**Hypothesis check.** Wrong on the ribs: 10 free twist keys did *not* beat M01 (0.71 vs 0.67 mm). Wrong on the
refinement count (expected 2–5 keys, got 0: the first key made its target worse). Right on the limit (fixed base),
on S01/S18–S19 outline failures, and on locality (0.59 / 0.63, inside 0.4–0.6). 3/4 came out worse than expected
(10/19 vs 12–15/19), front at the low end (3/19 vs 6–9/19).


## Final round — kernel v3 (2026-11-24): orientation offset + pool round 2
These are the numbers the judge uses. The conclusions above were written under kernel v1/v2, without the free orientation offset.

| | value |
|---|---|
| Rank / score | **5 / 10**, 0.592 |
| Front (as built) | **10/19** `···████····██████··` |
| 3/4 held out | **13/19** `······█████████████` |
| Ribs | 0.44 mm mean, 93 % ≤ 1 mm |
| 3/4 mean / outline max | 0.82 mm / 2.07 mm |
| Fit cost (best of 14 starts) | 90.7 from `pool:M03_E0v2` |
| Orientation offset | -1.55° |
| Locality twist / radius | 0.63 / 0.63 |
| Parameters | 22 (incl. the offset) |
| Buildable | yes (loft deviation 0.05 mm, best placement ≤ 39 sections) |

M04 note: refinement disabled in v3 (its internal refits bypass the kernel's offset). It runs on the 11 historical keys; refinement added 0 keys in v1 and v2.
