# M08_superformula_knots — progress

## Status  (overwrite this block only)
- State: final (kernel v3), rank 9/10
- Best E0 (as built): front 5/19, 3/4 10/19, 52 params, score 0.452
- Next: none (study complete)

## Log  (append only, newest at the bottom)

### 2026-11-23 22:43 — model created (kernel v2)
- model.py: superformula base bases.superformula(n1(z), n2(z)), 4-fold, normalised to 1 at the tip; n1, n2 each Catmull-Rom through 6 nodes KZ = 0, 38, 76, 114, 152, 190 (12 params) + radius knots every 10 mm (20, Catmull-Rom) + twist knots every 10 mm (twist(0)=0 fixed, 19) = 51 params
- smoothness: SMOOTH_W mm/deg (0.05/0.05) x second_diff of r / twist knots; **0.2 x second_diff on n1 and on n2** (orchestrator's choice: the units of n1/n2 differ from k, so SMOOTH_W['k'] = 2.0 is not reused)
- extra soft penalty 50*min(valley - 0.32, 0) on the node valley depth ρ(45°) = 2^(-(n2/2-1)/n1) (keeps the ρ > 0.3 constraint away during the fit; same pattern as M05's k floor)
- bounds: r 20..160 mm, twist -30..150 deg, n1 0.3..30, n2 2.05..30; constraints: ρ ≤ 1.001 everywhere (tip outermost), ρ > 0.3, n1(z) > 0 / n2(z) > 2 between nodes, r0 ≥ 20 mm
- start n1, n2: least squares of the superformula against the rose with M05's mean k(z) = 0.2029 -> n1 = 0.30 (on its lower bound), n2 = 2.3603; max |Δρ| 0.0031 (at the valley, 45°), rms 0.0015. Unbounded optimum n1 0.294 / n2 2.353 is not better (0.0034 max). Used at all 6 nodes.
- note: near n2 -> 2 the superformula is a one-parameter family (only (n2-2)/n1 matters: depth); shape freedom appears for larger n2 (pointed tips, rounder valleys). n2 < 2 would make the tip a minimum (excluded by the bound).
- start r0, twist: M05 E0 fit (kernel v2) sampled at the 10 mm knots, baked as literals
- start (P0) score: exact front 0/19, 3/4 9/19, ribs 1.20 mm; as built front 0/19, 3/4 7/19, ribs 1.21 mm (the S01 twist-dip effect M06 documented: knots with fixed twist(0) can't make M05's rim dip)
- settings: inherit M05: N 22, H 3.0, arc placement 9 mm, sections knots10 (20 sections on the knots) - docs/05 §5.4

### 2026-11-23 22:43 — MODEL.md written (kernel v2)
- definition (51 params) + hypothesis before running: E0 >= M06 (cost <= 194.8, front >= 5/19), n2 rises modestly to 2.5-4, front 5-7/19, 3/4 9-11/19, waist still fails, locality ~0.9, E6 end-interval loft deviation as M06

### 2026-11-23 22:46 — E0 fit (kernel v2)
- start (as built): front 0/19, 3/4 10/19, ribs 1.21 mm
- result (as built): front 6/19, 3/4 8/19, outline max 2.35, ribs 0.79 mm / 74 %, 3/4 mean 0.97
- exact curves: front 6/19, 3/4 8/19
- 51 params, 214.3 s, nfev 16, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 210.8, pool:M01_E0 211.6, pool:M05_E0 209.1, pool:M02_X1c 209.5 -> best: pool:M05_E0
- Fusion script: models\M08_superformula_knots\fusion\M08\M08.py
- command: python models/M08_superformula_knots/E0_fit/run.py

### 2026-11-23 22:50 — E0 checked + base-shape diagnostics (scratch, not official) (kernel v2)
- E0 accepted as is: constraints OK, no cap hit, all 4 starts end at cost 209.1-211.6 (stable). No change to model.py.
- fitted nodes: n1 = 0.300 0.306 0.300 0.394 0.335 0.311, n2 = 2.361 2.352 2.356 2.397 2.420 2.304 -> barely moved from the rose-matched start; valley-equivalent k = 0.205 0.197 0.203 0.173 0.214 0.167 (M06 fitted k: 0.204 0.196 0.201 0.170 0.205 0.167)
- cost 209.1 > M06 194.8 although the family contains the rose within 0.003: data part 104.5 vs M06 97.4 (penalty 0.03 / 0.04)
- check 1: M06's E0 curves + superformula matched node-by-node to M06's k: data cost 105.5 (M06 97.4); refit from there: 209.8, front 5/19, 3/4 12/19. So the ~8 cost gap is the 0.003 shape difference rose vs superformula (≈ 0.35 mm at the valley), not a start problem.
- check 2: n2 scan at the E0 result, n1 adjusted per node to keep the valley depth, exact curves: n2 2.1 -> data cost 123.6, 2.2 -> 109.4, 2.36 (E0) -> 105.0, 2.7 -> 155.9, 3.0 -> 223.9, 4 -> 441.7, 6 -> 727.5, 10 -> 1007.7 (ribs 0.78 -> 3.40 mm, front 6 -> 0/19). The drawing clearly rejects pointed tips; the family's best shape is near n2 ≈ 2.36, which at this depth is exactly where n1 meets its 0.3 bound (n1 ≈ 0.6·(n2/2 − 1)/0.6 ... depth a = (n2/2-1)/n1 ≈ 0.60), so the bound does not cut off a better shape.
- custom spline (M01-M04 base) vs families: best superformula max |Δρ| 0.024 (n1 0.30, n2 2.354), best rose 0.021 (k 0.199): the custom spline has a flatter tip (0.994 at 5°) and a flatter valley with steeper flanks, which the superformula cannot make on the n2 > 2 branch (it can only sharpen the tip).

### 2026-11-23 22:50 — E1 triangle count (kernel v2)
- N=12: front 4/19, 3/4 7/19, outline max 1.77, ribs 0.79 mm (74 %), 3/4 mean 0.94; Δ outline bias mean -0.31 (range -0.67..-0.05), Δ rib mean +0.00 mm
- N=16: front 6/19, 3/4 10/19, outline max 2.01, ribs 0.79 mm (74 %), 3/4 mean 0.87; Δ outline bias mean -0.17 (range -0.35..+0.01), Δ rib mean +0.00 mm
- N=22 (own): front 6/19, 3/4 8/19, outline max 2.35, ribs 0.79 mm (74 %), 3/4 mean 0.97; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 4/19, 3/4 10/19, outline max 2.53, ribs 0.79 mm (74 %), 3/4 mean 1.00; Δ outline bias mean +0.11 (range +0.05..+0.20), Δ rib mean +0.00 mm
- N=45: front 4/19, 3/4 9/19, outline max 2.64, ribs 0.79 mm (74 %), 3/4 mean 1.03; Δ outline bias mean +0.19 (range +0.09..+0.30), Δ rib mean +0.00 mm
- command: python models/M08_superformula_knots/E1_tri_count/run.py

### 2026-11-23 22:50 — E2 triangle width (fill) x placement (kernel v2)
- arc f=0.5: front 4/19, 3/4 11/19, outline max 2.48, ribs 0.79 mm (74 %), 3/4 mean 1.01; Δ outline bias mean +0.13 (range +0.07..+0.18), Δ rib mean +0.00 mm
- arc f=0.7: front 4/19, 3/4 9/19, outline max 2.44, ribs 0.79 mm (74 %), 3/4 mean 1.00; Δ outline bias mean +0.09 (range +0.05..+0.12), Δ rib mean +0.00 mm
- arc f=0.85: front 5/19, 3/4 9/19, outline max 2.40, ribs 0.79 mm (74 %), 3/4 mean 0.98; Δ outline bias mean +0.05 (range +0.02..+0.06), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 6/19, 3/4 8/19, outline max 2.35, ribs 0.79 mm (74 %), 3/4 mean 0.97; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 4/19, 3/4 11/19, outline max 2.74, ribs 0.79 mm (73 %), 3/4 mean 0.96; Δ outline bias mean +0.14 (range -0.02..+0.39), Δ rib mean +0.00 mm
- angle_half f=0.7: front 4/19, 3/4 11/19, outline max 2.74, ribs 0.79 mm (73 %), 3/4 mean 0.96; Δ outline bias mean +0.10 (range -0.03..+0.39), Δ rib mean +0.00 mm
- angle_half f=0.85: front 4/19, 3/4 10/19, outline max 2.74, ribs 0.79 mm (73 %), 3/4 mean 0.96; Δ outline bias mean +0.07 (range -0.05..+0.39), Δ rib mean +0.00 mm
- angle_half f=1.0: front 4/19, 3/4 10/19, outline max 2.74, ribs 0.79 mm (73 %), 3/4 mean 0.95; Δ outline bias mean +0.03 (range -0.11..+0.39), Δ rib mean +0.00 mm
- command: python models/M08_superformula_knots/E2_tri_width/run.py

### 2026-11-23 22:50 — E3 triangle height (kernel v2)
- H=1.5: front 0/19, 3/4 3/19, outline max 1.99, ribs 0.79 mm (74 %), 3/4 mean 1.44; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 3/19, outline max 1.49, ribs 0.79 mm (74 %), 3/4 mean 1.16; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 6/19, 3/4 8/19, outline max 2.35, ribs 0.79 mm (74 %), 3/4 mean 0.97; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 6/19, outline max 3.34, ribs 0.79 mm (74 %), 3/4 mean 1.46; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.33, ribs 0.79 mm (74 %), 3/4 mean 2.49; Δ outline bias mean +2.00 (range +1.98..+2.00), Δ rib mean +0.00 mm
- command: python models/M08_superformula_knots/E3_tri_height/run.py

### 2026-11-23 22:50 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v2)
- twist x0.94: front 3/19, 3/4 1/19, outline max 2.45, ribs 2.23 mm (41 %), 3/4 mean 1.65; Δ outline bias mean -0.28 (range -2.30..+2.04), Δ rib mean +1.82 mm
- twist x0.97: front 4/19, 3/4 2/19, outline max 2.35, ribs 1.30 mm (56 %), 3/4 mean 1.20; Δ outline bias mean -0.13 (range -1.14..+1.03), Δ rib mean +0.65 mm
- twist x1.0: front 6/19, 3/4 8/19, outline max 2.35, ribs 0.79 mm (74 %), 3/4 mean 0.97; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 4/19, 3/4 5/19, outline max 2.35, ribs 1.17 mm (59 %), 3/4 mean 1.20; Δ outline bias mean +0.12 (range -0.94..+1.11), Δ rib mean +0.49 mm
- twist x1.06: front 3/19, 3/4 5/19, outline max 2.82, ribs 1.99 mm (44 %), 3/4 mean 1.59; Δ outline bias mean +0.24 (range -1.68..+2.20), Δ rib mean +1.47 mm
- 1-knot bumps: mean locality share 0.93 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 °
- command: python models/M08_superformula_knots/E4_twist/run.py

### 2026-11-23 22:50 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v2)
- r0 -2 mm: front 0/19, 3/4 3/19, outline max 2.10, ribs 1.33 mm (61 %), 3/4 mean 1.74; Δ outline bias mean -1.89 (range -1.99..-1.64), Δ rib mean +0.68 mm
- r0 -1 mm: front 0/19, 3/4 3/19, outline max 1.35, ribs 0.98 mm (67 %), 3/4 mean 1.18; Δ outline bias mean -0.94 (range -1.00..-0.82), Δ rib mean +0.24 mm
- r0 +0 mm: front 6/19, 3/4 8/19, outline max 2.35, ribs 0.79 mm (74 %), 3/4 mean 0.97; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 7/19, outline max 3.34, ribs 0.85 mm (68 %), 3/4 mean 1.38; Δ outline bias mean +0.94 (range +0.82..+1.00), Δ rib mean +0.06 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.34, ribs 1.07 mm (60 %), 3/4 mean 2.23; Δ outline bias mean +1.89 (range +1.64..+1.99), Δ rib mean +0.32 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 mm
- command: python models/M08_superformula_knots/E5_radius/run.py

### 2026-11-23 22:50 — E6 sections (count x placement) (kernel v2)
- uniform_z n=8: loft deviation from exact max 0.91 / mean 0.191 mm; front 5/19, 3/4 9/19
- uniform_z n=11: loft deviation from exact max 0.95 / mean 0.136 mm; front 5/19, 3/4 9/19
- uniform_z n=15: loft deviation from exact max 0.77 / mean 0.086 mm; front 6/19, 3/4 8/19
- uniform_z n=20: loft deviation from exact max 0.72 / mean 0.052 mm; front 6/19, 3/4 8/19
- uniform_z n=30: loft deviation from exact max 0.36 / mean 0.029 mm; front 6/19, 3/4 6/19
- uniform_z n=39: loft deviation from exact max 0.08 / mean 0.010 mm; front 6/19, 3/4 7/19
- adaptive n=8: loft deviation from exact max 0.94 / mean 0.179 mm; front 5/19, 3/4 9/19
- adaptive n=11: loft deviation from exact max 0.82 / mean 0.128 mm; front 6/19, 3/4 11/19
- adaptive n=15: loft deviation from exact max 0.61 / mean 0.101 mm; front 6/19, 3/4 7/19
- adaptive n=20: loft deviation from exact max 0.44 / mean 0.056 mm; front 6/19, 3/4 8/19
- adaptive n=30: loft deviation from exact max 0.14 / mean 0.015 mm; front 6/19, 3/4 6/19
- adaptive n=39: loft deviation from exact max 0.09 / mean 0.005 mm; front 6/19, 3/4 6/19
- knots10 n=20: loft deviation from exact max 0.72 / mean 0.052 mm; front 6/19, 3/4 8/19
- own sections: {'mode': 'knots10'}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M08_superformula_knots/E6_sections/run.py

### 2026-11-23 22:50 — correction to the diagnostics entry above (kernel v2)
- the garbled clause 'n1 ≈ 0.6·(n2/2 − 1)/0.6 ...' in check 2 should read: the valley depth fixes a = (n2/2 − 1)/n1 ≈ 0.60, so n1 ≥ 0.3 means n2 ≥ ≈ 2.36; the scan shows n2 below that (n1 < 0.3) is worse anyway (2.2 -> 109.4, 2.1 -> 123.6), so the bound does not cut off a better shape

### 2026-11-23 22:51 — summary written (kernel v2)
- summary.json: front 6/19 (S02-S07), 3/4 8/19, ribs 0.79 mm / 74 %, locality 0.94 (twist 0.93, radius 0.96), loft_dev_20 0.44 mm -> buildability gate fails (same Catmull-Rom end-interval effect as M06), smoothness score 0.18 (r0 4 / twist 8 inflections), constraints OK

### 2026-11-23 22:51 — MODEL.md conclusions written (kernel v2)
- per-experiment numbers, segment pass/fail, limits (twist anchoring + base direction), hypothesis check: n2 stays 2.30-2.42 (rose-like), drawing rejects pointed tips; cost 209.1 > M06 194.8 because the superformula only matches the rose to 0.003 in rho

### 2026-11-23 23:11 — E0 fit (kernel v3)
- start (as built): front 0/19, 3/4 10/19, ribs 1.21 mm
- result (as built): front 5/19, 3/4 10/19, outline max 2.54, ribs 0.71 mm / 75 %, 3/4 mean 0.98
- exact curves: front 6/19, 3/4 9/19
- 52 params, 663.4 s, nfev 16, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 181.6, pool:M01_E0 177.5, pool:M05_E0 178.2, pool:M02_X1c 179.1, pool:M01_E0v2 179.7, pool:M02_E0v2 181.7, pool:M03_E0v2 177.8, pool:M04_E0v2 181.8, pool:M05_E0v2 175.6, pool:M06_E0v2 181.7, pool:M07_E0v2 178.8, pool:M08_E0v2 177.4, pool:M09_E0v2 203.0, pool:M10_E0v2 178.7 -> best: pool:M05_E0v2
- Fusion script: models\M08_superformula_knots\fusion\M08\M08.py
- command: python models/M08_superformula_knots/E0_fit/run.py

### 2026-11-23 23:11 — E1 triangle count (kernel v3)
- N=12: front 5/19, 3/4 3/19, outline max 1.97, ribs 0.71 mm (75 %), 3/4 mean 1.02; Δ outline bias mean -0.31 (range -0.72..-0.05), Δ rib mean +0.00 mm
- N=16: front 5/19, 3/4 7/19, outline max 2.21, ribs 0.71 mm (75 %), 3/4 mean 0.95; Δ outline bias mean -0.18 (range -0.36..+0.01), Δ rib mean +0.00 mm
- N=22 (own): front 5/19, 3/4 10/19, outline max 2.54, ribs 0.71 mm (75 %), 3/4 mean 0.98; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 4/19, 3/4 7/19, outline max 2.71, ribs 0.71 mm (75 %), 3/4 mean 1.01; Δ outline bias mean +0.12 (range +0.05..+0.26), Δ rib mean +0.00 mm
- N=45: front 4/19, 3/4 9/19, outline max 2.82, ribs 0.71 mm (75 %), 3/4 mean 1.00; Δ outline bias mean +0.19 (range +0.10..+0.33), Δ rib mean +0.00 mm
- command: python models/M08_superformula_knots/E1_tri_count/run.py

### 2026-11-23 23:11 — E2 triangle width (fill) x placement (kernel v3)
- arc f=0.5: front 4/19, 3/4 10/19, outline max 2.68, ribs 0.71 mm (75 %), 3/4 mean 1.01; Δ outline bias mean +0.14 (range +0.07..+0.18), Δ rib mean +0.00 mm
- arc f=0.7: front 4/19, 3/4 10/19, outline max 2.64, ribs 0.71 mm (75 %), 3/4 mean 1.01; Δ outline bias mean +0.09 (range +0.05..+0.12), Δ rib mean +0.00 mm
- arc f=0.85: front 5/19, 3/4 10/19, outline max 2.59, ribs 0.71 mm (75 %), 3/4 mean 0.99; Δ outline bias mean +0.05 (range +0.03..+0.07), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 5/19, 3/4 10/19, outline max 2.54, ribs 0.71 mm (75 %), 3/4 mean 0.98; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 2/19, 3/4 9/19, outline max 2.89, ribs 0.80 mm (75 %), 3/4 mean 0.99; Δ outline bias mean +0.15 (range +0.01..+0.42), Δ rib mean +0.10 mm
- angle_half f=0.7: front 2/19, 3/4 9/19, outline max 2.89, ribs 0.80 mm (75 %), 3/4 mean 0.99; Δ outline bias mean +0.11 (range -0.02..+0.42), Δ rib mean +0.10 mm
- angle_half f=0.85: front 2/19, 3/4 9/19, outline max 2.89, ribs 0.80 mm (75 %), 3/4 mean 0.99; Δ outline bias mean +0.08 (range -0.06..+0.42), Δ rib mean +0.10 mm
- angle_half f=1.0: front 2/19, 3/4 9/19, outline max 2.89, ribs 0.80 mm (75 %), 3/4 mean 0.99; Δ outline bias mean +0.04 (range -0.10..+0.42), Δ rib mean +0.10 mm
- command: python models/M08_superformula_knots/E2_tri_width/run.py

### 2026-11-23 23:11 — E3 triangle height (kernel v3)
- H=1.5: front 0/19, 3/4 3/19, outline max 1.83, ribs 0.71 mm (75 %), 3/4 mean 1.54; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 3/19, outline max 1.55, ribs 0.71 mm (75 %), 3/4 mean 1.26; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 5/19, 3/4 10/19, outline max 2.54, ribs 0.71 mm (75 %), 3/4 mean 0.98; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 6/19, outline max 3.53, ribs 0.71 mm (75 %), 3/4 mean 1.40; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.53, ribs 0.71 mm (75 %), 3/4 mean 2.35; Δ outline bias mean +2.00 (range +1.98..+2.00), Δ rib mean +0.00 mm
- command: python models/M08_superformula_knots/E3_tri_height/run.py

### 2026-11-23 23:11 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v3)
- twist x0.94: front 2/19, 3/4 2/19, outline max 2.54, ribs 2.17 mm (40 %), 3/4 mean 1.66; Δ outline bias mean -0.28 (range -2.17..+1.91), Δ rib mean +1.87 mm
- twist x0.97: front 3/19, 3/4 2/19, outline max 2.54, ribs 1.25 mm (55 %), 3/4 mean 1.21; Δ outline bias mean -0.13 (range -1.07..+0.96), Δ rib mean +0.69 mm
- twist x1.0: front 5/19, 3/4 10/19, outline max 2.54, ribs 0.71 mm (75 %), 3/4 mean 0.98; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 3/19, 3/4 4/19, outline max 2.54, ribs 1.15 mm (59 %), 3/4 mean 1.14; Δ outline bias mean +0.12 (range -0.93..+1.04), Δ rib mean +0.58 mm
- twist x1.06: front 2/19, 3/4 4/19, outline max 2.54, ribs 1.97 mm (47 %), 3/4 mean 1.45; Δ outline bias mean +0.22 (range -1.61..+2.05), Δ rib mean +1.60 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 °
- command: python models/M08_superformula_knots/E4_twist/run.py

### 2026-11-23 23:11 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v3)
- r0 -2 mm: front 0/19, 3/4 2/19, outline max 2.04, ribs 1.26 mm (57 %), 3/4 mean 1.85; Δ outline bias mean -1.89 (range -1.99..-1.66), Δ rib mean +0.70 mm
- r0 -1 mm: front 0/19, 3/4 4/19, outline max 1.54, ribs 0.88 mm (68 %), 3/4 mean 1.21; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.22 mm
- r0 +0 mm: front 5/19, 3/4 10/19, outline max 2.54, ribs 0.71 mm (75 %), 3/4 mean 0.98; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 6/19, outline max 3.53, ribs 0.79 mm (69 %), 3/4 mean 1.32; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.10 mm
- r0 +2 mm: front 0/19, 3/4 2/19, outline max 4.53, ribs 1.07 mm (63 %), 3/4 mean 2.06; Δ outline bias mean +1.89 (range +1.66..+1.99), Δ rib mean +0.44 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 mm
- command: python models/M08_superformula_knots/E5_radius/run.py

### 2026-11-23 23:11 — E6 sections (count x placement) (kernel v3)
- uniform_z n=8: loft deviation from exact max 0.91 / mean 0.195 mm; front 3/19, 3/4 7/19
- uniform_z n=11: loft deviation from exact max 0.96 / mean 0.168 mm; front 3/19, 3/4 8/19
- uniform_z n=15: loft deviation from exact max 0.76 / mean 0.090 mm; front 6/19, 3/4 9/19
- uniform_z n=20: loft deviation from exact max 0.71 / mean 0.051 mm; front 5/19, 3/4 10/19
- uniform_z n=30: loft deviation from exact max 0.36 / mean 0.029 mm; front 6/19, 3/4 9/19
- uniform_z n=39: loft deviation from exact max 0.08 / mean 0.010 mm; front 6/19, 3/4 9/19
- adaptive n=8: loft deviation from exact max 0.94 / mean 0.191 mm; front 3/19, 3/4 7/19
- adaptive n=11: loft deviation from exact max 0.83 / mean 0.153 mm; front 5/19, 3/4 9/19
- adaptive n=15: loft deviation from exact max 0.62 / mean 0.091 mm; front 6/19, 3/4 10/19
- adaptive n=20: loft deviation from exact max 0.49 / mean 0.061 mm; front 6/19, 3/4 8/19
- adaptive n=30: loft deviation from exact max 0.14 / mean 0.014 mm; front 6/19, 3/4 9/19
- adaptive n=39: loft deviation from exact max 0.10 / mean 0.006 mm; front 5/19, 3/4 9/19
- knots10 n=20: loft deviation from exact max 0.71 / mean 0.051 mm; front 5/19, 3/4 10/19
- own sections: {'mode': 'knots10'}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M08_superformula_knots/E6_sections/run.py

### 2026-11-23 23:14 — final round (kernel v3) — results recorded (kernel v3)
- rank 9/10, score 0.452; front 5/19, 3/4 10/19, ribs 0.71 mm, cost 175.6 (best start pool:M05_E0v2)
- orientation offset -1.13°; MODEL.md: 'Final round — kernel v3' section appended; verified by judge/verify_e0.py
