# M06_rose_knots — progress

## Status  (overwrite this block only)
- State: final (kernel v3), rank 7/10
- Best E0 (as built): front 7/19, 3/4 10/19, 46 params, score 0.488
- Next: none (study complete)

## Log  (append only, newest at the bottom)

### 2026-11-23 22:28 — model created (kernel v1)
- model.py: rose k(z) (6 Catmull-Rom nodes z=0,38..190, as M05) + radius knots every 10 mm (20 values, Catmull-Rom) + twist knots every 10 mm (twist(0)=0 fixed, 19 free), 45 params
- smoothness: SMOOTH_W mm/deg/k (0.05/0.05/2.0) x second_diff of r / twist / k knots; k soft floor 50*min(k-0.02,0) (as M05)
- bounds: r 20..160 mm, twist -30..150 deg, k 0..0.45; constraints: k(z) in 0.02..0.4, r0 >= 20 mm
- start: M05 E0 fit (models/M05_rose_bezier/E0_fit/params.json) sampled at the knots, k = M05 fitted k; baked as literals
- start vs M05 curves: identical within 0.02 mm / 0.12 deg in S02-S18; differs in S01 (r 0.76 mm, twist 1.04 deg: M05 Bezier twist dips to -1.06 deg at z=10, knots clamp the end) and S19 (r 0.77 mm)
- start (P0) score: exact front 0/19, 3/4 6/19, ribs 1.59 mm; as built front 0/19, 3/4 7/19, ribs 1.61 mm (vs M05 0.71): the 1 deg twist change in S01 moves the rib start invariant (ribs are anchored at their drawn start z0 near the rim), so every rib shifts
- settings: inherit M05: N 22, H 3.0, arc placement 9 mm, sections knots10 (20 sections on the knots) — docs/05 §5.4
- Fusion export: table-driven kernel template (kernel v1 decision), no pure-Python curve copies needed

### 2026-11-23 22:28 — MODEL.md written (kernel v1)
- definition (45 params) + hypothesis before running: front 11-14/19, 3/4 6-10/19, locality 0.6-0.8, base is the remaining limit

### 2026-11-23 22:30 — E0 fit (kernel v1)
- start (as built): front 0/19, 3/4 8/19, ribs 1.61 mm
- result (as built): front 4/19, 3/4 8/19, outline max 3.05, ribs 0.76 mm / 73 %, 3/4 mean 1.05
- exact curves: front 4/19, 3/4 4/19
- 45 params, 70.4 s, nfev 17, cap hit [False, False], constraints OK
- Fusion script: models\M06_rose_knots\fusion\M06\M06.py
- command: python models/M06_rose_knots/E0_fit/run.py

### 2026-11-23 22:34 — E1 triangle count (kernel v2)
- N=12: front 4/19, 3/4 1/19, outline max 2.48, ribs 0.76 mm (73 %), 3/4 mean 1.18; Δ outline bias mean -0.30 (range -0.66..-0.04), Δ rib mean +0.00 mm
- N=16: front 6/19, 3/4 4/19, outline max 2.71, ribs 0.76 mm (73 %), 3/4 mean 1.11; Δ outline bias mean -0.17 (range -0.35..+0.01), Δ rib mean +0.00 mm
- N=22 (own): front 4/19, 3/4 8/19, outline max 3.05, ribs 0.76 mm (73 %), 3/4 mean 1.05; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 4/19, 3/4 9/19, outline max 3.23, ribs 0.76 mm (73 %), 3/4 mean 1.12; Δ outline bias mean +0.11 (range +0.04..+0.19), Δ rib mean +0.00 mm
- N=45: front 2/19, 3/4 11/19, outline max 3.35, ribs 0.76 mm (73 %), 3/4 mean 1.12; Δ outline bias mean +0.19 (range +0.09..+0.30), Δ rib mean +0.00 mm
- command: python models/M06_rose_knots/E1_tri_count/run.py

