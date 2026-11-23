"""
M04 — scenario 4: custom spline base + keyframe radius + keyframe twist, refined where segments need it.
"a tool to save radius/height values; wherever a segment needed it, more points were added"
Settings and start values from ../BaseScript (docs/05_EXPERIMENTS.md §5.2, §5.4).

Parameters: radius value at every key (Catmull-Rom, t = z/190) + twist value at every key except t = 0 (fixed 0°).
Sections: one on every key (as in BaseScript: 11 keys -> 11 sections). Every added key adds a section.

Refinement (§5.2): `refine()` is called by study.run_E0 after the first fit. It adds ONE key (radius and twist) at the
centre of the worst failing segment (as built), refits from the current curves sampled on the new key set, and
repeats until the targeted segment improves by <= 0.1 mm or 20 keys. The final key positions go to E0_fit/keys.json;
this module loads keys.json at import, so E1-E6 and the summary rebuild the refined model.
E0_fit/run.py sets M04_BASE_KEYS=1 so a re-run of E0 always starts from the 11 historical keys.
"""
import os, json
import numpy as np
from study import Shape, SMOOTH_W
import curves as C
import bases as B

ID = 'M04'
TITLE = 'custom spline base + keyframe radius + keyframe twist (Catmull-Rom, refined per segment)'
SOURCE = ('../BaseScript (bez_points, angle_points, smooth_spline_interpolation, generate_shell_triangles_by_count, '
          'sections on the keys); refinement rule docs/05 §5.2')
HEIGHT = 190.0
HERE = os.path.dirname(os.path.abspath(__file__))
KEYS_FILE = os.path.join(HERE, 'E0_fit', 'keys.json')
MAX_KEYS = 20
MIN_GAIN = 0.1                       # mm: stop when the targeted segment improves by no more than this

# ../BaseScript/BaseScript.py run(): bez_points and angle_points (t = 0, 0.1 ... 1)
BASE_KT = [i / 10 for i in range(11)]
BASE_R = [81, 98, 109.0, 114.0, 114.2, 110.4, 103.2, 92.4, 78.4, 62.0, 44.0]
BASE_TW = [0.0, 2.2, 8.26, 17.2, 28.2, 40.3, 52.6, 64.4, 74.8, 82.6, 90.0]


def _set_keys(kt, r, tw):
    """(Re)build every key-dependent module attribute: KT, NAMES, P0, LB, UB, SETTINGS."""
    global KT, NAMES, P0, LB, UB, SETTINGS, NK
    KT = [float(t) for t in kt]; NK = len(KT)
    NAMES = [f'r@t{t:.4f}' for t in KT] + [f'tw@t{t:.4f}' for t in KT[1:]]
    P0 = np.r_[np.asarray(r, float), np.asarray(tw, float)[1:]]
    LB = np.r_[np.full(NK, 20.0), np.full(NK - 1, -30.0)]
    UB = np.r_[np.full(NK, 200.0), np.full(NK - 1, 150.0)]
    SETTINGS = dict(N=22, H=2.4, placement='angle_half', target_w=9.0,
                    sections=dict(mode='list', z=[round(HEIGHT * t, 6) for t in KT]))


_set_keys(BASE_KT, BASE_R, BASE_TW)
if os.path.exists(KEYS_FILE) and not os.environ.get('M04_BASE_KEYS'):
    _k = json.load(open(KEYS_FILE))
    _set_keys(_k['kt'], _k['r_start'], _k['tw_start'])


def split(p):
    p = np.asarray(p, float)
    return p[:NK], np.r_[0.0, p[NK:]]


def shape(p):
    r, tw = split(p); kt = np.asarray(KT)
    return Shape(r0=lambda z: C.catmull_keys(kt, r, np.asarray(z, float) / HEIGHT),
                 twist=lambda z: C.catmull_keys(kt, tw, np.asarray(z, float) / HEIGHT),
                 rho=lambda z: B.custom_spline())


def penalty(p):
    r, tw = split(p)
    return np.r_[SMOOTH_W['mm'] * C.second_diff(r), SMOOTH_W['deg'] * C.second_diff(tw)]


def constraints(p):
    r, tw = split(p)
    out = []
    rr = C.catmull_keys(KT, r, np.linspace(0, 1, 381))
    if rr.min() <= 10:
        out.append(f'r0 too small ({rr.min():.1f} mm)')
    if np.any(np.diff(KT) <= 0):
        out.append('keys not strictly increasing')
    return out


# ------------------------------------------------------------------------------------------- pure Python (Fusion)
def catmull_py(points, t_target):
    """Pure-Python Catmull-Rom over (t, value) keys, as ../BaseScript smooth_spline_interpolation (one value)."""
    n = len(points)
    if t_target <= points[0][0]:
        return points[0][1]
    if t_target >= points[-1][0]:
        return points[-1][1]
    idx = 0
    for j in range(n - 1):
        if points[j][0] <= t_target <= points[j + 1][0]:
            idx = j
            break
    p0 = points[max(0, idx - 1)]; p1 = points[idx]; p2 = points[min(n - 1, idx + 1)]; p3 = points[min(n - 1, idx + 2)]
    if p2[0] == p1[0]:
        return p1[1]
    t = (t_target - p1[0]) / (p2[0] - p1[0])
    v0, v1, v2, v3 = p0[1], p1[1], p2[1], p3[1]
    return 0.5 * (2 * v1 + (-v0 + v2) * t + (2 * v0 - 5 * v1 + 4 * v2 - v3) * t * t + (-v0 + 3 * v1 - 3 * v2 + v3) * t ** 3)


def r0_py(z, r_points):
    return catmull_py(r_points, z / HEIGHT)


