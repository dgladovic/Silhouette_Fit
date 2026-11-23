# M09_rose_logistic — progress

## Status  (overwrite this block only)
- State: final (kernel v3), rank 10/10
- Best E0 (as built): front 1/19, 3/4 7/19, 19 params, score 0.353
- Next: none (study complete)

## Log  (append only, newest at the bottom)

### 2026-11-23 22:42 — model created (kernel v2)
- model.py: rose base with ONE constant lobe depth k (1) + 8-pt 2D Bezier radius (r,z), P0.z=0 and P7.z=190 fixed (14) + logistic twist curves.logistic_twist(z, total, centre, width) at z in mm (3) = 18 params
- bounds: k 0.05..0.4, total 45..135 deg, centre 20..170 mm, width 3..80 mm; Bezier points unbounded (as M05)
- penalty: 20*min(diff(z),0) on the 8 Bezier z values (as M05); constraint: Bezier z(t) monotone, k in bounds. No knot values -> no SMOOTH_W term
- start: radius points = M05 E0 (kernel v2) fitted points; k = mean of M05 fitted k nodes = 0.2012; logistic = LS fit to M05 E0 twist (z 0..190 step 1): total 88.68, centre 102.36, width 34.62; rms 0.93 deg, max |d| 2.26 deg at z=14 (M05 twist dips to -0.6 deg there)
- settings inherit M05: N 22, H 3.0, arc placement 9 mm, sections uniform_z x15 (M05 own)
- sanity at P0: r0 81.6..115.1..42.6 mm, twist 0..88.7 deg, rho max 1.0, rho(0)=1; constraints OK
- start score (P0): exact front 1/19, 3/4 7/19, ribs 1.44 mm / 45 %; built front 1/19, 3/4 7/19, ribs 1.44 mm (constant k + logistic alone cost ~0.75 mm rib mean vs M05 E0 before refit)

### 2026-11-23 22:43 — E0 fit (kernel v2)
- start (as built): front 1/19, 3/4 7/19, ribs 1.44 mm
- result (as built): front 2/19, 3/4 9/19, outline max 1.49, ribs 1.10 mm / 56 %, 3/4 mean 0.96
- exact curves: front 2/19, 3/4 10/19
- 18 params, 49.1 s, nfev 20, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 330.5, pool:M01_E0 327.0, pool:M05_E0 330.2, pool:M02_X1c 339.1 -> best: pool:M01_E0
- Fusion script: models\M09_rose_logistic\fusion\M09\M09.py
- command: python models/M09_rose_logistic/E0_fit/run.py

### 2026-11-23 22:45 — E0 checked: real minimum, not a stall; model.py unchanged (kernel v2)
- E0 cost 327.0 (M05 163.8): fit is not broken (constraints OK, r0 81.6..115.4..42.6, twist 0..88.6, k 0.195), so model.py is kept as is
- stall check (diagnostic only, scratch script, not the protocol): restart from E0 -> 327.0; starts (k, centre, width) = (0.21, 95, 30) / (0.19, 110, 40) / (0.20, 100, 25) -> 327.1 / 326.8 / 329.6, all rib 1.10 mm, front 2/19. One basin: total 88.4-88.6, centre 100.2-100.6, width 36.0-36.2
- decomposition (exact curves, front-fit camera): M05 E0 27p: rib 0.674, front 5. M05 E0 with constant k=0.201: rib 0.859, front 2 (S10-S17 +0.2..0.5 mm). M05 E0 with logistic LS twist: rib 1.58. M09 E0 with M05 twist swapped in: rib 0.866, front 3; with M05 k(z) swapped in: 1.30 (parts are co-adapted)
- => both reductions cost: constant k ~ +0.19 mm rib mean, logistic twist ~ +0.2..0.4 mm (cannot follow the near-rim twist dip of M05 (-0.6 deg at z=10) nor an asymmetric rate; M09 has +1.8 deg at z=10)
- noticed: the fitted Bezier points P3..P5 collapse to z = 104.06-104.07 (P6 at 107): monotone, legal, r0 is smooth (curve matches M05 within 0.6 mm everywhere)