### 2026-11-23 22:34 — E2 triangle width (fill) x placement (kernel v2)
- arc f=0.5: front 4/19, 3/4 9/19, outline max 3.19, ribs 0.76 mm (73 %), 3/4 mean 1.07; Δ outline bias mean +0.13 (range +0.07..+0.17), Δ rib mean +0.00 mm
- arc f=0.7: front 4/19, 3/4 8/19, outline max 3.14, ribs 0.76 mm (73 %), 3/4 mean 1.06; Δ outline bias mean +0.09 (range +0.05..+0.12), Δ rib mean +0.00 mm
- arc f=0.85: front 4/19, 3/4 8/19, outline max 3.10, ribs 0.76 mm (73 %), 3/4 mean 1.05; Δ outline bias mean +0.05 (range +0.02..+0.06), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 4/19, 3/4 8/19, outline max 3.05, ribs 0.76 mm (73 %), 3/4 mean 1.05; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 4/19, 3/4 8/19, outline max 3.44, ribs 0.73 mm (76 %), 3/4 mean 1.14; Δ outline bias mean +0.14 (range -0.02..+0.39), Δ rib mean -0.05 mm
- angle_half f=0.7: front 4/19, 3/4 8/19, outline max 3.44, ribs 0.73 mm (76 %), 3/4 mean 1.13; Δ outline bias mean +0.10 (range -0.03..+0.39), Δ rib mean -0.05 mm
- angle_half f=0.85: front 4/19, 3/4 7/19, outline max 3.44, ribs 0.73 mm (76 %), 3/4 mean 1.13; Δ outline bias mean +0.07 (range -0.05..+0.39), Δ rib mean -0.05 mm
- angle_half f=1.0: front 4/19, 3/4 6/19, outline max 3.44, ribs 0.73 mm (76 %), 3/4 mean 1.13; Δ outline bias mean +0.03 (range -0.11..+0.39), Δ rib mean -0.05 mm
- command: python models/M06_rose_knots/E2_tri_width/run.py

### 2026-11-23 22:34 — E3 triangle height (kernel v2)
- H=1.5: front 0/19, 3/4 4/19, outline max 2.08, ribs 0.76 mm (73 %), 3/4 mean 1.64; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 4/19, outline max 2.06, ribs 0.76 mm (73 %), 3/4 mean 1.36; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 4/19, 3/4 8/19, outline max 3.05, ribs 0.76 mm (73 %), 3/4 mean 1.05; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 6/19, outline max 4.04, ribs 0.76 mm (73 %), 3/4 mean 1.45; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 5.03, ribs 0.76 mm (73 %), 3/4 mean 2.43; Δ outline bias mean +2.00 (range +1.98..+2.00), Δ rib mean +0.00 mm
- command: python models/M06_rose_knots/E3_tri_height/run.py

### 2026-11-23 22:34 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v2)
- twist x0.94: front 0/19, 3/4 3/19, outline max 3.05, ribs 2.25 mm (40 %), 3/4 mean 1.50; Δ outline bias mean -0.27 (range -2.27..+2.06), Δ rib mean +1.88 mm
- twist x0.97: front 2/19, 3/4 7/19, outline max 3.05, ribs 1.32 mm (53 %), 3/4 mean 1.10; Δ outline bias mean -0.13 (range -1.12..+1.04), Δ rib mean +0.70 mm
- twist x1.0: front 4/19, 3/4 8/19, outline max 3.05, ribs 0.76 mm (73 %), 3/4 mean 1.05; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 1/19, 3/4 3/19, outline max 3.05, ribs 1.16 mm (58 %), 3/4 mean 1.42; Δ outline bias mean +0.12 (range -0.93..+1.09), Δ rib mean +0.50 mm
- twist x1.06: front 1/19, 3/4 3/19, outline max 3.05, ribs 2.00 mm (40 %), 3/4 mean 1.84; Δ outline bias mean +0.23 (range -1.69..+2.22), Δ rib mean +1.52 mm
- 1-knot bumps: mean locality share 0.93 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 °
- command: python models/M06_rose_knots/E4_twist/run.py

