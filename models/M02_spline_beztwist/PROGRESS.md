# M02_spline_beztwist — progress

## Status  (overwrite this block only)
- State: final (kernel v3), rank 2/10
- Best E0 (as built): front 14/19, 3/4 13/19, 19 params, score 0.702
- Next: user decision; top 2 → Fusion build F2

## Log  (append only, newest at the bottom)

### 2026-11-23 22:28 — model created (kernel v1)
- model.py: custom spline base (fixed over height, bases.custom_spline) + 11 bez_points radius keys (Catmull-Rom, t = z/190, bounds 20..200, smoothness SMOOTH_W[mm]) + 5-point Bezier twist (t, deg) (curves.BezierTwist at t = z/190)
- twist params: T1..T3 (t free 0..1, deg -90..180) + T4.deg (t = 1 fixed, 45..135); P0 = (0, 0) fixed -> 7 twist params; penalty 200*min(diff(t), 0) like M05
- 18 params total (11 radius + 7 twist)
- start: radius = ../BaseScript bez_points (= M01 start); twist = ../Grasshoper_full calculate_bezier_twist2 twist_points [(0,0),(0.289,-0.7),(0.604,59.0),(0.827,78.4),(1,90)]
- settings from ../Grasshoper_full: N 22, H 3.0 (scale_perp 0.3 cm), arc placement (generate_arc_normal) target_w 9.0, 15 uniform_z sections
- start check: r0 44..114.6 mm, twist 0 -> 90 deg, rho(0) = 1; start exact front 0/19, 3/4 3/19, ribs 2.23 mm; as built front 1/19, 3/4 5/19, ribs 2.20 mm; constraints OK
- self-test (python models/M02_spline_beztwist/model.py): pure-Python r0/twist vs numpy max diff 0 mm / 1.4e-14 deg (pure twist uses a 2000-step LUT like the kernel; the user script uses 100 steps)

### 2026-11-23 22:29 — E0 fit (kernel v1)
- start (as built): front 1/19, 3/4 6/19, ribs 2.20 mm
- result (as built): front 4/19, 3/4 13/19, outline max 2.24, ribs 0.76 mm / 78 %, 3/4 mean 0.77
- exact curves: front 4/19, 3/4 13/19
- 18 params, 29.3 s, nfev 18, cap hit [False, False], constraints OK
- Fusion script: models\M02_spline_beztwist\fusion\M02\M02.py
- command: python models/M02_spline_beztwist/E0_fit/run.py

### 2026-11-23 22:30 — E1 triangle count (kernel v1)
- N=12: front 4/19, 3/4 10/19, outline max 1.83, ribs 0.76 mm (78 %), 3/4 mean 0.81; Δ outline bias mean -0.30 (range -0.62..-0.06), Δ rib mean +0.00 mm
- N=16: front 5/19, 3/4 14/19, outline max 1.99, ribs 0.76 mm (78 %), 3/4 mean 0.74; Δ outline bias mean -0.16 (range -0.33..+0.04), Δ rib mean +0.00 mm
- N=22 (own): front 4/19, 3/4 13/19, outline max 2.24, ribs 0.76 mm (78 %), 3/4 mean 0.77; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 3/19, 3/4 10/19, outline max 2.36, ribs 0.76 mm (78 %), 3/4 mean 0.87; Δ outline bias mean +0.10 (range +0.05..+0.18), Δ rib mean +0.00 mm
- N=45: front 3/19, 3/4 10/19, outline max 2.44, ribs 0.76 mm (78 %), 3/4 mean 0.92; Δ outline bias mean +0.17 (range +0.07..+0.28), Δ rib mean +0.00 mm
- command: python models/M02_spline_beztwist/E1_tri_count/run.py

