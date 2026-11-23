# M10_rose_ribangle — progress

## Status  (overwrite this block only)
- State: final (kernel v3), rank 8/10
- Best E0 (as built): front 5/19, 3/4 10/19, 47 params, score 0.453
- Next: none (study complete)

## Log  (append only, newest at the bottom)

### 2026-11-23 22:43 — model created (kernel v2)
- model.py: rose k(z) (6 Catmull-Rom nodes z=0,38..190, as M05/M06) + radius knots every 10 mm (20, Catmull-Rom) + rib lean angle alpha knots every 10 mm (20, Catmull-Rom, deg from vertical); 46 params
- twist(z) = (180/pi) * int_0^z tan(alpha)/r0 dz' : cumulative trapezoid on a 0.25 mm grid (761 pts), np.interp to the requested z; twist(0)=0 by construction, alpha(0) free; shape(p)+twist eval ~0.13 ms
- smoothness: SMOOTH_W mm/deg/k x second_diff of r / alpha / k knots; k soft floor 50*min(k-0.02,0) (as M05/M06)
- bounds: r 20..160 mm, alpha -30..75 deg, k 0..0.45; constraints: k(z) in 0.02..0.4, r0 >= 20 mm, |alpha(z)| <= 80
- start: M05 kernel-v2 E0 (study.load_E0) -> r0 at the knots, alpha = atan(r0 * dtwist/dz * pi/180) at the knots, k = M05 fitted k; baked as literals
- start check: alpha(0) sampled = -65.95 deg (M05's steep rim dip: twist -0.39 deg at z=0.25, -1.06 at z=4) -> outside bounds, clipped to -30. Rebuilt twist vs M05: max 0.60 deg (z=10), constant -0.48 deg above z=20 (unclipped: 4.1 deg, the trapezoid can't follow the infinite slope at z=0). r0 vs M05 max 0.85 mm (S01/S19 Catmull-Rom end intervals)
- for reference: a least-squares alpha projection reproduces M05 twist within 0.45 deg at z=1.25 and <= 0.09 deg elsewhere (alpha(0) = -22.4); the kernel's pool:M05 start does this projection anyway, so P0 stays the spec'd sampled version
- start (P0) score: exact front 0/19, 3/4 4/19, ribs 1.26 mm; as built front 0/19, 3/4 8/19, ribs 1.26 mm (M05 curves 0.67): the 0.5 deg rim-twist offset shifts every rib (ribs anchored at drawn start z0 near the rim), as in M06
- settings: inherit M05: N 22, H 3.0, arc placement 9 mm, sections knots10 (20 sections on the knots), docs/05 §5.4
- Fusion export: table-driven kernel template (curves sampled at the sections), no pure-Python copy of the integral needed

### 2026-11-23 22:43 — MODEL.md written (kernel v2)
- definition (46 params, twist derived from alpha) + hypothesis before running: cost 170-185 (between M05 163.8 and M06 194.8), front 5-7/19, 3/4 9-10/19, E4b locality 0.7-0.85, E5b 0.9+, E6 end-interval loft dev ~0.7 mm as M06

### 2026-11-23 22:45 — E0 fit (kernel v2)
- start (as built): front 0/19, 3/4 4/19, ribs 1.26 mm
- result (as built): front 5/19, 3/4 11/19, outline max 2.56, ribs 0.68 mm / 78 %, 3/4 mean 0.91
- exact curves: front 5/19, 3/4 11/19
- 46 params, 115.6 s, nfev 15, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 169.0, pool:M01_E0 175.4, pool:M05_E0 175.9, pool:M02_X1c 170.4 -> best: own start (P0)
- Fusion script: models\M10_rose_ribangle\fusion\M10\M10.py
- command: python models/M10_rose_ribangle/E0_fit/run.py

### 2026-11-23 22:46 — E1 triangle count (kernel v2)
- N=12: front 5/19, 3/4 6/19, outline max 1.99, ribs 0.68 mm (78 %), 3/4 mean 0.96; Δ outline bias mean -0.31 (range -0.70..-0.05), Δ rib mean +0.00 mm
- N=16: front 5/19, 3/4 9/19, outline max 2.22, ribs 0.68 mm (78 %), 3/4 mean 0.88; Δ outline bias mean -0.17 (range -0.34..+0.02), Δ rib mean +0.00 mm
- N=22 (own): front 5/19, 3/4 11/19, outline max 2.56, ribs 0.68 mm (78 %), 3/4 mean 0.91; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 4/19, 3/4 9/19, outline max 2.74, ribs 0.68 mm (78 %), 3/4 mean 0.92; Δ outline bias mean +0.12 (range +0.05..+0.23), Δ rib mean +0.00 mm
- N=45: front 4/19, 3/4 10/19, outline max 2.86, ribs 0.68 mm (78 %), 3/4 mean 0.95; Δ outline bias mean +0.19 (range +0.09..+0.31), Δ rib mean +0.00 mm
- command: python models/M10_rose_ribangle/E1_tri_count/run.py

