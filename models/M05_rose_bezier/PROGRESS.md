# M05_rose_bezier — progress

## Status  (overwrite this block only)
- State: final (kernel v3), rank 6/10
- Best E0 (as built): front 6/19, 3/4 10/19, 28 params, score 0.492
- Next: none (study complete)

## Log  (append only, newest at the bottom)

### 2026-11-23 22:21 — model created (kernel v1)
- model.py: rose k(z) (6 nodes) + 8-pt 2D Bezier radius + 5-pt Bezier twist, 27 params
- start values = joint two-view fit (commit 1e8223d)
- settings: N 22, H 3.0, arc placement 9 mm, 15 uniform sections (Grasshoper_full/)
- Gate A: kernel reproduces docs/03 §3.4 within 0.01 mm (exact, no rib exclusion); 3/4 residual = views/fit_joint.py (0.697 vs 0.696 mm)
- Gate B: loft simulator vs Fusion F1-1/2/3 outline (maxY) mean 0.12 / 0.017 / 0.003 mm at 8 / 15 / 30 sections

### 2026-11-23 22:21 — E0 fit (kernel v1)
- start (as built): front 5/19, 3/4 12/19, ribs 0.76 mm
- result (as built): front 8/19, 3/4 7/19, outline max 2.03, ribs 0.71 mm / 79 %, 3/4 mean 0.99
- exact curves: front 7/19, 3/4 7/19
- 27 params, 25.1 s, nfev 18, cap hit [False, False], constraints OK
- command: python models/M05_rose_bezier/E0_fit/run.py

