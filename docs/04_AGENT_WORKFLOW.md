# 4 — Multi-agent workflow

Read this before spawning a subagent, and (as a subagent) before starting your task.

---

## 4.1 Roles

| Role | Who | Writes to | Never |
|---|---|---|---|
| **Orchestrator** | main Claude session | `fit_ribs_result.json` (via the apply procedure), Fusion scripts (only via `apply_ribs_fit.py`), `PROGRESS.md`, `docs/`, `segments.json`, shared tools | fits a segment and accepts it without a verifier |
| **lamp-probe** | `.claude/agents/lamp-probe.md` | `work/probes/<name>/` | edits model, fit, scripts or docs |
| **segment-fitter** | `.claude/agents/segment-fitter.md` | `work/candidates/<id>/` | touches the active fit, Fusion scripts, or another segment's parameters without saying so |
| **fit-verifier** | `.claude/agents/fit-verifier.md` | `work/verify/<id>/` | trusts numbers it did not recompute itself |
| **model-runner** | `.claude/agents/model-runner.md` | its own `models/Mxx_*/` only (model study, `docs/05_EXPERIMENTS.md`) | edits `models/_common/`, targets, docs or other models |
| **User** | project owner (human) | Fusion runs, final decisions on targets and look | — |

Ad-hoc questions (for example, "count the ribs in the drawing", or "measure the creases in the top photo") go to a
general-purpose agent with the same rules as `lamp-probe`.

---

## 4.2 The loop

```
 ┌─► 1 MEASURE   orchestrator: per-segment table for the active fit (docs/03 §3.4)
 │   2 DIAGNOSE  orchestrator: worst failing segment + candidate parameters (docs/02)
 │   3 FIT       segment-fitter × 1–3 in parallel (hypotheses, or non-adjacent segments)
 │   4 VERIFY    fit-verifier per candidate → ACCEPT / REJECT
 │   5 APPLY     orchestrator: best ACCEPTED candidate → active fit → apply_ribs_fit.py → log
 │   6 FUSION    user, when a segment reaches its targets (or every few applies)
 └── repeat until every segment meets its targets
```

The probes (Phase 1) feed step 2. Re-probe when the parametrisation changes (Phase 2).

---

## 4.3 File contracts

All agent output lives under `work/` (JSON tracked by git, PNGs ignored). Each run gets its own folder:
`work/<kind>/<YYYYMMDD-HHMM>_<short-tag>/`.

**Probe** → `result.json` + `summary.md`
```json
{"param": "twist_points[3].deg", "base_fit": "<sha1 of fit_ribs_result.json>",
 "steps": [-2, -1, 1, 2],
 "delta": {"S01": {"sil_bias": 0.0, "sil_max": 0.0, "rib_mean": 0.0, "within1": 0.0}, "S02": {}, "...": {}, "S19": {}},
 "per_unit": {"S10": {"rib_mean": -0.21}}, "linear": true, "spill": ["S08", "S09", "S10", "S11", "S12"], "notes": "..."}
```

**Candidate** → `candidate.json` + `report.md` + optional PNGs
```json
{"segments": ["S09", "S10", "S11"], "hypothesis": "twist only", "base_fit": "<sha1>",
 "params_changed": ["twist_points[2]", "twist_points[3]"],
 "BEZIER_CONTROL_POINTS": [], "twist_points": [], "LOBE_DEPTH_Z": [], "LOBE_DEPTH_K": [],
 "metrics_before": {"S01": {}, "...": {}, "S19": {}},
 "metrics_after":  {"S01": {}, "...": {}, "S19": {}},
 "command": "exact command line that produced it"}
```
The shape keys are exactly those of `fit_ribs_result.json`, so an accepted candidate can be copied in directly.

**Verdict** → `verdict.json` + `verdict.md`
```json
{"candidate": "work/candidates/.../candidate.json", "verdict": "ACCEPT | REJECT | STALE",
 "recomputed": {"S01": {}, "...": {}, "S19": {}},
 "matches_claim": true, "regressions": [], "constraint_failures": [], "reasons": "..."}
```
`base_fit` = `sha1sum fit_ribs_result.json` at the start of the run. If it no longer matches the active fit,
the verdict is **STALE**: re-run the candidate on the new base.

---

## 4.4 Rules for every agent