def twist_py(z, tw_points):
    return catmull_py(tw_points, z / HEIGHT)


def self_test(p=None):
    p = P0 if p is None else p
    r, tw = split(p); sh = shape(p); Z = np.linspace(0, HEIGHT, 1901)
    rp = list(zip(KT, map(float, r))); tp = list(zip(KT, map(float, tw)))
    d1 = max(abs(r0_py(float(z), rp) - v) for z, v in zip(Z, sh.r0(Z)))
    d2 = max(abs(twist_py(float(z), tp) - v) for z, v in zip(Z, sh.twist(Z)))
    assert d1 < 1e-6 and d2 < 1e-6, (d1, d2)
    return d1, d2


# ------------------------------------------------------------------------------------------- refinement (§5.2)
class _Self:
    """The module as an object for study.fit / evaluate_both (load_model doesn't register it in sys.modules)."""
    def __getattr__(self, k):
        return globals()[k]


def _worst(bu):
    """Failing segment (as built) to refine: largest rib_mean among those failing on ribs, else largest sil_max."""
    fail = [s for s in bu['seg'] if not s['pass_front']]
    if not fail:
        return None, None
    rib_fail = [s for s in fail if s['rib_mean'] is not None and (s['rib_mean'] > 0.75 or s['within1'] < 80.0)]
    if rib_fail:
        return max(rib_fail, key=lambda s: s['rib_mean']), 'rib_mean'
    return max(fail, key=lambda s: s['sil_max']), 'sil_max'


def _fmt(bu):
    t = bu['tot']
    return (f"front {t['front_pass']}/19, 3/4 {t['v34_pass']}/19, outline max {t['sil_max']:.2f}, ribs {t['rib_mean']:.2f} mm "
            f"/ {t['within1']:.0f} %, 3/4 mean {t['v34_mean']:.2f}")


def _save_keys(p, rounds):
    r, tw = split(p)
    os.makedirs(os.path.dirname(KEYS_FILE), exist_ok=True)
    json.dump(dict(kt=KT, z=[HEIGHT * t for t in KT], r_start=list(map(float, r)), tw_start=list(map(float, tw)),
                   note='final key positions after refinement; r_start/tw_start = fitted key values (E0 params.json holds the same)',
                   rounds=rounds), open(KEYS_FILE, 'w'), indent=1)


def refine(p, info, fit, evaluate_both):
    import study
    me = _Self()
    _, bu = evaluate_both(me, p)
    rounds = []
    study.log(HERE, 'E0 refinement round 0 (first fit, 11 keys)',
              [f"as built: {_fmt(bu)}", f"nfev {info['nfev']}, cap hit {info['cap_hit']}"])
    nfev_total = info['nfev']; caps = list(info['cap_hit'])
    while NK < MAX_KEYS:
        seg, metric = _worst(bu)
        if seg is None:
            break
        # skip segments that already have a key at their centre (refitting would not add freedom)
        failing = sorted([s for s in bu['seg'] if not s['pass_front']], key=lambda s: -(s[metric] or 0))
        zc = None
        for s in [seg] + failing:
            z = float(int(s['id'][1:]) * 10 - 5)
            if not any(abs(HEIGHT * t - z) < 1e-6 for t in KT):
                seg, zc = s, z
                break
        if zc is None:
            break
        before = seg[metric]
        old = (list(KT), p.copy(), bu, dict(info))
        sh = shape(p); kt_new = sorted(KT + [zc / HEIGHT])
        zz = HEIGHT * np.asarray(kt_new)
        r_new, tw_new = sh.r0(zz), sh.twist(zz); tw_new[0] = 0.0
        _set_keys(kt_new, r_new, tw_new)
        p_start = P0.copy()
        p, info = fit(me, p_start)
        nfev_total += info['nfev']; caps += info['cap_hit']
        _, bu = evaluate_both(me, p)
        after = [s for s in bu['seg'] if s['id'] == seg['id']][0][metric]
        gain = before - after
        rd = dict(round=len(rounds) + 1, segment=seg['id'], metric=metric, key_z=zc, n_keys=NK, before=before, after=after,
                  gain=gain, kept=bool(gain > MIN_GAIN), tot=bu['tot'], nfev=info['nfev'], cap_hit=info['cap_hit'],
                  seg_rib_mean=[s['rib_mean'] for s in bu['seg']], seg_sil_max=[s['sil_max'] for s in bu['seg']],
                  seg_pass=[s['pass_front'] for s in bu['seg']])
        rounds.append(rd)
        study.log(HERE, f"E0 refinement round {rd['round']}: key added at z = {zc:.0f} mm ({seg['id']})", [
            f"target {seg['id']} {metric}: {before:.2f} → {after:.2f} mm (gain {gain:+.2f}, threshold {MIN_GAIN})",
            f"keys {NK - 1} → {NK}; as built: {_fmt(bu)}",
            f"nfev {info['nfev']}, cap hit {info['cap_hit']}",
            "kept" if rd['kept'] else "gain ≤ 0.1 mm → key removed, refinement stops (previous key set is final)"])
        if not rd['kept']:
            kt_old, p, bu, info = old
            r_o, tw_o = (np.asarray(p, float)[:len(kt_old)], np.r_[0.0, np.asarray(p, float)[len(kt_old):]])
            _set_keys(kt_old, r_o, tw_o)
            break
    _save_keys(p, rounds)
    info = dict(info, refine_rounds=len(rounds), keys_added=[r['key_z'] for r in rounds if r['kept']],
                n_keys=NK, nfev_total=nfev_total, cap_hit_any=bool(any(caps)))
    return p, info


if __name__ == '__main__':
    print('self-test max |numpy - pure|:', self_test())
