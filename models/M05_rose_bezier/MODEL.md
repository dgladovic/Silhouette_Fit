# M05 — rose base + 2D Bézier radius + Bézier twist (the active fit before the study)

## Definition
| Part | Representation | Parameters |
|---|---|---|
| Base | 4-petal rose `(1 + k cos4θ)/(1 + k)`, lobe depth k(z) Catmull-Rom through 6 nodes (z = 0, 38 … 190) | 6 |
| Radius r0(z) | 8-point 2D Bézier (r, z), P0 at z = 0, P7 at z = 190 | 14 |
| Twist | 5-point Bézier (t, deg), t = z/190, P0 = (0, 0) | 7 |
| **Total** | | **27** |

Settings (own, from `Grasshoper_full/`): N = 22, H = 3 mm, equal arc length (9 mm target), 15 uniform sections.
Start values: the joint two-view fit (commit 1e8223d). E0 refits it under the study protocol (front only, 3/4 held out).

## Hypothesis (written before running)
- The front fit will stay close to today's 4/19. The optimiser starts at a minimum of a very similar objective
  (today's fit also used the 3/4 view, and the unreliable rib x0 = −41 is now excluded, which should help S12–S15).
- Excluding the −41 rib should turn several shoulder/neck segments (S12–S19) green on ribs.
- Waist S08–S11 will still fail. The global Bézier twist can't add local twist at the waist without
  disturbing the bulge and the shoulder.
- Locality (E4b/E5b) will be low (≈ 0.2–0.4): every control point moves the whole height.
- The 3/4 view will get slightly worse than the joint fit (0.70 mm), because it is now held out.

## Conclusions (after running, kernel v1, 2026-11-23)

**E0 (as built): front 8/19, 3/4 7/19** · ribs 0.71 mm mean, 79 % ≤ 1 mm · outline max 2.03 mm (rim edge) · 3/4 mean 0.99 mm.
Front pass strip `.YYYYYY......YY....`: the bulge S02–S07 and S14–S15 pass.
- **Waist S08–S12 fails on ribs** (rib mean 0.95–1.53 mm, 53–70 % ≤ 1 mm). The outline there is now fine (|bias| ≤ 0.35):
  the fit moved the error from the outline into the ribs. **Neck S16–S19** fails on ribs, just above target (0.73–0.79 mm, 70–80 %).
- **3/4 got worse when held out**: start (joint fit) 12/19, 0.76 mm → front-only fit 7/19, 0.99 mm. The two drawings
  pull this model in different directions. The front fit costs the 3/4 view.
- E1 triangle count: N = 12 → 45 shifts the outline −0.32 → +0.20 mm on average. Ribs unchanged. Front pass count drops
  either side of N = 22 because the radius was fitted for N = 22.
- E2 width / placement: fill 0.5 shifts the outline +0.14 mm. Equal-angle placement changes the ribs by +0.05 mm
  (k(z) varies) and moves the outline up to +0.42 mm at single segments.
- E3 height: 1.00 mm outline per mm, uniform. Any change ≠ 0 needs a radius refit (0/19 at H = 2 or 4).
- **E4 twist is the most sensitive parameter**: ×0.97 or ×1.03 drops the ribs from 0.71 to 1.2–1.3 mm (front 3–5/19).
  1-knot bumps: locality share **0.37**, achieved bump only 0.25 of 1° → the Bézier twist can't make a local twist change.
- E5 radius: ±1 mm → bias ±0.95 mm, front 0/19 (the outline targets are tight). 1-knot bumps: locality 0.58, achieved 0.58 of 1 mm.
- E6 sections: the loft deviates from the exact curves by ≤ 0.15 mm even at 8 sections. Front pass varies 6–8/19 only by
  segments sitting on a threshold. Section count/placement is **not** a real lever for this model.

**Hypothesis check**: right on the waist failing, low locality, and 3/4 getting worse. Wrong on the shoulder/neck: excluding the
−41 rib fixed S14–S15 but not S16–S19. **Main limitation: twist representation (global, 5 points).**


## Final round — kernel v3 (2026-11-24): orientation offset + pool round 2
These are the numbers the judge uses. The conclusions above were written under kernel v1/v2, without the free orientation offset.

| | value |
|---|---|
| Rank / score | **6 / 10**, 0.492 |
| Front (as built) | **6/19** `·██████············` |
| 3/4 held out | **10/19** `·█····█···████████·` |
| Ribs | 0.67 mm mean, 79 % ≤ 1 mm |
| 3/4 mean / outline max | 0.90 mm / 1.53 mm |
| Fit cost (best of 14 starts) | 160.3 from `pool:M10_E0v2` |
| Orientation offset | -0.49° |
| Locality twist / radius | 0.37 / 0.59 |
| Parameters | 28 (incl. the offset) |
| Buildable | yes (loft deviation 0.01 mm, best placement ≤ 39 sections) |
