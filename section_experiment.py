"""
Which cross-section shape explains the drawing best?
For each candidate: refit profile + twist to the silhouette and centre rib slope (fit.py --out),
then score rib directions over the WHOLE drawing (rib_error_map).
Usage: python section_experiment.py rose:0.12 rose:0.2 circles:0.4 ...
Results: experiments/<name>/ and experiments/summary.txt
"""
import os, sys, subprocess, re
import model as m

HERE = os.path.dirname(os.path.abspath(__file__))
cands = sys.argv[1:] or ['rose:0.12', 'rose:0.2', 'rose:0.28', 'circles:0.3', 'circles:0.4', 'circles:0.5']
rows = []
for c in cands:
    name = c.replace(':', '_')
    out = os.path.join('experiments', name)
    r = subprocess.run([sys.executable, 'fit.py', '8', '5', f'--section={c}', f'--out={out}'],
                       cwd=HERE, capture_output=True, text=True)
    txt = r.stdout
    sil = re.search(r"RMS ([\d.]+) mm, max ([\d.]+)", txt)
    slope = re.search(r"Rib slope RMS error: ([\d.]+)", txt)
    top = re.search(r"Twist at top: ([-\d.]+)", txt)
    kind, p = c.split(':')
    m.set_section((kind, float(p)))
    import rib_error_map
    err = rib_error_map.main(out='rib_error_map.png', label=c, fit_dir=os.path.join(HERE, out))
    rows.append(f"{c:14s} silhouette RMS {sil.group(1)} max {sil.group(2)} mm | centre slope RMS {slope.group(1)} | "
                f"twist top {top.group(1)} | whole-drawing rib angle error {err:.2f} deg")
    print(rows[-1], flush=True)
open(os.path.join(HERE, 'experiments', 'summary.txt'), 'w').write("\n".join(rows))