### 2026-11-23 22:35 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v2)
- r0 -2 mm: front 0/19, 3/4 3/19, outline max 2.19, ribs 1.33 mm (59 %), 3/4 mean 1.84; Δ outline bias mean -1.89 (range -1.99..-1.65), Δ rib mean +0.71 mm
- r0 -1 mm: front 0/19, 3/4 4/19, outline max 2.05, ribs 0.98 mm (65 %), 3/4 mean 1.27; Δ outline bias mean -0.95 (range -1.00..-0.82), Δ rib mean +0.28 mm
- r0 +0 mm: front 4/19, 3/4 8/19, outline max 3.05, ribs 0.76 mm (73 %), 3/4 mean 1.05; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 7/19, outline max 4.05, ribs 0.81 mm (71 %), 3/4 mean 1.35; Δ outline bias mean +0.95 (range +0.82..+1.00), Δ rib mean +0.04 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 5.04, ribs 1.07 mm (55 %), 3/4 mean 2.21; Δ outline bias mean +1.89 (range +1.65..+1.99), Δ rib mean +0.34 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 mm
- command: python models/M06_rose_knots/E5_radius/run.py

### 2026-11-23 22:35 — E6 sections (count x placement) (kernel v2)
- uniform_z n=8: loft deviation from exact max 0.88 / mean 0.196 mm; front 5/19, 3/4 6/19
- uniform_z n=11: loft deviation from exact max 0.90 / mean 0.132 mm; front 4/19, 3/4 8/19
- uniform_z n=15: loft deviation from exact max 0.73 / mean 0.085 mm; front 5/19, 3/4 9/19
- uniform_z n=20: loft deviation from exact max 0.73 / mean 0.052 mm; front 4/19, 3/4 8/19
- uniform_z n=30: loft deviation from exact max 0.36 / mean 0.029 mm; front 4/19, 3/4 8/19
- uniform_z n=39: loft deviation from exact max 0.08 / mean 0.010 mm; front 4/19, 3/4 8/19
- adaptive n=8: loft deviation from exact max 0.91 / mean 0.179 mm; front 4/19, 3/4 8/19
- adaptive n=11: loft deviation from exact max 0.80 / mean 0.128 mm; front 5/19, 3/4 8/19
- adaptive n=15: loft deviation from exact max 0.61 / mean 0.104 mm; front 4/19, 3/4 8/19
- adaptive n=20: loft deviation from exact max 0.43 / mean 0.059 mm; front 4/19, 3/4 9/19
- adaptive n=30: loft deviation from exact max 0.13 / mean 0.018 mm; front 4/19, 3/4 9/19
- adaptive n=39: loft deviation from exact max 0.11 / mean 0.006 mm; front 4/19, 3/4 8/19
- knots10 n=20: loft deviation from exact max 0.73 / mean 0.052 mm; front 4/19, 3/4 8/19
- own sections: {'mode': 'knots10'}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M06_rose_knots/E6_sections/run.py

### 2026-11-23 22:35 — v1 E0 superseded; diagnostics; re-run under kernel v2 (kernel v2)
- the E0 entry above ran on kernel v1 (2 stages, single start): front 4/19, 3/4 8/19, ribs 0.76 mm, cost 202.8 (M05 v1: 171.8). E1-E6 above ran at 22:33-22:35 on kernel v2 code but around that v1 E0 -> all superseded by the re-run below
- diagnostic (scratch, not official): restarting the v1 fit from its own result 5x converges to cost 194.8 (front 5/19, 3/4 11/19) -> the v1 fit stopped on xtol before the minimum
- diagnostic: rib_start() (geometry.py) quantises the rib invariant on a 20001-point angle grid -> steps of ~1.1e-4 arc fraction; r@0 +0..0.02 mm gives a piecewise-constant invariant, so finite-difference Jacobians at diff_step 1e-4 see spikes (reported to orchestrator; v2 coarse 1e-2 stage addresses it)
- diagnostic: same model with twist(0) FREE (46 params): cost 159.2, front 6/19, 3/4 9/19, ribs 0.65 mm, tw@0 = -1.08 deg. Fixing twist(0)=0 (spec) costs ~35 cost units: ribs are anchored at z0 = 2.2 mm, and a value-only Catmull-Rom with a clamped end cannot reproduce M05s fast -1 deg dip in S01
- no change to model.py; re-running E0 and E1-E6 under kernel v2

