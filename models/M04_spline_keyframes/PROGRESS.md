# M04_spline_keyframes — progress

## Status  (overwrite this block only)
- State: final (kernel v3), rank 5/10
- Best E0 (as built): front 10/19, 3/4 13/19, 22 params, score 0.592
- Next: none (study complete)

## Log  (append only, newest at the bottom)

### 2026-11-23 22:29 — model created (kernel v1)
- model.py: custom spline base (fixed, bases.custom_spline) + radius keys (t, r) + twist keys (t, deg) at the same t, Catmull-Rom (curves.catmull_keys), t = z/190
- parameters: 11 radius keys + 10 twist keys (twist at t = 0 fixed 0) = 21 at the start; +2 per refinement key, max 20 keys (39 params)
- start: ../BaseScript bez_points (81, 98, 109, 114, 114.2, 110.4, 103.2, 92.4, 78.4, 62, 44) and angle_points (0, 2.2, 8.26, 17.2, 28.2, 40.3, 52.6, 64.4, 74.8, 82.6, 90), verified in BaseScript.py run()
- bounds: r 20..200 mm, twist -30..150 deg; penalty SMOOTH_W mm/deg x 2nd difference over the key sequence
- settings from ../BaseScript: N 22, H 2.4, angle_half placement, sections = list on the keys (11 at start = M01 uniform 11)
- refinement: model.refine() hook for study.run_E0; keys.json in E0_fit/, loaded at import; E0_fit/run.py sets M04_BASE_KEYS=1 to always restart from 11 keys
- self-test (pure-Python Catmull-Rom vs numpy, 1901 heights): max diff 1.4e-14 (radius and twist)
- start (P0) evaluated: exact front 1/19, 3/4 11/19, ribs 1.64 mm; as built front 2/19, 3/4 11/19, ribs 1.63 mm
- MODEL.md hypothesis written before any fit

### 2026-11-23 22:30 — E0 refinement round 0 (first fit, 11 keys) (kernel v1)
- as built: front 3/19, 3/4 10/19, outline max 2.28, ribs 0.71 mm / 78 %, 3/4 mean 0.99
- nfev 13, cap hit [False, False]

### 2026-11-23 22:30 — E0 refinement round 1: key added at z = 155 mm (S16) (kernel v1)
- target S16 rib_mean: 1.36 → 1.46 mm (gain -0.09, threshold 0.1)
- keys 11 → 12; as built: front 3/19, 3/4 6/19, outline max 2.84, ribs 0.70 mm / 80 %, 3/4 mean 1.13
- nfev 17, cap hit [False, False]
- gain ≤ 0.1 mm → key removed, refinement stops (previous key set is final)

### 2026-11-23 22:30 — E0 fit (kernel v1)
- start (as built): front 2/19, 3/4 11/19, ribs 1.63 mm
- result (as built): front 3/19, 3/4 10/19, outline max 2.28, ribs 0.71 mm / 78 %, 3/4 mean 0.99
- exact curves: front 3/19, 3/4 7/19
- 21 params, 45.3 s, nfev 13, cap hit [False, False], constraints OK
- Fusion script: models\M04_spline_keyframes\fusion\M04\M04.py
- command: python models/M04_spline_keyframes/E0_fit/run.py

### 2026-11-23 22:32 — E0 review + diagnostics (not part of the result) (kernel v1)
- refinement: 1 round; key at z = 155 (S16, worst rib 1.36 mm) made S16 worse (1.36 → 1.46) and 3/4 6/19 → rule stops, key removed; final model = 11 keys, 21 params
- optimiser: stage 1 ends on xtol (status 3) at nfev 19 with first-order optimality 6.1e3, i.e. trust region collapses on the non-smooth rib/visibility residuals; cap not hit. Same for every model (kernel protocol), not changed
- check 1: M01 E0 curves sampled onto the 11 M04 keys → soft_l1 cost 212.9; refit from there → 209.9 (M04 E0: 210.0; M01 own: 198.2). Same basin, the extra twist freedom buys nothing
- check 2 (probe, upper bound of the refinement rule): 20 keys on the 10 mm grid (0,10..180,190), refit from E0 → cost 183.0, as built front 4/19, 3/4 13/19, ribs 0.70 mm; S12–S19 ribs still 1.07–1.25 mm
- → the rib errors in S09–S19 are not a key-density problem; the fixed custom-spline base is the limit (same S12–S19 ribs 1.2–1.3 as M01)
- model.py unchanged; command for the probes: inline python (study.fit on model._set_keys(...)), results only in this log

