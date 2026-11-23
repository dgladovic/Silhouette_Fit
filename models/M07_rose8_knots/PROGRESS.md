# M07_rose8_knots — progress

## Status  (overwrite this block only)
- State: final (kernel v3), rank 3/10
- Best E0 (as built): front 13/19, 3/4 13/19, 52 params, score 0.650
- Next: none (study complete)

## Log  (append only, newest at the bottom)

### 2026-11-23 22:42 — model created (kernel v2)
- model.py: rose + 8θ harmonic base rho = (1 + k cos4θ + c cos8θ)/(1 + k + c) (bases.rose8); k(z) and c(z) each Catmull-Rom through 6 nodes z = 0,38,76,114,152,190 (12 params)
- radius r0(z): value knots every 10 mm (z = 0..190, 20 params), Catmull-Rom; twist: knots every 10 mm, twist(0) = 0 fixed (19 free) -> 51 params
- penalties: SMOOTH_W mm/deg/k (0.05/0.05/2.0) x second_diff of r / twist / k / c knots; k soft floor 50*min(k-0.02,0) (as M05/M06)
- bounds: r 20..160 mm, twist -30..150 deg, k 0..0.45, c -0.08..0.08 (orchestrator spec); constraints: rho > 0 and max rho <= 1.001 on bases.TH for every z (1 mm grid), k(z) in 0.02..0.4, r0 >= 20 mm (as M06)
- note: at k = 0.2 the tip stops being the outermost point for c below about -k/4 = -0.05 (rose8(0.2,-0.08) max 1.020), so the lower c bound can produce invalid sections; the constraint reports it, no penalty added (spec)
- start: M05 kernel-v2 E0 (models/M05_rose_bezier/E0_fit/params.json) sampled at the knots: r0, twist; k = M05 k values; c = 0 (baked as literals). So P0 = M06-like start with the v2 M05 curves
- start check: r0 42.6..115.1 mm, twist 0 -> 87.9 deg, rho(0) = 1, rho in 0.636..1.000, constraints OK
- start score: exact front 0/19, 3/4 6/19, ribs 1.39 mm; as built front 0/19, 3/4 8/19, ribs 1.40 mm (twist(0) clamp at the rim shifts the anchored ribs, same effect M06 logged)
- settings: inherit M05: N 22, H 3.0, arc placement 9 mm target, sections knots10 (20 sections on the knots) - docs/05 §5.4

### 2026-11-23 22:42 — MODEL.md written (kernel v2)
- definition (51 params) + hypothesis before running: c > 0 (+0.02..+0.05) in the waist, waist ribs -0.1..-0.3 mm vs M06, front 6-9/19, 3/4 9-11/19, neck still limited by fixed rim twist, locality ~ M06

### 2026-11-23 22:46 — E0 fit (kernel v2)
- start (as built): front 0/19, 3/4 8/19, ribs 1.40 mm
- result (as built): front 11/19, 3/4 6/19, outline max 1.30, ribs 0.41 mm / 90 %, 3/4 mean 1.51
- exact curves: front 12/19, 3/4 8/19
- 51 params, 227.1 s, nfev 13, cap hit [False, False, False], constraints ['section rho > 1.001 (max 1.0337 at z = 190, tip not outermost)']
- multi-start (cost per start): own start (P0) 73.6, pool:M01_E0 153.0, pool:M05_E0 77.7, pool:M02_X1c 73.0 -> best: pool:M02_X1c
- Fusion script: models\M07_rose8_knots\fusion\M07\M07.py
- command: python models/M07_rose8_knots/E0_fit/run.py

