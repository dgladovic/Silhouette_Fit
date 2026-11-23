"""
Study runner: model loading, E0 fit, E1-E6 sweeps, summaries, PROGRESS.md logging (docs/05_EXPERIMENTS.md).

Model contract (models/Mxx_*/model.py):
    ID, TITLE, SETTINGS (N, H, placement, target_w, sections), SOURCE (where the settings come from)
    NAMES, P0, LB, UB                        parameter names / start / bounds (numpy-able lists)
    shape(p)       -> Shape(r0=fn, twist=fn, rho=fn[, zt=fn])
    penalty(p)     -> extra residuals (smoothness, soft constraints), may be empty
    constraints(p) -> list of failure strings (empty = buildable)
    optional: refine(p, info, fit, evaluate_both) -> (p, info)  for M04-style key refinement

Run an experiment:  python models/<model>/E3_tri_height/run.py   (each run.py calls run_experiment)
"""
import os, sys, json, time, importlib.util, datetime, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import targets as T
import geometry as G
import score as SC

KERNEL_VERSION = 3
# v3: every model gets a free global orientation offset (deg) appended by the kernel (load_model)
ORIENT = os.environ.get('STUDY_NO_ORIENT') != '1'
ORIENT_BOUND = 15.0
# smoothness penalty (protocol §5.4): weight x 2nd difference of knot/key values, per unit
SMOOTH_W = dict(mm=0.05, deg=0.05, k=2.0)
ROOT = T.ROOT
MODELS = os.path.join(ROOT, 'models')


class Shape:
    def __init__(self, r0, twist, rho, zt=None):
        self.r0, self.twist, self.rho = r0, twist, rho
        if zt is not None:
            self.zt = zt


def _wrap_orient(mod):
    """Kernel v3: append a free global orientation offset (deg) to every model. The rotation of the whole lamp
    relative to the drawing is not part of the shape; twist(0) = 0 had silently fixed it for some models."""
    if getattr(mod, '_orient', False):
        return
    n = len(mod.P0)
    base_shape, base_pen, base_cons = mod.shape, mod.penalty, mod.constraints
    mod.NAMES = list(mod.NAMES) + ['orient_deg']
    mod.P0 = np.r_[np.asarray(mod.P0, float), 0.0]
    mod.LB = np.r_[np.asarray(mod.LB, float), -ORIENT_BOUND]
    mod.UB = np.r_[np.asarray(mod.UB, float), ORIENT_BOUND]

    def shape(p):
        p = np.asarray(p, float); sh = base_shape(p[:n]); o = float(p[n])
        return Shape(sh.r0, (lambda z, f=sh.twist: f(z) + o), sh.rho, getattr(sh, 'zt', None))
    mod.shape = shape
    mod.penalty = lambda p: base_pen(np.asarray(p, float)[:n])
    mod.constraints = lambda p: base_cons(np.asarray(p, float)[:n])
    if hasattr(mod, 'refine'):                 # M04: its internal refits don't carry the offset (logged in kernel PROGRESS)
        mod._refine_disabled = mod.refine
        del mod.refine
    mod._orient = True


def load_model(model_dir):
    model_dir = os.path.abspath(model_dir)
    spec = importlib.util.spec_from_file_location(os.path.basename(model_dir), os.path.join(model_dir, 'model.py'))
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, model_dir)
    spec.loader.exec_module(mod)
    mod.DIR = model_dir
    if ORIENT:
        _wrap_orient(mod)
    return mod


def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


def log(model_dir, title, lines):
    """Append one entry to the model's PROGRESS.md (append-only log)."""
    p = os.path.join(model_dir, 'PROGRESS.md')
    with open(p, 'a', encoding='utf-8') as f:
        f.write(f"\n### {now()} — {title} (kernel v{KERNEL_VERSION})\n" + "\n".join(f"- {l}" for l in lines) + "\n")


def jsonable(o):
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def slim(res):
    """evaluate() result without the big arrays."""
    return dict(seg=res['seg'], tot=res['tot'], camera=res['camera'], built=res['built'])