### 2026-11-23 22:32 — E1 triangle count (kernel v1)
- N=12: front 1/19, 3/4 6/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 1.34; Δ outline bias mean -0.47 (range -1.21..+0.00), Δ rib mean +0.00 mm
- N=16: front 2/19, 3/4 8/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 1.15; Δ outline bias mean -0.19 (range -0.50..+0.00), Δ rib mean +0.00 mm
- N=22 (own): front 3/19, 3/4 10/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 3/19, 3/4 10/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 0.99; Δ outline bias mean +0.10 (range +0.00..+0.22), Δ rib mean +0.00 mm
- N=45: front 2/19, 3/4 11/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 1.01; Δ outline bias mean +0.17 (range +0.00..+0.31), Δ rib mean +0.00 mm
- command: python models/M04_spline_keyframes/E1_tri_count/run.py

### 2026-11-23 22:32 — E2 triangle width (fill) x placement (kernel v1)
- arc f=0.5: front 2/19, 3/4 11/19, outline max 2.13, ribs 0.71 mm (78 %), 3/4 mean 0.98; Δ outline bias mean +0.13 (range -0.16..+0.30), Δ rib mean -0.00 mm
- arc f=0.7: front 3/19, 3/4 11/19, outline max 2.09, ribs 0.71 mm (78 %), 3/4 mean 0.97; Δ outline bias mean +0.09 (range -0.19..+0.25), Δ rib mean -0.00 mm
- arc f=0.85: front 3/19, 3/4 11/19, outline max 2.06, ribs 0.71 mm (78 %), 3/4 mean 0.96; Δ outline bias mean +0.05 (range -0.22..+0.20), Δ rib mean -0.00 mm
- arc f=1.0: front 3/19, 3/4 11/19, outline max 2.02, ribs 0.71 mm (78 %), 3/4 mean 0.98; Δ outline bias mean +0.00 (range -0.26..+0.14), Δ rib mean -0.00 mm
- angle_half f=0.5: front 2/19, 3/4 10/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 1.01; Δ outline bias mean +0.12 (range +0.00..+0.21), Δ rib mean +0.00 mm
- angle_half f=0.7: front 3/19, 3/4 10/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 1.00; Δ outline bias mean +0.08 (range +0.00..+0.14), Δ rib mean +0.00 mm
- angle_half f=0.85: front 3/19, 3/4 10/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 1.00; Δ outline bias mean +0.04 (range +0.00..+0.08), Δ rib mean +0.00 mm
- angle_half f=1.0 (own): front 3/19, 3/4 10/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- command: python models/M04_spline_keyframes/E2_tri_width/run.py

### 2026-11-23 22:32 — E3 triangle height (kernel v1)
- H=1.5: front 1/19, 3/4 6/19, outline max 1.38, ribs 0.71 mm (78 %), 3/4 mean 1.25; Δ outline bias mean -0.90 (range -0.90..-0.90), Δ rib mean +0.00 mm
- H=2.0: front 3/19, 3/4 9/19, outline max 1.88, ribs 0.71 mm (78 %), 3/4 mean 1.09; Δ outline bias mean -0.40 (range -0.40..-0.40), Δ rib mean +0.00 mm
- H=2.4 (own): front 3/19, 3/4 10/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=3.0: front 0/19, 3/4 9/19, outline max 2.88, ribs 0.71 mm (78 %), 3/4 mean 1.20; Δ outline bias mean +0.60 (range +0.60..+0.60), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 2/19, outline max 3.88, ribs 0.71 mm (78 %), 3/4 mean 2.07; Δ outline bias mean +1.60 (range +1.59..+1.60), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.88, ribs 0.71 mm (78 %), 3/4 mean 3.05; Δ outline bias mean +2.60 (range +2.59..+2.60), Δ rib mean +0.00 mm
- command: python models/M04_spline_keyframes/E3_tri_height/run.py