### 2026-11-23 22:38 — E0 fit (kernel v2)
- start (as built): front 0/19, 3/4 8/19, ribs 1.61 mm
- result (as built): front 5/19, 3/4 10/19, outline max 2.36, ribs 0.75 mm / 75 %, 3/4 mean 0.95
- exact curves: front 6/19, 3/4 9/19
- 45 params, 145.2 s, nfev 14, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 195.1, pool:M01_E0 195.1, pool:M05_E0 194.9, pool:M02_X1c 194.8 -> best: pool:M02_X1c
- Fusion script: models\M06_rose_knots\fusion\M06\M06.py
- command: python models/M06_rose_knots/E0_fit/run.py

### 2026-11-23 22:38 — E1 triangle count (kernel v2)
- N=12: front 4/19, 3/4 5/19, outline max 1.79, ribs 0.75 mm (75 %), 3/4 mean 1.03; Δ outline bias mean -0.30 (range -0.64..-0.04), Δ rib mean +0.00 mm
- N=16: front 6/19, 3/4 8/19, outline max 2.03, ribs 0.75 mm (75 %), 3/4 mean 0.91; Δ outline bias mean -0.17 (range -0.34..-0.00), Δ rib mean +0.00 mm
- N=22 (own): front 5/19, 3/4 10/19, outline max 2.36, ribs 0.75 mm (75 %), 3/4 mean 0.95; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 4/19, 3/4 11/19, outline max 2.53, ribs 0.75 mm (75 %), 3/4 mean 0.99; Δ outline bias mean +0.11 (range +0.04..+0.18), Δ rib mean +0.00 mm
- N=45: front 4/19, 3/4 12/19, outline max 2.64, ribs 0.75 mm (75 %), 3/4 mean 1.03; Δ outline bias mean +0.18 (range +0.09..+0.29), Δ rib mean +0.00 mm
- command: python models/M06_rose_knots/E1_tri_count/run.py

### 2026-11-23 22:38 — E2 triangle width (fill) x placement (kernel v2)
- arc f=0.5: front 4/19, 3/4 11/19, outline max 2.49, ribs 0.75 mm (75 %), 3/4 mean 0.97; Δ outline bias mean +0.13 (range +0.07..+0.17), Δ rib mean +0.00 mm
- arc f=0.7: front 4/19, 3/4 11/19, outline max 2.45, ribs 0.75 mm (75 %), 3/4 mean 0.96; Δ outline bias mean +0.09 (range +0.05..+0.12), Δ rib mean +0.00 mm
- arc f=0.85: front 5/19, 3/4 10/19, outline max 2.41, ribs 0.75 mm (75 %), 3/4 mean 0.95; Δ outline bias mean +0.05 (range +0.02..+0.06), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 5/19, 3/4 10/19, outline max 2.36, ribs 0.75 mm (75 %), 3/4 mean 0.95; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 4/19, 3/4 11/19, outline max 2.73, ribs 0.74 mm (76 %), 3/4 mean 1.00; Δ outline bias mean +0.14 (range -0.02..+0.38), Δ rib mean -0.01 mm
- angle_half f=0.7: front 4/19, 3/4 11/19, outline max 2.73, ribs 0.74 mm (76 %), 3/4 mean 1.01; Δ outline bias mean +0.10 (range -0.03..+0.38), Δ rib mean -0.01 mm
- angle_half f=0.85: front 4/19, 3/4 10/19, outline max 2.73, ribs 0.74 mm (76 %), 3/4 mean 1.01; Δ outline bias mean +0.07 (range -0.05..+0.38), Δ rib mean -0.01 mm
- angle_half f=1.0: front 4/19, 3/4 10/19, outline max 2.73, ribs 0.74 mm (76 %), 3/4 mean 1.02; Δ outline bias mean +0.03 (range -0.11..+0.38), Δ rib mean -0.01 mm
- command: python models/M06_rose_knots/E2_tri_width/run.py