# ================================================================================================ E0 fit
STAGES = (1e-2, 1e-3, 1e-4)  # diff_step per stage (v2: a coarse first stage steps over the non-smooth rib terms)
POOL = os.path.join(HERE, 'start_pool.json')   # v2 multi-start: shared reference curves r0(z), twist(z)
MAX_NFEV = 200               # per stage


def _resid(model, p, n=None):
    try:
        r = np.r_[SC.fit_residuals(model.shape(p), model.SETTINGS), model.penalty(p)]
        return np.where(np.isfinite(r), r, 50.0)
    except Exception:
        return np.full(n, 50.0)


def fit(model, p0=None, max_nfev=MAX_NFEV):
    from scipy.optimize import least_squares
    lb, ub = np.asarray(model.LB, float), np.asarray(model.UB, float)
    x0 = np.clip(np.asarray(p0 if p0 is not None else model.P0, float), lb + 1e-7, ub - 1e-7)
    n = len(_resid(model, x0))
    best, caps = None, []
    for ds in STAGES:
        r = least_squares(lambda p: _resid(model, p, n), x0 if best is None else best.x, bounds=(lb, ub), x_scale='jac',
                          diff_step=ds, loss='soft_l1', f_scale=1.5, xtol=1e-10, ftol=1e-9, gtol=1e-9, max_nfev=max_nfev)
        caps.append(bool(r.status == 0))
        if best is None or r.cost < best.cost:
            best = r
    return best.x, dict(cost=float(best.cost), nfev=int(best.nfev), cap_hit=caps)


def project_start(model, ref, w_tw=0.5):
    """Model parameters whose r0(z) / twist(z) best match a reference curve pair (smooth least squares on the curves)."""
    from scipy.optimize import least_squares
    Z = np.asarray(ref['z'], float); R = np.asarray(ref['r0'], float); TW = np.asarray(ref['twist'], float)
    lb, ub = np.asarray(model.LB, float), np.asarray(model.UB, float)
    x0 = np.clip(np.asarray(model.P0, float), lb + 1e-7, ub - 1e-7)
    sc = np.maximum(1.0, np.abs(x0))

    def res(p):
        try:
            sh = model.shape(p)
            r = np.r_[sh.r0(Z) - R, w_tw * (sh.twist(Z) - TW), np.asarray(model.penalty(p), float), 1e-3 * (p - x0) / sc]
            return np.where(np.isfinite(r), r, 1e3)
        except Exception:
            return np.full(2 * len(Z) + len(np.asarray(model.penalty(x0))) + len(x0), 1e3)
    r = least_squares(res, x0, bounds=(lb, ub), x_scale='jac', max_nfev=300)
    return r.x


def fit_multistart(model):
    """Kernel v2 E0: fit from the model's own (historical) start AND from every curve set in the shared pool projected
    onto the model's parameters; keep the lowest cost. All starts are logged."""
    starts = [('own start (P0)', np.asarray(model.P0, float))]
    if os.path.exists(POOL):
        for ref in json.load(open(POOL))['curves']:
            try:
                starts.append((f"pool:{ref['name']}", project_start(model, ref)))
            except Exception as e:
                starts.append((f"pool:{ref['name']} (projection failed: {e})", None))
    runs, best = [], None
    for name, p0 in starts:
        if p0 is None:
            runs.append(dict(start=name, cost=None)); continue
        p, info = fit(model, p0)
        runs.append(dict(start=name, cost=info['cost'], nfev=info['nfev'], cap_hit=info['cap_hit']))
        if best is None or info['cost'] < best[1]['cost']:
            best = (p, info, name)
    p, info, name = best
    info = dict(info, best_start=name, starts=runs)
    return p, info


def evaluate_both(model, p, camera=None):
    sh = model.shape(p)
    ex = SC.evaluate(sh, model.SETTINGS, built=False, camera=camera, fit_cam=True)
    bu = SC.evaluate(sh, model.SETTINGS, built=True, camera=ex['camera'], fit_cam=True)
    return ex, bu