### 2026-11-23 22:32 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v1)
- twist x0.94: front 1/19, 3/4 5/19, outline max 2.31, ribs 2.27 mm (41 %), 3/4 mean 1.55; Δ outline bias mean -0.26 (range -2.31..+1.98), Δ rib mean +1.97 mm
- twist x0.97: front 2/19, 3/4 6/19, outline max 2.28, ribs 1.32 mm (53 %), 3/4 mean 1.13; Δ outline bias mean -0.13 (range -1.12..+1.00), Δ rib mean +0.77 mm
- twist x1.0: front 3/19, 3/4 10/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 2/19, 3/4 7/19, outline max 2.28, ribs 1.14 mm (57 %), 3/4 mean 1.41; Δ outline bias mean +0.12 (range -0.92..+1.12), Δ rib mean +0.52 mm
- twist x1.06: front 1/19, 3/4 3/19, outline max 3.11, ribs 1.82 mm (48 %), 3/4 mean 1.84; Δ outline bias mean +0.23 (range -1.64..+2.30), Δ rib mean +1.34 mm
- 1-knot bumps: mean locality share 0.59 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.47 of 1 °
- command: python models/M04_spline_keyframes/E4_twist/run.py

### 2026-11-23 22:32 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v1)
- r0 -2 mm: front 1/19, 3/4 0/19, outline max 2.15, ribs 1.29 mm (65 %), 3/4 mean 1.90; Δ outline bias mean -1.90 (range -2.00..-1.66), Δ rib mean +0.72 mm
- r0 -1 mm: front 1/19, 3/4 6/19, outline max 1.28, ribs 0.89 mm (77 %), 3/4 mean 1.26; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.23 mm
- r0 +0 mm: front 3/19, 3/4 10/19, outline max 2.28, ribs 0.71 mm (78 %), 3/4 mean 0.99; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 8/19, outline max 3.28, ribs 0.74 mm (76 %), 3/4 mean 1.43; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.00 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.28, ribs 0.93 mm (64 %), 3/4 mean 2.26; Δ outline bias mean +1.90 (range +1.66..+2.00), Δ rib mean +0.21 mm
- 1-knot bumps: mean locality share 0.63 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.49 of 1 mm
- command: python models/M04_spline_keyframes/E5_radius/run.py

### 2026-11-23 22:32 — E6 sections (count x placement) (kernel v1)
- uniform_z n=8: loft deviation from exact max 1.73 / mean 0.247 mm; front 3/19, 3/4 12/19
- uniform_z n=11: loft deviation from exact max 1.88 / mean 0.200 mm; front 3/19, 3/4 10/19
- uniform_z n=15: loft deviation from exact max 1.11 / mean 0.141 mm; front 4/19, 3/4 9/19
- uniform_z n=20: loft deviation from exact max 0.26 / mean 0.046 mm; front 4/19, 3/4 8/19
- uniform_z n=30: loft deviation from exact max 0.09 / mean 0.010 mm; front 3/19, 3/4 9/19
- uniform_z n=39: loft deviation from exact max 0.05 / mean 0.003 mm; front 3/19, 3/4 9/19
- adaptive n=8: loft deviation from exact max 1.79 / mean 0.259 mm; front 1/19, 3/4 13/19
- adaptive n=11: loft deviation from exact max 1.53 / mean 0.205 mm; front 4/19, 3/4 9/19
- adaptive n=15: loft deviation from exact max 0.52 / mean 0.102 mm; front 4/19, 3/4 8/19
- adaptive n=20: loft deviation from exact max 0.05 / mean 0.013 mm; front 3/19, 3/4 9/19
- adaptive n=30: loft deviation from exact max 0.06 / mean 0.007 mm; front 3/19, 3/4 9/19
- adaptive n=39: loft deviation from exact max 0.05 / mean 0.004 mm; front 3/19, 3/4 9/19
- knots10 n=20: loft deviation from exact max 0.26 / mean 0.046 mm; front 4/19, 3/4 8/19
- own sections: {'mode': 'list', 'z': [0.0, 19.0, 38.0, 57.0, 76.0, 95.0, 114.0, 133.0, 152.0, 171.0, 190.0]}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M04_spline_keyframes/E6_sections/run.py

