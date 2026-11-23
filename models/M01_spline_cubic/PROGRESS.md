# M01_spline_cubic — progress

## Status  (overwrite this block only)
- State: final (kernel v3), rank 4/10
- Best E0 (as built): front 10/19, 3/4 13/19, 15 params, score 0.623
- Next: none (study complete)

## Log  (append only, newest at the bottom)

### 2026-11-23 22:24 — model created (kernel v1)
- model.py: custom spline base (fixed) + 11 bez_points keys (Catmull-Rom) + cubic twist (k1, k2, max), 14 params
- settings from ../BaseScript: N 22, H 2.4, angle_half placement, 11 uniform sections
- Gate C: BaseScript Fusion build (fusion_runs/F1-4) reproduced within 0.05 mm mean / 0.20 mm max (outline maxY)

### 2026-11-23 22:25 — E0 fit (kernel v1)
- start (as built): front 2/19, 3/4 11/19, ribs 1.38 mm
- result (as built): front 3/19, 3/4 14/19, outline max 2.30, ribs 0.67 mm / 80 %, 3/4 mean 0.75
- exact curves: front 4/19, 3/4 13/19
- 14 params, 14.6 s, nfev 15, cap hit [False, False], constraints OK
- Fusion script: models\M01_spline_cubic\fusion\M01\M01.py
- command: python models/M01_spline_cubic/E0_fit/run.py

### 2026-11-23 22:25 — E1 triangle count (kernel v1)
- N=12: front 1/19, 3/4 7/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.94; Δ outline bias mean -0.47 (range -1.21..+0.00), Δ rib mean +0.00 mm
- N=16: front 2/19, 3/4 12/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.78; Δ outline bias mean -0.19 (range -0.50..+0.00), Δ rib mean +0.00 mm
- N=22 (own): front 3/19, 3/4 14/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.75; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 3/19, 3/4 14/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.81; Δ outline bias mean +0.10 (range +0.00..+0.22), Δ rib mean +0.00 mm
- N=45: front 1/19, 3/4 12/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.86; Δ outline bias mean +0.17 (range +0.00..+0.31), Δ rib mean +0.00 mm
- command: python models/M01_spline_cubic/E1_tri_count/run.py

### 2026-11-23 22:25 — E2 triangle width (fill) x placement (kernel v1)
- arc f=0.5: front 1/19, 3/4 13/19, outline max 2.15, ribs 0.67 mm (80 %), 3/4 mean 0.84; Δ outline bias mean +0.13 (range -0.15..+0.30), Δ rib mean +0.00 mm
- arc f=0.7: front 2/19, 3/4 14/19, outline max 2.11, ribs 0.67 mm (80 %), 3/4 mean 0.81; Δ outline bias mean +0.09 (range -0.19..+0.25), Δ rib mean +0.00 mm
- arc f=0.85: front 3/19, 3/4 14/19, outline max 2.08, ribs 0.67 mm (80 %), 3/4 mean 0.79; Δ outline bias mean +0.05 (range -0.22..+0.20), Δ rib mean +0.00 mm
- arc f=1.0: front 3/19, 3/4 14/19, outline max 2.05, ribs 0.67 mm (80 %), 3/4 mean 0.76; Δ outline bias mean +0.00 (range -0.26..+0.14), Δ rib mean +0.00 mm
- angle_half f=0.5: front 1/19, 3/4 14/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.81; Δ outline bias mean +0.12 (range +0.00..+0.21), Δ rib mean +0.00 mm
- angle_half f=0.7: front 2/19, 3/4 14/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.78; Δ outline bias mean +0.08 (range +0.00..+0.14), Δ rib mean +0.00 mm
- angle_half f=0.85: front 3/19, 3/4 14/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.76; Δ outline bias mean +0.04 (range +0.00..+0.08), Δ rib mean +0.00 mm
- angle_half f=1.0 (own): front 3/19, 3/4 14/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.75; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- command: python models/M01_spline_cubic/E2_tri_width/run.py

