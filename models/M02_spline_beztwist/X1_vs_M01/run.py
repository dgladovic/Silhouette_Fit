"""
X1 (extra, not part of E0-E6): is the M02 vs M01 difference the twist, or the settings?
 a) M02 E0 params scored with M01's settings (H 2.4, angle_half, 11 sections)
 b) M02 family refitted (same kernel fit, same protocol) with M01's settings, start = M02 start
 c) M02 family refitted with M02's settings, start = M01's E0 fit (cubic twist degree-elevated to 5 points, r0 - 0.6 mm for H)
    -> checks whether E0 sits in a local minimum
 d) M02 family refitted with M02's settings, start = M02's own E0 result (does a plain restart escape?)
Writes results.json here. python models/M02_spline_beztwist/X1_vs_M01/run.py
"""
import os, sys, json, copy
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MD = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(MD, '..', '_common'))
import study, score as SC

m = study.load_model(MD)
pe = np.array(json.load(open(os.path.join(MD, 'E0_fit', 'params.json')))['values'])
p1 = json.load(open(os.path.join(MD, '..', 'M01_spline_cubic', 'E0_fit', 'params.json')))['values']
S1 = dict(N=22, H=2.4, placement='angle_half', target_w=9.0, sections=dict(mode='uniform_z', count=11))


def ev(p, st):
    sh = m.shape(p)
    ex = SC.evaluate(sh, st, built=False, fit_cam=True)
    bu = SC.evaluate(sh, st, built=True, camera=ex['camera'], fit_cam=True)
    return dict(built=bu['tot'], exact=ex['tot'], seg_front=[r['pass_front'] for r in bu['seg']],
                seg_rib=[r['rib_mean'] for r in bu['seg']], seg_v34=[r['pass_v34'] for r in bu['seg']])


def cubic_as_bez5(k1, k2, mx):
    c3 = np.array([[0, 0], [1 / 3, mx * k1], [2 / 3, mx * k2], [1, mx]])
    return [tuple(c3[0])] + [tuple((i / 4) * c3[i - 1] + (1 - i / 4) * c3[i]) for i in range(1, 4)] + [tuple(c3[3])]


out = {}
out['a_E0_params_M01_settings'] = dict(params=pe, **ev(pe, S1))

import types
m1 = types.SimpleNamespace(**{k: getattr(m, k) for k in ("shape", "penalty", "LB", "UB", "P0")}, SETTINGS=S1)
pb, ib = study.fit(m1)
out['b_refit_M01_settings'] = dict(params=pb, fit=ib, **ev(pb, S1))

p0c = m.pack(np.array(p1[:11]) - 0.6, cubic_as_bez5(*p1[11:14]))
pc, ic = study.fit(m, p0=p0c)
out['c_refit_from_M01_fit'] = dict(start=p0c, params=pc, fit=ic, **ev(pc, m.SETTINGS))
pd, idd = study.fit(m, p0=pe)
out['d_refit_from_own_E0'] = dict(params=pd, fit=idd, **ev(pd, m.SETTINGS))
m1E0 = json.load(open(os.path.join(MD, '..', 'M01_spline_cubic', 'E0_fit', 'metrics.json')))['built']
out['M01_E0_built'] = dict(tot=m1E0['tot'], seg_rib=[r['rib_mean'] for r in m1E0['seg']], seg_front=[r['pass_front'] for r in m1E0['seg']])
json.dump(study.jsonable(out), open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
for k, v in out.items():
    t = v.get('built', v.get('tot'))
    print(k, f"front {t['front_pass']}/19, 3/4 {t['v34_pass']}/19, ribs {t['rib_mean']:.3f} ({t['within1']:.0f} %), 3/4 mean {t['v34_mean']:.2f}",
          v.get('fit', ''))