### 2026-11-23 22:32 — summary + conclusions (kernel v1)
- study.write_summary → summary.json: 21 params, locality 0.61 (twist 0.59, radius 0.63), smoothness 1.0 (2 r0 / 1 twist inflections), loft dev at 20 uniform sections 0.26 mm, buildable, constraints OK
- MODEL.md conclusions written (hypothesis section unchanged)
- Fusion script (generated, not run): models/M04_spline_keyframes/fusion/M04/M04.py, 11 sections on the keys
- command: python -c "import sys; sys.path.insert(0,'models/_common'); import study; study.write_summary('models/M04_spline_keyframes')"

### 2026-11-23 22:38 — E0 refinement round 0 (first fit, 11 keys) (kernel v2)
- as built: front 3/19, 3/4 13/19, outline max 2.33, ribs 0.72 mm / 78 %, 3/4 mean 0.81
- nfev 15, cap hit [False, False, False]

### 2026-11-23 22:38 — E0 refinement round 1: key added at z = 125 mm (S13) (kernel v2)
- target S13 rib_mean: 1.35 → 1.28 mm (gain +0.07, threshold 0.1)
- keys 11 → 12; as built: front 3/19, 3/4 13/19, outline max 2.32, ribs 0.72 mm / 77 %, 3/4 mean 0.80
- nfev 23, cap hit [False, False, False]
- gain ≤ 0.1 mm → key removed, refinement stops (previous key set is final)

### 2026-11-23 22:38 — E0 fit (kernel v2)
- start (as built): front 2/19, 3/4 11/19, ribs 1.63 mm
- result (as built): front 3/19, 3/4 13/19, outline max 2.33, ribs 0.72 mm / 78 %, 3/4 mean 0.81
- exact curves: front 4/19, 3/4 13/19
- 21 params, 53.6 s, nfev 15, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 209.6, pool:M01_E0 209.5, pool:M05_E0 210.1, pool:M02_X1c 209.7 -> best: pool:M01_E0
- Fusion script: models\M04_spline_keyframes\fusion\M04\M04.py
- command: python models/M04_spline_keyframes/E0_fit/run.py

### 2026-11-23 22:39 — E1 triangle count (kernel v2)
- N=12: front 1/19, 3/4 8/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.89; Δ outline bias mean -0.47 (range -1.21..+0.00), Δ rib mean +0.00 mm
- N=16: front 2/19, 3/4 12/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.83; Δ outline bias mean -0.19 (range -0.51..+0.00), Δ rib mean +0.00 mm
- N=22 (own): front 3/19, 3/4 13/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.81; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 3/19, 3/4 12/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.88; Δ outline bias mean +0.10 (range +0.00..+0.22), Δ rib mean +0.00 mm
- N=45: front 1/19, 3/4 9/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.96; Δ outline bias mean +0.17 (range +0.00..+0.31), Δ rib mean +0.00 mm
- command: python models/M04_spline_keyframes/E1_tri_count/run.py

### 2026-11-23 22:39 — E2 triangle width (fill) x placement (kernel v2)
- arc f=0.5: front 1/19, 3/4 10/19, outline max 2.17, ribs 0.72 mm (78 %), 3/4 mean 0.92; Δ outline bias mean +0.13 (range -0.16..+0.29), Δ rib mean +0.00 mm
- arc f=0.7: front 3/19, 3/4 10/19, outline max 2.14, ribs 0.72 mm (78 %), 3/4 mean 0.89; Δ outline bias mean +0.09 (range -0.19..+0.24), Δ rib mean +0.00 mm
- arc f=0.85: front 3/19, 3/4 11/19, outline max 2.11, ribs 0.72 mm (78 %), 3/4 mean 0.87; Δ outline bias mean +0.05 (range -0.23..+0.20), Δ rib mean +0.00 mm
- arc f=1.0: front 3/19, 3/4 14/19, outline max 2.07, ribs 0.72 mm (78 %), 3/4 mean 0.84; Δ outline bias mean -0.00 (range -0.27..+0.14), Δ rib mean +0.00 mm
- angle_half f=0.5: front 1/19, 3/4 13/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.88; Δ outline bias mean +0.12 (range +0.00..+0.21), Δ rib mean +0.00 mm
- angle_half f=0.7: front 3/19, 3/4 13/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.85; Δ outline bias mean +0.08 (range +0.00..+0.14), Δ rib mean +0.00 mm
- angle_half f=0.85: front 3/19, 3/4 13/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.83; Δ outline bias mean +0.04 (range +0.00..+0.08), Δ rib mean +0.00 mm
- angle_half f=1.0 (own): front 3/19, 3/4 13/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.81; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- command: python models/M04_spline_keyframes/E2_tri_width/run.py