### 2026-11-23 22:30 — E2 triangle width (fill) x placement (kernel v1)
- arc f=0.5: front 3/19, 3/4 12/19, outline max 2.34, ribs 0.76 mm (78 %), 3/4 mean 0.84; Δ outline bias mean +0.13 (range +0.06..+0.16), Δ rib mean +0.00 mm
- arc f=0.7: front 3/19, 3/4 13/19, outline max 2.30, ribs 0.76 mm (78 %), 3/4 mean 0.82; Δ outline bias mean +0.09 (range +0.04..+0.11), Δ rib mean +0.00 mm
- arc f=0.85: front 3/19, 3/4 13/19, outline max 2.27, ribs 0.76 mm (78 %), 3/4 mean 0.79; Δ outline bias mean +0.05 (range +0.02..+0.06), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 4/19, 3/4 13/19, outline max 2.24, ribs 0.76 mm (78 %), 3/4 mean 0.77; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 3/19, 3/4 13/19, outline max 2.50, ribs 0.76 mm (78 %), 3/4 mean 0.82; Δ outline bias mean +0.12 (range +0.01..+0.27), Δ rib mean +0.00 mm
- angle_half f=0.7: front 3/19, 3/4 13/19, outline max 2.50, ribs 0.76 mm (78 %), 3/4 mean 0.80; Δ outline bias mean +0.08 (range -0.03..+0.27), Δ rib mean +0.00 mm
- angle_half f=0.85: front 4/19, 3/4 13/19, outline max 2.50, ribs 0.76 mm (78 %), 3/4 mean 0.78; Δ outline bias mean +0.05 (range -0.08..+0.27), Δ rib mean +0.00 mm
- angle_half f=1.0: front 4/19, 3/4 13/19, outline max 2.50, ribs 0.76 mm (78 %), 3/4 mean 0.76; Δ outline bias mean +0.00 (range -0.14..+0.27), Δ rib mean +0.00 mm
- command: python models/M02_spline_beztwist/E2_tri_width/run.py

