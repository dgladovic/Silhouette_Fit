# Fusion runs — ground truth from real Fusion builds

The Python kernel *simulates* what Fusion builds. The files here are what Fusion *actually* built, measured
with the `DumpCanvas` script. They check the loft simulator (section positions, E6), the custom spline base and
the equal-angle tooth placement. See `docs/05_EXPERIMENTS.md` §5.10, steps 0 and 3–4.

## F1 — what to run (manual, ~4 builds)

**Rule for every run:** start from a **new, empty design** (File → New Design). DumpCanvas measures *every visible
body* in the design, so leftovers from an earlier build would mix into the numbers.

DumpCanvas always writes to `Silhouette_Fit/fusion_dump.txt`. **After each run, move that file into this
folder under the name in the table.** (The original `fusion_dump.txt` is in git; Claude restores it afterwards.)

| Run | Script to run in Fusion | Change before running | Then | Save the dump as |
|---|---|---|---|---|
| F1-1 | `Silhouette_Fit/Grasshoper_full` | in `run()`: `num_sections = 8` | run `Silhouette_Fit/DumpCanvas` | `fusion_runs/F1-1_M05_sections08.txt` |
| F1-2 | `Silhouette_Fit/Grasshoper_full` | `num_sections = 15` (the current value) | run DumpCanvas | `fusion_runs/F1-2_M05_sections15.txt` |
| F1-3 | `Silhouette_Fit/Grasshoper_full` | `num_sections = 30` | run DumpCanvas | `fusion_runs/F1-3_M05_sections30.txt` |
| F1-4 | `Lamp_scripts/BaseScript` | nothing, run as it is (11 sections, custom spline base, 22 equal-angle teeth, 2.4 mm) | run DumpCanvas | `fusion_runs/F1-4_M01_basescript.txt` |

After F1-3: **set `num_sections` back to 15** in `Grasshoper_full.py`.

Notes:
- Don't change anything else in the scripts. The kernel reproduces them exactly as they are on disk now.
- If a build fails or shows a warning (for example, "generated N wedge profiles instead of M" in
  `generator_debug.log`), save the dump anyway. Also copy the log here as `F1-x_generator_debug.log`.
- Roughly how long each build took is useful (the section count costs build time). Note it below.

## Log
| Run | Date | Build time | Notes |
|---|---|---|---|
| F1-1 | | | |
| F1-2 | | | |
| F1-3 | | | |
| F1-4 | | | |

## F2 — build the top 2 models (manual)

The kernel generated one Fusion script per model (table-driven, one quarter, the model's own sections and teeth).
**These generated scripts have not been run in Fusion yet**, so this is also their first test.

| Run | Script folder to add in Fusion's Scripts dialog | Then | Save the dump as |
|---|---|---|---|
| F2-1 | `Silhouette_Fit/models/M03_spline_bez2d/fusion/M03` (30 sections, 23 teeth, equal angle) | DumpCanvas | `fusion_runs/F2-1_M03.txt` |
| F2-2 | `Silhouette_Fit/models/M02_spline_beztwist/fusion/M02` (15 sections, 22 teeth, arc) | DumpCanvas | `fusion_runs/F2-2_M02.txt` |

Same rules as F1: a new empty design for each run, move `fusion_dump.txt` after each run, note the build time and any
warning. Claude then compares each dump with the kernel's as-built prediction (as in Gate B/C).