### 2026-11-23 22:39 — E3 triangle height (kernel v2)
- H=1.5: front 1/19, 3/4 12/19, outline max 1.43, ribs 0.72 mm (78 %), 3/4 mean 0.78; Δ outline bias mean -0.90 (range -0.90..-0.90), Δ rib mean +0.00 mm
- H=2.0: front 3/19, 3/4 14/19, outline max 1.93, ribs 0.72 mm (78 %), 3/4 mean 0.68; Δ outline bias mean -0.40 (range -0.40..-0.40), Δ rib mean +0.00 mm
- H=2.4 (own): front 3/19, 3/4 13/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.81; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=3.0: front 0/19, 3/4 4/19, outline max 2.93, ribs 0.72 mm (78 %), 3/4 mean 1.31; Δ outline bias mean +0.60 (range +0.60..+0.60), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 0/19, outline max 3.93, ribs 0.72 mm (78 %), 3/4 mean 2.31; Δ outline bias mean +1.60 (range +1.59..+1.60), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.93, ribs 0.72 mm (78 %), 3/4 mean 3.47; Δ outline bias mean +2.60 (range +2.59..+2.60), Δ rib mean +0.00 mm
- command: python models/M04_spline_keyframes/E3_tri_height/run.py

### 2026-11-23 22:39 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v2)
- twist x0.94: front 1/19, 3/4 4/19, outline max 2.33, ribs 2.28 mm (41 %), 3/4 mean 1.73; Δ outline bias mean -0.26 (range -2.31..+1.98), Δ rib mean +1.97 mm
- twist x0.97: front 2/19, 3/4 5/19, outline max 2.33, ribs 1.33 mm (53 %), 3/4 mean 1.21; Δ outline bias mean -0.13 (range -1.12..+1.00), Δ rib mean +0.77 mm
- twist x1.0: front 3/19, 3/4 13/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.81; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 2/19, 3/4 7/19, outline max 2.33, ribs 1.16 mm (58 %), 3/4 mean 1.05; Δ outline bias mean +0.12 (range -0.92..+1.11), Δ rib mean +0.52 mm
- twist x1.06: front 1/19, 3/4 4/19, outline max 3.09, ribs 1.84 mm (48 %), 3/4 mean 1.47; Δ outline bias mean +0.23 (range -1.64..+2.29), Δ rib mean +1.34 mm
- 1-knot bumps: mean locality share 0.59 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.47 of 1 °
- command: python models/M04_spline_keyframes/E4_twist/run.py

### 2026-11-23 22:39 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v2)
- r0 -2 mm: front 0/19, 3/4 1/19, outline max 2.14, ribs 1.29 mm (65 %), 3/4 mean 1.41; Δ outline bias mean -1.90 (range -2.00..-1.66), Δ rib mean +0.71 mm
- r0 -1 mm: front 1/19, 3/4 8/19, outline max 1.33, ribs 0.90 mm (76 %), 3/4 mean 0.81; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.22 mm
- r0 +0 mm: front 3/19, 3/4 13/19, outline max 2.33, ribs 0.72 mm (78 %), 3/4 mean 0.81; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 0/19, outline max 3.33, ribs 0.75 mm (75 %), 3/4 mean 1.60; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.01 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.33, ribs 0.95 mm (64 %), 3/4 mean 2.54; Δ outline bias mean +1.90 (range +1.66..+2.00), Δ rib mean +0.22 mm
- 1-knot bumps: mean locality share 0.63 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.49 of 1 mm
- command: python models/M04_spline_keyframes/E5_radius/run.py

