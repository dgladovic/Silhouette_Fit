# Model study — index

Plan: `docs/05_EXPERIMENTS.md`. Kernel: `_common/` (history in `_common/PROGRESS.md`). Judge: `judge/`.
Every model folder: `MODEL.md` (definition, hypothesis, conclusions), `PROGRESS.md` (append-only history),
`model.py`, `E0_fit/` … `E6_sections/` (each with `run.py`), `fusion/<ID>/` (Fusion script), `summary.json`.

| ID | Folder | What | Rank | Front / 3/4 | State |
|---|---|---|---|---|---|
| M01 | `M01_spline_cubic` | custom spline base + keyframe radius + cubic twist (k1, k2, max angle) | **4** (0.623) | 10/19 · 13/19 | final, kernel v3 |
| M02 | `M02_spline_beztwist` | custom spline base + keyframe radius + 5-point Bezier twist (t, deg) | **2** (0.702) | 14/19 · 13/19 | final, kernel v3 |
| M03 | `M03_spline_bez2d` | custom spline base + 7-point 2D Bezier radius + cubic twist at Bezier t | **1** (0.706) | 14/19 · 14/19 | final, kernel v3 |
| M04 | `M04_spline_keyframes` | custom spline base + keyframe radius + keyframe twist (Catmull-Rom, refined per segment) | **5** (0.592) | 10/19 · 13/19 | final, kernel v3 |
| M05 | `M05_rose_bezier` | rose k(z) + 2D Bezier radius + Bezier twist | **6** (0.492) | 6/19 · 10/19 | final, kernel v3 |
| M06 | `M06_rose_knots` | rose k(z) + 10 mm knots radius + 10 mm knots twist | **7** (0.488) | 7/19 · 10/19 | final, kernel v3 |
| M07 | `M07_rose8_knots` | rose + 8θ harmonic c(z) + 10 mm knots radius + 10 mm knots twist | **3** (0.650) | 13/19 · 13/19 | final, kernel v3 |
| M08 | `M08_superformula_knots` | superformula n1(z), n2(z) + 10 mm knots radius + 10 mm knots twist | **9** (0.452) | 5/19 · 10/19 | final, kernel v3 |
| M09 | `M09_rose_logistic` | rose (constant k) + 2D Bezier radius + logistic twist | **10** (0.353) | 1/19 · 7/19 | final, kernel v3 |
| M10 | `M10_rose_ribangle` | rose k(z) + 10 mm knots radius + 10 mm knots rib lean angle (twist = integral tan(alpha)/r0) | **8** (0.453) | 5/19 · 10/19 | final, kernel v3 |

Results: `judge/RESULTS.md`, local page `judge/results.html`.

Quick start for a model folder:
```bash
python -c "import sys; sys.path.insert(0,'models/_common'); import study; study.init_model_dir('models/M0x_name')"
python models/M0x_name/E0_fit/run.py      # then E1_tri_count … E6_sections
python -c "import sys; sys.path.insert(0,'models/_common'); import study; study.write_summary('models/M0x_name')"
```