### 2026-11-23 22:46 — E2 triangle width (fill) x placement (kernel v2)
- arc f=0.5: front 4/19, 3/4 8/19, outline max 2.70, ribs 0.68 mm (78 %), 3/4 mean 0.95; Δ outline bias mean +0.13 (range +0.07..+0.18), Δ rib mean +0.00 mm
- arc f=0.7: front 4/19, 3/4 9/19, outline max 2.66, ribs 0.68 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.09 (range +0.05..+0.12), Δ rib mean +0.00 mm
- arc f=0.85: front 4/19, 3/4 9/19, outline max 2.61, ribs 0.68 mm (78 %), 3/4 mean 0.93; Δ outline bias mean +0.05 (range +0.03..+0.06), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 5/19, 3/4 11/19, outline max 2.56, ribs 0.68 mm (78 %), 3/4 mean 0.91; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 4/19, 3/4 12/19, outline max 2.95, ribs 0.71 mm (77 %), 3/4 mean 0.91; Δ outline bias mean +0.15 (range -0.02..+0.39), Δ rib mean +0.03 mm
- angle_half f=0.7: front 4/19, 3/4 13/19, outline max 2.95, ribs 0.71 mm (77 %), 3/4 mean 0.91; Δ outline bias mean +0.11 (range -0.03..+0.39), Δ rib mean +0.03 mm
- angle_half f=0.85: front 4/19, 3/4 13/19, outline max 2.95, ribs 0.71 mm (77 %), 3/4 mean 0.91; Δ outline bias mean +0.07 (range -0.04..+0.39), Δ rib mean +0.03 mm
- angle_half f=1.0: front 4/19, 3/4 12/19, outline max 2.95, ribs 0.71 mm (77 %), 3/4 mean 0.90; Δ outline bias mean +0.03 (range -0.10..+0.39), Δ rib mean +0.03 mm
- command: python models/M10_rose_ribangle/E2_tri_width/run.py

### 2026-11-23 22:46 — E3 triangle height (kernel v2)
- H=1.5: front 0/19, 3/4 3/19, outline max 2.12, ribs 0.68 mm (78 %), 3/4 mean 1.43; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 4/19, outline max 1.62, ribs 0.68 mm (78 %), 3/4 mean 1.14; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 5/19, 3/4 11/19, outline max 2.56, ribs 0.68 mm (78 %), 3/4 mean 0.91; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 6/19, outline max 3.55, ribs 0.68 mm (78 %), 3/4 mean 1.46; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.55, ribs 0.68 mm (78 %), 3/4 mean 2.49; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M10_rose_ribangle/E3_tri_height/run.py

### 2026-11-23 22:46 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v2)
- twist x0.94: front 2/19, 3/4 2/19, outline max 2.61, ribs 2.17 mm (40 %), 3/4 mean 1.72; Δ outline bias mean -0.28 (range -2.27..+2.02), Δ rib mean +1.89 mm
- twist x0.97: front 3/19, 3/4 2/19, outline max 2.56, ribs 1.25 mm (53 %), 3/4 mean 1.20; Δ outline bias mean -0.13 (range -1.12..+1.02), Δ rib mean +0.73 mm
- twist x1.0: front 5/19, 3/4 11/19, outline max 2.56, ribs 0.68 mm (78 %), 3/4 mean 0.91; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 3/19, 3/4 7/19, outline max 2.56, ribs 1.15 mm (59 %), 3/4 mean 1.12; Δ outline bias mean +0.12 (range -0.96..+1.09), Δ rib mean +0.61 mm
- twist x1.06: front 2/19, 3/4 4/19, outline max 2.58, ribs 2.00 mm (45 %), 3/4 mean 1.49; Δ outline bias mean +0.24 (range -1.65..+2.15), Δ rib mean +1.65 mm
- 1-knot bumps: mean locality share 0.77 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.68 of 1 °
- command: python models/M10_rose_ribangle/E4_twist/run.py