### 2026-11-23 22:39 — E6 sections (count x placement) (kernel v2)
- uniform_z n=8: loft deviation from exact max 1.72 / mean 0.239 mm; front 3/19, 3/4 14/19
- uniform_z n=11: loft deviation from exact max 1.80 / mean 0.195 mm; front 3/19, 3/4 13/19
- uniform_z n=15: loft deviation from exact max 1.07 / mean 0.137 mm; front 4/19, 3/4 13/19
- uniform_z n=20: loft deviation from exact max 0.25 / mean 0.046 mm; front 4/19, 3/4 13/19
- uniform_z n=30: loft deviation from exact max 0.09 / mean 0.010 mm; front 4/19, 3/4 13/19
- uniform_z n=39: loft deviation from exact max 0.05 / mean 0.003 mm; front 4/19, 3/4 13/19
- adaptive n=8: loft deviation from exact max 1.75 / mean 0.247 mm; front 2/19, 3/4 13/19
- adaptive n=11: loft deviation from exact max 1.50 / mean 0.199 mm; front 4/19, 3/4 13/19
- adaptive n=15: loft deviation from exact max 0.51 / mean 0.103 mm; front 4/19, 3/4 13/19
- adaptive n=20: loft deviation from exact max 0.05 / mean 0.013 mm; front 4/19, 3/4 13/19
- adaptive n=30: loft deviation from exact max 0.06 / mean 0.007 mm; front 4/19, 3/4 13/19
- adaptive n=39: loft deviation from exact max 0.05 / mean 0.004 mm; front 4/19, 3/4 13/19
- knots10 n=20: loft deviation from exact max 0.25 / mean 0.046 mm; front 4/19, 3/4 13/19
- own sections: {'mode': 'list', 'z': [0.0, 19.0, 38.0, 57.0, 76.0, 95.0, 114.0, 133.0, 152.0, 171.0, 190.0]}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M04_spline_keyframes/E6_sections/run.py

### 2026-11-23 22:42 — conclusions updated for kernel v2 (kernel v2)
- read the v2 results (coordinator re-ran E0 incl. refinement + E1–E6 + summary): front 3/19, 3/4 13/19, ribs 0.72 mm, cost 209.5 (all 4 starts 209.5–210.1)
- refinement under v2: 1 round, key at z = 125 (S13) gave 1.35 → 1.28 mm (gain 0.07 ≤ 0.1) → removed; keys added 0; keys.json = 11 historical keys
- read-only cost checks (no fit, nothing written): M02 v2 E0 curves under M04 settings 147.3; M04 E0 curves + constant twist offset 0 / -0.5 / -1 / -1.5 / -2 deg → 209.2 / 165.8 / 148.6 / 157.9 / 219.8; M02 twist sampled on 11 (20) M04 keys misses its rim drop by 1.78 (1.33) deg → cost 715 (598)
- CORRECTION of the v1 conclusion: the base is NOT the limit (same base: M02 12/19). The limit is the twist basin: M04 lacks a global rotation (twist(0) fixed at 0), and fit + refinement never find the -1 deg offset
- MODEL.md: new Conclusions (kernel v2); v1 text kept under "Superseded (kernel v1)"; hypothesis unchanged
- open for the orchestrator: free twist at t = 0 / global rotation parameter, or a pool start with -1 deg offset (spec change, not done)

### 2026-11-23 23:02 — E0 fit (kernel v3)
- start (as built): front 2/19, 3/4 11/19, ribs 1.63 mm
- result (as built): front 10/19, 3/4 13/19, outline max 2.07, ribs 0.44 mm / 93 %, 3/4 mean 0.82
- exact curves: front 12/19, 3/4 11/19
- 22 params, 167.9 s, nfev 18, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 91.1, pool:M01_E0 91.0, pool:M05_E0 90.9, pool:M02_X1c 90.9, pool:M01_E0v2 91.0, pool:M02_E0v2 90.9, pool:M03_E0v2 90.7, pool:M04_E0v2 91.1, pool:M05_E0v2 91.0, pool:M06_E0v2 91.0, pool:M07_E0v2 90.9, pool:M08_E0v2 90.8, pool:M09_E0v2 90.9, pool:M10_E0v2 90.9 -> best: pool:M03_E0v2
- Fusion script: models\M04_spline_keyframes\fusion\M04\M04.py
- command: python models/M04_spline_keyframes/E0_fit/run.py