### 2026-11-23 22:25 — E3 triangle height (kernel v1)
- H=1.5: front 1/19, 3/4 8/19, outline max 1.40, ribs 0.67 mm (80 %), 3/4 mean 0.83; Δ outline bias mean -0.90 (range -0.90..-0.90), Δ rib mean +0.00 mm
- H=2.0: front 3/19, 3/4 15/19, outline max 1.90, ribs 0.67 mm (80 %), 3/4 mean 0.68; Δ outline bias mean -0.40 (range -0.40..-0.40), Δ rib mean +0.00 mm
- H=2.4 (own): front 3/19, 3/4 14/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.75; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=3.0: front 0/19, 3/4 8/19, outline max 2.90, ribs 0.67 mm (80 %), 3/4 mean 1.19; Δ outline bias mean +0.60 (range +0.60..+0.60), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 0/19, outline max 3.90, ribs 0.67 mm (80 %), 3/4 mean 2.20; Δ outline bias mean +1.60 (range +1.59..+1.60), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.90, ribs 0.67 mm (80 %), 3/4 mean 3.31; Δ outline bias mean +2.59 (range +2.59..+2.60), Δ rib mean +0.00 mm
- command: python models/M01_spline_cubic/E3_tri_height/run.py

### 2026-11-23 22:25 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v1)
- twist x0.94: front 1/19, 3/4 4/19, outline max 2.31, ribs 2.24 mm (40 %), 3/4 mean 1.63; Δ outline bias mean -0.27 (range -2.31..+1.98), Δ rib mean +1.98 mm
- twist x0.97: front 2/19, 3/4 6/19, outline max 2.31, ribs 1.29 mm (53 %), 3/4 mean 1.16; Δ outline bias mean -0.13 (range -1.12..+1.00), Δ rib mean +0.78 mm
- twist x1.0: front 3/19, 3/4 14/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.75; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 2/19, 3/4 8/19, outline max 2.30, ribs 1.12 mm (59 %), 3/4 mean 0.99; Δ outline bias mean +0.12 (range -0.91..+1.12), Δ rib mean +0.54 mm
- twist x1.06: front 1/19, 3/4 7/19, outline max 3.12, ribs 1.81 mm (49 %), 3/4 mean 1.42; Δ outline bias mean +0.24 (range -1.63..+2.30), Δ rib mean +1.37 mm
- 1-knot bumps: mean locality share 0.21 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.15 of 1 °
- command: python models/M01_spline_cubic/E4_twist/run.py

### 2026-11-23 22:25 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v1)
- r0 -2 mm: front 0/19, 3/4 1/19, outline max 2.09, ribs 1.26 mm (63 %), 3/4 mean 1.52; Δ outline bias mean -1.90 (range -2.00..-1.66), Δ rib mean +0.73 mm
- r0 -1 mm: front 1/19, 3/4 8/19, outline max 1.30, ribs 0.86 mm (77 %), 3/4 mean 0.84; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.23 mm
- r0 +0 mm: front 3/19, 3/4 14/19, outline max 2.30, ribs 0.67 mm (80 %), 3/4 mean 0.75; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 3/19, outline max 3.30, ribs 0.70 mm (76 %), 3/4 mean 1.47; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.00 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.30, ribs 0.92 mm (66 %), 3/4 mean 2.40; Δ outline bias mean +1.90 (range +1.66..+2.00), Δ rib mean +0.24 mm
- 1-knot bumps: mean locality share 0.63 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.49 of 1 mm
- command: python models/M01_spline_cubic/E5_radius/run.py