### 2026-11-23 22:38 — E3 triangle height (kernel v2)
- H=1.5: front 0/19, 3/4 5/19, outline max 2.04, ribs 0.75 mm (75 %), 3/4 mean 1.45; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 4/19, outline max 1.54, ribs 0.75 mm (75 %), 3/4 mean 1.16; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 5/19, 3/4 10/19, outline max 2.36, ribs 0.75 mm (75 %), 3/4 mean 0.95; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 7/19, outline max 3.35, ribs 0.75 mm (75 %), 3/4 mean 1.45; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.34, ribs 0.75 mm (75 %), 3/4 mean 2.47; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M06_rose_knots/E3_tri_height/run.py

### 2026-11-23 22:38 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v2)
- twist x0.94: front 2/19, 3/4 0/19, outline max 2.44, ribs 2.22 mm (41 %), 3/4 mean 1.56; Δ outline bias mean -0.27 (range -2.28..+2.05), Δ rib mean +1.87 mm
- twist x0.97: front 3/19, 3/4 3/19, outline max 2.36, ribs 1.30 mm (56 %), 3/4 mean 1.09; Δ outline bias mean -0.13 (range -1.13..+1.04), Δ rib mean +0.69 mm
- twist x1.0: front 5/19, 3/4 10/19, outline max 2.36, ribs 0.75 mm (75 %), 3/4 mean 0.95; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 3/19, 3/4 4/19, outline max 2.36, ribs 1.15 mm (60 %), 3/4 mean 1.27; Δ outline bias mean +0.12 (range -0.93..+1.10), Δ rib mean +0.51 mm
- twist x1.06: front 2/19, 3/4 2/19, outline max 2.87, ribs 1.99 mm (44 %), 3/4 mean 1.68; Δ outline bias mean +0.24 (range -1.69..+2.21), Δ rib mean +1.51 mm
- 1-knot bumps: mean locality share 0.93 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 °
- command: python models/M06_rose_knots/E4_twist/run.py

### 2026-11-23 22:38 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v2)
- r0 -2 mm: front 0/19, 3/4 3/19, outline max 2.15, ribs 1.32 mm (62 %), 3/4 mean 1.71; Δ outline bias mean -1.89 (range -1.99..-1.65), Δ rib mean +0.71 mm
- r0 -1 mm: front 0/19, 3/4 3/19, outline max 1.36, ribs 0.96 mm (66 %), 3/4 mean 1.17; Δ outline bias mean -0.94 (range -1.00..-0.82), Δ rib mean +0.27 mm
- r0 +0 mm: front 5/19, 3/4 10/19, outline max 2.36, ribs 0.75 mm (75 %), 3/4 mean 0.95; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 9/19, outline max 3.35, ribs 0.82 mm (70 %), 3/4 mean 1.36; Δ outline bias mean +0.94 (range +0.82..+1.00), Δ rib mean +0.06 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.35, ribs 1.06 mm (59 %), 3/4 mean 2.24; Δ outline bias mean +1.89 (range +1.65..+1.99), Δ rib mean +0.34 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 mm
- command: python models/M06_rose_knots/E5_radius/run.py