### 2026-11-23 23:03 — E1 triangle count (kernel v3)
- N=12: front 2/19, 3/4 8/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.98; Δ outline bias mean -0.46 (range -1.22..+0.00), Δ rib mean +0.00 mm
- N=16: front 6/19, 3/4 12/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.87; Δ outline bias mean -0.18 (range -0.52..+0.00), Δ rib mean +0.00 mm
- N=22 (own): front 10/19, 3/4 13/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.82; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 10/19, 3/4 13/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.86; Δ outline bias mean +0.10 (range +0.00..+0.22), Δ rib mean +0.00 mm
- N=45: front 10/19, 3/4 11/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.86; Δ outline bias mean +0.17 (range +0.00..+0.32), Δ rib mean +0.00 mm
- command: python models/M04_spline_keyframes/E1_tri_count/run.py

### 2026-11-23 23:03 — E2 triangle width (fill) x placement (kernel v3)
- arc f=0.5: front 10/19, 3/4 11/19, outline max 2.00, ribs 0.44 mm (93 %), 3/4 mean 0.87; Δ outline bias mean +0.12 (range -0.15..+0.32), Δ rib mean -0.00 mm
- arc f=0.7: front 11/19, 3/4 12/19, outline max 1.97, ribs 0.44 mm (93 %), 3/4 mean 0.86; Δ outline bias mean +0.08 (range -0.19..+0.27), Δ rib mean -0.00 mm
- arc f=0.85: front 11/19, 3/4 11/19, outline max 1.93, ribs 0.44 mm (93 %), 3/4 mean 0.86; Δ outline bias mean +0.04 (range -0.22..+0.22), Δ rib mean -0.00 mm
- arc f=1.0: front 12/19, 3/4 12/19, outline max 1.90, ribs 0.44 mm (93 %), 3/4 mean 0.84; Δ outline bias mean -0.00 (range -0.27..+0.16), Δ rib mean -0.00 mm
- angle_half f=0.5: front 10/19, 3/4 13/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.86; Δ outline bias mean +0.12 (range +0.00..+0.21), Δ rib mean +0.00 mm
- angle_half f=0.7: front 10/19, 3/4 14/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.84; Δ outline bias mean +0.08 (range +0.00..+0.14), Δ rib mean +0.00 mm
- angle_half f=0.85: front 10/19, 3/4 13/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.84; Δ outline bias mean +0.04 (range +0.00..+0.08), Δ rib mean +0.00 mm
- angle_half f=1.0 (own): front 10/19, 3/4 13/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.82; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- command: python models/M04_spline_keyframes/E2_tri_width/run.py

### 2026-11-23 23:03 — E3 triangle height (kernel v3)
- H=1.5: front 2/19, 3/4 8/19, outline max 1.69, ribs 0.44 mm (93 %), 3/4 mean 0.98; Δ outline bias mean -0.90 (range -0.90..-0.90), Δ rib mean +0.00 mm
- H=2.0: front 5/19, 3/4 11/19, outline max 1.67, ribs 0.44 mm (93 %), 3/4 mean 0.81; Δ outline bias mean -0.40 (range -0.40..-0.40), Δ rib mean +0.00 mm
- H=2.4 (own): front 10/19, 3/4 13/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.82; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=3.0: front 1/19, 3/4 4/19, outline max 2.67, ribs 0.44 mm (93 %), 3/4 mean 1.13; Δ outline bias mean +0.60 (range +0.60..+0.60), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 0/19, outline max 3.67, ribs 0.44 mm (93 %), 3/4 mean 2.07; Δ outline bias mean +1.60 (range +1.59..+1.60), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.67, ribs 0.44 mm (93 %), 3/4 mean 3.13; Δ outline bias mean +2.60 (range +2.59..+2.60), Δ rib mean +0.00 mm
- command: python models/M04_spline_keyframes/E3_tri_height/run.py