### 2026-11-23 22:30 — E3 triangle height (kernel v1)
- H=1.5: front 0/19, 3/4 4/19, outline max 1.87, ribs 0.76 mm (78 %), 3/4 mean 1.18; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 6/19, outline max 1.38, ribs 0.76 mm (78 %), 3/4 mean 0.84; Δ outline bias mean -1.00 (range -1.00..-1.00), Δ rib mean +0.00 mm
- H=3.0 (own): front 4/19, 3/4 13/19, outline max 2.24, ribs 0.76 mm (78 %), 3/4 mean 0.77; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 0/19, outline max 3.23, ribs 0.76 mm (78 %), 3/4 mean 1.61; Δ outline bias mean +1.00 (range +1.00..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.23, ribs 0.76 mm (78 %), 3/4 mean 2.72; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M02_spline_beztwist/E3_tri_height/run.py

### 2026-11-23 22:30 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v1)
- twist x0.94: front 1/19, 3/4 3/19, outline max 2.24, ribs 2.33 mm (40 %), 3/4 mean 1.73; Δ outline bias mean -0.25 (range -2.23..+2.02), Δ rib mean +1.98 mm
- twist x0.97: front 3/19, 3/4 5/19, outline max 2.24, ribs 1.38 mm (52 %), 3/4 mean 1.18; Δ outline bias mean -0.12 (range -1.10..+1.03), Δ rib mean +0.79 mm
- twist x1.0: front 4/19, 3/4 13/19, outline max 2.24, ribs 0.76 mm (78 %), 3/4 mean 0.77; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 3/19, 3/4 9/19, outline max 2.24, ribs 1.17 mm (57 %), 3/4 mean 1.04; Δ outline bias mean +0.12 (range -0.87..+1.11), Δ rib mean +0.49 mm
- twist x1.06: front 3/19, 3/4 4/19, outline max 3.34, ribs 1.84 mm (48 %), 3/4 mean 1.51; Δ outline bias mean +0.22 (range -1.56..+2.22), Δ rib mean +1.29 mm
- 1-knot bumps: mean locality share 0.38 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.29 of 1 °
- command: python models/M02_spline_beztwist/E4_twist/run.py

### 2026-11-23 22:30 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v1)
- r0 -2 mm: front 0/19, 3/4 0/19, outline max 2.10, ribs 1.34 mm (62 %), 3/4 mean 1.52; Δ outline bias mean -1.90 (range -1.99..-1.66), Δ rib mean +0.73 mm
- r0 -1 mm: front 0/19, 3/4 9/19, outline max 1.24, ribs 0.95 mm (76 %), 3/4 mean 0.84; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.23 mm
- r0 +0 mm: front 4/19, 3/4 13/19, outline max 2.24, ribs 0.76 mm (78 %), 3/4 mean 0.77; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 0/19, outline max 3.23, ribs 0.79 mm (75 %), 3/4 mean 1.54; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.00 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.23, ribs 0.95 mm (62 %), 3/4 mean 2.41; Δ outline bias mean +1.90 (range +1.66..+1.99), Δ rib mean +0.14 mm
- 1-knot bumps: mean locality share 0.63 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.49 of 1 mm
- command: python models/M02_spline_beztwist/E5_radius/run.py

### 2026-11-23 22:30 — E6 sections (count x placement) (kernel v1)
- uniform_z n=8: loft deviation from exact max 1.70 / mean 0.239 mm; front 3/19, 3/4 14/19
- uniform_z n=11: loft deviation from exact max 1.77 / mean 0.189 mm; front 3/19, 3/4 13/19
- uniform_z n=15: loft deviation from exact max 1.07 / mean 0.133 mm; front 4/19, 3/4 13/19
- uniform_z n=20: loft deviation from exact max 0.25 / mean 0.045 mm; front 4/19, 3/4 13/19
- uniform_z n=30: loft deviation from exact max 0.08 / mean 0.009 mm; front 4/19, 3/4 13/19
- uniform_z n=39: loft deviation from exact max 0.05 / mean 0.003 mm; front 4/19, 3/4 13/19
- adaptive n=8: loft deviation from exact max 1.73 / mean 0.249 mm; front 3/19, 3/4 14/19
- adaptive n=11: loft deviation from exact max 1.49 / mean 0.191 mm; front 4/19, 3/4 13/19
- adaptive n=15: loft deviation from exact max 0.56 / mean 0.104 mm; front 4/19, 3/4 14/19
- adaptive n=20: loft deviation from exact max 0.08 / mean 0.013 mm; front 4/19, 3/4 13/19
- adaptive n=30: loft deviation from exact max 0.06 / mean 0.006 mm; front 4/19, 3/4 13/19
- adaptive n=39: loft deviation from exact max 0.04 / mean 0.003 mm; front 4/19, 3/4 13/19
- knots10 n=20: loft deviation from exact max 0.25 / mean 0.045 mm; front 4/19, 3/4 13/19
- own sections: {'mode': 'uniform_z', 'count': 15}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M02_spline_beztwist/E6_sections/run.py

### 2026-11-23 22:33 — E0 review (no change to model.py) (kernel v1)
- E0 fit is valid (constraints OK, cap not hit) but stops early: nfev 18, cost 1035 -> 223.5. Stage 1 ends on the xtol condition with first-order optimality 1.1e3 (diagnostic re-run of least_squares with the kernel settings, verbose=1), i.e. the trust region collapsed, not a stationary point
- fitted twist barely moved from the Grasshoper_full start: T1 (0.289,-0.7)->(0.271,-2.5), T2 (0.604,59.0)->(0.610,60.9), T3 (0.827,78.4)->(0.783,81.5), T4 90->89.86
- E0 kept as the protocol result (historical start). Not changing P0: a better start would come from another model fit, which the protocol does not allow; reported to the orchestrator instead
- self-test on E0 params: pure-Python vs numpy r0 0 mm, twist 2.8e-14 deg -> OK

### 2026-11-23 22:33 — X1 extra check: twist vs settings vs start (not part of E0-E6) (kernel v1)
- a) E0 params scored with M01 settings (H 2.4, angle_half, 11 sec): front 2/19, 3/4 15/19, ribs 0.74 mm (77 %)
- b) refit (kernel study.fit) with M01 settings from M02 start: front 3/19, 3/4 14/19, ribs 0.67 mm (81 %), cost 176.8, nfev 16 -> same as M01 E0 (3/19, 14/19, 0.67 mm)
- c) refit with M02 settings from M01 E0 fit (cubic degree-elevated to 5 points, r0 - 0.6 mm): front 13/19, 3/4 13/19, ribs 0.52 mm (89 %), 3/4 mean 0.82, cost 102.8 (vs E0 223.5), nfev 31, cap not hit. Twist T1 (0.006,-9.1) T2 (0.463,11.7) T3 (0.528,64.4) T4 90.4: a steep S between z 80 and 110
-    front pass S02-S07, S11-S17; fails S01, S08-S10, S18-S19. Ribs S11-S17 0.37-0.63 mm (E0 1.25-1.50)
- d) refit from own E0 result: front 4/19, 3/4 13/19, ribs 0.73 mm, cost 193.4 -> plain restart does not escape
- conclusion: the 5-point Bezier CAN fix the shoulder/neck ribs that the cubic cannot, but the kernel fit from the historical start lands in a poor basin (start-dependent, xtol stop)
- command: python models/M02_spline_beztwist/X1_vs_M01/run.py (results.json there)