### 2026-11-23 22:25 — E6 sections (count x placement) (kernel v1)
- uniform_z n=8: loft deviation from exact max 1.72 / mean 0.239 mm; front 3/19, 3/4 14/19
- uniform_z n=11: loft deviation from exact max 1.77 / mean 0.190 mm; front 3/19, 3/4 14/19
- uniform_z n=15: loft deviation from exact max 1.08 / mean 0.133 mm; front 4/19, 3/4 14/19
- uniform_z n=20: loft deviation from exact max 0.26 / mean 0.045 mm; front 4/19, 3/4 14/19
- uniform_z n=30: loft deviation from exact max 0.09 / mean 0.009 mm; front 4/19, 3/4 14/19
- uniform_z n=39: loft deviation from exact max 0.05 / mean 0.003 mm; front 4/19, 3/4 14/19
- adaptive n=8: loft deviation from exact max 1.74 / mean 0.248 mm; front 3/19, 3/4 14/19
- adaptive n=11: loft deviation from exact max 1.47 / mean 0.190 mm; front 4/19, 3/4 14/19
- adaptive n=15: loft deviation from exact max 0.59 / mean 0.105 mm; front 4/19, 3/4 15/19
- adaptive n=20: loft deviation from exact max 0.09 / mean 0.013 mm; front 4/19, 3/4 14/19
- adaptive n=30: loft deviation from exact max 0.05 / mean 0.006 mm; front 4/19, 3/4 14/19
- adaptive n=39: loft deviation from exact max 0.03 / mean 0.003 mm; front 4/19, 3/4 14/19
- knots10 n=20: loft deviation from exact max 0.26 / mean 0.045 mm; front 4/19, 3/4 14/19
- own sections: {'mode': 'uniform_z', 'count': 11}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M01_spline_cubic/E6_sections/run.py

### 2026-11-23 22:28 — conclusions written (kernel v1)
- MODEL.md conclusions: main limitation = 3-parameter cubic twist (upper half ribs fail); best held-out 3/4 so far (14/19); H=2.0 better than own 2.4

### 2026-11-23 22:37 — E0 fit (kernel v2)
- start (as built): front 2/19, 3/4 11/19, ribs 1.38 mm
- result (as built): front 3/19, 3/4 13/19, outline max 2.27, ribs 0.67 mm / 80 %, 3/4 mean 0.74
- exact curves: front 4/19, 3/4 11/19
- 14 params, 30.8 s, nfev 14, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 198.5, pool:M01_E0 198.4, pool:M05_E0 198.3, pool:M02_X1c 198.6 -> best: pool:M05_E0
- Fusion script: models\M01_spline_cubic\fusion\M01\M01.py
- command: python models/M01_spline_cubic/E0_fit/run.py

### 2026-11-23 22:38 — E1 triangle count (kernel v2)
- N=12: front 1/19, 3/4 6/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.89; Δ outline bias mean -0.47 (range -1.21..+0.00), Δ rib mean +0.00 mm
- N=16: front 2/19, 3/4 13/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.78; Δ outline bias mean -0.19 (range -0.50..+0.00), Δ rib mean +0.00 mm
- N=22 (own): front 3/19, 3/4 13/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.74; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 3/19, 3/4 12/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.83; Δ outline bias mean +0.10 (range +0.00..+0.22), Δ rib mean +0.00 mm
- N=45: front 2/19, 3/4 12/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.89; Δ outline bias mean +0.17 (range +0.00..+0.31), Δ rib mean +0.00 mm
- command: python models/M01_spline_cubic/E1_tri_count/run.py