### 2026-11-23 23:03 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v3)
- twist x0.94: front 1/19, 3/4 3/19, outline max 3.18, ribs 2.05 mm (40 %), 3/4 mean 1.78; Δ outline bias mean -0.27 (range -2.36..+1.89), Δ rib mean +2.03 mm
- twist x0.97: front 3/19, 3/4 3/19, outline max 2.08, ribs 1.09 mm (53 %), 3/4 mean 1.32; Δ outline bias mean -0.13 (range -1.14..+0.95), Δ rib mean +0.83 mm
- twist x1.0: front 10/19, 3/4 13/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.82; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 2/19, 3/4 12/19, outline max 2.07, ribs 1.08 mm (58 %), 3/4 mean 0.83; Δ outline bias mean +0.12 (range -0.97..+1.07), Δ rib mean +0.83 mm
- twist x1.06: front 1/19, 3/4 7/19, outline max 2.07, ribs 1.98 mm (44 %), 3/4 mean 1.26; Δ outline bias mean +0.23 (range -1.78..+2.08), Δ rib mean +1.96 mm
- 1-knot bumps: mean locality share 0.63 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.49 of 1 °
- command: python models/M04_spline_keyframes/E4_twist/run.py

### 2026-11-23 23:03 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v3)
- r0 -2 mm: front 0/19, 3/4 0/19, outline max 2.41, ribs 1.14 mm (56 %), 3/4 mean 1.73; Δ outline bias mean -1.90 (range -2.00..-1.65), Δ rib mean +0.87 mm
- r0 -1 mm: front 1/19, 3/4 8/19, outline max 1.60, ribs 0.71 mm (73 %), 3/4 mean 1.01; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.34 mm
- r0 +0 mm: front 10/19, 3/4 13/19, outline max 2.07, ribs 0.44 mm (93 %), 3/4 mean 0.82; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 3/19, outline max 3.07, ribs 0.69 mm (73 %), 3/4 mean 1.37; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.32 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.07, ribs 1.14 mm (57 %), 3/4 mean 2.27; Δ outline bias mean +1.90 (range +1.65..+2.00), Δ rib mean +0.90 mm
- 1-knot bumps: mean locality share 0.63 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.49 of 1 mm
- command: python models/M04_spline_keyframes/E5_radius/run.py

### 2026-11-23 23:03 — E6 sections (count x placement) (kernel v3)
- uniform_z n=8: loft deviation from exact max 1.69 / mean 0.194 mm; front 10/19, 3/4 13/19
- uniform_z n=11: loft deviation from exact max 1.83 / mean 0.184 mm; front 10/19, 3/4 13/19
- uniform_z n=15: loft deviation from exact max 1.10 / mean 0.133 mm; front 12/19, 3/4 13/19
- uniform_z n=20: loft deviation from exact max 0.26 / mean 0.045 mm; front 12/19, 3/4 14/19
- uniform_z n=30: loft deviation from exact max 0.09 / mean 0.009 mm; front 12/19, 3/4 13/19
- uniform_z n=39: loft deviation from exact max 0.05 / mean 0.003 mm; front 12/19, 3/4 13/19
- adaptive n=8: loft deviation from exact max 1.76 / mean 0.205 mm; front 10/19, 3/4 14/19
- adaptive n=11: loft deviation from exact max 1.48 / mean 0.173 mm; front 13/19, 3/4 14/19
- adaptive n=15: loft deviation from exact max 0.51 / mean 0.096 mm; front 10/19, 3/4 14/19
- adaptive n=20: loft deviation from exact max 0.05 / mean 0.011 mm; front 12/19, 3/4 13/19
- adaptive n=30: loft deviation from exact max 0.06 / mean 0.007 mm; front 12/19, 3/4 13/19
- adaptive n=39: loft deviation from exact max 0.05 / mean 0.003 mm; front 12/19, 3/4 13/19
- knots10 n=20: loft deviation from exact max 0.26 / mean 0.045 mm; front 12/19, 3/4 14/19
- own sections: {'mode': 'list', 'z': [0.0, 19.0, 38.0, 57.0, 76.0, 95.0, 114.0, 133.0, 152.0, 171.0, 190.0]}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M04_spline_keyframes/E6_sections/run.py

### 2026-11-23 23:14 — final round (kernel v3) — results recorded (kernel v3)
- rank 5/10, score 0.592; front 10/19, 3/4 13/19, ribs 0.44 mm, cost 90.7 (best start pool:M03_E0v2)
- orientation offset -1.55°; MODEL.md: 'Final round — kernel v3' section appended; verified by judge/verify_e0.py