### 2026-11-23 22:47 — first E0 rejected: invalid section at the top; model.py change (kernel v2)
- first E0 (saved in E0_fit_first_invalid/): cost 73.0 (best start pool:M02_X1c; own P0 73.6, M05 77.7, M01 153.0), as built front 11/19, 3/4 6/19, ribs 0.41 mm / 90 %, outline max 1.30, 3/4 mean 1.51
- constraint failure: c(z) ran to the lower bound at z = 190 (c = -0.079, k = 0.164); for c < -k/4 the tip at θ = 0 is no longer the outermost point: max rho 1.034, invalid for z = 175..190 (S18, S19)
- fitted c elsewhere: -0.035 / -0.031 / -0.032 / -0.014 / -0.005 at z = 0/38/76/114/152 (negative = rounder lobes, not sharper creases)
- change model.py: penalty(p) gets 19 extra residuals W_VALID * max(max_theta rho - 1, 0) per 10 mm band (1 mm grid), W_VALID = 300 (0.03 excess -> residual 9). Old: no validity term (spec listed only the constraint). Why: the protocol requires a buildable section; the bound -0.08 alone does not keep c above -k/4
- bounds, start, settings, other penalties unchanged; re-running E0

### 2026-11-23 22:50 — E0 fit (kernel v2)
- start (as built): front 0/19, 3/4 8/19, ribs 1.40 mm
- result (as built): front 10/19, 3/4 11/19, outline max 1.09, ribs 0.41 mm / 88 %, 3/4 mean 1.11
- exact curves: front 11/19, 3/4 12/19
- 51 params, 216.3 s, nfev 14, cap hit [False, False, False], constraints ['section rho > 1.001 (max 1.0025 at z = 190, tip not outermost)']
- multi-start (cost per start): own start (P0) 74.5, pool:M01_E0 74.6, pool:M05_E0 73.9, pool:M02_X1c 74.8 -> best: pool:M05_E0
- Fusion script: models\M07_rose8_knots\fusion\M07\M07.py
- command: python models/M07_rose8_knots/E0_fit/run.py

### 2026-11-23 22:51 — second E0 still invalid; model.py change W_VALID 300 -> 3000 (kernel v2)
- second E0 (W_VALID 300, saved in E0_fit_second_w300/): cost 73.9 (all 4 starts 73.9..74.8, best pool:M05_E0), as built front 10/19, 3/4 11/19, ribs 0.41 mm / 88 %, outline max 1.09, 3/4 mean 1.11
- constraint still fails: max rho 1.0025 at z = 190 (c@190 = -0.054, k@190 = 0.180, c/k = -0.30); the penalty residual was only 0.75, too weak against the neck pull
- fitted c: -0.041 / -0.035 / -0.036 / -0.016 / -0.007 / -0.054 at z = 0/38/76/114/152/190 (negative everywhere)
- change model.py: W_VALID 300 -> 3000 (excess 0.0025 -> residual 7.5). Nothing else changed; re-running E0

### 2026-11-23 22:54 — E0 fit (kernel v2)
- start (as built): front 0/19, 3/4 8/19, ribs 1.40 mm
- result (as built): front 10/19, 3/4 12/19, outline max 1.03, ribs 0.43 mm / 88 %, 3/4 mean 1.11
- exact curves: front 11/19, 3/4 13/19
- 51 params, 196.8 s, nfev 14, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 77.3, pool:M01_E0 82.9, pool:M05_E0 74.9, pool:M02_X1c 75.5 -> best: pool:M05_E0
- Fusion script: models\M07_rose8_knots\fusion\M07\M07.py
- command: python models/M07_rose8_knots/E0_fit/run.py

### 2026-11-23 22:56 — E0 accepted (third run, W_VALID 3000) (kernel v2)
- cost 74.9 (starts: own 77.3, M01 82.9, M05 74.9, M02_X1c 75.5: all 4 within 8 %, so a stable minimum), constraints OK (max rho excess 0.00009 at z = 190)
- as built front 10/19 (S02-S07, S12-S14, S18), 3/4 12/19 (S05-S16); exact 11/19 / 13/19. vs M06 cost 194.8 front 5/19 3/4 10/19
- fitted c (z = 0/38/76/114/152/190): -0.042 / -0.034 / -0.037 / -0.016 / -0.007 / -0.046 (c/k -0.17 / -0.14 / -0.17 / -0.08 / -0.03 / -0.26): NEGATIVE = rounder, fuller lobes with a broader valley, not sharper creases
- k rose vs M05: 0.241 / 0.241 / 0.225 / 0.202 / 0.200 / 0.178 (M05 0.215 / 0.204 / 0.209 / 0.184 / 0.222 / 0.173)
- cost of the validity penalty: 73.0 (invalid) -> 73.9 (w300, still invalid) -> 74.9 (valid): the fit wants c below -k/4 at the neck
- note: 3/4 v34_max 27.7 mm is one row (z = 189.5, top-left rim edge, row 0 of 272); it lifts S19 3/4 mean to 3.68 mm. S01 3/4 3.03 mm, S02/S03 1.8 mm (rim flare, see overlay_v34)