### 2026-11-23 22:22 — E1 triangle count (kernel v1)
- N=12: front 5/19, 3/4 4/19, outline max 1.44, ribs 0.71 mm (79 %), 3/4 mean 1.11; Δ outline bias mean -0.32 (range -0.72..-0.06), Δ rib mean +0.00 mm
- N=16: front 7/19, 3/4 6/19, outline max 1.69, ribs 0.71 mm (79 %), 3/4 mean 0.99; Δ outline bias mean -0.18 (range -0.37..+0.03), Δ rib mean +0.00 mm
- N=22 (own): front 8/19, 3/4 7/19, outline max 2.03, ribs 0.71 mm (79 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 6/19, 3/4 10/19, outline max 2.22, ribs 0.71 mm (79 %), 3/4 mean 0.97; Δ outline bias mean +0.12 (range +0.05..+0.25), Δ rib mean +0.00 mm
- N=45: front 5/19, 3/4 8/19, outline max 2.34, ribs 0.71 mm (79 %), 3/4 mean 0.99; Δ outline bias mean +0.20 (range +0.09..+0.33), Δ rib mean +0.00 mm
- command: python models/M05_rose_bezier/E1_tri_count/run.py

### 2026-11-23 22:22 — E2 triangle width (fill) x placement (kernel v1)
- arc f=0.5: front 5/19, 3/4 7/19, outline max 2.17, ribs 0.71 mm (79 %), 3/4 mean 1.02; Δ outline bias mean +0.14 (range +0.07..+0.18), Δ rib mean +0.00 mm
- arc f=0.7: front 6/19, 3/4 7/19, outline max 2.13, ribs 0.71 mm (79 %), 3/4 mean 1.02; Δ outline bias mean +0.09 (range +0.05..+0.12), Δ rib mean +0.00 mm
- arc f=0.85: front 7/19, 3/4 7/19, outline max 2.09, ribs 0.71 mm (79 %), 3/4 mean 1.02; Δ outline bias mean +0.05 (range +0.03..+0.07), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 8/19, 3/4 7/19, outline max 2.03, ribs 0.71 mm (79 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 4/19, 3/4 9/19, outline max 2.44, ribs 0.76 mm (74 %), 3/4 mean 0.97; Δ outline bias mean +0.15 (range -0.02..+0.42), Δ rib mean +0.05 mm
- angle_half f=0.7: front 5/19, 3/4 10/19, outline max 2.44, ribs 0.76 mm (74 %), 3/4 mean 0.97; Δ outline bias mean +0.12 (range -0.03..+0.42), Δ rib mean +0.05 mm
- angle_half f=0.85: front 5/19, 3/4 9/19, outline max 2.44, ribs 0.76 mm (74 %), 3/4 mean 0.97; Δ outline bias mean +0.08 (range -0.05..+0.42), Δ rib mean +0.05 mm
- angle_half f=1.0: front 5/19, 3/4 8/19, outline max 2.44, ribs 0.76 mm (74 %), 3/4 mean 0.97; Δ outline bias mean +0.04 (range -0.11..+0.42), Δ rib mean +0.05 mm
- command: python models/M05_rose_bezier/E2_tri_width/run.py

### 2026-11-23 22:22 — E3 triangle height (kernel v1)
- H=1.5: front 0/19, 3/4 4/19, outline max 2.05, ribs 0.71 mm (79 %), 3/4 mean 1.61; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 5/19, outline max 1.55, ribs 0.71 mm (79 %), 3/4 mean 1.28; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 8/19, 3/4 7/19, outline max 2.03, ribs 0.71 mm (79 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 8/19, outline max 3.03, ribs 0.71 mm (79 %), 3/4 mean 1.30; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 1/19, outline max 4.02, ribs 0.71 mm (79 %), 3/4 mean 2.16; Δ outline bias mean +1.99 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M05_rose_bezier/E3_tri_height/run.py

### 2026-11-23 22:22 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v1)
- twist x0.94: front 3/19, 3/4 1/19, outline max 2.77, ribs 2.18 mm (41 %), 3/4 mean 1.69; Δ outline bias mean -0.28 (range -2.33..+2.00), Δ rib mean +1.89 mm
- twist x0.97: front 5/19, 3/4 2/19, outline max 2.03, ribs 1.28 mm (53 %), 3/4 mean 1.26; Δ outline bias mean -0.13 (range -1.15..+1.01), Δ rib mean +0.74 mm
- twist x1.0: front 8/19, 3/4 7/19, outline max 2.03, ribs 0.71 mm (79 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 3/19, 3/4 3/19, outline max 2.03, ribs 1.20 mm (54 %), 3/4 mean 1.20; Δ outline bias mean +0.12 (range -1.02..+1.12), Δ rib mean +0.66 mm
- twist x1.06: front 2/19, 3/4 1/19, outline max 2.54, ribs 2.03 mm (43 %), 3/4 mean 1.56; Δ outline bias mean +0.23 (range -1.75..+2.21), Δ rib mean +1.68 mm
- 1-knot bumps: mean locality share 0.26 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.22 of 1 °
- command: python models/M05_rose_bezier/E4_twist/run.py

### 2026-11-23 22:22 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v1)
- r0 -2 mm: front 0/19, 3/4 1/19, outline max 2.26, ribs 1.30 mm (54 %), 3/4 mean 1.93; Δ outline bias mean -1.89 (range -1.99..-1.64), Δ rib mean +0.77 mm
- r0 -1 mm: front 0/19, 3/4 3/19, outline max 1.41, ribs 0.91 mm (65 %), 3/4 mean 1.28; Δ outline bias mean -0.95 (range -1.00..-0.82), Δ rib mean +0.26 mm
- r0 +0 mm: front 8/19, 3/4 7/19, outline max 2.03, ribs 0.71 mm (79 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 7/19, outline max 3.03, ribs 0.83 mm (67 %), 3/4 mean 1.24; Δ outline bias mean +0.95 (range +0.82..+1.00), Δ rib mean +0.16 mm
- r0 +2 mm: front 0/19, 3/4 1/19, outline max 4.02, ribs 1.13 mm (57 %), 3/4 mean 1.98; Δ outline bias mean +1.89 (range +1.64..+1.99), Δ rib mean +0.53 mm
- 1-knot bumps: mean locality share 0.09 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 5.92 of 1 mm
- command: python models/M05_rose_bezier/E5_radius/run.py

### 2026-11-23 22:22 — E6 sections (count x placement) (kernel v1)
- uniform_z n=8: loft deviation from exact max 0.15 / mean 0.046 mm; front 7/19, 3/4 7/19
- uniform_z n=11: loft deviation from exact max 0.18 / mean 0.024 mm; front 7/19, 3/4 7/19
- uniform_z n=15: loft deviation from exact max 0.05 / mean 0.006 mm; front 8/19, 3/4 7/19
- uniform_z n=20: loft deviation from exact max 0.03 / mean 0.001 mm; front 8/19, 3/4 7/19
- uniform_z n=30: loft deviation from exact max 0.03 / mean 0.001 mm; front 7/19, 3/4 7/19
- uniform_z n=39: loft deviation from exact max 0.02 / mean 0.000 mm; front 7/19, 3/4 7/19
- adaptive n=8: loft deviation from exact max 0.17 / mean 0.038 mm; front 6/19, 3/4 7/19
- adaptive n=11: loft deviation from exact max 0.19 / mean 0.030 mm; front 7/19, 3/4 7/19
- adaptive n=15: loft deviation from exact max 0.06 / mean 0.009 mm; front 7/19, 3/4 7/19
- adaptive n=20: loft deviation from exact max 0.02 / mean 0.002 mm; front 8/19, 3/4 7/19
- adaptive n=30: loft deviation from exact max 0.03 / mean 0.001 mm; front 7/19, 3/4 7/19
- adaptive n=39: loft deviation from exact max 0.03 / mean 0.001 mm; front 7/19, 3/4 7/19
- bezier_t n=8: loft deviation from exact max 0.82 / mean 0.168 mm; front 6/19, 3/4 3/19
- bezier_t n=11: loft deviation from exact max 0.14 / mean 0.024 mm; front 6/19, 3/4 3/19
- bezier_t n=15: loft deviation from exact max 0.10 / mean 0.014 mm; front 8/19, 3/4 6/19
- bezier_t n=20: loft deviation from exact max 0.07 / mean 0.007 mm; front 7/19, 3/4 7/19
- bezier_t n=30: loft deviation from exact max 0.03 / mean 0.002 mm; front 7/19, 3/4 7/19
- bezier_t n=39: loft deviation from exact max 0.02 / mean 0.001 mm; front 7/19, 3/4 7/19
- knots10 n=20: loft deviation from exact max 0.03 / mean 0.001 mm; front 8/19, 3/4 7/19
- own sections: {'mode': 'uniform_z', 'count': 15}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M05_rose_bezier/E6_sections/run.py

### 2026-11-23 22:22 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v1)
- twist x0.94: front 3/19, 3/4 1/19, outline max 2.77, ribs 2.18 mm (41 %), 3/4 mean 1.69; Δ outline bias mean -0.28 (range -2.33..+2.00), Δ rib mean +1.89 mm
- twist x0.97: front 5/19, 3/4 2/19, outline max 2.03, ribs 1.28 mm (53 %), 3/4 mean 1.26; Δ outline bias mean -0.13 (range -1.15..+1.01), Δ rib mean +0.74 mm
- twist x1.0: front 8/19, 3/4 7/19, outline max 2.03, ribs 0.71 mm (79 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 3/19, 3/4 3/19, outline max 2.03, ribs 1.20 mm (54 %), 3/4 mean 1.20; Δ outline bias mean +0.12 (range -1.02..+1.12), Δ rib mean +0.66 mm
- twist x1.06: front 2/19, 3/4 1/19, outline max 2.54, ribs 2.03 mm (43 %), 3/4 mean 1.56; Δ outline bias mean +0.23 (range -1.75..+2.21), Δ rib mean +1.68 mm
- 1-knot bumps: mean locality share 0.36 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.26 of 1 °
- command: python models/M05_rose_bezier/E4_twist/run.py

### 2026-11-23 22:22 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v1)
- r0 -2 mm: front 0/19, 3/4 1/19, outline max 2.26, ribs 1.30 mm (54 %), 3/4 mean 1.93; Δ outline bias mean -1.89 (range -1.99..-1.64), Δ rib mean +0.77 mm
- r0 -1 mm: front 0/19, 3/4 3/19, outline max 1.41, ribs 0.91 mm (65 %), 3/4 mean 1.28; Δ outline bias mean -0.95 (range -1.00..-0.82), Δ rib mean +0.26 mm
- r0 +0 mm: front 8/19, 3/4 7/19, outline max 2.03, ribs 0.71 mm (79 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 7/19, outline max 3.03, ribs 0.83 mm (67 %), 3/4 mean 1.24; Δ outline bias mean +0.95 (range +0.82..+1.00), Δ rib mean +0.16 mm
- r0 +2 mm: front 0/19, 3/4 1/19, outline max 4.02, ribs 1.13 mm (57 %), 3/4 mean 1.98; Δ outline bias mean +1.89 (range +1.64..+1.99), Δ rib mean +0.53 mm
- 1-knot bumps: mean locality share 0.18 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 2.23 of 1 mm
- command: python models/M05_rose_bezier/E5_radius/run.py

### 2026-11-23 22:23 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v1)
- twist x0.94: front 3/19, 3/4 1/19, outline max 2.77, ribs 2.18 mm (41 %), 3/4 mean 1.69; Δ outline bias mean -0.28 (range -2.33..+2.00), Δ rib mean +1.89 mm
- twist x0.97: front 5/19, 3/4 2/19, outline max 2.03, ribs 1.28 mm (53 %), 3/4 mean 1.26; Δ outline bias mean -0.13 (range -1.15..+1.01), Δ rib mean +0.74 mm
- twist x1.0: front 8/19, 3/4 7/19, outline max 2.03, ribs 0.71 mm (79 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 3/19, 3/4 3/19, outline max 2.03, ribs 1.20 mm (54 %), 3/4 mean 1.20; Δ outline bias mean +0.12 (range -1.02..+1.12), Δ rib mean +0.66 mm
- twist x1.06: front 2/19, 3/4 1/19, outline max 2.54, ribs 2.03 mm (43 %), 3/4 mean 1.56; Δ outline bias mean +0.23 (range -1.75..+2.21), Δ rib mean +1.68 mm
- 1-knot bumps: mean locality share 0.37 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.25 of 1 °
- command: python models/M05_rose_bezier/E4_twist/run.py

### 2026-11-23 22:23 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v1)
- r0 -2 mm: front 0/19, 3/4 1/19, outline max 2.26, ribs 1.30 mm (54 %), 3/4 mean 1.93; Δ outline bias mean -1.89 (range -1.99..-1.64), Δ rib mean +0.77 mm
- r0 -1 mm: front 0/19, 3/4 3/19, outline max 1.41, ribs 0.91 mm (65 %), 3/4 mean 1.28; Δ outline bias mean -0.95 (range -1.00..-0.82), Δ rib mean +0.26 mm
- r0 +0 mm: front 8/19, 3/4 7/19, outline max 2.03, ribs 0.71 mm (79 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 7/19, outline max 3.03, ribs 0.83 mm (67 %), 3/4 mean 1.24; Δ outline bias mean +0.95 (range +0.82..+1.00), Δ rib mean +0.16 mm
- r0 +2 mm: front 0/19, 3/4 1/19, outline max 4.02, ribs 1.13 mm (57 %), 3/4 mean 1.98; Δ outline bias mean +1.89 (range +1.64..+1.99), Δ rib mean +0.53 mm
- 1-knot bumps: mean locality share 0.58 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.58 of 1 mm
- command: python models/M05_rose_bezier/E5_radius/run.py

### 2026-11-23 22:28 — conclusions written (kernel v1)
- MODEL.md conclusions: main limitation = global 5-point twist; waist S08-S12 fails on ribs; 3/4 worse when held out (12 -> 7/19)

### 2026-11-23 22:36 — E0 fit (kernel v2)
- start (as built): front 5/19, 3/4 12/19, ribs 0.76 mm
- result (as built): front 5/19, 3/4 9/19, outline max 1.52, ribs 0.68 mm / 81 %, 3/4 mean 0.93
- exact curves: front 5/19, 3/4 8/19
- 27 params, 107.1 s, nfev 19, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 163.8, pool:M01_E0 175.6, pool:M05_E0 163.8, pool:M02_X1c 178.4 -> best: own start (P0)
- Fusion script: models\M05_rose_bezier\fusion\M05\M05.py
- command: python models/M05_rose_bezier/E0_fit/run.py

### 2026-11-23 22:39 — E1 triangle count (kernel v2)
- N=12: front 4/19, 3/4 5/19, outline max 0.94, ribs 0.68 mm (81 %), 3/4 mean 1.00; Δ outline bias mean -0.32 (range -0.71..-0.06), Δ rib mean +0.00 mm
- N=16: front 5/19, 3/4 7/19, outline max 1.17, ribs 0.68 mm (81 %), 3/4 mean 0.93; Δ outline bias mean -0.18 (range -0.36..+0.03), Δ rib mean +0.00 mm
- N=22 (own): front 5/19, 3/4 9/19, outline max 1.52, ribs 0.68 mm (81 %), 3/4 mean 0.93; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 4/19, 3/4 9/19, outline max 1.69, ribs 0.68 mm (81 %), 3/4 mean 0.94; Δ outline bias mean +0.12 (range +0.05..+0.23), Δ rib mean +0.00 mm
- N=45: front 4/19, 3/4 11/19, outline max 1.81, ribs 0.68 mm (81 %), 3/4 mean 0.96; Δ outline bias mean +0.19 (range +0.09..+0.32), Δ rib mean +0.00 mm
- command: python models/M05_rose_bezier/E1_tri_count/run.py

### 2026-11-23 22:39 — E2 triangle width (fill) x placement (kernel v2)
- arc f=0.5: front 3/19, 3/4 9/19, outline max 1.65, ribs 0.68 mm (81 %), 3/4 mean 0.94; Δ outline bias mean +0.13 (range +0.07..+0.18), Δ rib mean +0.00 mm
- arc f=0.7: front 4/19, 3/4 7/19, outline max 1.61, ribs 0.68 mm (81 %), 3/4 mean 0.95; Δ outline bias mean +0.09 (range +0.05..+0.12), Δ rib mean +0.00 mm
- arc f=0.85: front 4/19, 3/4 8/19, outline max 1.57, ribs 0.68 mm (81 %), 3/4 mean 0.93; Δ outline bias mean +0.05 (range +0.03..+0.07), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 5/19, 3/4 9/19, outline max 1.52, ribs 0.68 mm (81 %), 3/4 mean 0.93; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 3/19, 3/4 11/19, outline max 1.90, ribs 0.71 mm (79 %), 3/4 mean 0.94; Δ outline bias mean +0.15 (range -0.02..+0.41), Δ rib mean +0.03 mm
- angle_half f=0.7: front 4/19, 3/4 11/19, outline max 1.90, ribs 0.71 mm (79 %), 3/4 mean 0.94; Δ outline bias mean +0.11 (range -0.03..+0.41), Δ rib mean +0.03 mm
- angle_half f=0.85: front 4/19, 3/4 10/19, outline max 1.90, ribs 0.71 mm (79 %), 3/4 mean 0.94; Δ outline bias mean +0.07 (range -0.07..+0.41), Δ rib mean +0.03 mm
- angle_half f=1.0: front 4/19, 3/4 10/19, outline max 1.90, ribs 0.71 mm (79 %), 3/4 mean 0.94; Δ outline bias mean +0.03 (range -0.13..+0.41), Δ rib mean +0.03 mm
- command: python models/M05_rose_bezier/E2_tri_width/run.py

### 2026-11-23 22:39 — E3 triangle height (kernel v2)
- H=1.5: front 0/19, 3/4 4/19, outline max 2.00, ribs 0.68 mm (81 %), 3/4 mean 1.50; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 1/19, 3/4 4/19, outline max 1.50, ribs 0.68 mm (81 %), 3/4 mean 1.21; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 5/19, 3/4 9/19, outline max 1.52, ribs 0.68 mm (81 %), 3/4 mean 0.93; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 8/19, outline max 2.51, ribs 0.68 mm (81 %), 3/4 mean 1.36; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 3.50, ribs 0.68 mm (81 %), 3/4 mean 2.28; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M05_rose_bezier/E3_tri_height/run.py

### 2026-11-23 22:39 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v2)
- twist x0.94: front 2/19, 3/4 1/19, outline max 2.67, ribs 2.15 mm (43 %), 3/4 mean 1.66; Δ outline bias mean -0.28 (range -2.37..+2.03), Δ rib mean +1.89 mm
- twist x0.97: front 3/19, 3/4 2/19, outline max 1.52, ribs 1.25 mm (53 %), 3/4 mean 1.18; Δ outline bias mean -0.13 (range -1.17..+1.02), Δ rib mean +0.73 mm
- twist x1.0: front 5/19, 3/4 9/19, outline max 1.52, ribs 0.68 mm (81 %), 3/4 mean 0.93; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 3/19, 3/4 4/19, outline max 1.53, ribs 1.16 mm (60 %), 3/4 mean 1.19; Δ outline bias mean +0.12 (range -1.00..+1.14), Δ rib mean +0.62 mm
- twist x1.06: front 2/19, 3/4 2/19, outline max 2.55, ribs 1.98 mm (45 %), 3/4 mean 1.60; Δ outline bias mean +0.24 (range -1.67..+2.25), Δ rib mean +1.64 mm
- 1-knot bumps: mean locality share 0.37 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.25 of 1 °
- command: python models/M05_rose_bezier/E4_twist/run.py

### 2026-11-23 22:39 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v2)
- r0 -2 mm: front 0/19, 3/4 3/19, outline max 2.21, ribs 1.27 mm (58 %), 3/4 mean 1.82; Δ outline bias mean -1.89 (range -1.99..-1.63), Δ rib mean +0.76 mm
- r0 -1 mm: front 1/19, 3/4 5/19, outline max 1.35, ribs 0.88 mm (68 %), 3/4 mean 1.19; Δ outline bias mean -0.95 (range -1.00..-0.82), Δ rib mean +0.25 mm
- r0 +0 mm: front 5/19, 3/4 9/19, outline max 1.52, ribs 0.68 mm (81 %), 3/4 mean 0.93; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 8/19, outline max 2.51, ribs 0.78 mm (68 %), 3/4 mean 1.27; Δ outline bias mean +0.95 (range +0.82..+1.00), Δ rib mean +0.12 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 3.51, ribs 1.08 mm (62 %), 3/4 mean 2.06; Δ outline bias mean +1.89 (range +1.63..+1.99), Δ rib mean +0.48 mm
- 1-knot bumps: mean locality share 0.58 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.58 of 1 mm
- command: python models/M05_rose_bezier/E5_radius/run.py

### 2026-11-23 22:39 — E6 sections (count x placement) (kernel v2)
- uniform_z n=8: loft deviation from exact max 0.12 / mean 0.038 mm; front 5/19, 3/4 9/19
- uniform_z n=11: loft deviation from exact max 0.11 / mean 0.017 mm; front 5/19, 3/4 8/19
- uniform_z n=15: loft deviation from exact max 0.04 / mean 0.005 mm; front 5/19, 3/4 9/19
- uniform_z n=20: loft deviation from exact max 0.01 / mean 0.001 mm; front 5/19, 3/4 8/19
- uniform_z n=30: loft deviation from exact max 0.02 / mean 0.000 mm; front 5/19, 3/4 8/19
- uniform_z n=39: loft deviation from exact max 0.02 / mean 0.000 mm; front 5/19, 3/4 8/19
- adaptive n=8: loft deviation from exact max 0.12 / mean 0.035 mm; front 5/19, 3/4 7/19
- adaptive n=11: loft deviation from exact max 0.11 / mean 0.023 mm; front 5/19, 3/4 9/19
- adaptive n=15: loft deviation from exact max 0.06 / mean 0.008 mm; front 5/19, 3/4 9/19
- adaptive n=20: loft deviation from exact max 0.02 / mean 0.002 mm; front 5/19, 3/4 8/19
- adaptive n=30: loft deviation from exact max 0.02 / mean 0.001 mm; front 5/19, 3/4 8/19
- adaptive n=39: loft deviation from exact max 0.02 / mean 0.000 mm; front 5/19, 3/4 8/19
- bezier_t n=8: loft deviation from exact max 0.78 / mean 0.144 mm; front 5/19, 3/4 6/19
- bezier_t n=11: loft deviation from exact max 0.10 / mean 0.022 mm; front 5/19, 3/4 6/19
- bezier_t n=15: loft deviation from exact max 0.10 / mean 0.014 mm; front 5/19, 3/4 8/19
- bezier_t n=20: loft deviation from exact max 0.07 / mean 0.007 mm; front 5/19, 3/4 8/19
- bezier_t n=30: loft deviation from exact max 0.02 / mean 0.002 mm; front 5/19, 3/4 8/19
- bezier_t n=39: loft deviation from exact max 0.02 / mean 0.001 mm; front 5/19, 3/4 8/19
- knots10 n=20: loft deviation from exact max 0.01 / mean 0.001 mm; front 5/19, 3/4 8/19
- own sections: {'mode': 'uniform_z', 'count': 15}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M05_rose_bezier/E6_sections/run.py

### 2026-11-23 23:04 — E0 fit (kernel v3)
- start (as built): front 5/19, 3/4 12/19, ribs 0.76 mm
- result (as built): front 6/19, 3/4 10/19, outline max 1.53, ribs 0.67 mm / 79 %, 3/4 mean 0.90
- exact curves: front 6/19, 3/4 10/19
- 28 params, 274.0 s, nfev 25, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 164.9, pool:M01_E0 163.0, pool:M05_E0 166.6, pool:M02_X1c 189.9, pool:M01_E0v2 166.4, pool:M02_E0v2 176.1, pool:M03_E0v2 167.9, pool:M04_E0v2 169.2, pool:M05_E0v2 163.3, pool:M06_E0v2 167.5, pool:M07_E0v2 162.4, pool:M08_E0v2 169.3, pool:M09_E0v2 163.8, pool:M10_E0v2 160.3 -> best: pool:M10_E0v2
- Fusion script: models\M05_rose_bezier\fusion\M05\M05.py
- command: python models/M05_rose_bezier/E0_fit/run.py

### 2026-11-23 23:04 — E1 triangle count (kernel v3)
- N=12: front 4/19, 3/4 3/19, outline max 1.04, ribs 0.67 mm (79 %), 3/4 mean 0.96; Δ outline bias mean -0.31 (range -0.71..-0.06), Δ rib mean +0.00 mm
- N=16: front 4/19, 3/4 6/19, outline max 1.19, ribs 0.67 mm (79 %), 3/4 mean 0.87; Δ outline bias mean -0.18 (range -0.36..+0.02), Δ rib mean +0.00 mm
- N=22 (own): front 6/19, 3/4 10/19, outline max 1.53, ribs 0.67 mm (79 %), 3/4 mean 0.90; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 3/19, 3/4 11/19, outline max 1.70, ribs 0.67 mm (79 %), 3/4 mean 0.92; Δ outline bias mean +0.12 (range +0.05..+0.23), Δ rib mean +0.00 mm
- N=45: front 3/19, 3/4 12/19, outline max 1.81, ribs 0.67 mm (79 %), 3/4 mean 0.91; Δ outline bias mean +0.19 (range +0.09..+0.31), Δ rib mean +0.00 mm
- command: python models/M05_rose_bezier/E1_tri_count/run.py

### 2026-11-23 23:04 — E2 triangle width (fill) x placement (kernel v3)
- arc f=0.5: front 3/19, 3/4 10/19, outline max 1.66, ribs 0.67 mm (79 %), 3/4 mean 0.92; Δ outline bias mean +0.13 (range +0.07..+0.18), Δ rib mean +0.00 mm
- arc f=0.7: front 3/19, 3/4 9/19, outline max 1.62, ribs 0.67 mm (79 %), 3/4 mean 0.92; Δ outline bias mean +0.09 (range +0.05..+0.12), Δ rib mean +0.00 mm
- arc f=0.85: front 6/19, 3/4 9/19, outline max 1.58, ribs 0.67 mm (79 %), 3/4 mean 0.91; Δ outline bias mean +0.05 (range +0.03..+0.07), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 6/19, 3/4 10/19, outline max 1.53, ribs 0.67 mm (79 %), 3/4 mean 0.90; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 3/19, 3/4 11/19, outline max 1.89, ribs 0.71 mm (78 %), 3/4 mean 0.92; Δ outline bias mean +0.15 (range -0.01..+0.40), Δ rib mean +0.03 mm
- angle_half f=0.7: front 3/19, 3/4 11/19, outline max 1.89, ribs 0.71 mm (78 %), 3/4 mean 0.91; Δ outline bias mean +0.11 (range -0.02..+0.40), Δ rib mean +0.03 mm
- angle_half f=0.85: front 4/19, 3/4 10/19, outline max 1.89, ribs 0.71 mm (78 %), 3/4 mean 0.91; Δ outline bias mean +0.08 (range -0.05..+0.40), Δ rib mean +0.03 mm
- angle_half f=1.0: front 4/19, 3/4 11/19, outline max 1.89, ribs 0.71 mm (78 %), 3/4 mean 0.90; Δ outline bias mean +0.04 (range -0.10..+0.40), Δ rib mean +0.03 mm
- command: python models/M05_rose_bezier/E2_tri_width/run.py

### 2026-11-23 23:04 — E3 triangle height (kernel v3)
- H=1.5: front 0/19, 3/4 3/19, outline max 1.99, ribs 0.67 mm (79 %), 3/4 mean 1.56; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 1/19, 3/4 5/19, outline max 1.49, ribs 0.67 mm (79 %), 3/4 mean 1.24; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 6/19, 3/4 10/19, outline max 1.53, ribs 0.67 mm (79 %), 3/4 mean 0.90; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 7/19, outline max 2.52, ribs 0.67 mm (79 %), 3/4 mean 1.31; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 3.51, ribs 0.67 mm (79 %), 3/4 mean 2.25; Δ outline bias mean +1.99 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M05_rose_bezier/E3_tri_height/run.py

### 2026-11-23 23:04 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v3)
- twist x0.94: front 3/19, 3/4 2/19, outline max 2.70, ribs 2.15 mm (41 %), 3/4 mean 1.48; Δ outline bias mean -0.27 (range -2.30..+2.01), Δ rib mean +1.88 mm
- twist x0.97: front 4/19, 3/4 3/19, outline max 1.53, ribs 1.23 mm (53 %), 3/4 mean 1.02; Δ outline bias mean -0.13 (range -1.13..+1.02), Δ rib mean +0.72 mm
- twist x1.0: front 6/19, 3/4 10/19, outline max 1.53, ribs 0.67 mm (79 %), 3/4 mean 0.90; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 4/19, 3/4 5/19, outline max 1.53, ribs 1.15 mm (59 %), 3/4 mean 1.20; Δ outline bias mean +0.12 (range -0.99..+1.10), Δ rib mean +0.62 mm
- twist x1.06: front 3/19, 3/4 4/19, outline max 2.47, ribs 1.98 mm (45 %), 3/4 mean 1.62; Δ outline bias mean +0.23 (range -1.64..+2.18), Δ rib mean +1.65 mm
- 1-knot bumps: mean locality share 0.37 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.25 of 1 °
- command: python models/M05_rose_bezier/E4_twist/run.py

### 2026-11-23 23:04 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v3)
- r0 -2 mm: front 0/19, 3/4 2/19, outline max 2.13, ribs 1.26 mm (58 %), 3/4 mean 1.82; Δ outline bias mean -1.89 (range -1.99..-1.64), Δ rib mean +0.74 mm
- r0 -1 mm: front 1/19, 3/4 5/19, outline max 1.30, ribs 0.86 mm (70 %), 3/4 mean 1.19; Δ outline bias mean -0.95 (range -1.00..-0.82), Δ rib mean +0.24 mm
- r0 +0 mm: front 6/19, 3/4 10/19, outline max 1.53, ribs 0.67 mm (79 %), 3/4 mean 0.90; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 7/19, outline max 2.52, ribs 0.77 mm (69 %), 3/4 mean 1.23; Δ outline bias mean +0.95 (range +0.82..+1.00), Δ rib mean +0.12 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 3.52, ribs 1.07 mm (62 %), 3/4 mean 2.02; Δ outline bias mean +1.89 (range +1.64..+1.99), Δ rib mean +0.48 mm
- 1-knot bumps: mean locality share 0.59 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.54 of 1 mm
- command: python models/M05_rose_bezier/E5_radius/run.py

### 2026-11-23 23:05 — E6 sections (count x placement) (kernel v3)
- uniform_z n=8: loft deviation from exact max 0.39 / mean 0.091 mm; front 6/19, 3/4 7/19
- uniform_z n=11: loft deviation from exact max 0.18 / mean 0.039 mm; front 6/19, 3/4 9/19
- uniform_z n=15: loft deviation from exact max 0.06 / mean 0.010 mm; front 6/19, 3/4 10/19
- uniform_z n=20: loft deviation from exact max 0.03 / mean 0.003 mm; front 6/19, 3/4 10/19
- uniform_z n=30: loft deviation from exact max 0.01 / mean 0.000 mm; front 6/19, 3/4 10/19
- uniform_z n=39: loft deviation from exact max 0.01 / mean 0.000 mm; front 6/19, 3/4 10/19
- adaptive n=8: loft deviation from exact max 0.26 / mean 0.092 mm; front 6/19, 3/4 7/19
- adaptive n=11: loft deviation from exact max 0.14 / mean 0.030 mm; front 6/19, 3/4 9/19
- adaptive n=15: loft deviation from exact max 0.08 / mean 0.013 mm; front 6/19, 3/4 10/19
- adaptive n=20: loft deviation from exact max 0.03 / mean 0.004 mm; front 6/19, 3/4 10/19
- adaptive n=30: loft deviation from exact max 0.01 / mean 0.001 mm; front 6/19, 3/4 10/19
- adaptive n=39: loft deviation from exact max 0.01 / mean 0.000 mm; front 6/19, 3/4 10/19
- bezier_t n=8: loft deviation from exact max 1.67 / mean 0.323 mm; front 6/19, 3/4 8/19
- bezier_t n=11: loft deviation from exact max 0.07 / mean 0.016 mm; front 6/19, 3/4 7/19
- bezier_t n=15: loft deviation from exact max 0.13 / mean 0.019 mm; front 6/19, 3/4 9/19
- bezier_t n=20: loft deviation from exact max 0.08 / mean 0.010 mm; front 6/19, 3/4 10/19
- bezier_t n=30: loft deviation from exact max 0.03 / mean 0.002 mm; front 6/19, 3/4 10/19
- bezier_t n=39: loft deviation from exact max 0.01 / mean 0.001 mm; front 6/19, 3/4 10/19
- knots10 n=20: loft deviation from exact max 0.03 / mean 0.003 mm; front 6/19, 3/4 10/19
- own sections: {'mode': 'uniform_z', 'count': 15}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M05_rose_bezier/E6_sections/run.py

### 2026-11-23 23:14 — final round (kernel v3) — results recorded (kernel v3)
- rank 6/10, score 0.492; front 6/19, 3/4 10/19, ribs 0.67 mm, cost 160.3 (best start pool:M10_E0v2)
- orientation offset -0.49°; MODEL.md: 'Final round — kernel v3' section appended; verified by judge/verify_e0.py