### 2026-11-23 22:46 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v2)
- r0 -2 mm: front 0/19, 3/4 2/19, outline max 2.22, ribs 1.26 mm (57 %), 3/4 mean 1.73; Δ outline bias mean -1.89 (range -1.99..-1.64), Δ rib mean +0.74 mm
- r0 -1 mm: front 0/19, 3/4 4/19, outline max 1.57, ribs 0.89 mm (68 %), 3/4 mean 1.10; Δ outline bias mean -0.95 (range -1.00..-0.82), Δ rib mean +0.26 mm
- r0 +0 mm: front 5/19, 3/4 11/19, outline max 2.56, ribs 0.68 mm (78 %), 3/4 mean 0.91; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 6/19, outline max 3.56, ribs 0.77 mm (70 %), 3/4 mean 1.36; Δ outline bias mean +0.95 (range +0.82..+1.00), Δ rib mean +0.10 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.55, ribs 1.07 mm (63 %), 3/4 mean 2.20; Δ outline bias mean +1.89 (range +1.64..+1.99), Δ rib mean +0.46 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 mm
- command: python models/M10_rose_ribangle/E5_radius/run.py

### 2026-11-23 22:46 — E6 sections (count x placement) (kernel v2)
- uniform_z n=8: loft deviation from exact max 0.88 / mean 0.171 mm; front 5/19, 3/4 11/19
- uniform_z n=11: loft deviation from exact max 0.91 / mean 0.129 mm; front 5/19, 3/4 10/19
- uniform_z n=15: loft deviation from exact max 0.74 / mean 0.086 mm; front 6/19, 3/4 10/19
- uniform_z n=20: loft deviation from exact max 0.72 / mean 0.050 mm; front 5/19, 3/4 11/19
- uniform_z n=30: loft deviation from exact max 0.35 / mean 0.029 mm; front 5/19, 3/4 11/19
- uniform_z n=39: loft deviation from exact max 0.08 / mean 0.010 mm; front 5/19, 3/4 11/19
- adaptive n=8: loft deviation from exact max 0.91 / mean 0.170 mm; front 4/19, 3/4 13/19
- adaptive n=11: loft deviation from exact max 0.73 / mean 0.123 mm; front 6/19, 3/4 10/19
- adaptive n=15: loft deviation from exact max 0.52 / mean 0.101 mm; front 5/19, 3/4 12/19
- adaptive n=20: loft deviation from exact max 0.40 / mean 0.054 mm; front 6/19, 3/4 10/19
- adaptive n=30: loft deviation from exact max 0.14 / mean 0.015 mm; front 5/19, 3/4 11/19
- adaptive n=39: loft deviation from exact max 0.03 / mean 0.004 mm; front 5/19, 3/4 11/19
- knots10 n=20: loft deviation from exact max 0.72 / mean 0.050 mm; front 5/19, 3/4 11/19
- own sections: {'mode': 'knots10'}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M10_rose_ribangle/E6_sections/run.py