### 2026-11-23 22:38 — E6 sections (count x placement) (kernel v2)
- uniform_z n=8: loft deviation from exact max 0.89 / mean 0.190 mm; front 5/19, 3/4 8/19
- uniform_z n=11: loft deviation from exact max 0.93 / mean 0.131 mm; front 5/19, 3/4 10/19
- uniform_z n=15: loft deviation from exact max 0.79 / mean 0.086 mm; front 6/19, 3/4 10/19
- uniform_z n=20: loft deviation from exact max 0.73 / mean 0.053 mm; front 5/19, 3/4 10/19
- uniform_z n=30: loft deviation from exact max 0.36 / mean 0.030 mm; front 6/19, 3/4 9/19
- uniform_z n=39: loft deviation from exact max 0.08 / mean 0.010 mm; front 5/19, 3/4 9/19
- adaptive n=8: loft deviation from exact max 0.93 / mean 0.175 mm; front 5/19, 3/4 9/19
- adaptive n=11: loft deviation from exact max 0.81 / mean 0.124 mm; front 6/19, 3/4 11/19
- adaptive n=15: loft deviation from exact max 0.63 / mean 0.102 mm; front 6/19, 3/4 8/19
- adaptive n=20: loft deviation from exact max 0.45 / mean 0.058 mm; front 6/19, 3/4 9/19
- adaptive n=30: loft deviation from exact max 0.14 / mean 0.016 mm; front 6/19, 3/4 9/19
- adaptive n=39: loft deviation from exact max 0.08 / mean 0.005 mm; front 5/19, 3/4 9/19
- knots10 n=20: loft deviation from exact max 0.73 / mean 0.053 mm; front 5/19, 3/4 10/19
- own sections: {'mode': 'knots10'}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M06_rose_knots/E6_sections/run.py

### 2026-11-23 22:40 — summary.json + MODEL.md conclusions (kernel v2)
- summary.json: 45 params, built front 5/19, 3/4 10/19, locality 0.94 (twist 0.93, radius 0.96), smooth score 0.18 (r0 4 / twist 8 inflections), loft_dev_20 0.73 -> buildable False, constraints OK
- E6 cause: catmull_keys duplicates the end knot; end intervals [0,10] and [180,190] differ from a not-a-knot spline through the same knots by up to 0.74 mm (r0, z=187) / 0.33 deg (twist, z=3); interior <= 0.08 mm
- waist diagnosis: signed per-rib errors in S09 have mixed signs across the width (-1.6, -1.3, +2.8, +0.5, -4.6 mm) -> no twist/radius knot can fix them; limit = base / rib traces
- vs M05 (kernel v2 E0: front 5/19, 3/4 9/19, cost 163.8): same front segments, 3/4 +1, cost higher (194.8) because twist(0)=0 + Catmull end cannot reproduce M05 rim dip (twist(2.2 mm) -0.94 vs -0.02 deg) and ribs are anchored at z0=2.2 mm
- hypothesis: front 11-14/19 not met (5/19); locality exceeded; 3/4 not proportional (worse at the waist S08-S10)
- command: python -c "import sys; sys.path.insert(0,'models/_common'); import study; study.write_summary('models/M06_rose_knots')"

### 2026-11-23 23:07 — E0 fit (kernel v3)
- start (as built): front 0/19, 3/4 8/19, ribs 1.61 mm
- result (as built): front 7/19, 3/4 10/19, outline max 2.49, ribs 0.66 mm / 78 %, 3/4 mean 0.94
- exact curves: front 7/19, 3/4 10/19
- 46 params, 412.4 s, nfev 15, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 160.7, pool:M01_E0 162.0, pool:M05_E0 163.5, pool:M02_X1c 161.2, pool:M01_E0v2 160.4, pool:M02_E0v2 160.5, pool:M03_E0v2 163.5, pool:M04_E0v2 160.0, pool:M05_E0v2 160.9, pool:M06_E0v2 163.0, pool:M07_E0v2 167.1, pool:M08_E0v2 160.5, pool:M09_E0v2 164.7, pool:M10_E0v2 162.8 -> best: pool:M04_E0v2
- Fusion script: models\M06_rose_knots\fusion\M06\M06.py
- command: python models/M06_rose_knots/E0_fit/run.py