def run_E0(model_dir):
    import plots as PL
    model = load_model(model_dir)
    out = os.path.join(model_dir, 'E0_fit'); os.makedirs(out, exist_ok=True)
    t0 = time.time()
    ex0, bu0 = evaluate_both(model, model.P0)
    p, info = fit_multistart(model)
    if hasattr(model, 'refine'):                         # M04-style: add keys where segments fail (protocol §5.2)
        p, info = model.refine(p, info, fit, evaluate_both)
    ex, bu = evaluate_both(model, p)
    info['fit_seconds'] = round(time.time() - t0, 1)
    cons = model.constraints(p)
    json.dump(jsonable(dict(names=list(model.NAMES), values=list(map(float, p)), settings=model.SETTINGS,
                            camera=bu['camera'], kernel=KERNEL_VERSION)), open(os.path.join(out, 'params.json'), 'w'), indent=1)
    json.dump(jsonable(dict(exact=slim(ex), built=slim(bu), start_exact=slim(ex0), start_built=slim(bu0), fit=info,
                            constraints=cons)), open(os.path.join(out, 'metrics.json'), 'w'), indent=1)
    import fusion_template as FT
    fpath = FT.export(model, p, model_dir, KERNEL_VERSION)
    sh = model.shape(p)
    PL.overlay_front(sh, model.SETTINGS, os.path.join(out, 'overlay_front.png'), True, f"{model.ID} E0 as built")
    PL.overlay_v34(sh, model.SETTINGS, bu['camera'], os.path.join(out, 'overlay_v34.png'), True, f"{model.ID} E0")
    rep = [f"# {model.ID} — E0 fit\n", f"Settings: `{model.SETTINGS}`  ", f"Parameters: {len(p)} · fit {info['fit_seconds']} s · "
           f"nfev {info['nfev']} · cap hit {info['cap_hit']} · constraints: {cons or 'OK'}\n",
           "## As built (judge uses this)\n", SC.table(bu), "\n## Exact curves\n", SC.table(ex),
           "\n## Start values (before fit), as built\n", SC.table(bu0)]
    open(os.path.join(out, 'report.md'), 'w', encoding='utf-8').write("\n".join(rep))
    tb, te, t0b = bu['tot'], ex['tot'], bu0['tot']
    log(model_dir, 'E0 fit', [
        f"start (as built): front {t0b['front_pass']}/19, 3/4 {t0b['v34_pass']}/19, ribs {t0b['rib_mean']:.2f} mm",
        f"result (as built): front {tb['front_pass']}/19, 3/4 {tb['v34_pass']}/19, outline max {tb['sil_max']:.2f}, "
        f"ribs {tb['rib_mean']:.2f} mm / {tb['within1']:.0f} %, 3/4 mean {tb['v34_mean']:.2f}",
        f"exact curves: front {te['front_pass']}/19, 3/4 {te['v34_pass']}/19",
        f"{len(p)} params, {info['fit_seconds']} s, nfev {info['nfev']}, cap hit {info['cap_hit']}, constraints {cons or 'OK'}",
        "multi-start (cost per start): " + ", ".join(f"{r['start']} {r['cost']:.1f}" if r['cost'] is not None else r['start'] for r in info.get('starts', [])) + f" -> best: {info.get('best_start')}",
        f"Fusion script: {os.path.relpath(fpath, ROOT)}",
        f"command: python models/{os.path.basename(model_dir)}/E0_fit/run.py"])
    return p, ex, bu


def load_E0(model_dir):
    model = load_model(model_dir)
    d = json.load(open(os.path.join(model_dir, 'E0_fit', 'params.json')))
    return model, np.array(d['values']), d['camera']


# ================================================================================================ sweeps
SEG_KEYS = ('sil_max', 'sil_bias', 'rib_mean', 'within1', 'v34_mean')


def _seg_small(res):
    return [{k: r[k] for k in ('id',) + SEG_KEYS + ('pass_front', 'pass_v34')} for r in res['seg']]


