"""Compare kernel geometry with Fusion ground truth (fusion_runs/*.txt from DumpCanvas): quarter maxX / maxY every 5 mm."""
import os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geometry as G
import targets as T


def read_dump(path):
    rows = []
    on = False
    for line in open(path, encoding='utf-8'):
        if line.startswith('z_mm'):
            on = True; continue
        if on and line.strip():
            rows.append([float(v) for v in line.split(',')])
    return np.array(rows)          # z, maxX, maxY, minX, minY, maxR


def compare(shape, st, path, built=True, spline_kind='not-a-knot'):
    d = read_dump(path)
    z = np.clip(d[:, 0], 0.05, 189.95)
    P = G.points(shape, z, st, built)
    mx, my, nx, ny = G.quarter_extents(P)
    e = np.c_[mx - d[:, 1], my - d[:, 2]]
    return d[:, 0], e