### 2026-11-23 22:47 — E0 checked + diagnostics (scratch, not official) (kernel v2)
- E0 accepted as is: constraints OK, no cap hit, overlay sane; no change to model.py after the first fit
- alpha(0) ends at the lower bound (-29.97). Diagnostic: LB alpha(0) = -70, refit from the E0 result -> cost 169.0, nfev 15, alpha(0) stays -29.97: the bound is not what holds the fit. Fitted twist: -0.74 deg at z=2.2, -1.17 at z=5, -0.57 at z=10 (M05 dip reproduced, M06 couldn't: twist(0) knot fixed)
- cost split at E0: data 166.3 + penalty 2.75 (M06: 194.8 + 0.07)
- conditioning: cond of the column-normalised residual Jacobian at E0 (diff step 1e-2): M10 35, M06 6.6, M05 1.1e3. alpha knots act cumulatively (twist above every knot), so the columns are more correlated than M06's twist knots
- multi-start spread: M10 169.0-175.9 (4 starts, nfev 15-16) vs M06 194.8-195.1 (13-15): M10 is lower but more start-dependent

### 2026-11-23 22:47 — summary written (kernel v2)
- study.write_summary -> summary.json: built front 5/19, 3/4 11/19, locality twist 0.77 / radius 0.96, smoothness r0 6 / twist 3 inflections (score 0.25), loft_dev_20 0.40 mm (adaptive 20) -> buildability gate fails (S01 0.60, S19 0.72 mm on knots10)

### 2026-11-23 22:47 — MODEL.md conclusions written (kernel v2)
- per-experiment conclusions, E4b influence-map explanation, M06/M05 comparison (cost 169.0 vs 194.8 / 163.8; cond 35 vs 6.6), limits (base waist, radius end intervals), hypothesis check

### 2026-11-23 23:06 — E0 fit (kernel v3)
- start (as built): front 0/19, 3/4 4/19, ribs 1.26 mm
- result (as built): front 5/19, 3/4 10/19, outline max 2.48, ribs 0.66 mm / 78 %, 3/4 mean 0.94
- exact curves: front 5/19, 3/4 10/19
- 47 params, 376.9 s, nfev 14, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 165.8, pool:M01_E0 159.8, pool:M05_E0 164.6, pool:M02_X1c 161.0, pool:M01_E0v2 159.9, pool:M02_E0v2 160.9, pool:M03_E0v2 162.1, pool:M04_E0v2 160.6, pool:M05_E0v2 161.8, pool:M06_E0v2 160.0, pool:M07_E0v2 162.7, pool:M08_E0v2 160.9, pool:M09_E0v2 163.8, pool:M10_E0v2 160.2 -> best: pool:M01_E0
- Fusion script: models\M10_rose_ribangle\fusion\M10\M10.py
- command: python models/M10_rose_ribangle/E0_fit/run.py

### 2026-11-23 23:06 — E1 triangle count (kernel v3)
- N=12: front 5/19, 3/4 9/19, outline max 1.93, ribs 0.66 mm (78 %), 3/4 mean 0.95; Δ outline bias mean -0.31 (range -0.70..-0.06), Δ rib mean +0.00 mm
- N=16: front 5/19, 3/4 10/19, outline max 2.16, ribs 0.66 mm (78 %), 3/4 mean 0.88; Δ outline bias mean -0.18 (range -0.34..+0.02), Δ rib mean +0.00 mm
- N=22 (own): front 5/19, 3/4 10/19, outline max 2.48, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 4/19, 3/4 9/19, outline max 2.65, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.12 (range +0.05..+0.23), Δ rib mean +0.00 mm
- N=45: front 4/19, 3/4 11/19, outline max 2.76, ribs 0.66 mm (78 %), 3/4 mean 0.96; Δ outline bias mean +0.19 (range +0.09..+0.31), Δ rib mean +0.00 mm
- command: python models/M10_rose_ribangle/E1_tri_count/run.py

### 2026-11-23 23:06 — E2 triangle width (fill) x placement (kernel v3)
- arc f=0.5: front 4/19, 3/4 10/19, outline max 2.62, ribs 0.66 mm (78 %), 3/4 mean 0.96; Δ outline bias mean +0.13 (range +0.07..+0.18), Δ rib mean +0.00 mm
- arc f=0.7: front 4/19, 3/4 11/19, outline max 2.58, ribs 0.66 mm (78 %), 3/4 mean 0.95; Δ outline bias mean +0.09 (range +0.05..+0.12), Δ rib mean +0.00 mm
- arc f=0.85: front 5/19, 3/4 11/19, outline max 2.53, ribs 0.66 mm (78 %), 3/4 mean 0.95; Δ outline bias mean +0.05 (range +0.03..+0.07), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 5/19, 3/4 10/19, outline max 2.48, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 4/19, 3/4 10/19, outline max 2.83, ribs 0.70 mm (77 %), 3/4 mean 0.93; Δ outline bias mean +0.15 (range -0.02..+0.40), Δ rib mean +0.05 mm
- angle_half f=0.7: front 4/19, 3/4 11/19, outline max 2.83, ribs 0.70 mm (77 %), 3/4 mean 0.93; Δ outline bias mean +0.11 (range -0.03..+0.40), Δ rib mean +0.05 mm
- angle_half f=0.85: front 4/19, 3/4 11/19, outline max 2.83, ribs 0.70 mm (77 %), 3/4 mean 0.92; Δ outline bias mean +0.08 (range -0.04..+0.40), Δ rib mean +0.05 mm
- angle_half f=1.0: front 4/19, 3/4 11/19, outline max 2.83, ribs 0.70 mm (77 %), 3/4 mean 0.92; Δ outline bias mean +0.04 (range -0.09..+0.40), Δ rib mean +0.05 mm
- command: python models/M10_rose_ribangle/E2_tri_width/run.py

### 2026-11-23 23:06 — E3 triangle height (kernel v3)
- H=1.5: front 0/19, 3/4 3/19, outline max 2.04, ribs 0.66 mm (78 %), 3/4 mean 1.40; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 6/19, outline max 1.54, ribs 0.66 mm (78 %), 3/4 mean 1.12; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 5/19, 3/4 10/19, outline max 2.48, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 6/19, outline max 3.48, ribs 0.66 mm (78 %), 3/4 mean 1.45; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.47, ribs 0.66 mm (78 %), 3/4 mean 2.49; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M10_rose_ribangle/E3_tri_height/run.py

### 2026-11-23 23:06 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v3)
- twist x0.94: front 2/19, 3/4 2/19, outline max 2.63, ribs 2.15 mm (40 %), 3/4 mean 1.76; Δ outline bias mean -0.28 (range -2.26..+2.00), Δ rib mean +1.90 mm
- twist x0.97: front 3/19, 3/4 2/19, outline max 2.48, ribs 1.23 mm (53 %), 3/4 mean 1.21; Δ outline bias mean -0.13 (range -1.11..+1.01), Δ rib mean +0.73 mm
- twist x1.0: front 5/19, 3/4 10/19, outline max 2.48, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 3/19, 3/4 6/19, outline max 2.48, ribs 1.12 mm (60 %), 3/4 mean 1.13; Δ outline bias mean +0.12 (range -0.97..+1.08), Δ rib mean +0.61 mm
- twist x1.06: front 2/19, 3/4 3/19, outline max 2.55, ribs 1.97 mm (46 %), 3/4 mean 1.48; Δ outline bias mean +0.23 (range -1.63..+2.13), Δ rib mean +1.64 mm
- 1-knot bumps: mean locality share 0.79 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.68 of 1 °
- command: python models/M10_rose_ribangle/E4_twist/run.py

### 2026-11-23 23:06 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v3)
- r0 -2 mm: front 0/19, 3/4 2/19, outline max 2.14, ribs 1.25 mm (57 %), 3/4 mean 1.71; Δ outline bias mean -1.89 (range -1.99..-1.65), Δ rib mean +0.74 mm
- r0 -1 mm: front 0/19, 3/4 5/19, outline max 1.49, ribs 0.86 mm (69 %), 3/4 mean 1.10; Δ outline bias mean -0.95 (range -1.00..-0.82), Δ rib mean +0.25 mm
- r0 +0 mm: front 5/19, 3/4 10/19, outline max 2.48, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 6/19, outline max 3.48, ribs 0.74 mm (70 %), 3/4 mean 1.39; Δ outline bias mean +0.95 (range +0.82..+1.00), Δ rib mean +0.10 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.48, ribs 1.04 mm (63 %), 3/4 mean 2.19; Δ outline bias mean +1.89 (range +1.65..+1.99), Δ rib mean +0.47 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 mm
- command: python models/M10_rose_ribangle/E5_radius/run.py

### 2026-11-23 23:06 — E6 sections (count x placement) (kernel v3)
- uniform_z n=8: loft deviation from exact max 0.89 / mean 0.165 mm; front 5/19, 3/4 10/19
- uniform_z n=11: loft deviation from exact max 0.95 / mean 0.130 mm; front 5/19, 3/4 9/19
- uniform_z n=15: loft deviation from exact max 0.76 / mean 0.085 mm; front 6/19, 3/4 10/19
- uniform_z n=20: loft deviation from exact max 0.72 / mean 0.051 mm; front 5/19, 3/4 10/19
- uniform_z n=30: loft deviation from exact max 0.35 / mean 0.029 mm; front 6/19, 3/4 10/19
- uniform_z n=39: loft deviation from exact max 0.08 / mean 0.010 mm; front 5/19, 3/4 10/19
- adaptive n=8: loft deviation from exact max 0.93 / mean 0.165 mm; front 5/19, 3/4 10/19
- adaptive n=11: loft deviation from exact max 0.78 / mean 0.122 mm; front 6/19, 3/4 9/19
- adaptive n=15: loft deviation from exact max 0.57 / mean 0.098 mm; front 5/19, 3/4 11/19
- adaptive n=20: loft deviation from exact max 0.44 / mean 0.053 mm; front 6/19, 3/4 9/19
- adaptive n=30: loft deviation from exact max 0.15 / mean 0.014 mm; front 6/19, 3/4 10/19
- adaptive n=39: loft deviation from exact max 0.06 / mean 0.005 mm; front 5/19, 3/4 10/19
- knots10 n=20: loft deviation from exact max 0.72 / mean 0.051 mm; front 5/19, 3/4 10/19
- own sections: {'mode': 'knots10'}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M10_rose_ribangle/E6_sections/run.py

### 2026-11-23 23:14 — final round (kernel v3) — results recorded (kernel v3)
- rank 8/10, score 0.453; front 5/19, 3/4 10/19, ribs 0.66 mm, cost 159.8 (best start pool:M01_E0)
- orientation offset -0.77°; MODEL.md: 'Final round — kernel v3' section appended; verified by judge/verify_e0.py