def _delta(seg, base):
    out = []
    for a, b in zip(seg, base):
        d = {'id': a['id']}
        for k in SEG_KEYS:
            d[k] = None if a[k] is None or b[k] is None else a[k] - b[k]
        out.append(d)
    return out


class _Wrap:
    """Shape with a transformed curve (E4a / E5a)."""
    def __init__(self, sh, r0=None, twist=None):
        self.r0 = r0 or sh.r0; self.twist = twist or sh.twist; self.rho = sh.rho
        if hasattr(sh, 'zt'):
            self.zt = sh.zt


def _levels(model, sh, cam, base_res, variants):
    rows = []
    for label, shape, st in variants:
        res = SC.evaluate(shape, st, built=True, camera=cam)
        rows.append(dict(label=label, settings=st, tot=res['tot'], seg=_seg_small(res),
                         delta=_delta(_seg_small(res), _seg_small(base_res))))
    return rows


def _write(model_dir, folder, name, payload, plot_levels=None, lines=()):
    import plots as PL
    out = os.path.join(model_dir, folder); os.makedirs(out, exist_ok=True)
    json.dump(jsonable(payload), open(os.path.join(out, 'results.json'), 'w'), indent=1)
    if plot_levels:
        for key, yl in (('sil_bias', 'Δ outline bias (mm)'), ('rib_mean', 'Δ rib mean (mm)'), ('v34_mean', 'Δ 3/4 mean (mm)')):
            PL.delta_lines([(r['label'], r['delta']) for r in plot_levels], key, os.path.join(out, f'delta_{key}.png'),
                           f"{payload['model']} {name}: {key}", yl)
    md = [f"# {payload['model']} — {name}\n"] + [f"- {l}" for l in lines]
    open(os.path.join(out, 'summary.md'), 'w', encoding='utf-8').write("\n".join(md) + "\n")
    log(model_dir, name, list(lines) + [f"command: python models/{os.path.basename(model_dir)}/{folder}/run.py"])


def _tot_line(r):
    t = r['tot']
    db = [d['sil_bias'] for d in r['delta'] if d['sil_bias'] is not None]
    dr = [d['rib_mean'] for d in r['delta'] if d['rib_mean'] is not None]
    return (f"{r['label']}: front {t['front_pass']}/19, 3/4 {t['v34_pass']}/19, outline max {t['sil_max']:.2f}, "
            f"ribs {t['rib_mean']:.2f} mm ({t['within1']:.0f} %), 3/4 mean {t['v34_mean']:.2f}; "
            f"Δ outline bias mean {np.mean(db):+.2f} (range {min(db):+.2f}..{max(db):+.2f}), Δ rib mean {np.mean(dr):+.2f} mm")


def run_E1(model_dir):
    model, p, cam = load_E0(model_dir); sh = model.shape(p); st0 = model.SETTINGS
    base = SC.evaluate(sh, st0, built=True, camera=cam)
    lv = sorted(set([12, 16, 22, 30, 45, int(st0['N'])]))
    rows = _levels(model, sh, cam, base, [(f"N={n}" + (' (own)' if n == st0['N'] else ''), sh, dict(st0, N=n)) for n in lv])
    _write(model_dir, 'E1_tri_count', 'E1 triangle count', dict(model=model.ID, levels=rows), rows, [_tot_line(r) for r in rows])


def run_E2(model_dir):
    model, p, cam = load_E0(model_dir); sh = model.shape(p); st0 = model.SETTINGS
    base = SC.evaluate(sh, st0, built=True, camera=cam)
    var = [(f"{pl} f={f}" + (' (own)' if pl == st0['placement'] and f == st0.get('fill', 1.0) else ''), sh,
            dict(st0, placement=pl, fill=f)) for pl in ('arc', 'angle_half') for f in (0.5, 0.7, 0.85, 1.0)]
    rows = _levels(model, sh, cam, base, var)
    _write(model_dir, 'E2_tri_width', 'E2 triangle width (fill) x placement', dict(model=model.ID, levels=rows), rows,
           [_tot_line(r) for r in rows])