### 2026-11-23 22:45 — E1 triangle count (kernel v2)
- N=12: front 1/19, 3/4 4/19, outline max 1.29, ribs 1.10 mm (56 %), 3/4 mean 1.05; Δ outline bias mean -0.31 (range -0.62..-0.04), Δ rib mean +0.00 mm
- N=16: front 1/19, 3/4 8/19, outline max 1.21, ribs 1.10 mm (56 %), 3/4 mean 0.97; Δ outline bias mean -0.17 (range -0.33..-0.01), Δ rib mean +0.00 mm
- N=22 (own): front 2/19, 3/4 9/19, outline max 1.49, ribs 1.10 mm (56 %), 3/4 mean 0.96; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 2/19, 3/4 6/19, outline max 1.66, ribs 1.10 mm (56 %), 3/4 mean 1.05; Δ outline bias mean +0.11 (range +0.04..+0.19), Δ rib mean +0.00 mm
- N=45: front 2/19, 3/4 9/19, outline max 1.76, ribs 1.10 mm (56 %), 3/4 mean 1.06; Δ outline bias mean +0.18 (range +0.09..+0.29), Δ rib mean +0.00 mm
- command: python models/M09_rose_logistic/E1_tri_count/run.py

### 2026-11-23 22:45 — E2 triangle width (fill) x placement (kernel v2)
- arc f=0.5: front 2/19, 3/4 7/19, outline max 1.62, ribs 1.10 mm (56 %), 3/4 mean 1.00; Δ outline bias mean +0.13 (range +0.07..+0.17), Δ rib mean +0.00 mm
- arc f=0.7: front 2/19, 3/4 7/19, outline max 1.58, ribs 1.10 mm (56 %), 3/4 mean 1.00; Δ outline bias mean +0.09 (range +0.05..+0.11), Δ rib mean +0.00 mm
- arc f=0.85: front 2/19, 3/4 8/19, outline max 1.54, ribs 1.10 mm (56 %), 3/4 mean 0.98; Δ outline bias mean +0.05 (range +0.03..+0.06), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 2/19, 3/4 9/19, outline max 1.49, ribs 1.10 mm (56 %), 3/4 mean 0.96; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 2/19, 3/4 10/19, outline max 1.85, ribs 1.10 mm (56 %), 3/4 mean 1.01; Δ outline bias mean +0.13 (range -0.01..+0.33), Δ rib mean +0.00 mm
- angle_half f=0.7: front 2/19, 3/4 10/19, outline max 1.85, ribs 1.10 mm (56 %), 3/4 mean 1.00; Δ outline bias mean +0.09 (range -0.04..+0.33), Δ rib mean +0.00 mm
- angle_half f=0.85: front 2/19, 3/4 10/19, outline max 1.85, ribs 1.10 mm (56 %), 3/4 mean 1.00; Δ outline bias mean +0.05 (range -0.08..+0.33), Δ rib mean +0.00 mm
- angle_half f=1.0: front 2/19, 3/4 7/19, outline max 1.85, ribs 1.10 mm (56 %), 3/4 mean 0.99; Δ outline bias mean +0.01 (range -0.14..+0.33), Δ rib mean +0.00 mm
- command: python models/M09_rose_logistic/E2_tri_width/run.py

### 2026-11-23 22:45 — E3 triangle height (kernel v2)
- H=1.5: front 0/19, 3/4 3/19, outline max 2.59, ribs 1.10 mm (56 %), 3/4 mean 1.45; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 1/19, 3/4 4/19, outline max 2.09, ribs 1.10 mm (56 %), 3/4 mean 1.14; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 2/19, 3/4 9/19, outline max 1.49, ribs 1.10 mm (56 %), 3/4 mean 0.96; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 7/19, outline max 2.48, ribs 1.10 mm (56 %), 3/4 mean 1.43; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 3.48, ribs 1.10 mm (56 %), 3/4 mean 2.39; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M09_rose_logistic/E3_tri_height/run.py