### 2026-11-23 22:38 — E2 triangle width (fill) x placement (kernel v2)
- arc f=0.5: front 1/19, 3/4 14/19, outline max 2.11, ribs 0.67 mm (80 %), 3/4 mean 0.85; Δ outline bias mean +0.13 (range -0.15..+0.30), Δ rib mean -0.00 mm
- arc f=0.7: front 3/19, 3/4 14/19, outline max 2.08, ribs 0.67 mm (80 %), 3/4 mean 0.82; Δ outline bias mean +0.09 (range -0.19..+0.25), Δ rib mean -0.00 mm
- arc f=0.85: front 3/19, 3/4 14/19, outline max 2.05, ribs 0.67 mm (80 %), 3/4 mean 0.79; Δ outline bias mean +0.05 (range -0.22..+0.20), Δ rib mean -0.00 mm
- arc f=1.0: front 3/19, 3/4 14/19, outline max 2.01, ribs 0.67 mm (80 %), 3/4 mean 0.77; Δ outline bias mean +0.00 (range -0.26..+0.14), Δ rib mean -0.00 mm
- angle_half f=0.5: front 2/19, 3/4 13/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.82; Δ outline bias mean +0.12 (range +0.00..+0.21), Δ rib mean +0.00 mm
- angle_half f=0.7: front 3/19, 3/4 13/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.79; Δ outline bias mean +0.08 (range +0.00..+0.14), Δ rib mean +0.00 mm
- angle_half f=0.85: front 3/19, 3/4 13/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.77; Δ outline bias mean +0.04 (range +0.00..+0.08), Δ rib mean +0.00 mm
- angle_half f=1.0 (own): front 3/19, 3/4 13/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.74; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- command: python models/M01_spline_cubic/E2_tri_width/run.py

### 2026-11-23 22:38 — E3 triangle height (kernel v2)
- H=1.5: front 1/19, 3/4 8/19, outline max 1.37, ribs 0.67 mm (80 %), 3/4 mean 0.82; Δ outline bias mean -0.90 (range -0.90..-0.90), Δ rib mean +0.00 mm
- H=2.0: front 3/19, 3/4 16/19, outline max 1.87, ribs 0.67 mm (80 %), 3/4 mean 0.70; Δ outline bias mean -0.40 (range -0.40..-0.40), Δ rib mean +0.00 mm
- H=2.4 (own): front 3/19, 3/4 13/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.74; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=3.0: front 0/19, 3/4 8/19, outline max 2.87, ribs 0.67 mm (80 %), 3/4 mean 1.22; Δ outline bias mean +0.60 (range +0.60..+0.60), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 0/19, outline max 3.87, ribs 0.67 mm (80 %), 3/4 mean 2.26; Δ outline bias mean +1.60 (range +1.59..+1.60), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.87, ribs 0.67 mm (80 %), 3/4 mean 3.37; Δ outline bias mean +2.59 (range +2.59..+2.60), Δ rib mean +0.00 mm
- command: python models/M01_spline_cubic/E3_tri_height/run.py

### 2026-11-23 22:38 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v2)
- twist x0.94: front 1/19, 3/4 4/19, outline max 2.31, ribs 2.25 mm (40 %), 3/4 mean 1.62; Δ outline bias mean -0.27 (range -2.31..+1.98), Δ rib mean +1.98 mm
- twist x0.97: front 2/19, 3/4 5/19, outline max 2.27, ribs 1.30 mm (52 %), 3/4 mean 1.16; Δ outline bias mean -0.13 (range -1.12..+1.00), Δ rib mean +0.79 mm
- twist x1.0: front 3/19, 3/4 13/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.74; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 2/19, 3/4 8/19, outline max 2.27, ribs 1.12 mm (59 %), 3/4 mean 1.00; Δ outline bias mean +0.12 (range -0.91..+1.12), Δ rib mean +0.54 mm
- twist x1.06: front 1/19, 3/4 5/19, outline max 3.13, ribs 1.81 mm (49 %), 3/4 mean 1.43; Δ outline bias mean +0.24 (range -1.63..+2.31), Δ rib mean +1.37 mm
- 1-knot bumps: mean locality share 0.21 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.15 of 1 °
- command: python models/M01_spline_cubic/E4_twist/run.py