def run_E3(model_dir):
    model, p, cam = load_E0(model_dir); sh = model.shape(p); st0 = model.SETTINGS
    base = SC.evaluate(sh, st0, built=True, camera=cam)
    lv = sorted(set([1.5, 2.0, 3.0, 4.0, 5.0, float(st0['H'])]))
    rows = _levels(model, sh, cam, base, [(f"H={h}" + (' (own)' if h == st0['H'] else ''), sh, dict(st0, H=h)) for h in lv])
    _write(model_dir, 'E3_tri_height', 'E3 triangle height', dict(model=model.ID, levels=rows), rows, [_tot_line(r) for r in rows])


def _curve_jac(model, p, which, Z):
    p = np.asarray(p, float); f0 = getattr(model.shape(p), which)(Z)
    J = np.zeros((len(Z), len(p)))
    for i in range(len(p)):
        h = 1e-4 * max(1.0, abs(p[i]))
        q1, q2 = p.copy(), p.copy(); q1[i] += h; q2[i] -= h
        J[:, i] = (getattr(model.shape(q1), which)(Z) - getattr(model.shape(q2), which)(Z)) / (2 * h)
    return f0, J


def _bumps(model, p, cam, base, which, amp):
    """E4b / E5b: +amp hat bump (±10 mm) at each 10 mm knot, made with the model's own parameters
    (linear least squares on the curve; the other curve is held fixed)."""
    Z = np.arange(0.0, 190.01, 1.0)
    other = 'r0' if which == 'twist' else 'twist'
    f0, J = _curve_jac(model, p, which, Z)
    _, Jo = _curve_jac(model, p, other, Z)
    scale = np.maximum(1.0, np.abs(p))
    M = np.zeros((20, 19)); rows = []
    for j, zk in enumerate(np.arange(0, 191, 10)):
        b = amp * np.clip(1 - np.abs(Z - zk) / 10.0, 0, None)
        A = np.r_[J, 3.0 * Jo, 1e-2 * np.diag(1 / scale)]
        y = np.r_[b, np.zeros(len(Z)), np.zeros(len(p))]
        dp = np.linalg.lstsq(A, y, rcond=None)[0]
        # small step (largest parameter change <= 0.2 % of its scale): stay in the linear regime, then scale back
        eps = min(0.1, 0.002 / max(np.max(np.abs(dp) / scale), 1e-12))
        sh1 = model.shape(p + eps * dp)
        d = (getattr(sh1, which)(Z) - f0) / eps
        segm = np.array([np.abs(d[(Z >= 10 * s) & (Z <= 10 * s + 10)]).mean() for s in range(19)])
        M[j] = segm
        own = [s for s in (j - 1, j) if 0 <= s < 19]
        share = float(segm[own].sum() / (segm.sum() + 1e-12))
        res = SC.evaluate(sh1, model.SETTINGS, built=True, camera=cam)
        dl = _delta(_seg_small(res), _seg_small(base))
        for row in dl:                                     # per full bump (linear scaling of the small step)
            for k in SEG_KEYS:
                if row[k] is not None:
                    row[k] /= eps
        rows.append(dict(knot=float(zk), achieved=float(d[int(zk)] / amp), locality_share=share,
                         seg_change=list(map(float, segm)), delta=dl))
    return M, rows