### 2026-11-23 22:45 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v2)
- twist x0.94: front 2/19, 3/4 1/19, outline max 2.32, ribs 2.40 mm (34 %), 3/4 mean 1.56; Δ outline bias mean -0.29 (range -2.43..+2.09), Δ rib mean +1.71 mm
- twist x0.97: front 1/19, 3/4 2/19, outline max 1.49, ribs 1.54 mm (45 %), 3/4 mean 1.16; Δ outline bias mean -0.14 (range -1.20..+1.06), Δ rib mean +0.59 mm
- twist x1.0: front 2/19, 3/4 9/19, outline max 1.49, ribs 1.10 mm (56 %), 3/4 mean 0.96; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 1/19, 3/4 5/19, outline max 2.01, ribs 1.40 mm (44 %), 3/4 mean 1.30; Δ outline bias mean +0.14 (range -0.83..+1.17), Δ rib mean +0.40 mm
- twist x1.06: front 0/19, 3/4 4/19, outline max 3.18, ribs 2.12 mm (30 %), 3/4 mean 1.75; Δ outline bias mean +0.26 (range -1.67..+2.33), Δ rib mean +1.27 mm
- 1-knot bumps: mean locality share 0.21 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.15 of 1 °
- command: python models/M09_rose_logistic/E4_twist/run.py

### 2026-11-23 22:45 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v2)
- r0 -2 mm: front 0/19, 3/4 4/19, outline max 2.68, ribs 1.59 mm (47 %), 3/4 mean 1.74; Δ outline bias mean -1.89 (range -1.99..-1.64), Δ rib mean +0.66 mm
- r0 -1 mm: front 1/19, 3/4 5/19, outline max 1.88, ribs 1.30 mm (49 %), 3/4 mean 1.11; Δ outline bias mean -0.95 (range -1.00..-0.82), Δ rib mean +0.28 mm
- r0 +0 mm: front 2/19, 3/4 9/19, outline max 1.49, ribs 1.10 mm (56 %), 3/4 mean 0.96; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 6/19, outline max 2.49, ribs 1.10 mm (52 %), 3/4 mean 1.39; Δ outline bias mean +0.95 (range +0.82..+1.00), Δ rib mean -0.01 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 3.48, ribs 1.29 mm (43 %), 3/4 mean 2.20; Δ outline bias mean +1.89 (range +1.64..+1.99), Δ rib mean +0.21 mm
- 1-knot bumps: mean locality share 0.57 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.52 of 1 mm
- command: python models/M09_rose_logistic/E5_radius/run.py

### 2026-11-23 22:45 — E6 sections (count x placement) (kernel v2)
- uniform_z n=8: loft deviation from exact max 0.55 / mean 0.113 mm; front 2/19, 3/4 9/19
- uniform_z n=11: loft deviation from exact max 0.61 / mean 0.041 mm; front 2/19, 3/4 9/19
- uniform_z n=15: loft deviation from exact max 0.49 / mean 0.031 mm; front 2/19, 3/4 9/19
- uniform_z n=20: loft deviation from exact max 0.32 / mean 0.014 mm; front 2/19, 3/4 8/19
- uniform_z n=30: loft deviation from exact max 0.12 / mean 0.004 mm; front 2/19, 3/4 7/19
- uniform_z n=39: loft deviation from exact max 0.05 / mean 0.001 mm; front 2/19, 3/4 7/19
- adaptive n=8: loft deviation from exact max 0.58 / mean 0.091 mm; front 2/19, 3/4 9/19
- adaptive n=11: loft deviation from exact max 0.56 / mean 0.068 mm; front 2/19, 3/4 9/19
- adaptive n=15: loft deviation from exact max 0.37 / mean 0.024 mm; front 2/19, 3/4 8/19
- adaptive n=20: loft deviation from exact max 0.18 / mean 0.009 mm; front 2/19, 3/4 8/19
- adaptive n=30: loft deviation from exact max 0.05 / mean 0.002 mm; front 2/19, 3/4 7/19
- adaptive n=39: loft deviation from exact max 0.01 / mean 0.000 mm; front 2/19, 3/4 7/19
- bezier_t n=8: loft deviation from exact max 0.81 / mean 0.179 mm; front 2/19, 3/4 10/19
- bezier_t n=11: loft deviation from exact max 0.45 / mean 0.054 mm; front 2/19, 3/4 9/19
- bezier_t n=15: loft deviation from exact max 0.22 / mean 0.031 mm; front 2/19, 3/4 9/19
- bezier_t n=20: loft deviation from exact max 0.09 / mean 0.012 mm; front 2/19, 3/4 9/19
- bezier_t n=30: loft deviation from exact max 0.02 / mean 0.002 mm; front 2/19, 3/4 8/19
- bezier_t n=39: loft deviation from exact max 0.01 / mean 0.001 mm; front 2/19, 3/4 7/19
- knots10 n=20: loft deviation from exact max 0.32 / mean 0.014 mm; front 2/19, 3/4 8/19
- own sections: {'mode': 'uniform_z', 'count': 15}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M09_rose_logistic/E6_sections/run.py

