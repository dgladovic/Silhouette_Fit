"""
Does the lobe depth change towards the top rim?
k = 0.20 below z = KFROM, smoothly changing to k_top at the rim (190 mm).
For each k_top: refit profile + twist (fit.py --ktop), score rib directions over the whole drawing,
with extra detail for the top bands.  Baseline = constant k 0.20 (experiments/rose_0.2).
Usage: python ktop_experiment.py [kfrom] [ktop ...]
Results: experiments/ktop_*/ and experiments/ktop_summary.txt
"""
import os, sys, subprocess, re
import model as m
import rib_error_map as rem

HERE = os.path.dirname(os.path.abspath(__file__))
KFROM = float(sys.argv[1]) if len(sys.argv) > 1 else 120.0
KTOPS = [float(a) for a in sys.argv[2:]] or [0.10, 0.15, 0.25, 0.30]


def score(label, fit_dir):
    err = rem.main(out='rib_error_map.png', label=label, fit_dir=fit_dir)
    bands = "  ".join(f"z{z0}-{z0+20}: {s:+.2f}/{a:.2f}" for z0, (s, a) in rem.LAST_BANDS.items())
    return err, bands


rows = []
m.K_OF_Z = None
m.set_section(('rose', 0.2))
err, bands = score('k 0.20 constant', os.path.join(HERE, 'experiments', 'rose_0.2'))
rows.append(f"k 0.20 constant          | sil RMS 0.10 | whole-drawing {err:.2f} deg | signed/abs by band: {bands}")
print(rows[-1], flush=True)

for kt in KTOPS:
    name = f"ktop_{kt:.2f}_from{KFROM:.0f}"
    out = os.path.join('experiments', name)
    r = subprocess.run([sys.executable, 'fit.py', '8', '5', f'--ktop={kt}', f'--kfrom={KFROM}', f'--out={out}'],
                       cwd=HERE, capture_output=True, text=True)
    sil = re.search(r"RMS ([\d.]+) mm, max ([\d.]+)", r.stdout)
    m.set_section(('rose', 0.2))
    m.K_OF_Z = m.k_top_blend(0.2, kt, KFROM)
    err, bands = score(name, os.path.join(HERE, out))
    m.K_OF_Z = None
    rows.append(f"k 0.20 -> {kt:.2f} from {KFROM:.0f} | sil RMS {sil.group(1) if sil else '?'} | whole-drawing {err:.2f} deg | "
                f"signed/abs by band: {bands}")
    print(rows[-1], flush=True)

open(os.path.join(HERE, 'experiments', 'ktop_summary.txt'), 'w').write("\n".join(rows))