def _run_curve(model_dir, which):
    import plots as PL
    model, p, cam = load_E0(model_dir); sh = model.shape(p); st0 = model.SETTINGS
    base = SC.evaluate(sh, st0, built=True, camera=cam)
    if which == 'twist':
        var = [(f"twist x{f}", _Wrap(sh, twist=(lambda z, f=f: f * sh.twist(z))), st0) for f in (0.94, 0.97, 1.0, 1.03, 1.06)]
        folder, name, unit = 'E4_twist', 'E4 twist (a: scale whole curve, b: 1-knot bumps)', '°'
    else:
        var = [(f"r0 {d:+g} mm", _Wrap(sh, r0=(lambda z, d=d: sh.r0(z) + d)), st0) for d in (-2, -1, 0, 1, 2)]
        folder, name, unit = 'E5_radius', 'E5 radius (a: offset whole curve, b: 1-knot bumps)', 'mm'
    rows = _levels(model, sh, cam, base, var)
    M, bumps = _bumps(model, p, cam, base, which, 1.0)
    out = os.path.join(model_dir, folder); os.makedirs(out, exist_ok=True)
    PL.influence_map(M, os.path.join(out, 'influence_map.png'),
                     f"{model.ID}: +1 {unit} {which} bump at each knot, made with the model's own parameters", unit)
    loc = float(np.mean([b['locality_share'] for b in bumps])); ach = float(np.median([b['achieved'] for b in bumps]))
    lines = [_tot_line(r) for r in rows] + [
        f"1-knot bumps: mean locality share {loc:.2f} (1.0 = the whole change stays in the 2 segments at the knot), "
        f"median achieved bump {ach:.2f} of 1 {unit}"]
    _write(model_dir, folder, name, dict(model=model.ID, levels=rows, bumps=bumps, influence=M, locality=loc, achieved=ach), rows, lines)


def run_E4(model_dir):
    _run_curve(model_dir, 'twist')


def run_E5(model_dir):
    _run_curve(model_dir, 'r0')


def run_E6(model_dir):
    model, p, cam = load_E0(model_dir); sh = model.shape(p); st0 = model.SETTINGS
    base = SC.evaluate(sh, st0, built=True, camera=cam)
    exact = G.full_outline(G.points(sh, SC.Z_SCORE, st0, built=False))
    modes = ['uniform_z', 'adaptive'] + (['bezier_t'] if hasattr(sh, 'zt') else [])
    var = [(f"{mo} n={n}", sh, dict(st0, sections=dict(mode=mo, count=n))) for mo in modes for n in (8, 11, 15, 20, 30, 39)]
    var.append(("knots10 n=20", sh, dict(st0, sections=dict(mode='knots10'))))
    rows = _levels(model, sh, cam, base, var)
    for r in rows:
        dev = np.abs(G.full_outline(G.points(sh, SC.Z_SCORE, r['settings'], built=True)) - exact)
        r['loft_dev_max'] = float(dev.max()); r['loft_dev_mean'] = float(dev.mean())
        r['loft_dev_seg'] = [float(dev[(SC.Z_SCORE >= 10 * s) & (SC.Z_SCORE <= 10 * s + 10)].max()) for s in range(19)]
    note = "loft simulator accuracy vs Fusion (Gate B): ±0.5 mm below 15 sections, ≤0.13 mm at 15+"
    lines = [f"{r['label']}: loft deviation from exact max {r['loft_dev_max']:.2f} / mean {r['loft_dev_mean']:.3f} mm; "
             f"front {r['tot']['front_pass']}/19, 3/4 {r['tot']['v34_pass']}/19" for r in rows] + [f"own sections: {st0.get('sections')}", note]
    _write(model_dir, 'E6_sections', 'E6 sections (count x placement)', dict(model=model.ID, own=st0.get('sections'), levels=rows, note=note),
           None, lines)


EXPERIMENTS = {'E0': run_E0, 'E1': run_E1, 'E2': run_E2, 'E3': run_E3, 'E4': run_E4, 'E5': run_E5, 'E6': run_E6}
FOLDERS = {'E0': 'E0_fit', 'E1': 'E1_tri_count', 'E2': 'E2_tri_width', 'E3': 'E3_tri_height', 'E4': 'E4_twist',
           'E5': 'E5_radius', 'E6': 'E6_sections'}


def run_experiment(model_dir, exp):
    return EXPERIMENTS[exp](os.path.abspath(model_dir))