### 2026-11-23 23:07 — E1 triangle count (kernel v3)
- N=12: front 6/19, 3/4 6/19, outline max 1.94, ribs 0.66 mm (78 %), 3/4 mean 0.97; Δ outline bias mean -0.31 (range -0.71..-0.06), Δ rib mean +0.00 mm
- N=16: front 6/19, 3/4 9/19, outline max 2.17, ribs 0.66 mm (78 %), 3/4 mean 0.90; Δ outline bias mean -0.18 (range -0.35..+0.02), Δ rib mean +0.00 mm
- N=22 (own): front 7/19, 3/4 10/19, outline max 2.49, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 4/19, 3/4 10/19, outline max 2.65, ribs 0.66 mm (78 %), 3/4 mean 0.95; Δ outline bias mean +0.12 (range +0.05..+0.24), Δ rib mean +0.00 mm
- N=45: front 4/19, 3/4 11/19, outline max 2.76, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.19 (range +0.09..+0.32), Δ rib mean +0.00 mm
- command: python models/M06_rose_knots/E1_tri_count/run.py

### 2026-11-23 23:07 — E2 triangle width (fill) x placement (kernel v3)
- arc f=0.5: front 4/19, 3/4 8/19, outline max 2.62, ribs 0.66 mm (78 %), 3/4 mean 1.00; Δ outline bias mean +0.13 (range +0.07..+0.18), Δ rib mean +0.00 mm
- arc f=0.7: front 5/19, 3/4 9/19, outline max 2.58, ribs 0.66 mm (78 %), 3/4 mean 0.98; Δ outline bias mean +0.09 (range +0.05..+0.12), Δ rib mean +0.00 mm
- arc f=0.85: front 6/19, 3/4 10/19, outline max 2.54, ribs 0.66 mm (78 %), 3/4 mean 0.96; Δ outline bias mean +0.05 (range +0.03..+0.07), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 7/19, 3/4 10/19, outline max 2.49, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 4/19, 3/4 11/19, outline max 2.82, ribs 0.71 mm (77 %), 3/4 mean 0.94; Δ outline bias mean +0.15 (range -0.02..+0.40), Δ rib mean +0.05 mm
- angle_half f=0.7: front 4/19, 3/4 11/19, outline max 2.82, ribs 0.71 mm (77 %), 3/4 mean 0.94; Δ outline bias mean +0.11 (range -0.03..+0.40), Δ rib mean +0.05 mm
- angle_half f=0.85: front 5/19, 3/4 10/19, outline max 2.82, ribs 0.71 mm (77 %), 3/4 mean 0.93; Δ outline bias mean +0.08 (range -0.04..+0.40), Δ rib mean +0.05 mm
- angle_half f=1.0: front 5/19, 3/4 10/19, outline max 2.82, ribs 0.71 mm (77 %), 3/4 mean 0.93; Δ outline bias mean +0.04 (range -0.10..+0.40), Δ rib mean +0.05 mm
- command: python models/M06_rose_knots/E2_tri_width/run.py

