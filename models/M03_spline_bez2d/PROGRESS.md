# M03_spline_bez2d — progress

## Status  (overwrite this block only)
- State: ACTIVE model (chosen 2026-11-24)
- Best E0 (as built): front 14/19, 3/4 14/19, 16 params, Fusion-verified
- Next: segment loop: S01 rim, waist S08-S11

## Log  (append only, newest at the bottom)

### 2026-11-23 22:28 — model created (kernel v1)
- model.py: custom spline base (fixed over height, bases.custom_spline) + 7-point 2D Bezier radius (r, z)(t) (curves.BezierRZ) + cubic twist (k1, k2, max) evaluated at the Bezier t of the radius curve: twist(z) = cubic_twist(bz.t(z))
- parameters (15): P0.r, P1..P5 (r, z) = 10, P6.r (P0 z = 0 and P6 z = 190 fixed), k1, k2, max_angle
- start (../FulLTextureLamp/FulLTextureLamp.py, verified): P0 (80, 0), P1 (92.5, 10), P2 (106, 25), P3 (102, 35), P4 (140, 50), P5 (115, 120), P6 (43, 190); k1 0, k2 0.80, max 90
- bounds: r 20..200 mm, inner z 0..190, k1/k2 -1..2, max 45..135 deg; penalty 20*min(diff(z_controls), 0); constraints: bz.monotone(), r0 > 10 mm
- settings (../FulLTextureLamp): N 23, H 2.0 mm (scale_perp 0.20 cm), angle_half placement (generate_polar_triangles_by_count), 30 sections uniform in Bezier t; base = custom spline per the user scenario (script now draws the rose)
- self-test: numpy (kernel) vs pure-Python Bezier/twist at the 30 sections: max diff 5.7e-14 (t-by-height lookup 6.3e-6)
- start values (exact and as built): front 0/19, 3/4 1/19, outline max 19.5 mm, ribs 20.6 mm, 3/4 mean 6.2 mm (start is far from the drawing)
- command: python models/M03_spline_bez2d/model.py (self-test)

### 2026-11-23 22:29 — E0 fit (kernel v1)
- start (as built): front 0/19, 3/4 1/19, ribs 20.62 mm
- result (as built): front 6/19, 3/4 10/19, outline max 1.02, ribs 0.64 mm / 83 %, 3/4 mean 0.76
- exact curves: front 6/19, 3/4 11/19
- 15 params, 25.1 s, nfev 19, cap hit [False, False], constraints OK
- Fusion script: models\M03_spline_bez2d\fusion\M03\M03.py
- command: python models/M03_spline_bez2d/E0_fit/run.py

### 2026-11-23 22:29 — E1 triangle count (kernel v1)
- N=12: front 2/19, 3/4 9/19, outline max 1.49, ribs 0.64 mm (83 %), 3/4 mean 0.90; Δ outline bias mean -0.49 (range -1.26..+0.00), Δ rib mean +0.00 mm
- N=16: front 5/19, 3/4 11/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.77; Δ outline bias mean -0.20 (range -0.52..+0.00), Δ rib mean +0.00 mm
- N=22: front 6/19, 3/4 9/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.78; Δ outline bias mean -0.02 (range -0.09..+0.01), Δ rib mean +0.00 mm
- N=23 (own): front 6/19, 3/4 10/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.76; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 6/19, 3/4 10/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.82; Δ outline bias mean +0.08 (range +0.00..+0.20), Δ rib mean +0.00 mm
- N=45: front 6/19, 3/4 10/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.86; Δ outline bias mean +0.15 (range +0.00..+0.30), Δ rib mean +0.00 mm
- command: python models/M03_spline_bez2d/E1_tri_count/run.py