1. Read `CLAUDE.md`, then the doc sections named in your task. Use `segments.json` for boundaries and targets.
2. Run Python from the repo root. Change parameters **in-process** (for example, `m.TRI_H = 4.0`, or pass curves to
   functions). Never edit `model.py`, fit files or Fusion scripts to run an experiment.
3. Report **all 19 segments**, before → after, even when you worked on one.
4. Give numbers, not adjectives. Include the exact command line so the run can be repeated.
5. If the drawing looks unreliable at a checkpoint (tracer jumped lines, rib hidden), say so and exclude it explicitly.
   Don't fit to it silently.
6. Long fits: cap `max_nfev`, and report if the optimiser stopped on the cap.
7. Your final message is all the orchestrator sees. Put the verdict and numbers first and file paths last.

**Orchestrator only**
- Apply procedure: copy `fit_ribs_result.json` → `work/history/<timestamp>_fit_ribs_result.json`, write the new one,
  `python apply_ribs_fit.py`, re-measure, update `docs/03_SEGMENTS.md` §3.4 and `PROGRESS.md`. One apply at a time.
- Parallel fitters only on parameter-disjoint segments (`docs/03` §3.5), or several hypotheses for one segment.
- Spawn agents only for real fan-out (probes, competing hypotheses, independent verification). Small checks are
  done inline.

---

## 4.5 Spawn templates

**Probe**
> Agent `lamp-probe`. Parameter: `<name>` (for example, `LOBE_DEPTH_K[3]`). Steps: `<±values>`. Base: active fit.
> Report per-segment deltas, per-unit sensitivity, spill, linearity. Output to `work/probes/`.

**Segment fit**
> Agent `segment-fitter`. Segment `<S#>` (z `<z0>`–`<z1>`). Problem: `<metric values from §3.4>`.
> Hypothesis: `<which parameters, why>` (from `docs/02`). Free parameters: `<list>`, everything else frozen.
> Other segments: regression rule from `segments.json`. Output a candidate to `work/candidates/`.

**Verify**
> Agent `fit-verifier`. Candidate: `<path>`. Recompute every metric from scratch, check regressions and
> Fusion constraints, return ACCEPT / REJECT / STALE with numbers.

---

## 4.6 Phase plan

| Phase | Goal | Work | Agents | Done when |
|---|---|---|---|---|
| **0** setup | shared understanding | these docs, `segments.json`, agent definitions | — | ✅ 2026-11-23 |
| **1** learn = **model study** | which model setup fits best, and what each parameter does in each model | `docs/05_EXPERIMENTS.md`: build `models/_common/` (per-segment scoring = the planned `seg_eval.py`, sweeps = the planned `probe.py`) + `targets/`; models M01–M10 × experiments E0–E5; judge; also measure the drawing's rib count and noise floor | one agent per model (batches of 3–5) + `fit-verifier` | `judge/RESULTS.md` done; user picks a model |
| **2** localise | segments own their parameters | knot-Hermite curves (`03` §3.5) in `model.py`, fitters, `apply_ribs_fit.py`, Fusion scripts, LampWall; refit to the current shape (≤ 0.1 mm); per-segment Fusion build | orchestrator + `fit-verifier` | new curves reproduce the current fit; Fusion check passes |
| **3** fit | every segment meets its targets | loop §4.2, worst first: waist S08–S11 → shoulder/neck ribs S12–S19 → S07 → S01/S04 | `segment-fitter` + `fit-verifier` | all segments green in §3.4 |
| **4** confirm | Fusion = model = drawing | DumpCanvas + TwoTriangles + final build; optional base-shape upgrade (cos 8θ) | user + orchestrator | Fusion outline within targets |

## 4.7 Tooling status

| Tool | Status | Until it exists |
|---|---|---|
| `model.py`, `checkpoints.py`, `fit_ribs.py`, `views/fit_joint.py`, `apply_ribs_fit.py` | ✅ exist | — |
| `seg_eval.py` — per-segment metrics (front outline, ribs every 2 mm, 3/4 rows) for a fit JSON | ⏳ Phase 1 | compute with `checkpoints.trace_all` + `model_rib` + `model.silhouettes`, binned by `segments.json` |
| `probe.py` — perturb one parameter, write the probe JSON | ⏳ Phase 1 | in-process perturbation + the above |
| `fit_seg.py` — fit one segment's knots with the rest frozen | ⏳ Phase 2 | `fit_ribs.py` residuals plus a penalty on change outside the segment |