### 2026-11-23 22:46 — summary + conclusions (kernel v2)
- summary.json written: front 2/19, 3/4 9/19, rib 1.10 mm, locality twist 0.21 / radius 0.57 (mean 0.39), loft_dev_20 0.09 mm (bezier_t 20), buildable, smoothness score 1.0
- E6 note: loft deviation 0.49 mm at 15 uniform sections is all in S01 (fitted P1/P2 at z 15/25 make a sharp rim flare); passes unaffected
- MODEL.md conclusions: constant k costs ~0.19 mm rib mean (S10-S17), logistic twist ~0.2-0.4 mm (near-rim dip, symmetric rate); hypothesis (close to M05) did not hold

### 2026-11-23 23:03 — E0 fit (kernel v3)
- start (as built): front 1/19, 3/4 7/19, ribs 1.44 mm
- result (as built): front 1/19, 3/4 7/19, outline max 0.99, ribs 0.97 mm / 62 %, 3/4 mean 0.85
- exact curves: front 1/19, 3/4 7/19
- 19 params, 196.1 s, nfev 19, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 263.9, pool:M01_E0 262.8, pool:M05_E0 265.4, pool:M02_X1c 279.0, pool:M01_E0v2 262.1, pool:M02_E0v2 278.4, pool:M03_E0v2 271.8, pool:M04_E0v2 269.6, pool:M05_E0v2 264.5, pool:M06_E0v2 264.2, pool:M07_E0v2 264.0, pool:M08_E0v2 262.5, pool:M09_E0v2 265.3, pool:M10_E0v2 263.0 -> best: pool:M01_E0v2
- Fusion script: models\M09_rose_logistic\fusion\M09\M09.py
- command: python models/M09_rose_logistic/E0_fit/run.py

### 2026-11-23 23:03 — E1 triangle count (kernel v3)
- N=12: front 2/19, 3/4 4/19, outline max 1.38, ribs 0.97 mm (62 %), 3/4 mean 0.98; Δ outline bias mean -0.32 (range -0.72..-0.06), Δ rib mean +0.00 mm
- N=16: front 2/19, 3/4 6/19, outline max 1.09, ribs 0.97 mm (62 %), 3/4 mean 0.91; Δ outline bias mean -0.18 (range -0.36..+0.03), Δ rib mean +0.00 mm
- N=22 (own): front 1/19, 3/4 7/19, outline max 0.99, ribs 0.97 mm (62 %), 3/4 mean 0.85; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 1/19, 3/4 10/19, outline max 1.14, ribs 0.97 mm (62 %), 3/4 mean 0.87; Δ outline bias mean +0.12 (range +0.04..+0.25), Δ rib mean +0.00 mm
- N=45: front 1/19, 3/4 11/19, outline max 1.24, ribs 0.97 mm (62 %), 3/4 mean 0.86; Δ outline bias mean +0.19 (range +0.10..+0.31), Δ rib mean +0.00 mm
- command: python models/M09_rose_logistic/E1_tri_count/run.py