### 2026-11-23 22:29 — E2 triangle width (fill) x placement (kernel v1)
- arc f=0.5: front 7/19, 3/4 8/19, outline max 0.89, ribs 0.64 mm (83 %), 3/4 mean 0.87; Δ outline bias mean +0.11 (range -0.13..+0.25), Δ rib mean -0.00 mm
- arc f=0.7: front 7/19, 3/4 8/19, outline max 0.86, ribs 0.64 mm (83 %), 3/4 mean 0.85; Δ outline bias mean +0.07 (range -0.16..+0.20), Δ rib mean -0.00 mm
- arc f=0.85: front 7/19, 3/4 10/19, outline max 0.83, ribs 0.64 mm (83 %), 3/4 mean 0.83; Δ outline bias mean +0.03 (range -0.19..+0.16), Δ rib mean -0.00 mm
- arc f=1.0: front 7/19, 3/4 10/19, outline max 0.80, ribs 0.64 mm (83 %), 3/4 mean 0.81; Δ outline bias mean -0.01 (range -0.23..+0.10), Δ rib mean -0.00 mm
- angle_half f=0.5: front 6/19, 3/4 10/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.81; Δ outline bias mean +0.11 (range +0.00..+0.19), Δ rib mean +0.00 mm
- angle_half f=0.7: front 6/19, 3/4 10/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.80; Δ outline bias mean +0.07 (range +0.00..+0.13), Δ rib mean +0.00 mm
- angle_half f=0.85: front 6/19, 3/4 10/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.78; Δ outline bias mean +0.04 (range +0.00..+0.07), Δ rib mean +0.00 mm
- angle_half f=1.0 (own): front 6/19, 3/4 10/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.76; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- command: python models/M03_spline_bez2d/E2_tri_width/run.py