### 2026-11-23 22:38 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v2)
- r0 -2 mm: front 0/19, 3/4 1/19, outline max 2.10, ribs 1.27 mm (62 %), 3/4 mean 1.47; Δ outline bias mean -1.90 (range -2.00..-1.66), Δ rib mean +0.74 mm
- r0 -1 mm: front 1/19, 3/4 9/19, outline max 1.27, ribs 0.87 mm (77 %), 3/4 mean 0.80; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.24 mm
- r0 +0 mm: front 3/19, 3/4 13/19, outline max 2.27, ribs 0.67 mm (80 %), 3/4 mean 0.74; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 3/19, outline max 3.27, ribs 0.70 mm (76 %), 3/4 mean 1.53; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.00 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.27, ribs 0.91 mm (66 %), 3/4 mean 2.45; Δ outline bias mean +1.90 (range +1.66..+2.00), Δ rib mean +0.23 mm
- 1-knot bumps: mean locality share 0.63 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.49 of 1 mm
- command: python models/M01_spline_cubic/E5_radius/run.py

### 2026-11-23 22:38 — E6 sections (count x placement) (kernel v2)
- uniform_z n=8: loft deviation from exact max 1.72 / mean 0.240 mm; front 3/19, 3/4 14/19
- uniform_z n=11: loft deviation from exact max 1.77 / mean 0.190 mm; front 3/19, 3/4 13/19
- uniform_z n=15: loft deviation from exact max 1.08 / mean 0.133 mm; front 4/19, 3/4 13/19
- uniform_z n=20: loft deviation from exact max 0.26 / mean 0.045 mm; front 4/19, 3/4 13/19
- uniform_z n=30: loft deviation from exact max 0.09 / mean 0.009 mm; front 4/19, 3/4 13/19
- uniform_z n=39: loft deviation from exact max 0.05 / mean 0.003 mm; front 4/19, 3/4 13/19
- adaptive n=8: loft deviation from exact max 1.74 / mean 0.249 mm; front 3/19, 3/4 14/19
- adaptive n=11: loft deviation from exact max 1.47 / mean 0.191 mm; front 4/19, 3/4 13/19
- adaptive n=15: loft deviation from exact max 0.59 / mean 0.105 mm; front 4/19, 3/4 13/19
- adaptive n=20: loft deviation from exact max 0.09 / mean 0.013 mm; front 4/19, 3/4 13/19
- adaptive n=30: loft deviation from exact max 0.05 / mean 0.006 mm; front 4/19, 3/4 13/19
- adaptive n=39: loft deviation from exact max 0.03 / mean 0.003 mm; front 4/19, 3/4 13/19
- knots10 n=20: loft deviation from exact max 0.26 / mean 0.045 mm; front 4/19, 3/4 13/19
- own sections: {'mode': 'uniform_z', 'count': 11}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M01_spline_cubic/E6_sections/run.py

### 2026-11-23 23:02 — E0 fit (kernel v3)
- start (as built): front 2/19, 3/4 11/19, ribs 1.38 mm
- result (as built): front 10/19, 3/4 13/19, outline max 2.09, ribs 0.43 mm / 92 %, 3/4 mean 0.83
- exact curves: front 12/19, 3/4 13/19
- 15 params, 123.7 s, nfev 14, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 91.6, pool:M01_E0 91.1, pool:M05_E0 91.2, pool:M02_X1c 91.2, pool:M01_E0v2 91.2, pool:M02_E0v2 91.2, pool:M03_E0v2 91.3, pool:M04_E0v2 91.2, pool:M05_E0v2 91.2, pool:M06_E0v2 91.3, pool:M07_E0v2 91.3, pool:M08_E0v2 91.2, pool:M09_E0v2 91.2, pool:M10_E0v2 91.2 -> best: pool:M01_E0
- Fusion script: models\M01_spline_cubic\fusion\M01\M01.py
- command: python models/M01_spline_cubic/E0_fit/run.py

### 2026-11-23 23:02 — E1 triangle count (kernel v3)
- N=12: front 2/19, 3/4 8/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 1.01; Δ outline bias mean -0.46 (range -1.22..+0.00), Δ rib mean +0.00 mm
- N=16: front 6/19, 3/4 10/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 0.90; Δ outline bias mean -0.18 (range -0.52..+0.00), Δ rib mean +0.00 mm
- N=22 (own): front 10/19, 3/4 13/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 0.83; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 11/19, 3/4 12/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 0.84; Δ outline bias mean +0.10 (range +0.00..+0.22), Δ rib mean +0.00 mm
- N=45: front 10/19, 3/4 12/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 0.86; Δ outline bias mean +0.17 (range +0.00..+0.32), Δ rib mean +0.00 mm
- command: python models/M01_spline_cubic/E1_tri_count/run.py