### 2026-11-23 23:03 — E2 triangle width (fill) x placement (kernel v3)
- arc f=0.5: front 1/19, 3/4 10/19, outline max 1.12, ribs 0.97 mm (62 %), 3/4 mean 0.87; Δ outline bias mean +0.14 (range +0.08..+0.18), Δ rib mean +0.00 mm
- arc f=0.7: front 1/19, 3/4 8/19, outline max 1.08, ribs 0.97 mm (62 %), 3/4 mean 0.87; Δ outline bias mean +0.09 (range +0.05..+0.12), Δ rib mean +0.00 mm
- arc f=0.85: front 1/19, 3/4 8/19, outline max 1.03, ribs 0.97 mm (62 %), 3/4 mean 0.85; Δ outline bias mean +0.05 (range +0.03..+0.07), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 1/19, 3/4 7/19, outline max 0.99, ribs 0.97 mm (62 %), 3/4 mean 0.85; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 1/19, 3/4 11/19, outline max 1.30, ribs 0.97 mm (62 %), 3/4 mean 0.84; Δ outline bias mean +0.14 (range -0.02..+0.37), Δ rib mean -0.00 mm
- angle_half f=0.7: front 1/19, 3/4 11/19, outline max 1.30, ribs 0.97 mm (62 %), 3/4 mean 0.85; Δ outline bias mean +0.10 (range -0.05..+0.37), Δ rib mean -0.00 mm
- angle_half f=0.85: front 1/19, 3/4 10/19, outline max 1.30, ribs 0.97 mm (62 %), 3/4 mean 0.85; Δ outline bias mean +0.07 (range -0.10..+0.37), Δ rib mean -0.00 mm
- angle_half f=1.0: front 1/19, 3/4 10/19, outline max 1.30, ribs 0.97 mm (62 %), 3/4 mean 0.86; Δ outline bias mean +0.02 (range -0.16..+0.37), Δ rib mean -0.00 mm
- command: python models/M09_rose_logistic/E2_tri_width/run.py

### 2026-11-23 23:03 — E3 triangle height (kernel v3)
- H=1.5: front 0/19, 3/4 5/19, outline max 2.49, ribs 0.97 mm (62 %), 3/4 mean 1.63; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 4/19, outline max 1.99, ribs 0.97 mm (62 %), 3/4 mean 1.28; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 1/19, 3/4 7/19, outline max 0.99, ribs 0.97 mm (62 %), 3/4 mean 0.85; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 9/19, outline max 1.98, ribs 0.97 mm (62 %), 3/4 mean 1.18; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 2.97, ribs 0.97 mm (62 %), 3/4 mean 2.12; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M09_rose_logistic/E3_tri_height/run.py

### 2026-11-23 23:03 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v3)
- twist x0.94: front 2/19, 3/4 2/19, outline max 2.77, ribs 2.31 mm (36 %), 3/4 mean 1.44; Δ outline bias mean -0.30 (range -2.49..+2.09), Δ rib mean +1.76 mm
- twist x0.97: front 1/19, 3/4 6/19, outline max 1.52, ribs 1.47 mm (41 %), 3/4 mean 0.99; Δ outline bias mean -0.14 (range -1.23..+1.05), Δ rib mean +0.67 mm
- twist x1.0: front 1/19, 3/4 7/19, outline max 0.99, ribs 0.97 mm (62 %), 3/4 mean 0.85; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 2/19, 3/4 4/19, outline max 1.88, ribs 1.37 mm (46 %), 3/4 mean 1.20; Δ outline bias mean +0.13 (range -0.98..+1.18), Δ rib mean +0.53 mm
- twist x1.06: front 0/19, 3/4 5/19, outline max 2.77, ribs 2.15 mm (35 %), 3/4 mean 1.67; Δ outline bias mean +0.26 (range -1.64..+2.29), Δ rib mean +1.50 mm
- 1-knot bumps: mean locality share 0.27 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.18 of 1 °
- command: python models/M09_rose_logistic/E4_twist/run.py