### 2026-11-23 22:29 — E3 triangle height (kernel v1)
- H=1.5: front 3/19, 3/4 12/19, outline max 0.87, ribs 0.64 mm (83 %), 3/4 mean 0.79; Δ outline bias mean -0.50 (range -0.50..-0.50), Δ rib mean +0.00 mm
- H=2.0 (own): front 6/19, 3/4 10/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.76; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=3.0: front 0/19, 3/4 3/19, outline max 2.02, ribs 0.64 mm (83 %), 3/4 mean 1.46; Δ outline bias mean +1.00 (range +1.00..+1.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 0/19, outline max 3.02, ribs 0.64 mm (83 %), 3/4 mean 2.50; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.02, ribs 0.64 mm (83 %), 3/4 mean 3.53; Δ outline bias mean +2.99 (range +2.99..+3.00), Δ rib mean +0.00 mm
- command: python models/M03_spline_bez2d/E3_tri_height/run.py

### 2026-11-23 22:29 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v1)
- twist x0.94: front 2/19, 3/4 4/19, outline max 2.36, ribs 2.17 mm (41 %), 3/4 mean 1.65; Δ outline bias mean -0.26 (range -2.43..+1.93), Δ rib mean +1.87 mm
- twist x0.97: front 4/19, 3/4 6/19, outline max 1.21, ribs 1.24 mm (56 %), 3/4 mean 1.18; Δ outline bias mean -0.13 (range -1.18..+0.98), Δ rib mean +0.72 mm
- twist x1.0: front 6/19, 3/4 10/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.76; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 3/19, 3/4 14/19, outline max 1.56, ribs 1.13 mm (61 %), 3/4 mean 0.84; Δ outline bias mean +0.11 (range -0.99..+1.11), Δ rib mean +0.60 mm
- twist x1.06: front 2/19, 3/4 8/19, outline max 2.66, ribs 1.98 mm (43 %), 3/4 mean 1.20; Δ outline bias mean +0.22 (range -1.68..+2.14), Δ rib mean +1.64 mm
- 1-knot bumps: mean locality share 0.39 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.26 of 1 °
- command: python models/M03_spline_bez2d/E4_twist/run.py

### 2026-11-23 22:29 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v1)
- r0 -2 mm: front 0/19, 3/4 1/19, outline max 2.15, ribs 1.24 mm (57 %), 3/4 mean 1.68; Δ outline bias mean -1.90 (range -2.00..-1.65), Δ rib mean +0.74 mm
- r0 -1 mm: front 0/19, 3/4 6/19, outline max 1.25, ribs 0.89 mm (74 %), 3/4 mean 0.96; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.31 mm
- r0 +0 mm: front 6/19, 3/4 10/19, outline max 1.02, ribs 0.64 mm (83 %), 3/4 mean 0.76; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 4/19, outline max 2.02, ribs 0.71 mm (82 %), 3/4 mean 1.39; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.05 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 3.02, ribs 1.09 mm (57 %), 3/4 mean 2.29; Δ outline bias mean +1.90 (range +1.65..+2.00), Δ rib mean +0.52 mm
- 1-knot bumps: mean locality share 0.40 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.32 of 1 mm
- command: python models/M03_spline_bez2d/E5_radius/run.py

### 2026-11-23 22:29 — E6 sections (count x placement) (kernel v1)
- uniform_z n=8: loft deviation from exact max 0.21 / mean 0.045 mm; front 7/19, 3/4 11/19
- uniform_z n=11: loft deviation from exact max 0.04 / mean 0.007 mm; front 6/19, 3/4 10/19
- uniform_z n=15: loft deviation from exact max 0.03 / mean 0.002 mm; front 6/19, 3/4 10/19
- uniform_z n=20: loft deviation from exact max 0.03 / mean 0.001 mm; front 6/19, 3/4 10/19
- uniform_z n=30: loft deviation from exact max 0.02 / mean 0.001 mm; front 6/19, 3/4 10/19
- uniform_z n=39: loft deviation from exact max 0.01 / mean 0.000 mm; front 6/19, 3/4 10/19
- adaptive n=8: loft deviation from exact max 0.15 / mean 0.038 mm; front 7/19, 3/4 10/19
- adaptive n=11: loft deviation from exact max 0.05 / mean 0.009 mm; front 6/19, 3/4 10/19
- adaptive n=15: loft deviation from exact max 0.03 / mean 0.003 mm; front 6/19, 3/4 10/19
- adaptive n=20: loft deviation from exact max 0.03 / mean 0.001 mm; front 6/19, 3/4 10/19
- adaptive n=30: loft deviation from exact max 0.02 / mean 0.000 mm; front 6/19, 3/4 10/19
- adaptive n=39: loft deviation from exact max 0.01 / mean 0.000 mm; front 6/19, 3/4 10/19
- bezier_t n=8: loft deviation from exact max 0.28 / mean 0.056 mm; front 6/19, 3/4 10/19
- bezier_t n=11: loft deviation from exact max 0.08 / mean 0.015 mm; front 6/19, 3/4 10/19
- bezier_t n=15: loft deviation from exact max 0.04 / mean 0.005 mm; front 6/19, 3/4 10/19
- bezier_t n=20: loft deviation from exact max 0.01 / mean 0.002 mm; front 6/19, 3/4 10/19
- bezier_t n=30: loft deviation from exact max 0.00 / mean 0.000 mm; front 6/19, 3/4 10/19
- bezier_t n=39: loft deviation from exact max 0.00 / mean 0.000 mm; front 6/19, 3/4 10/19
- knots10 n=20: loft deviation from exact max 0.03 / mean 0.001 mm; front 6/19, 3/4 10/19
- own sections: {'mode': 'bezier_t', 'count': 30}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M03_spline_bez2d/E6_sections/run.py

### 2026-11-23 22:30 — summary + conclusions (kernel v1)
- summary.json written (study.write_summary): 15 params, locality 0.40 (twist 0.39, radius 0.40), smoothness score 1.0 (r0 0 / twist 1 inflections), loft_dev_20 0.03 mm, constraints OK, buildable
- MODEL.md conclusions written; limit = cubic twist (ribs fail S09-S19); vs M01: front 6 vs 3/19, 3/4 10 vs 14/19
- Fusion script: models/M03_spline_bez2d/fusion/M03/M03.py (kernel table-driven template, generated by E0, not run)
- no changes to model.py after the first fit; no caps hit; no kernel problems found
- command: python -c "import sys; sys.path.insert(0,'models/_common'); import study; study.write_summary('models/M03_spline_bez2d')"

### 2026-11-23 22:38 — E0 fit (kernel v2)
- start (as built): front 0/19, 3/4 1/19, ribs 20.62 mm
- result (as built): front 14/19, 3/4 13/19, outline max 0.81, ribs 0.48 mm / 92 %, 3/4 mean 0.75
- exact curves: front 14/19, 3/4 13/19
- 15 params, 59.4 s, nfev 19, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 84.6, pool:M01_E0 186.3, pool:M05_E0 84.5, pool:M02_X1c 85.2 -> best: pool:M05_E0
- Fusion script: models\M03_spline_bez2d\fusion\M03\M03.py
- command: python models/M03_spline_bez2d/E0_fit/run.py

### 2026-11-23 22:39 — E1 triangle count (kernel v2)
- N=12: front 6/19, 3/4 8/19, outline max 1.58, ribs 0.48 mm (92 %), 3/4 mean 0.86; Δ outline bias mean -0.49 (range -1.24..+0.00), Δ rib mean +0.00 mm
- N=16: front 11/19, 3/4 10/19, outline max 1.38, ribs 0.48 mm (92 %), 3/4 mean 0.82; Δ outline bias mean -0.20 (range -0.51..+0.00), Δ rib mean +0.00 mm
- N=22: front 14/19, 3/4 12/19, outline max 0.88, ribs 0.48 mm (92 %), 3/4 mean 0.74; Δ outline bias mean -0.02 (range -0.10..+0.02), Δ rib mean +0.00 mm
- N=23 (own): front 14/19, 3/4 13/19, outline max 0.81, ribs 0.48 mm (92 %), 3/4 mean 0.75; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 14/19, 3/4 12/19, outline max 0.81, ribs 0.48 mm (92 %), 3/4 mean 0.76; Δ outline bias mean +0.08 (range +0.00..+0.19), Δ rib mean +0.00 mm
- N=45: front 13/19, 3/4 12/19, outline max 0.81, ribs 0.48 mm (92 %), 3/4 mean 0.80; Δ outline bias mean +0.15 (range +0.00..+0.29), Δ rib mean +0.00 mm
- command: python models/M03_spline_bez2d/E1_tri_count/run.py

### 2026-11-23 22:39 — E2 triangle width (fill) x placement (kernel v2)
- arc f=0.5: front 13/19, 3/4 8/19, outline max 0.73, ribs 0.48 mm (92 %), 3/4 mean 0.84; Δ outline bias mean +0.11 (range -0.13..+0.24), Δ rib mean +0.00 mm
- arc f=0.7: front 13/19, 3/4 10/19, outline max 0.70, ribs 0.48 mm (92 %), 3/4 mean 0.83; Δ outline bias mean +0.07 (range -0.16..+0.19), Δ rib mean +0.00 mm
- arc f=0.85: front 13/19, 3/4 10/19, outline max 0.67, ribs 0.48 mm (92 %), 3/4 mean 0.83; Δ outline bias mean +0.04 (range -0.20..+0.15), Δ rib mean +0.00 mm
- arc f=1.0: front 14/19, 3/4 9/19, outline max 0.70, ribs 0.48 mm (92 %), 3/4 mean 0.82; Δ outline bias mean -0.00 (range -0.24..+0.09), Δ rib mean +0.00 mm
- angle_half f=0.5: front 13/19, 3/4 11/19, outline max 0.81, ribs 0.48 mm (92 %), 3/4 mean 0.79; Δ outline bias mean +0.11 (range +0.00..+0.19), Δ rib mean +0.00 mm
- angle_half f=0.7: front 13/19, 3/4 12/19, outline max 0.81, ribs 0.48 mm (92 %), 3/4 mean 0.78; Δ outline bias mean +0.07 (range +0.00..+0.13), Δ rib mean +0.00 mm
- angle_half f=0.85: front 14/19, 3/4 12/19, outline max 0.81, ribs 0.48 mm (92 %), 3/4 mean 0.78; Δ outline bias mean +0.04 (range +0.00..+0.07), Δ rib mean +0.00 mm
- angle_half f=1.0 (own): front 14/19, 3/4 13/19, outline max 0.81, ribs 0.48 mm (92 %), 3/4 mean 0.75; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- command: python models/M03_spline_bez2d/E2_tri_width/run.py

### 2026-11-23 22:39 — E3 triangle height (kernel v2)
- H=1.5: front 3/19, 3/4 11/19, outline max 1.27, ribs 0.48 mm (92 %), 3/4 mean 0.74; Δ outline bias mean -0.50 (range -0.50..-0.50), Δ rib mean +0.00 mm
- H=2.0 (own): front 14/19, 3/4 13/19, outline max 0.81, ribs 0.48 mm (92 %), 3/4 mean 0.75; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=3.0: front 0/19, 3/4 2/19, outline max 1.81, ribs 0.48 mm (92 %), 3/4 mean 1.37; Δ outline bias mean +1.00 (range +1.00..+1.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 0/19, outline max 2.81, ribs 0.48 mm (92 %), 3/4 mean 2.39; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 3.81, ribs 0.48 mm (92 %), 3/4 mean 3.53; Δ outline bias mean +2.99 (range +2.99..+3.00), Δ rib mean +0.00 mm
- command: python models/M03_spline_bez2d/E3_tri_height/run.py

### 2026-11-23 22:39 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v2)
- twist x0.94: front 3/19, 3/4 3/19, outline max 3.10, ribs 2.08 mm (42 %), 3/4 mean 1.66; Δ outline bias mean -0.27 (range -2.42..+1.87), Δ rib mean +2.02 mm
- twist x0.97: front 4/19, 3/4 5/19, outline max 1.94, ribs 1.13 mm (53 %), 3/4 mean 1.22; Δ outline bias mean -0.14 (range -1.18..+0.95), Δ rib mean +0.83 mm
- twist x1.0: front 14/19, 3/4 13/19, outline max 0.81, ribs 0.48 mm (92 %), 3/4 mean 0.75; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 4/19, 3/4 13/19, outline max 1.29, ribs 1.11 mm (58 %), 3/4 mean 0.74; Δ outline bias mean +0.12 (range -0.99..+1.10), Δ rib mean +0.79 mm
- twist x1.06: front 3/19, 3/4 8/19, outline max 2.28, ribs 2.02 mm (42 %), 3/4 mean 1.18; Δ outline bias mean +0.24 (range -1.78..+2.14), Δ rib mean +1.92 mm
- 1-knot bumps: mean locality share 0.37 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.24 of 1 °
- command: python models/M03_spline_bez2d/E4_twist/run.py

### 2026-11-23 22:39 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v2)
- r0 -2 mm: front 0/19, 3/4 0/19, outline max 2.43, ribs 1.13 mm (55 %), 3/4 mean 1.73; Δ outline bias mean -1.90 (range -2.00..-1.65), Δ rib mean +0.83 mm
- r0 -1 mm: front 0/19, 3/4 9/19, outline max 1.60, ribs 0.73 mm (76 %), 3/4 mean 0.96; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.31 mm
- r0 +0 mm: front 14/19, 3/4 13/19, outline max 0.81, ribs 0.48 mm (92 %), 3/4 mean 0.75; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 4/19, outline max 1.81, ribs 0.71 mm (76 %), 3/4 mean 1.27; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.26 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 2.81, ribs 1.16 mm (54 %), 3/4 mean 2.20; Δ outline bias mean +1.90 (range +1.65..+2.00), Δ rib mean +0.84 mm
- 1-knot bumps: mean locality share 0.39 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.26 of 1 mm
- command: python models/M03_spline_bez2d/E5_radius/run.py

### 2026-11-23 22:39 — E6 sections (count x placement) (kernel v2)
- uniform_z n=8: loft deviation from exact max 0.89 / mean 0.100 mm; front 14/19, 3/4 14/19
- uniform_z n=11: loft deviation from exact max 0.64 / mean 0.047 mm; front 15/19, 3/4 13/19
- uniform_z n=15: loft deviation from exact max 0.47 / mean 0.024 mm; front 15/19, 3/4 12/19
- uniform_z n=20: loft deviation from exact max 0.36 / mean 0.013 mm; front 14/19, 3/4 13/19
- uniform_z n=30: loft deviation from exact max 0.24 / mean 0.006 mm; front 14/19, 3/4 13/19
- uniform_z n=39: loft deviation from exact max 0.19 / mean 0.003 mm; front 14/19, 3/4 13/19
- adaptive n=8: loft deviation from exact max 0.54 / mean 0.091 mm; front 13/19, 3/4 13/19
- adaptive n=11: loft deviation from exact max 0.39 / mean 0.044 mm; front 13/19, 3/4 13/19
- adaptive n=15: loft deviation from exact max 0.27 / mean 0.021 mm; front 14/19, 3/4 13/19
- adaptive n=20: loft deviation from exact max 0.09 / mean 0.007 mm; front 14/19, 3/4 13/19
- adaptive n=30: loft deviation from exact max 0.02 / mean 0.001 mm; front 14/19, 3/4 13/19
- adaptive n=39: loft deviation from exact max 0.01 / mean 0.000 mm; front 14/19, 3/4 13/19
- bezier_t n=8: loft deviation from exact max 0.63 / mean 0.082 mm; front 14/19, 3/4 14/19
- bezier_t n=11: loft deviation from exact max 0.39 / mean 0.032 mm; front 13/19, 3/4 13/19
- bezier_t n=15: loft deviation from exact max 0.24 / mean 0.013 mm; front 14/19, 3/4 13/19
- bezier_t n=20: loft deviation from exact max 0.15 / mean 0.005 mm; front 14/19, 3/4 13/19
- bezier_t n=30: loft deviation from exact max 0.05 / mean 0.001 mm; front 14/19, 3/4 13/19
- bezier_t n=39: loft deviation from exact max 0.02 / mean 0.000 mm; front 14/19, 3/4 13/19
- knots10 n=20: loft deviation from exact max 0.36 / mean 0.013 mm; front 14/19, 3/4 13/19
- own sections: {'mode': 'bezier_t', 'count': 30}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M03_spline_bez2d/E6_sections/run.py

### 2026-11-23 22:41 — conclusions updated for kernel v2 (kernel v2)
- MODEL.md Conclusions rewritten from the v2 results (E0_fit/report.md, E*/summary.md, summary.json, all re-run by the orchestrator); v1 text kept under "Superseded (kernel v1)"; nothing re-run by me
- v2 E0 (as built): front 14/19 (fail S01, S08-S11), 3/4 13/19, outline max 0.81, ribs 0.48 mm / 92 %, 3/4 mean 0.75, cost 84.5, best start pool:M05_E0 (own start 84.6, M02_X1c 85.2, M01_E0 186.3); buildable (best placement at <= 20 sections 0.09 mm)
- main limitation now: twist at the waist S08-S11 (no local twist control, locality 0.37), coupled to the radius through t(z); S01 rim edge fails for every model
- v1 conclusion "t(z) barely changes the twist" is superseded: t leads z/190 in the lower half and front-loads the cubic (36.7 vs 32.3 deg at z 90), worth ~0.6 mm of rib vs M01 (front 14 vs 3/19)
- hypothesis: mostly wrong in M03s favour (expected ~M01 level, 2-5/19)

### 2026-11-23 23:03 — E0 fit (kernel v3)
- start (as built): front 0/19, 3/4 1/19, ribs 20.62 mm
- result (as built): front 14/19, 3/4 14/19, outline max 0.76, ribs 0.43 mm / 92 %, 3/4 mean 0.74
- exact curves: front 14/19, 3/4 13/19
- 16 params, 194.0 s, nfev 14, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 82.2, pool:M01_E0 78.5, pool:M05_E0 73.3, pool:M02_X1c 103.4, pool:M01_E0v2 77.0, pool:M02_E0v2 90.4, pool:M03_E0v2 82.2, pool:M04_E0v2 78.0, pool:M05_E0v2 74.3, pool:M06_E0v2 76.2, pool:M07_E0v2 72.9, pool:M08_E0v2 73.2, pool:M09_E0v2 74.1, pool:M10_E0v2 73.3 -> best: pool:M07_E0v2
- Fusion script: models\M03_spline_bez2d\fusion\M03\M03.py
- command: python models/M03_spline_bez2d/E0_fit/run.py

### 2026-11-23 23:03 — E1 triangle count (kernel v3)
- N=12: front 6/19, 3/4 7/19, outline max 1.57, ribs 0.43 mm (92 %), 3/4 mean 0.97; Δ outline bias mean -0.48 (range -1.23..+0.00), Δ rib mean +0.00 mm
- N=16: front 10/19, 3/4 12/19, outline max 1.35, ribs 0.43 mm (92 %), 3/4 mean 0.83; Δ outline bias mean -0.20 (range -0.50..+0.00), Δ rib mean +0.00 mm
- N=22: front 14/19, 3/4 13/19, outline max 0.87, ribs 0.43 mm (92 %), 3/4 mean 0.75; Δ outline bias mean -0.02 (range -0.10..+0.02), Δ rib mean +0.00 mm
- N=23 (own): front 14/19, 3/4 14/19, outline max 0.76, ribs 0.43 mm (92 %), 3/4 mean 0.74; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 14/19, 3/4 14/19, outline max 0.70, ribs 0.43 mm (92 %), 3/4 mean 0.73; Δ outline bias mean +0.08 (range +0.00..+0.18), Δ rib mean +0.00 mm
- N=45: front 15/19, 3/4 14/19, outline max 0.70, ribs 0.43 mm (92 %), 3/4 mean 0.76; Δ outline bias mean +0.15 (range +0.00..+0.29), Δ rib mean +0.00 mm
- command: python models/M03_spline_bez2d/E1_tri_count/run.py

### 2026-11-23 23:03 — E2 triangle width (fill) x placement (kernel v3)
- arc f=0.5: front 15/19, 3/4 13/19, outline max 0.62, ribs 0.43 mm (92 %), 3/4 mean 0.80; Δ outline bias mean +0.11 (range -0.13..+0.24), Δ rib mean -0.00 mm
- arc f=0.7: front 15/19, 3/4 12/19, outline max 0.59, ribs 0.43 mm (92 %), 3/4 mean 0.79; Δ outline bias mean +0.07 (range -0.17..+0.19), Δ rib mean -0.00 mm
- arc f=0.85: front 14/19, 3/4 12/19, outline max 0.63, ribs 0.43 mm (92 %), 3/4 mean 0.79; Δ outline bias mean +0.04 (range -0.20..+0.14), Δ rib mean -0.00 mm
- arc f=1.0: front 15/19, 3/4 12/19, outline max 0.69, ribs 0.43 mm (92 %), 3/4 mean 0.79; Δ outline bias mean -0.00 (range -0.24..+0.09), Δ rib mean -0.00 mm
- angle_half f=0.5: front 15/19, 3/4 14/19, outline max 0.70, ribs 0.43 mm (92 %), 3/4 mean 0.76; Δ outline bias mean +0.11 (range +0.00..+0.19), Δ rib mean +0.00 mm
- angle_half f=0.7: front 14/19, 3/4 14/19, outline max 0.70, ribs 0.43 mm (92 %), 3/4 mean 0.75; Δ outline bias mean +0.07 (range +0.00..+0.13), Δ rib mean +0.00 mm
- angle_half f=0.85: front 14/19, 3/4 14/19, outline max 0.70, ribs 0.43 mm (92 %), 3/4 mean 0.75; Δ outline bias mean +0.04 (range +0.00..+0.07), Δ rib mean +0.00 mm
- angle_half f=1.0 (own): front 14/19, 3/4 14/19, outline max 0.76, ribs 0.43 mm (92 %), 3/4 mean 0.74; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- command: python models/M03_spline_bez2d/E2_tri_width/run.py

### 2026-11-23 23:03 — E3 triangle height (kernel v3)
- H=1.5: front 2/19, 3/4 10/19, outline max 1.26, ribs 0.43 mm (92 %), 3/4 mean 0.83; Δ outline bias mean -0.50 (range -0.50..-0.50), Δ rib mean +0.00 mm
- H=2.0 (own): front 14/19, 3/4 14/19, outline max 0.76, ribs 0.43 mm (92 %), 3/4 mean 0.74; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=3.0: front 0/19, 3/4 2/19, outline max 1.70, ribs 0.43 mm (92 %), 3/4 mean 1.30; Δ outline bias mean +1.00 (range +1.00..+1.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 0/19, outline max 2.70, ribs 0.43 mm (92 %), 3/4 mean 2.28; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 3.70, ribs 0.43 mm (92 %), 3/4 mean 3.32; Δ outline bias mean +2.99 (range +2.99..+3.00), Δ rib mean +0.00 mm
- command: python models/M03_spline_bez2d/E3_tri_height/run.py

### 2026-11-23 23:03 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v3)
- twist x0.94: front 3/19, 3/4 3/19, outline max 3.08, ribs 2.03 mm (40 %), 3/4 mean 1.63; Δ outline bias mean -0.27 (range -2.43..+1.87), Δ rib mean +2.04 mm
- twist x0.97: front 5/19, 3/4 3/19, outline max 1.92, ribs 1.08 mm (52 %), 3/4 mean 1.16; Δ outline bias mean -0.13 (range -1.18..+0.94), Δ rib mean +0.84 mm
- twist x1.0: front 14/19, 3/4 14/19, outline max 0.76, ribs 0.43 mm (92 %), 3/4 mean 0.74; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 4/19, 3/4 11/19, outline max 1.12, ribs 1.06 mm (57 %), 3/4 mean 0.93; Δ outline bias mean +0.12 (range -0.99..+1.11), Δ rib mean +0.81 mm
- twist x1.06: front 3/19, 3/4 8/19, outline max 2.05, ribs 1.98 mm (44 %), 3/4 mean 1.29; Δ outline bias mean +0.24 (range -1.81..+2.15), Δ rib mean +1.95 mm
- 1-knot bumps: mean locality share 0.42 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.30 of 1 °
- command: python models/M03_spline_bez2d/E4_twist/run.py

### 2026-11-23 23:03 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v3)
- r0 -2 mm: front 0/19, 3/4 1/19, outline max 2.41, ribs 1.10 mm (56 %), 3/4 mean 1.94; Δ outline bias mean -1.90 (range -2.00..-1.65), Δ rib mean +0.86 mm
- r0 -1 mm: front 0/19, 3/4 4/19, outline max 1.59, ribs 0.69 mm (74 %), 3/4 mean 1.11; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.33 mm
- r0 +0 mm: front 14/19, 3/4 14/19, outline max 0.76, ribs 0.43 mm (92 %), 3/4 mean 0.74; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 5/19, outline max 1.70, ribs 0.67 mm (74 %), 3/4 mean 1.19; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.30 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 2.70, ribs 1.12 mm (58 %), 3/4 mean 2.07; Δ outline bias mean +1.90 (range +1.65..+2.00), Δ rib mean +0.88 mm
- 1-knot bumps: mean locality share 0.41 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.30 of 1 mm
- command: python models/M03_spline_bez2d/E5_radius/run.py

### 2026-11-23 23:03 — E6 sections (count x placement) (kernel v3)
- uniform_z n=8: loft deviation from exact max 0.30 / mean 0.072 mm; front 15/19, 3/4 14/19
- uniform_z n=11: loft deviation from exact max 0.09 / mean 0.016 mm; front 14/19, 3/4 14/19
- uniform_z n=15: loft deviation from exact max 0.03 / mean 0.003 mm; front 14/19, 3/4 14/19
- uniform_z n=20: loft deviation from exact max 0.01 / mean 0.001 mm; front 14/19, 3/4 14/19
- uniform_z n=30: loft deviation from exact max 0.00 / mean 0.000 mm; front 14/19, 3/4 14/19
- uniform_z n=39: loft deviation from exact max 0.00 / mean 0.000 mm; front 14/19, 3/4 14/19
- adaptive n=8: loft deviation from exact max 0.23 / mean 0.057 mm; front 15/19, 3/4 13/19
- adaptive n=11: loft deviation from exact max 0.14 / mean 0.022 mm; front 14/19, 3/4 14/19
- adaptive n=15: loft deviation from exact max 0.05 / mean 0.006 mm; front 14/19, 3/4 14/19
- adaptive n=20: loft deviation from exact max 0.02 / mean 0.001 mm; front 14/19, 3/4 14/19
- adaptive n=30: loft deviation from exact max 0.00 / mean 0.000 mm; front 14/19, 3/4 14/19
- adaptive n=39: loft deviation from exact max 0.00 / mean 0.000 mm; front 14/19, 3/4 14/19
- bezier_t n=8: loft deviation from exact max 0.29 / mean 0.071 mm; front 15/19, 3/4 14/19
- bezier_t n=11: loft deviation from exact max 0.09 / mean 0.018 mm; front 14/19, 3/4 14/19
- bezier_t n=15: loft deviation from exact max 0.03 / mean 0.004 mm; front 14/19, 3/4 14/19
- bezier_t n=20: loft deviation from exact max 0.01 / mean 0.001 mm; front 14/19, 3/4 14/19
- bezier_t n=30: loft deviation from exact max 0.00 / mean 0.000 mm; front 14/19, 3/4 14/19
- bezier_t n=39: loft deviation from exact max 0.00 / mean 0.000 mm; front 14/19, 3/4 14/19
- knots10 n=20: loft deviation from exact max 0.01 / mean 0.001 mm; front 14/19, 3/4 14/19
- own sections: {'mode': 'bezier_t', 'count': 30}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M03_spline_bez2d/E6_sections/run.py

### 2026-11-23 23:14 — final round (kernel v3) — results recorded (kernel v3)
- rank 1/10, score 0.706; front 14/19, 3/4 14/19, ribs 0.43 mm, cost 72.9 (best start pool:M07_E0v2)
- orientation offset -1.33°; MODEL.md: 'Final round — kernel v3' section appended; verified by judge/verify_e0.py

### 2026-11-23 23:32 — Fusion build F2-1 verified (kernel v3)
- generated script built in Fusion by the user (23 bodies); DumpCanvas outline vs kernel as built: mean 0.003 / max 0.007 mm -> buildability confirmed

### 2026-11-23 23:33 — made the ACTIVE model (kernel v3)
- chosen by the user 2026-11-24 (rank 1); ACTIVE_MODEL.json points here; previous active fit (M05) backed up in work/history/