### 2026-11-23 22:33 — summary + conclusions (kernel v1)
- summary.json written (study.write_summary): built front 4/19, 3/4 13/19, locality 0.50 (twist 0.38, radius 0.63), smoothness 0.5 (r0 4 inflections, twist 1), buildable True (loft dev @20 sec 0.25 mm)
- MODEL.md conclusions written; fusion script at models/M02_spline_beztwist/fusion/M02/M02.py (generated by E0, not run)
- reported to orchestrator: kernel fit start-dependence / xtol early stop (X1c 13/19 vs E0 4/19)

### 2026-11-23 22:38 — E0 fit (kernel v2)
- start (as built): front 1/19, 3/4 6/19, ribs 2.20 mm
- result (as built): front 12/19, 3/4 15/19, outline max 2.08, ribs 0.52 mm / 89 %, 3/4 mean 0.78
- exact curves: front 12/19, 3/4 11/19
- 18 params, 50.1 s, nfev 20, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 217.3, pool:M01_E0 101.6, pool:M05_E0 101.8, pool:M02_X1c 101.7 -> best: pool:M01_E0
- Fusion script: models\M02_spline_beztwist\fusion\M02\M02.py
- command: python models/M02_spline_beztwist/E0_fit/run.py

### 2026-11-23 22:38 — E1 triangle count (kernel v2)
- N=12: front 10/19, 3/4 8/19, outline max 1.67, ribs 0.52 mm (89 %), 3/4 mean 1.03; Δ outline bias mean -0.30 (range -0.63..-0.06), Δ rib mean +0.00 mm
- N=16: front 12/19, 3/4 12/19, outline max 1.84, ribs 0.52 mm (89 %), 3/4 mean 0.89; Δ outline bias mean -0.16 (range -0.34..+0.02), Δ rib mean +0.00 mm
- N=22 (own): front 12/19, 3/4 15/19, outline max 2.08, ribs 0.52 mm (89 %), 3/4 mean 0.78; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 11/19, 3/4 15/19, outline max 2.20, ribs 0.52 mm (89 %), 3/4 mean 0.77; Δ outline bias mean +0.10 (range +0.04..+0.18), Δ rib mean +0.00 mm
- N=45: front 11/19, 3/4 15/19, outline max 2.28, ribs 0.52 mm (89 %), 3/4 mean 0.79; Δ outline bias mean +0.17 (range +0.07..+0.27), Δ rib mean +0.00 mm
- command: python models/M02_spline_beztwist/E1_tri_count/run.py

### 2026-11-23 22:39 — E2 triangle width (fill) x placement (kernel v2)
- arc f=0.5: front 11/19, 3/4 16/19, outline max 2.18, ribs 0.52 mm (89 %), 3/4 mean 0.80; Δ outline bias mean +0.12 (range +0.06..+0.16), Δ rib mean +0.00 mm
- arc f=0.7: front 11/19, 3/4 15/19, outline max 2.15, ribs 0.52 mm (89 %), 3/4 mean 0.79; Δ outline bias mean +0.08 (range +0.04..+0.11), Δ rib mean +0.00 mm
- arc f=0.85: front 11/19, 3/4 15/19, outline max 2.12, ribs 0.52 mm (89 %), 3/4 mean 0.79; Δ outline bias mean +0.05 (range +0.02..+0.06), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 12/19, 3/4 15/19, outline max 2.08, ribs 0.52 mm (89 %), 3/4 mean 0.78; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 11/19, 3/4 16/19, outline max 2.34, ribs 0.52 mm (89 %), 3/4 mean 0.80; Δ outline bias mean +0.13 (range +0.02..+0.26), Δ rib mean -0.00 mm
- angle_half f=0.7: front 11/19, 3/4 15/19, outline max 2.34, ribs 0.52 mm (89 %), 3/4 mean 0.79; Δ outline bias mean +0.09 (range -0.03..+0.26), Δ rib mean -0.00 mm
- angle_half f=0.85: front 11/19, 3/4 15/19, outline max 2.34, ribs 0.52 mm (89 %), 3/4 mean 0.79; Δ outline bias mean +0.05 (range -0.08..+0.26), Δ rib mean -0.00 mm
- angle_half f=1.0: front 12/19, 3/4 15/19, outline max 2.34, ribs 0.52 mm (89 %), 3/4 mean 0.79; Δ outline bias mean +0.01 (range -0.16..+0.26), Δ rib mean -0.00 mm
- command: python models/M02_spline_beztwist/E2_tri_width/run.py