### 2026-11-23 23:03 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v3)
- r0 -2 mm: front 0/19, 3/4 2/19, outline max 2.58, ribs 1.48 mm (45 %), 3/4 mean 1.91; Δ outline bias mean -1.89 (range -1.99..-1.63), Δ rib mean +0.69 mm
- r0 -1 mm: front 0/19, 3/4 4/19, outline max 1.78, ribs 1.15 mm (55 %), 3/4 mean 1.22; Δ outline bias mean -0.95 (range -1.00..-0.81), Δ rib mean +0.25 mm
- r0 +0 mm: front 1/19, 3/4 7/19, outline max 0.99, ribs 0.97 mm (62 %), 3/4 mean 0.85; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 10/19, outline max 1.98, ribs 1.03 mm (56 %), 3/4 mean 1.10; Δ outline bias mean +0.95 (range +0.81..+1.00), Δ rib mean +0.06 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 2.98, ribs 1.28 mm (47 %), 3/4 mean 1.88; Δ outline bias mean +1.89 (range +1.63..+1.99), Δ rib mean +0.38 mm
- 1-knot bumps: mean locality share 0.57 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.51 of 1 mm
- command: python models/M09_rose_logistic/E5_radius/run.py

### 2026-11-23 23:03 — E6 sections (count x placement) (kernel v3)
- uniform_z n=8: loft deviation from exact max 0.55 / mean 0.111 mm; front 1/19, 3/4 9/19
- uniform_z n=11: loft deviation from exact max 0.14 / mean 0.020 mm; front 1/19, 3/4 7/19
- uniform_z n=15: loft deviation from exact max 0.09 / mean 0.010 mm; front 1/19, 3/4 7/19
- uniform_z n=20: loft deviation from exact max 0.01 / mean 0.001 mm; front 1/19, 3/4 7/19
- uniform_z n=30: loft deviation from exact max 0.01 / mean 0.001 mm; front 1/19, 3/4 7/19
- uniform_z n=39: loft deviation from exact max 0.01 / mean 0.000 mm; front 1/19, 3/4 7/19
- adaptive n=8: loft deviation from exact max 0.20 / mean 0.060 mm; front 1/19, 3/4 8/19
- adaptive n=11: loft deviation from exact max 0.15 / mean 0.039 mm; front 1/19, 3/4 8/19
- adaptive n=15: loft deviation from exact max 0.03 / mean 0.006 mm; front 1/19, 3/4 7/19
- adaptive n=20: loft deviation from exact max 0.02 / mean 0.002 mm; front 1/19, 3/4 7/19
- adaptive n=30: loft deviation from exact max 0.01 / mean 0.000 mm; front 1/19, 3/4 7/19
- adaptive n=39: loft deviation from exact max 0.00 / mean 0.000 mm; front 1/19, 3/4 7/19
- bezier_t n=8: loft deviation from exact max 0.78 / mean 0.191 mm; front 1/19, 3/4 9/19
- bezier_t n=11: loft deviation from exact max 0.07 / mean 0.018 mm; front 1/19, 3/4 8/19
- bezier_t n=15: loft deviation from exact max 0.19 / mean 0.023 mm; front 1/19, 3/4 7/19
- bezier_t n=20: loft deviation from exact max 0.10 / mean 0.010 mm; front 1/19, 3/4 8/19
- bezier_t n=30: loft deviation from exact max 0.03 / mean 0.002 mm; front 1/19, 3/4 7/19
- bezier_t n=39: loft deviation from exact max 0.01 / mean 0.001 mm; front 1/19, 3/4 7/19
- knots10 n=20: loft deviation from exact max 0.01 / mean 0.001 mm; front 1/19, 3/4 7/19
- own sections: {'mode': 'uniform_z', 'count': 15}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M09_rose_logistic/E6_sections/run.py

### 2026-11-23 23:14 — final round (kernel v3) — results recorded (kernel v3)
- rank 10/10, score 0.353; front 1/19, 3/4 7/19, ribs 0.97 mm, cost 262.1 (best start pool:M01_E0v2)
- orientation offset -1.28°; MODEL.md: 'Final round — kernel v3' section appended; verified by judge/verify_e0.py