### 2026-11-23 22:56 — E1 triangle count (kernel v2)
- N=12: front 8/19, 3/4 6/19, outline max 0.85, ribs 0.43 mm (88 %), 3/4 mean 1.15; Δ outline bias mean -0.24 (range -0.56..-0.03), Δ rib mean +0.00 mm
- N=16: front 10/19, 3/4 10/19, outline max 0.81, ribs 0.43 mm (88 %), 3/4 mean 1.07; Δ outline bias mean -0.13 (range -0.32..-0.01), Δ rib mean +0.00 mm
- N=22 (own): front 10/19, 3/4 12/19, outline max 1.03, ribs 0.43 mm (88 %), 3/4 mean 1.11; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 10/19, 3/4 12/19, outline max 1.13, ribs 0.43 mm (88 %), 3/4 mean 1.13; Δ outline bias mean +0.10 (range +0.02..+0.17), Δ rib mean +0.00 mm
- N=45: front 10/19, 3/4 11/19, outline max 1.20, ribs 0.43 mm (88 %), 3/4 mean 1.18; Δ outline bias mean +0.17 (range +0.05..+0.25), Δ rib mean +0.00 mm
- command: python models/M07_rose8_knots/E1_tri_count/run.py

### 2026-11-23 22:56 — E2 triangle width (fill) x placement (kernel v2)
- arc f=0.5: front 10/19, 3/4 12/19, outline max 1.11, ribs 0.43 mm (88 %), 3/4 mean 1.15; Δ outline bias mean +0.12 (range +0.03..+0.17), Δ rib mean +0.00 mm
- arc f=0.7: front 10/19, 3/4 12/19, outline max 1.09, ribs 0.43 mm (88 %), 3/4 mean 1.13; Δ outline bias mean +0.08 (range +0.02..+0.11), Δ rib mean +0.00 mm
- arc f=0.85: front 10/19, 3/4 12/19, outline max 1.06, ribs 0.43 mm (88 %), 3/4 mean 1.12; Δ outline bias mean +0.04 (range +0.01..+0.06), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 10/19, 3/4 12/19, outline max 1.03, ribs 0.43 mm (88 %), 3/4 mean 1.11; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 7/19, 3/4 12/19, outline max 1.25, ribs 0.65 mm (79 %), 3/4 mean 1.12; Δ outline bias mean +0.13 (range +0.04..+0.24), Δ rib mean +0.28 mm
- angle_half f=0.7: front 7/19, 3/4 12/19, outline max 1.25, ribs 0.65 mm (79 %), 3/4 mean 1.10; Δ outline bias mean +0.09 (range +0.03..+0.24), Δ rib mean +0.28 mm
- angle_half f=0.85: front 7/19, 3/4 12/19, outline max 1.25, ribs 0.65 mm (79 %), 3/4 mean 1.07; Δ outline bias mean +0.06 (range -0.02..+0.24), Δ rib mean +0.28 mm
- angle_half f=1.0: front 7/19, 3/4 12/19, outline max 1.25, ribs 0.65 mm (79 %), 3/4 mean 1.06; Δ outline bias mean +0.01 (range -0.07..+0.24), Δ rib mean +0.28 mm
- command: python models/M07_rose8_knots/E2_tri_width/run.py

