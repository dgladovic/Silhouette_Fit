# Targets — the images every model is fitted to and scored against

Two targets, one folder each. Every model and every experiment reads targets **only** from here.

| Folder | Image | Used for | Default source |
|---|---|---|---|
| `front/` | straight-on front view | **fitting**: outline every 2 mm + rib checkpoints | `reference/fusion_rel_size_YZ.jpg` |
| `view34/` | 3/4 view from above | **held-out scoring**: outline per image row | `reference/view34_drawing.png` |

## What each target folder must contain

An image without calibration can't be measured in mm. So each folder holds:

| File | Content | Made by |
|---|---|---|
| `image.(png/jpg)` | the drawing or silhouette | you |
| `calibration.json` (front) | mm per pixel horizontal and vertical, pixel column of the lamp axis, the z (mm) of the top and bottom rim rows, mirrored yes/no | `measure_canvas.py` logic (from the Fusion canvas) or measured from the 190 mm shade height |
| `camera.json` (3/4) | rotation, elevation, scale, position, perspective | `views/fit_view34.py` |
| `outline.csv` | left/right outline per height (mm) | extraction script (`models/_common/`) |
| `ribs.json` (front only) | traced rib lines (z, x in mm) | `checkpoints.trace_all` |

## Replacing a target

1. Put the new image in the folder.
2. Calibrate it (and re-fit the camera for the 3/4 view).
3. Re-run the extraction.
4. **Re-run E0 for every model.** Results against different targets are not comparable.

Note the change and the date here.

## Log
- 2026-11-23: folder created. Targets confirmed by the user: front drawing + 3/4 drawing (defaults above).
  They get copied in and extracted in build step 1 (`docs/05_EXPERIMENTS.md` §5.10), together with the noise floors
  and the rib count (§5.5).