### 2026-11-23 23:02 — E2 triangle width (fill) x placement (kernel v3)
- arc f=0.5: front 11/19, 3/4 11/19, outline max 2.01, ribs 0.43 mm (92 %), 3/4 mean 0.87; Δ outline bias mean +0.12 (range -0.15..+0.32), Δ rib mean +0.00 mm
- arc f=0.7: front 11/19, 3/4 11/19, outline max 1.98, ribs 0.43 mm (92 %), 3/4 mean 0.86; Δ outline bias mean +0.08 (range -0.19..+0.27), Δ rib mean +0.00 mm
- arc f=0.85: front 11/19, 3/4 10/19, outline max 1.95, ribs 0.43 mm (92 %), 3/4 mean 0.85; Δ outline bias mean +0.04 (range -0.22..+0.22), Δ rib mean +0.00 mm
- arc f=1.0: front 12/19, 3/4 10/19, outline max 1.91, ribs 0.43 mm (92 %), 3/4 mean 0.84; Δ outline bias mean -0.00 (range -0.27..+0.16), Δ rib mean +0.00 mm
- angle_half f=0.5: front 10/19, 3/4 11/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 0.86; Δ outline bias mean +0.12 (range +0.00..+0.21), Δ rib mean +0.00 mm
- angle_half f=0.7: front 11/19, 3/4 11/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 0.85; Δ outline bias mean +0.08 (range +0.00..+0.14), Δ rib mean +0.00 mm
- angle_half f=0.85: front 10/19, 3/4 13/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 0.85; Δ outline bias mean +0.04 (range +0.00..+0.08), Δ rib mean +0.00 mm
- angle_half f=1.0 (own): front 10/19, 3/4 13/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 0.83; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- command: python models/M01_spline_cubic/E2_tri_width/run.py

### 2026-11-23 23:02 — E3 triangle height (kernel v3)
- H=1.5: front 2/19, 3/4 9/19, outline max 1.67, ribs 0.43 mm (92 %), 3/4 mean 1.01; Δ outline bias mean -0.90 (range -0.90..-0.90), Δ rib mean +0.00 mm
- H=2.0: front 4/19, 3/4 12/19, outline max 1.69, ribs 0.43 mm (92 %), 3/4 mean 0.81; Δ outline bias mean -0.40 (range -0.40..-0.40), Δ rib mean +0.00 mm
- H=2.4 (own): front 10/19, 3/4 13/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 0.83; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=3.0: front 1/19, 3/4 7/19, outline max 2.69, ribs 0.43 mm (92 %), 3/4 mean 1.12; Δ outline bias mean +0.60 (range +0.60..+0.60), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 0/19, outline max 3.69, ribs 0.43 mm (92 %), 3/4 mean 2.06; Δ outline bias mean +1.60 (range +1.59..+1.60), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.69, ribs 0.43 mm (92 %), 3/4 mean 3.19; Δ outline bias mean +2.59 (range +2.59..+2.60), Δ rib mean +0.00 mm
- command: python models/M01_spline_cubic/E3_tri_height/run.py