def init_model_dir(model_dir):
    """Create the E*/run.py stubs and the PROGRESS.md skeleton (idempotent)."""
    model_dir = os.path.abspath(model_dir)
    for e, folder in FOLDERS.items():
        d = os.path.join(model_dir, folder); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'run.py'), 'w').write(
            "import os, sys\nHERE = os.path.dirname(os.path.abspath(__file__))\n"
            "sys.path.insert(0, os.path.join(HERE, '..', '..', '_common'))\nimport study\n"
            f"study.run_experiment(os.path.dirname(HERE), '{e}')\n")
    p = os.path.join(model_dir, 'PROGRESS.md')
    if not os.path.exists(p):
        name = os.path.basename(model_dir)
        open(p, 'w', encoding='utf-8').write(
            f"# {name} — progress\n\n## Status  (overwrite this block only)\n- State: not started\n- Best E0 (as built): —\n"
            f"- Next: E0\n\n## Log  (append only, newest at the bottom)\n")


def set_status(model_dir, state, best, nxt):
    p = os.path.join(model_dir, 'PROGRESS.md')
    s = open(p, encoding='utf-8').read()
    head, rest = s.split('## Log', 1)
    head = head.split('## Status')[0] + (f"## Status  (overwrite this block only)\n- State: {state}\n- Best E0 (as built): {best}\n"
                                         f"- Next: {nxt}\n\n")
    open(p, 'w', encoding='utf-8').write(head + '## Log' + rest)


# ================================================================================================ summary for the judge
def smoothness(model, p):
    Z = np.arange(0.0, 190.01, 1.0); sh = model.shape(p)

    def sc(v):
        d2 = np.gradient(np.gradient(v, Z), Z)
        thr = 0.05 * np.abs(d2).max()
        s = np.sign(np.where(np.abs(d2) < thr, 0, d2)); s = s[s != 0]
        return int(np.sum(s[1:] != s[:-1]))
    sr, stw = sc(sh.r0(Z)), sc(sh.twist(Z))
    extra = max(0, sr - 2) + max(0, stw - 1)
    return dict(r0_inflections=sr, twist_inflections=stw, extra=extra, score=1.0 / (1.0 + extra / 2.0))


def write_summary(model_dir):
    model, p, cam = load_E0(model_dir)
    m0 = json.load(open(os.path.join(model_dir, 'E0_fit', 'metrics.json')))

    def R(f):
        q = os.path.join(model_dir, f, 'results.json')
        return json.load(open(q)) if os.path.exists(q) else None
    e4, e5, e6 = R('E4_twist'), R('E5_radius'), R('E6_sections')
    loft20 = None
    if e6:                                   # gate (v3): loft OK (<= 0.3 mm) at <= 39 sections, best placement
        r = [l['loft_dev_max'] for l in e6['levels'] if (l['settings']['sections'].get('count') or 20) <= 39]
        loft20 = min(r) if r else None
    cons = model.constraints(p)
    s = dict(id=model.ID, title=model.TITLE, folder=os.path.basename(model_dir), n_params=len(p), settings=model.SETTINGS,
             source=getattr(model, 'SOURCE', ''), kernel=KERNEL_VERSION,
             built=m0['built']['tot'], exact=m0['exact']['tot'],
             seg_front=[r['pass_front'] for r in m0['built']['seg']], seg_v34=[r['pass_v34'] for r in m0['built']['seg']],
             seg_front_exact=[r['pass_front'] for r in m0['exact']['seg']],
             seg_rib_mean=[r['rib_mean'] for r in m0['built']['seg']], seg_v34_mean=[r['v34_mean'] for r in m0['built']['seg']],
             seg_sil_max=[r['sil_max'] for r in m0['built']['seg']],
             locality=None if not (e4 and e5) else float((e4['locality'] + e5['locality']) / 2),
             locality_twist=e4['locality'] if e4 else None, locality_radius=e5['locality'] if e5 else None,
             smooth=smoothness(model, p), constraints=cons, loft_dev_20=loft20, loft_gate_sections=39,
             buildable=bool(not cons and (loft20 is None or loft20 <= 0.3)), fit=m0['fit'])
    json.dump(jsonable(s), open(os.path.join(model_dir, 'summary.json'), 'w'), indent=1)
    return s
