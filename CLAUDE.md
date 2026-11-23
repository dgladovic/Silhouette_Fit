# Lamp Silhouette Fit

Goal: a parametric 3D model (Fusion 360 Python scripts) of a twisted, 4-lobed, ribbed lamp shade that matches the
reference drawings and photos in `reference/`, matching **both the outline and the rib paths at every height**.

## Read before you work

| Task | Read first |
|---|---|
| Anything | this file, then `PROGRESS.md` → "Current status" |
| Geometry, the base (cross-section), how it changes with height, how the fit works | `docs/01_MODEL_AND_METHODS.md` |
| Changing or choosing a parameter (profile, twist, lobe depth, triangle size/count, sections) | `docs/02_PARAMETERS.md` |
| A height band looks wrong, fitting, accepting a result | `docs/03_SEGMENTS.md` + `segments.json` |
| Spawning a subagent, or working as one | `docs/04_AGENT_WORKFLOW.md` (agents: `.claude/agents/`) |
| Model study: model setups M01–M10, the 5-parameter sweeps, the judge, geometry options | `docs/05_EXPERIMENTS.md`, `targets/README.md` |

The user's **earlier scripts** (custom-spline base, cubic and Bézier twists, keyframe tables, the tkinter Bézier
designer tools) live one level up in `../` (`BaseScript`, `FulLTextureLamp`, `Grasshoper`, `Grasshoper_full`,
`Test_osnovna`, …). Read them as reference only. Never edit them from here.

## Ground rules

1. **Units**: mm and degrees in Python. The Fusion API uses cm; the scripts divide by 10. `max_height_cm = 190.0` in
   the Fusion scripts is really mm.
2. **One geometry, two copies**: `model.py` replicates the Fusion scripts exactly. Change one → change the other in the
   same task, and flag that a Fusion re-check (DumpCanvas / TwoTriangles) is needed.
3. **Active model** = `ACTIVE_MODEL.json` → **M03** (`models/M03_spline_bez2d`, since 2026-11-24). Change it only via the
   segment loop: candidate in `work/candidates/` → `fit-verifier` → copy to `E0_fit/params.json` (back up first to
   `work/history/`) → re-export the Fusion script (`fusion_template.export`) → log in the model's `PROGRESS.md`.
   The old rose pipeline (`fit_ribs_result.json`, `apply_ribs_fit.py`, `Grasshoper_full/`) is M05, kept as reference only.
4. **Per-segment reporting**: every result is shown for all 19 segments (S01–S19, 10 mm each), before → after. A fix that breaks a
   neighbour segment is not a fix (regression rule in `segments.json`).
5. **Measure, don't guess**: if a parameter effect isn't in `docs/02_PARAMETERS.md`, probe it and add the row.
6. **Fusion can't run here.** Steps that need it go to the user as exact instructions (which script, which settings,
   what to look at).
7. **Keep the docs true**: after a task, update `PROGRESS.md` and any doc whose numbers or claims changed.
   Fix a doc as soon as you find it wrong.
8. `backup_*/` and `experiments/` are frozen records. Don't edit them. Agent output goes to `work/`.
9. If the Fusion canvas is moved or rescaled, run DumpCanvas and update `measure_canvas.py` before measuring anything.
10. **Model study history**: every `models/<model>/` folder and `models/_common/` has a `PROGRESS.md`. Append an
    entry for every change, run and result. It is append-only; only the status block at the top gets overwritten.
    Read it before touching that model.
11. **Fusion**: a Fusion MCP is installed. Use it **read-only** (inspect the design, bodies, sketches) unless the
    user says otherwise; the user runs builds manually. Fusion ground truth goes to `fusion_runs/`.

## Key commands

```bash
python checkpoints.py          # 10 mm error table for the active fit (+ checkpoints.png)
python fit_ribs.py             # fit outline + traced ribs (front drawing)
python views/fit_joint.py      # joint fit front + 3/4 drawing   (--apply makes it active)
python apply_ribs_fit.py       # push fit_ribs_result.json into all Fusion scripts + LampWall
python expected_triangles.py   # images to compare with the Fusion TwoTriangles build
```