### 2026-11-23 23:07 — E3 triangle height (kernel v3)
- H=1.5: front 0/19, 3/4 3/19, outline max 2.04, ribs 0.66 mm (78 %), 3/4 mean 1.51; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 5/19, outline max 1.54, ribs 0.66 mm (78 %), 3/4 mean 1.19; Δ outline bias mean -1.00 (range -1.00..-0.99), Δ rib mean +0.00 mm
- H=3.0 (own): front 7/19, 3/4 10/19, outline max 2.49, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 6/19, outline max 3.48, ribs 0.66 mm (78 %), 3/4 mean 1.38; Δ outline bias mean +1.00 (range +0.99..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.48, ribs 0.66 mm (78 %), 3/4 mean 2.32; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M06_rose_knots/E3_tri_height/run.py

### 2026-11-23 23:07 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v3)
- twist x0.94: front 3/19, 3/4 2/19, outline max 2.67, ribs 2.15 mm (40 %), 3/4 mean 1.62; Δ outline bias mean -0.28 (range -2.28..+2.00), Δ rib mean +1.89 mm
- twist x0.97: front 4/19, 3/4 2/19, outline max 2.49, ribs 1.23 mm (53 %), 3/4 mean 1.19; Δ outline bias mean -0.13 (range -1.12..+1.01), Δ rib mean +0.73 mm
- twist x1.0: front 7/19, 3/4 10/19, outline max 2.49, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 4/19, 3/4 5/19, outline max 2.49, ribs 1.14 mm (60 %), 3/4 mean 1.15; Δ outline bias mean +0.12 (range -0.98..+1.09), Δ rib mean +0.63 mm
- twist x1.06: front 3/19, 3/4 3/19, outline max 2.49, ribs 1.98 mm (47 %), 3/4 mean 1.46; Δ outline bias mean +0.23 (range -1.66..+2.15), Δ rib mean +1.66 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 °
- command: python models/M06_rose_knots/E4_twist/run.py

### 2026-11-23 23:07 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v3)
- r0 -2 mm: front 0/19, 3/4 2/19, outline max 2.15, ribs 1.26 mm (56 %), 3/4 mean 1.80; Δ outline bias mean -1.89 (range -1.99..-1.64), Δ rib mean +0.75 mm
- r0 -1 mm: front 0/19, 3/4 5/19, outline max 1.49, ribs 0.86 mm (70 %), 3/4 mean 1.17; Δ outline bias mean -0.95 (range -1.00..-0.82), Δ rib mean +0.25 mm
- r0 +0 mm: front 7/19, 3/4 10/19, outline max 2.49, ribs 0.66 mm (78 %), 3/4 mean 0.94; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 6/19, outline max 3.48, ribs 0.76 mm (69 %), 3/4 mean 1.31; Δ outline bias mean +0.95 (range +0.82..+1.00), Δ rib mean +0.12 mm
- r0 +2 mm: front 0/19, 3/4 1/19, outline max 4.48, ribs 1.07 mm (61 %), 3/4 mean 2.07; Δ outline bias mean +1.89 (range +1.64..+1.99), Δ rib mean +0.49 mm
- 1-knot bumps: mean locality share 0.96 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.89 of 1 mm
- command: python models/M06_rose_knots/E5_radius/run.py

### 2026-11-23 23:07 — E6 sections (count x placement) (kernel v3)
- uniform_z n=8: loft deviation from exact max 0.90 / mean 0.165 mm; front 4/19, 3/4 10/19
- uniform_z n=11: loft deviation from exact max 0.93 / mean 0.123 mm; front 5/19, 3/4 9/19
- uniform_z n=15: loft deviation from exact max 0.77 / mean 0.083 mm; front 7/19, 3/4 11/19
- uniform_z n=20: loft deviation from exact max 0.72 / mean 0.050 mm; front 7/19, 3/4 10/19
- uniform_z n=30: loft deviation from exact max 0.36 / mean 0.029 mm; front 7/19, 3/4 10/19
- uniform_z n=39: loft deviation from exact max 0.08 / mean 0.010 mm; front 7/19, 3/4 9/19
- adaptive n=8: loft deviation from exact max 0.92 / mean 0.163 mm; front 4/19, 3/4 12/19
- adaptive n=11: loft deviation from exact max 0.79 / mean 0.117 mm; front 6/19, 3/4 10/19
- adaptive n=15: loft deviation from exact max 0.59 / mean 0.097 mm; front 6/19, 3/4 9/19
- adaptive n=20: loft deviation from exact max 0.45 / mean 0.053 mm; front 7/19, 3/4 9/19
- adaptive n=30: loft deviation from exact max 0.14 / mean 0.015 mm; front 7/19, 3/4 9/19
- adaptive n=39: loft deviation from exact max 0.06 / mean 0.005 mm; front 7/19, 3/4 9/19
- knots10 n=20: loft deviation from exact max 0.72 / mean 0.050 mm; front 7/19, 3/4 10/19
- own sections: {'mode': 'knots10'}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M06_rose_knots/E6_sections/run.py

### 2026-11-23 23:14 — final round (kernel v3) — results recorded (kernel v3)
- rank 7/10, score 0.488; front 7/19, 3/4 10/19, ribs 0.66 mm, cost 160.0 (best start pool:M04_E0v2)
- orientation offset -1.06°; MODEL.md: 'Final round — kernel v3' section appended; verified by judge/verify_e0.py