### 2026-11-23 23:02 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v3)
- twist x0.94: front 1/19, 3/4 3/19, outline max 3.16, ribs 2.04 mm (40 %), 3/4 mean 1.85; Δ outline bias mean -0.27 (range -2.36..+1.89), Δ rib mean +2.03 mm
- twist x0.97: front 3/19, 3/4 4/19, outline max 2.10, ribs 1.08 mm (53 %), 3/4 mean 1.32; Δ outline bias mean -0.13 (range -1.15..+0.95), Δ rib mean +0.83 mm
- twist x1.0: front 10/19, 3/4 13/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 0.83; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 2/19, 3/4 12/19, outline max 2.09, ribs 1.09 mm (57 %), 3/4 mean 0.79; Δ outline bias mean +0.12 (range -0.97..+1.07), Δ rib mean +0.84 mm
- twist x1.06: front 1/19, 3/4 7/19, outline max 2.09, ribs 1.98 mm (44 %), 3/4 mean 1.19; Δ outline bias mean +0.24 (range -1.78..+2.08), Δ rib mean +1.97 mm
- 1-knot bumps: mean locality share 0.26 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.16 of 1 °
- command: python models/M01_spline_cubic/E4_twist/run.py

### 2026-11-23 23:02 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v3)
- r0 -2 mm: front 0/19, 3/4 0/19, outline max 2.39, ribs 1.13 mm (57 %), 3/4 mean 1.76; Δ outline bias mean -1.90 (range -2.00..-1.65), Δ rib mean +0.87 mm
- r0 -1 mm: front 1/19, 3/4 8/19, outline max 1.58, ribs 0.70 mm (73 %), 3/4 mean 1.04; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.33 mm
- r0 +0 mm: front 10/19, 3/4 13/19, outline max 2.09, ribs 0.43 mm (92 %), 3/4 mean 0.83; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 3/19, outline max 3.09, ribs 0.70 mm (71 %), 3/4 mean 1.36; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.34 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.09, ribs 1.15 mm (56 %), 3/4 mean 2.25; Δ outline bias mean +1.90 (range +1.65..+2.00), Δ rib mean +0.92 mm
- 1-knot bumps: mean locality share 0.63 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.49 of 1 mm
- command: python models/M01_spline_cubic/E5_radius/run.py

### 2026-11-23 23:02 — E6 sections (count x placement) (kernel v3)
- uniform_z n=8: loft deviation from exact max 1.69 / mean 0.194 mm; front 10/19, 3/4 14/19
- uniform_z n=11: loft deviation from exact max 1.83 / mean 0.181 mm; front 10/19, 3/4 13/19
- uniform_z n=15: loft deviation from exact max 1.10 / mean 0.129 mm; front 12/19, 3/4 13/19
- uniform_z n=20: loft deviation from exact max 0.26 / mean 0.044 mm; front 12/19, 3/4 13/19
- uniform_z n=30: loft deviation from exact max 0.09 / mean 0.009 mm; front 12/19, 3/4 13/19
- uniform_z n=39: loft deviation from exact max 0.05 / mean 0.003 mm; front 12/19, 3/4 13/19
- adaptive n=8: loft deviation from exact max 1.76 / mean 0.204 mm; front 10/19, 3/4 14/19
- adaptive n=11: loft deviation from exact max 1.49 / mean 0.171 mm; front 12/19, 3/4 13/19
- adaptive n=15: loft deviation from exact max 0.59 / mean 0.095 mm; front 11/19, 3/4 14/19
- adaptive n=20: loft deviation from exact max 0.10 / mean 0.011 mm; front 12/19, 3/4 13/19
- adaptive n=30: loft deviation from exact max 0.05 / mean 0.005 mm; front 12/19, 3/4 13/19
- adaptive n=39: loft deviation from exact max 0.04 / mean 0.003 mm; front 12/19, 3/4 13/19
- knots10 n=20: loft deviation from exact max 0.26 / mean 0.044 mm; front 12/19, 3/4 13/19
- own sections: {'mode': 'uniform_z', 'count': 11}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M01_spline_cubic/E6_sections/run.py

### 2026-11-23 23:14 — final round (kernel v3) — results recorded (kernel v3)
- rank 4/10, score 0.623; front 10/19, 3/4 13/19, ribs 0.43 mm, cost 91.1 (best start pool:M01_E0)
- orientation offset -1.45°; MODEL.md: 'Final round — kernel v3' section appended; verified by judge/verify_e0.py