### 2026-11-23 22:39 — E3 triangle height (kernel v2)
- H=1.5: front 0/19, 3/4 0/19, outline max 1.98, ribs 0.52 mm (89 %), 3/4 mean 1.80; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 0/19, outline max 1.48, ribs 0.52 mm (89 %), 3/4 mean 1.40; Δ outline bias mean -1.00 (range -1.00..-1.00), Δ rib mean +0.00 mm
- H=3.0 (own): front 12/19, 3/4 15/19, outline max 2.08, ribs 0.52 mm (89 %), 3/4 mean 0.78; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 5/19, outline max 3.08, ribs 0.52 mm (89 %), 3/4 mean 1.32; Δ outline bias mean +1.00 (range +1.00..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.07, ribs 0.52 mm (89 %), 3/4 mean 2.31; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M02_spline_beztwist/E3_tri_height/run.py

### 2026-11-23 22:39 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v2)
- twist x0.94: front 1/19, 3/4 4/19, outline max 2.87, ribs 2.11 mm (40 %), 3/4 mean 1.48; Δ outline bias mean -0.26 (range -2.24..+1.86), Δ rib mean +2.02 mm
- twist x0.97: front 4/19, 3/4 7/19, outline max 2.08, ribs 1.16 mm (53 %), 3/4 mean 1.04; Δ outline bias mean -0.12 (range -1.10..+0.95), Δ rib mean +0.82 mm
- twist x1.0: front 12/19, 3/4 15/19, outline max 2.08, ribs 0.52 mm (89 %), 3/4 mean 0.78; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 3/19, 3/4 8/19, outline max 2.08, ribs 1.14 mm (58 %), 3/4 mean 1.15; Δ outline bias mean +0.11 (range -1.00..+1.08), Δ rib mean +0.79 mm
- twist x1.06: front 2/19, 3/4 7/19, outline max 2.10, ribs 2.00 mm (43 %), 3/4 mean 1.53; Δ outline bias mean +0.23 (range -1.77..+2.13), Δ rib mean +1.87 mm
- 1-knot bumps: mean locality share 0.38 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.27 of 1 °
- command: python models/M02_spline_beztwist/E4_twist/run.py

### 2026-11-23 22:39 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v2)
- r0 -2 mm: front 0/19, 3/4 0/19, outline max 2.16, ribs 1.19 mm (53 %), 3/4 mean 2.09; Δ outline bias mean -1.90 (range -1.99..-1.65), Δ rib mean +0.86 mm
- r0 -1 mm: front 0/19, 3/4 0/19, outline max 1.29, ribs 0.78 mm (74 %), 3/4 mean 1.33; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.34 mm
- r0 +0 mm: front 12/19, 3/4 15/19, outline max 2.08, ribs 0.52 mm (89 %), 3/4 mean 0.78; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 6/19, outline max 3.08, ribs 0.76 mm (73 %), 3/4 mean 1.25; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.29 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.07, ribs 1.21 mm (53 %), 3/4 mean 2.10; Δ outline bias mean +1.90 (range +1.65..+1.99), Δ rib mean +0.86 mm
- 1-knot bumps: mean locality share 0.63 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.49 of 1 mm
- command: python models/M02_spline_beztwist/E5_radius/run.py

### 2026-11-23 22:39 — E6 sections (count x placement) (kernel v2)
- uniform_z n=8: loft deviation from exact max 1.67 / mean 0.198 mm; front 9/19, 3/4 15/19
- uniform_z n=11: loft deviation from exact max 1.86 / mean 0.183 mm; front 10/19, 3/4 15/19
- uniform_z n=15: loft deviation from exact max 1.09 / mean 0.128 mm; front 12/19, 3/4 15/19
- uniform_z n=20: loft deviation from exact max 0.25 / mean 0.043 mm; front 12/19, 3/4 14/19
- uniform_z n=30: loft deviation from exact max 0.09 / mean 0.010 mm; front 12/19, 3/4 14/19
- uniform_z n=39: loft deviation from exact max 0.05 / mean 0.003 mm; front 12/19, 3/4 14/19
- adaptive n=8: loft deviation from exact max 1.77 / mean 0.206 mm; front 9/19, 3/4 15/19
- adaptive n=11: loft deviation from exact max 1.33 / mean 0.179 mm; front 13/19, 3/4 15/19
- adaptive n=15: loft deviation from exact max 0.49 / mean 0.079 mm; front 9/19, 3/4 13/19
- adaptive n=20: loft deviation from exact max 0.08 / mean 0.013 mm; front 12/19, 3/4 14/19
- adaptive n=30: loft deviation from exact max 0.07 / mean 0.008 mm; front 12/19, 3/4 14/19
- adaptive n=39: loft deviation from exact max 0.06 / mean 0.003 mm; front 12/19, 3/4 14/19
- knots10 n=20: loft deviation from exact max 0.25 / mean 0.043 mm; front 12/19, 3/4 14/19
- own sections: {'mode': 'uniform_z', 'count': 15}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M02_spline_beztwist/E6_sections/run.py

### 2026-11-23 22:41 — conclusions updated for kernel v2 (kernel v2)
- MODEL.md: new Conclusions section from the v2 results (E0 re-run by the orchestrator: multi-start, best start pool:M01_E0, cost 101.6; own start 217.3)
- v2 E0 as built: front 12/19, 3/4 15/19, ribs 0.52 mm / 89 %, 3/4 mean 0.78, outline max 2.08; locality twist 0.38 / radius 0.63; smoothness 1.0; buildable
- v1 conclusions kept under "Superseded (kernel v1)"; hypothesis untouched; nothing re-run by this runner

### 2026-11-23 23:02 — E0 fit (kernel v3)
- start (as built): front 1/19, 3/4 6/19, ribs 2.20 mm
- result (as built): front 14/19, 3/4 13/19, outline max 2.00, ribs 0.47 mm / 91 %, 3/4 mean 0.78
- exact curves: front 13/19, 3/4 13/19
- 19 params, 157.1 s, nfev 16, cap hit [False, False, False], constraints OK
- multi-start (cost per start): own start (P0) 94.5, pool:M01_E0 94.3, pool:M05_E0 95.5, pool:M02_X1c 97.5, pool:M01_E0v2 94.3, pool:M02_E0v2 97.4, pool:M03_E0v2 101.4, pool:M04_E0v2 94.6, pool:M05_E0v2 97.1, pool:M06_E0v2 94.8, pool:M07_E0v2 94.7, pool:M08_E0v2 94.6, pool:M09_E0v2 94.4, pool:M10_E0v2 94.6 -> best: pool:M01_E0
- Fusion script: models\M02_spline_beztwist\fusion\M02\M02.py
- command: python models/M02_spline_beztwist/E0_fit/run.py

### 2026-11-23 23:02 — E1 triangle count (kernel v3)
- N=12: front 9/19, 3/4 6/19, outline max 1.64, ribs 0.47 mm (91 %), 3/4 mean 0.93; Δ outline bias mean -0.30 (range -0.64..-0.06), Δ rib mean +0.00 mm
- N=16: front 10/19, 3/4 8/19, outline max 1.79, ribs 0.47 mm (91 %), 3/4 mean 0.87; Δ outline bias mean -0.16 (range -0.34..+0.02), Δ rib mean +0.00 mm
- N=22 (own): front 14/19, 3/4 13/19, outline max 2.00, ribs 0.47 mm (91 %), 3/4 mean 0.78; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- N=30: front 13/19, 3/4 12/19, outline max 2.10, ribs 0.47 mm (91 %), 3/4 mean 0.83; Δ outline bias mean +0.10 (range +0.04..+0.18), Δ rib mean +0.00 mm
- N=45: front 12/19, 3/4 13/19, outline max 2.16, ribs 0.47 mm (91 %), 3/4 mean 0.81; Δ outline bias mean +0.17 (range +0.06..+0.27), Δ rib mean +0.00 mm
- command: python models/M02_spline_beztwist/E1_tri_count/run.py

### 2026-11-23 23:02 — E2 triangle width (fill) x placement (kernel v3)
- arc f=0.5: front 12/19, 3/4 15/19, outline max 2.10, ribs 0.47 mm (91 %), 3/4 mean 0.81; Δ outline bias mean +0.12 (range +0.06..+0.16), Δ rib mean +0.00 mm
- arc f=0.7: front 12/19, 3/4 15/19, outline max 2.07, ribs 0.47 mm (91 %), 3/4 mean 0.80; Δ outline bias mean +0.08 (range +0.04..+0.11), Δ rib mean +0.00 mm
- arc f=0.85: front 13/19, 3/4 13/19, outline max 2.04, ribs 0.47 mm (91 %), 3/4 mean 0.79; Δ outline bias mean +0.05 (range +0.02..+0.06), Δ rib mean +0.00 mm
- arc f=1.0 (own): front 14/19, 3/4 13/19, outline max 2.00, ribs 0.47 mm (91 %), 3/4 mean 0.78; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- angle_half f=0.5: front 12/19, 3/4 14/19, outline max 2.17, ribs 0.47 mm (91 %), 3/4 mean 0.83; Δ outline bias mean +0.12 (range +0.01..+0.26), Δ rib mean -0.00 mm
- angle_half f=0.7: front 12/19, 3/4 13/19, outline max 2.17, ribs 0.47 mm (91 %), 3/4 mean 0.82; Δ outline bias mean +0.09 (range -0.03..+0.26), Δ rib mean -0.00 mm
- angle_half f=0.85: front 12/19, 3/4 13/19, outline max 2.17, ribs 0.47 mm (91 %), 3/4 mean 0.81; Δ outline bias mean +0.05 (range -0.08..+0.26), Δ rib mean -0.00 mm
- angle_half f=1.0: front 12/19, 3/4 12/19, outline max 2.17, ribs 0.47 mm (91 %), 3/4 mean 0.81; Δ outline bias mean +0.01 (range -0.16..+0.26), Δ rib mean -0.00 mm
- command: python models/M02_spline_beztwist/E2_tri_width/run.py

### 2026-11-23 23:02 — E3 triangle height (kernel v3)
- H=1.5: front 0/19, 3/4 0/19, outline max 1.97, ribs 0.47 mm (91 %), 3/4 mean 1.51; Δ outline bias mean -1.50 (range -1.50..-1.49), Δ rib mean +0.00 mm
- H=2.0: front 0/19, 3/4 2/19, outline max 1.47, ribs 0.47 mm (91 %), 3/4 mean 1.13; Δ outline bias mean -1.00 (range -1.00..-1.00), Δ rib mean +0.00 mm
- H=3.0 (own): front 14/19, 3/4 13/19, outline max 2.00, ribs 0.47 mm (91 %), 3/4 mean 0.78; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- H=4.0: front 0/19, 3/4 3/19, outline max 3.00, ribs 0.47 mm (91 %), 3/4 mean 1.42; Δ outline bias mean +1.00 (range +1.00..+1.00), Δ rib mean +0.00 mm
- H=5.0: front 0/19, 3/4 0/19, outline max 4.00, ribs 0.47 mm (91 %), 3/4 mean 2.42; Δ outline bias mean +2.00 (range +1.99..+2.00), Δ rib mean +0.00 mm
- command: python models/M02_spline_beztwist/E3_tri_height/run.py

### 2026-11-23 23:03 — E4 twist (a: scale whole curve, b: 1-knot bumps) (kernel v3)
- twist x0.94: front 3/19, 3/4 2/19, outline max 2.88, ribs 2.09 mm (40 %), 3/4 mean 1.77; Δ outline bias mean -0.26 (range -2.25..+1.87), Δ rib mean +2.05 mm
- twist x0.97: front 5/19, 3/4 4/19, outline max 2.00, ribs 1.13 mm (53 %), 3/4 mean 1.24; Δ outline bias mean -0.12 (range -1.10..+0.96), Δ rib mean +0.85 mm
- twist x1.0: front 14/19, 3/4 13/19, outline max 2.00, ribs 0.47 mm (91 %), 3/4 mean 0.78; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- twist x1.03: front 4/19, 3/4 10/19, outline max 2.00, ribs 1.07 mm (59 %), 3/4 mean 0.83; Δ outline bias mean +0.11 (range -1.00..+1.08), Δ rib mean +0.78 mm
- twist x1.06: front 3/19, 3/4 7/19, outline max 2.14, ribs 1.95 mm (45 %), 3/4 mean 1.25; Δ outline bias mean +0.22 (range -1.77..+2.13), Δ rib mean +1.87 mm
- 1-knot bumps: mean locality share 0.41 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.30 of 1 °
- command: python models/M02_spline_beztwist/E4_twist/run.py

### 2026-11-23 23:03 — E5 radius (a: offset whole curve, b: 1-knot bumps) (kernel v3)
- r0 -2 mm: front 0/19, 3/4 0/19, outline max 2.19, ribs 1.17 mm (56 %), 3/4 mean 1.83; Δ outline bias mean -1.90 (range -1.99..-1.65), Δ rib mean +0.89 mm
- r0 -1 mm: front 0/19, 3/4 7/19, outline max 1.28, ribs 0.74 mm (73 %), 3/4 mean 1.12; Δ outline bias mean -0.95 (range -1.00..-0.83), Δ rib mean +0.35 mm
- r0 +0 mm: front 14/19, 3/4 13/19, outline max 2.00, ribs 0.47 mm (91 %), 3/4 mean 0.78; Δ outline bias mean +0.00 (range +0.00..+0.00), Δ rib mean +0.00 mm
- r0 +1 mm: front 0/19, 3/4 4/19, outline max 3.00, ribs 0.70 mm (73 %), 3/4 mean 1.28; Δ outline bias mean +0.95 (range +0.83..+1.00), Δ rib mean +0.28 mm
- r0 +2 mm: front 0/19, 3/4 0/19, outline max 4.00, ribs 1.15 mm (58 %), 3/4 mean 2.18; Δ outline bias mean +1.90 (range +1.65..+1.99), Δ rib mean +0.85 mm
- 1-knot bumps: mean locality share 0.63 (1.0 = the whole change stays in the 2 segments at the knot), median achieved bump 0.49 of 1 mm
- command: python models/M02_spline_beztwist/E5_radius/run.py

### 2026-11-23 23:03 — E6 sections (count x placement) (kernel v3)
- uniform_z n=8: loft deviation from exact max 1.70 / mean 0.198 mm; front 10/19, 3/4 14/19
- uniform_z n=11: loft deviation from exact max 1.89 / mean 0.184 mm; front 11/19, 3/4 13/19
- uniform_z n=15: loft deviation from exact max 1.12 / mean 0.131 mm; front 14/19, 3/4 13/19
- uniform_z n=20: loft deviation from exact max 0.26 / mean 0.044 mm; front 13/19, 3/4 13/19
- uniform_z n=30: loft deviation from exact max 0.09 / mean 0.009 mm; front 13/19, 3/4 13/19
- uniform_z n=39: loft deviation from exact max 0.05 / mean 0.003 mm; front 13/19, 3/4 13/19
- adaptive n=8: loft deviation from exact max 1.79 / mean 0.210 mm; front 10/19, 3/4 14/19
- adaptive n=11: loft deviation from exact max 1.51 / mean 0.176 mm; front 14/19, 3/4 13/19
- adaptive n=15: loft deviation from exact max 0.56 / mean 0.091 mm; front 12/19, 3/4 12/19
- adaptive n=20: loft deviation from exact max 0.08 / mean 0.011 mm; front 13/19, 3/4 13/19
- adaptive n=30: loft deviation from exact max 0.06 / mean 0.006 mm; front 13/19, 3/4 13/19
- adaptive n=39: loft deviation from exact max 0.04 / mean 0.003 mm; front 13/19, 3/4 13/19
- knots10 n=20: loft deviation from exact max 0.26 / mean 0.044 mm; front 13/19, 3/4 13/19
- own sections: {'mode': 'uniform_z', 'count': 15}
- loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+
- command: python models/M02_spline_beztwist/E6_sections/run.py

### 2026-11-23 23:14 — final round (kernel v3) — results recorded (kernel v3)
- rank 2/10, score 0.702; front 14/19, 3/4 13/19, ribs 0.47 mm, cost 94.3 (best start pool:M01_E0)
- orientation offset -1.66°; MODEL.md: 'Final round — kernel v3' section appended; verified by judge/verify_e0.py
