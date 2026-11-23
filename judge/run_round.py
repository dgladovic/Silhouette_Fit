"""
Final round: re-run E0-E6 + summary for every model with the current kernel, one process per model in parallel.
Run: python judge/run_round.py [M01 M02 ...]     logs -> work/round_v<kernel>/<model>.log
"""
import os, sys, glob, subprocess, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'models', '_common'))
import study as S

EXPS = ['E0_fit', 'E1_tri_count', 'E2_tri_width', 'E3_tri_height', 'E4_twist', 'E5_radius', 'E6_sections']
LOGDIR = os.path.join(ROOT, 'work', f'round_v{S.KERNEL_VERSION}'); os.makedirs(LOGDIR, exist_ok=True)
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8')


def run_model(d):
    name = os.path.basename(d); log = open(os.path.join(LOGDIR, f'{name}.log'), 'w', encoding='utf-8')
    t0 = time.time()
    for e in EXPS:
        r = subprocess.run([sys.executable, os.path.join(d, e, 'run.py')], cwd=ROOT, env=ENV, stdout=log, stderr=subprocess.STDOUT)
        log.write(f"\n== {e}: exit {r.returncode}, {time.time() - t0:.0f} s\n"); log.flush()
        if r.returncode:
            return name, f'FAILED at {e}'
    r = subprocess.run([sys.executable, '-c', f"import sys; sys.path.insert(0, r'{os.path.join(ROOT, 'models', '_common')}'); import study; "
                        f"s = study.write_summary(r'{d}'); print(s['built'])"], cwd=ROOT, env=ENV, stdout=log, stderr=subprocess.STDOUT)
    return name, f'done in {time.time() - t0:.0f} s (summary exit {r.returncode})'


if __name__ == '__main__':
    ids = sys.argv[1:]
    dirs = [d for d in sorted(glob.glob(os.path.join(ROOT, 'models', 'M*'))) if not ids or os.path.basename(d)[:3] in ids]
    with ThreadPoolExecutor(len(dirs)) as ex:
        for name, msg in ex.map(run_model, dirs):
            print(name, msg, flush=True)