### 2026-11-23 22:56 — E3 triangle height (kernel v2)
- H=1.5: front 0/19, 3/4 1/19, outline max 1.87, ribs 0.43 mm (88 %), 3/4 mean 1.49; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 2/19, outline max 1.37, ribs 0.43 mm (88 %), 3/4 mean 1.27; Δ outline bias mean -1.00 (range -1.00..-1.00), Δ rib mean +0.00 mm
- H=3.0 (own): front 10/19, 3/4 12/19, outline max 1.03, ribs 0.43 mm (88 %), 3/4 mean 1.11; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 2/19, outline max 2.02, ribs 0.43 mm (88 %), 3/4 mean 1.80; Δ outline bias mean +1.00 (range +1.00..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 3.02, ribs 0.43 mm (88 %), 3/4 mean 2.82; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M07_rose8_knots/E3_tri_height/run.py

### 2026-11-23 22:56 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v2)
- twist x0.94: front 3/19, 3/4 4/19, outline max 2.38, ribs 2.15 mm (39 %), 3/4 mean 1.85; Δ outline bias mean -0.28 (range -2.21..+1.98), Δ rib mean +2.17 mm
- twist x0.97: front 5/19, 3/4 8/19, outline max 1.22, ribs 1.17 mm (52 %), 3/4 mean 1.41; Δ outline bias mean -0.14 (range -1.09..+1.01), Δ rib mean +0.94 mm
- twist x1.0: front 10/19, 3/4 12/19, outline max 1.03, ribs 0.43 mm (88 %), 3/4 mean 1.11; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 5/19, 3/4 9/19, outline max 1.90, ribs 1.04 mm (59 %), 3/4 mean 1.21; Δ outline bias mean +0.14 (range -0.86..+1.07), Δ rib mean +0.77 mm
- twist x1.06: front 3/19, 3/4 5/19, outline max 3.06, ribs 1.93 mm (45 %), 3/4 mean 1.47; Δ outline bias mean +0.27 (range -1.45..+2.17), Δ rib mean +1.87 mm
- 1-knot bumps: mean locality share 0.93 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 °
- command: python models/M07_rose8_knots/E4_twist/run.py

### 2026-11-23 22:56 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v2)
- r0 -2 mm: front 0/19, 3/4 0/19, outline max 2.18, ribs 1.39 mm (56 %), 3/4 mean 1.78; Δ outline bias mean -1.90 (range -2.00..-1.67), Δ rib mean +1.20 mm
- r0 -1 mm: front 0/19, 3/4 3/19, outline max 1.22, ribs 0.81 mm (75 %), 3/4 mean 1.23; Δ outline bias mean -0.95 (range -1.00..-0.84), Δ rib mean +0.47 mm
- r0 +0 mm: front 10/19, 3/4 12/19, outline max 1.03, ribs 0.43 mm (88 %), 3/4 mean 1.11; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 3/19, outline max 2.02, ribs 0.68 mm (81 %), 3/4 mean 1.72; Δ outline bias mean +0.95 (range +0.84..+1.00), Δ rib mean +0.30 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 3.02, ribs 1.08 mm (60 %), 3/4 mean 2.58; Δ outline bias mean +1.90 (range +1.67..+2.00), Δ rib mean +0.80 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 mm
- command: python models/M07_rose8_knots/E5_radius/run.py

### 2026-11-23 22:56 — E6 sections (count x placement) (kernel v2)
- uniform_z n=8: loft deviation from exact max 0.83 / mean 0.149 mm; front 10/19, 3/4 10/19
- uniform_z n=11: loft deviation from exact max 0.84 / mean 0.107 mm; front 11/19, 3/4 12/19
- uniform_z n=15: loft deviation from exact max 0.93 / mean 0.081 mm; front 11/19, 3/4 12/19
- uniform_z n=20: loft deviation from exact max 0.89 / mean 0.057 mm; front 10/19, 3/4 12/19
- uniform_z n=30: loft deviation from exact max 0.43 / mean 0.033 mm; front 11/19, 3/4 12/19
- uniform_z n=39: loft deviation from exact max 0.09 / mean 0.010 mm; front 11/19, 3/4 12/19
- adaptive n=8: loft deviation from exact max 0.85 / mean 0.122 mm; front 11/19, 3/4 11/19
- adaptive n=11: loft deviation from exact max 0.89 / mean 0.103 mm; front 10/19, 3/4 12/19
- adaptive n=15: loft deviation from exact max 0.67 / mean 0.100 mm; front 11/19, 3/4 12/19
- adaptive n=20: loft deviation from exact max 0.52 / mean 0.076 mm; front 12/19, 3/4 12/19
- adaptive n=30: loft deviation from exact max 0.12 / mean 0.013 mm; front 11/19, 3/4 13/19
- adaptive n=39: loft deviation from exact max 0.04 / mean 0.004 mm; front 11/19, 3/4 13/19
- knots10 n=20: loft deviation from exact max 0.89 / mean 0.057 mm; front 10/19, 3/4 12/19
- own sections: {'mode': 'knots10'}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M07_rose8_knots/E6_sections/run.py

### 2026-11-23 22:57 — summary + observations (kernel v2)
- summary.json written: 51 params, locality 0.94 (twist 0.93, radius 0.96), smoothness r0 4 / twist 6 inflections (score 0.22), constraints OK, loft_dev_20 0.52 mm (adaptive 20) -> buildable False (gate 0.3 mm); knots10 own sections: S01 0.89, S19 0.72 mm, S02-S18 <= 0.05 mm (Catmull-Rom end intervals, same cause as M06)
- front fails S08-S11, S15-S17 are all on within-1 mm (67-75 %), not on rib mean (0.49-1.05) or outline; they come from a few whole ribs > 1 mm off: x0 -49 / 0 / +41 in S07-S11, x0 +-9 in S10-S16, x0 -20 in S15-S18. x0 = +40.6 (not excluded by the kernel; only -40.7 is) runs -7.6 mm off in S09-S13 (diagnostic only, nothing excluded)
- 3/4 (held out) worse than M06 at the ends: S01 3.03 (M06 2.45), S02 1.83 (0.88), S03 1.86 (0.91), S18 1.76 (0.60), S19 3.68 (0.62; 1.93 without the single z = 189.5 rim row). Better in S06-S10 (0.29-0.53 vs 0.58-2.10)
- MODEL.md: the definition paragraph "What c does" had the crease direction backwards (c < 0 sharpens the valley: valley curvature 16k - 64c); corrected with a note. Hypothesis left unchanged

### 2026-11-23 22:58 — MODEL.md conclusions written (kernel v2)
- per-experiment conclusions, segment pass/fail, M06/M05 comparison, limits, hypothesis check (c negative not positive; front 10/19 exceeded the 6-9 guess; neck not limited by the rim twist)

### 2026-11-23 23:10 — E0 fit (kernel v3)
- start (as built): front 0/19, 3/4 8/19, ribs 1.40 mm
- result (as built): front 13/19, 3/4 13/19, outline max 1.73, ribs 0.43 mm / 90 %, 3/4 mean 0.91
- exact curves: front 14/19, 3/4 13/19
- 52 params, 596.8 s, nfev 48, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 107.6, pool:M01_E0 101.1, pool:M05_E0 111.8, pool:M02_X1c 101.6, pool:M01_E0v2 104.4, pool:M02_E0v2 95.0, pool:M03_E0v2 99.7, pool:M04_E0v2 79.3, pool:M05_E0v2 112.1, pool:M06_E0v2 103.6, pool:M07_E0v2 82.4, pool:M08_E0v2 101.1, pool:M09_E0v2 107.5, pool:M10_E0v2 101.1 -> best: pool:M04_E0v2
- Fusion script: models\M07_rose8_knots\fusion\M07\M07.py
- command: python models/M07_rose8_knots/E0_fit/run.py

### 2026-11-23 23:10 — E1 triangle count (kernel v3)
- N=12: front 9/19, 3/4 6/19, outline max 1.33, ribs 0.43 mm (90 %), 3/4 mean 1.08; Δ outline bias mean -0.25 (range -0.58..-0.06), Δ rib mean +0.00 mm
- N=16: front 11/19, 3/4 10/19, outline max 1.47, ribs 0.43 mm (90 %), 3/4 mean 1.00; Δ outline bias mean -0.14 (range -0.33..+0.03), Δ rib mean +0.00 mm
- N=22 (own): front 13/19, 3/4 13/19, outline max 1.73, ribs 0.43 mm (90 %), 3/4 mean 0.91; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 11/19, 3/4 12/19, outline max 1.86, ribs 0.43 mm (90 %), 3/4 mean 0.99; Δ outline bias mean +0.11 (range +0.02..+0.19), Δ rib mean +0.00 mm
- N=45: front 11/19, 3/4 13/19, outline max 1.95, ribs 0.43 mm (90 %), 3/4 mean 1.03; Δ outline bias mean +0.18 (range +0.05..+0.25), Δ rib mean +0.00 mm
- command: python models/M07_rose8_knots/E1_tri_count/run.py

### 2026-11-23 23:10 — E2 triangle width (fill) x placement (kernel v3)
- arc f=0.5: front 13/19, 3/4 13/19, outline max 1.84, ribs 0.43 mm (90 %), 3/4 mean 0.94; Δ outline bias mean +0.12 (range +0.03..+0.16), Δ rib mean +0.00 mm
- arc f=0.7: front 13/19, 3/4 13/19, outline max 1.80, ribs 0.43 mm (90 %), 3/4 mean 0.93; Δ outline bias mean +0.08 (range +0.02..+0.11), Δ rib mean +0.00 mm
- arc f=0.85: front 13/19, 3/4 13/19, outline max 1.77, ribs 0.43 mm (90 %), 3/4 mean 0.93; Δ outline bias mean +0.04 (range +0.01..+0.06), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 13/19, 3/4 13/19, outline max 1.73, ribs 0.43 mm (90 %), 3/4 mean 0.91; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 5/19, 3/4 14/19, outline max 2.01, ribs 0.52 mm (84 %), 3/4 mean 0.96; Δ outline bias mean +0.14 (range +0.04..+0.30), Δ rib mean +0.11 mm
- angle_half f=0.7: front 5/19, 3/4 14/19, outline max 2.01, ribs 0.52 mm (84 %), 3/4 mean 0.94; Δ outline bias mean +0.10 (range +0.02..+0.30), Δ rib mean +0.11 mm
- angle_half f=0.85: front 5/19, 3/4 14/19, outline max 2.01, ribs 0.52 mm (84 %), 3/4 mean 0.93; Δ outline bias mean +0.07 (range -0.03..+0.30), Δ rib mean +0.11 mm
- angle_half f=1.0: front 5/19, 3/4 14/19, outline max 2.01, ribs 0.52 mm (84 %), 3/4 mean 0.92; Δ outline bias mean +0.02 (range -0.08..+0.30), Δ rib mean +0.11 mm
- command: python models/M07_rose8_knots/E2_tri_width/run.py

### 2026-11-23 23:10 — E3 triangle height (kernel v3)
- H=1.5: front 0/19, 3/4 1/19, outline max 1.88, ribs 0.43 mm (90 %), 3/4 mean 1.41; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 1/19, 3/4 4/19, outline max 1.39, ribs 0.43 mm (90 %), 3/4 mean 1.14; Δ outline bias mean -1.00 (range -1.00..-1.00), Δ rib mean +0.00 mm
- H=3.0 (own): front 13/19, 3/4 13/19, outline max 1.73, ribs 0.43 mm (90 %), 3/4 mean 0.91; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 1/19, outline max 2.73, ribs 0.43 mm (90 %), 3/4 mean 1.66; Δ outline bias mean +1.00 (range +1.00..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 3.72, ribs 0.43 mm (90 %), 3/4 mean 2.67; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M07_rose8_knots/E3_tri_height/run.py

### 2026-11-23 23:10 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v3)
- twist x0.94: front 3/19, 3/4 4/19, outline max 2.40, ribs 2.15 mm (39 %), 3/4 mean 1.73; Δ outline bias mean -0.27 (range -2.19..+1.96), Δ rib mean +2.17 mm
- twist x0.97: front 5/19, 3/4 9/19, outline max 1.73, ribs 1.18 mm (52 %), 3/4 mean 1.29; Δ outline bias mean -0.14 (range -1.07..+1.00), Δ rib mean +0.94 mm
- twist x1.0: front 13/19, 3/4 13/19, outline max 1.73, ribs 0.43 mm (90 %), 3/4 mean 0.91; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 5/19, 3/4 9/19, outline max 1.73, ribs 1.03 mm (60 %), 3/4 mean 1.02; Δ outline bias mean +0.13 (range -0.91..+1.04), Δ rib mean +0.76 mm
- twist x1.06: front 3/19, 3/4 8/19, outline max 2.84, ribs 1.93 mm (45 %), 3/4 mean 1.34; Δ outline bias mean +0.26 (range -1.45..+2.13), Δ rib mean +1.86 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 °
- command: python models/M07_rose8_knots/E4_twist/run.py

### 2026-11-23 23:10 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v3)
- r0 -2 mm: front 0/19, 3/4 1/19, outline max 2.30, ribs 1.26 mm (56 %), 3/4 mean 1.72; Δ outline bias mean -1.90 (range -2.00..-1.67), Δ rib mean +1.04 mm
- r0 -1 mm: front 1/19, 3/4 3/19, outline max 1.34, ribs 0.77 mm (72 %), 3/4 mean 1.19; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.42 mm
- r0 +0 mm: front 13/19, 3/4 13/19, outline max 1.73, ribs 0.43 mm (90 %), 3/4 mean 0.91; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 3/19, outline max 2.73, ribs 0.61 mm (83 %), 3/4 mean 1.56; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.23 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 3.72, ribs 1.01 mm (64 %), 3/4 mean 2.48; Δ outline bias mean +1.90 (range +1.67..+2.00), Δ rib mean +0.71 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 mm
- command: python models/M07_rose8_knots/E5_radius/run.py

### 2026-11-23 23:10 — E6 sections (count x placement) (kernel v3)
- uniform_z n=8: loft deviation from exact max 0.85 / mean 0.138 mm; front 12/19, 3/4 13/19
- uniform_z n=11: loft deviation from exact max 0.87 / mean 0.110 mm; front 13/19, 3/4 13/19
- uniform_z n=15: loft deviation from exact max 0.86 / mean 0.074 mm; front 12/19, 3/4 13/19
- uniform_z n=20: loft deviation from exact max 0.76 / mean 0.052 mm; front 13/19, 3/4 13/19
- uniform_z n=30: loft deviation from exact max 0.39 / mean 0.030 mm; front 14/19, 3/4 13/19
- uniform_z n=39: loft deviation from exact max 0.08 / mean 0.010 mm; front 14/19, 3/4 13/19
- adaptive n=8: loft deviation from exact max 0.88 / mean 0.124 mm; front 13/19, 3/4 12/19
- adaptive n=11: loft deviation from exact max 0.82 / mean 0.097 mm; front 12/19, 3/4 13/19
- adaptive n=15: loft deviation from exact max 0.62 / mean 0.090 mm; front 14/19, 3/4 13/19
- adaptive n=20: loft deviation from exact max 0.46 / mean 0.066 mm; front 14/19, 3/4 13/19
- adaptive n=30: loft deviation from exact max 0.15 / mean 0.014 mm; front 14/19, 3/4 13/19
- adaptive n=39: loft deviation from exact max 0.02 / mean 0.003 mm; front 14/19, 3/4 13/19
- knots10 n=20: loft deviation from exact max 0.76 / mean 0.052 mm; front 13/19, 3/4 13/19
- own sections: {'mode': 'knots10'}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M07_rose8_knots/E6_sections/run.py

### 2026-11-23 23:14 — final round (kernel v3) — results recorded (kernel v3)
- rank 3/10, score 0.650; front 13/19, 3/4 13/19, ribs 0.43 mm, cost 79.3 (best start pool:M04_E0v2)
- orientation offset -0.46°; MODEL.md: 'Final round — kernel v3' section appended; verified by judge/verify_e0.py
