"""Plots for the study: overlays on both targets, per-segment delta lines, influence maps."""
import os
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import targets as T
import geometry as G
import score as SC

TDIR = T.TDIR


def _front_px():
    c = T.front()['calib']
    img = cv2.imread(os.path.join(TDIR, 'front', 'image.jpg'), 0)
    Hpx = img.shape[0]
    col = lambda x: c['axis_col_px'] + np.asarray(x) / c['mm_per_px_x']
    row = lambda z: (1 - (np.asarray(z) - c['PLANE_Z'] - c['V_OFF']) / c['H_MM']) * Hpx - 0.5
    return img, col, row


def overlay_front(shape, st, path, built=True, title=''):
    img, col, row = _front_px()
    vis = (cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) * 0.45 + 255 * 0.55).astype(np.uint8)
    Z = SC.Z_SCORE
    w = G.full_outline(G.points(shape, Z, st, built))
    for sgn in (-1, 1):
        pts = np.c_[col(sgn * w), row(Z)].astype(np.int32)
        cv2.polylines(vis, [pts], False, (0, 0, 230), 2, cv2.LINE_AA)
    ribs = SC.rib_set('score', exclude=False)
    for (x0, z0, zc, xd, ok), (xm, v) in zip(ribs, SC.model_ribs(shape, st, ribs, built)):
        cv2.polylines(vis, [np.c_[col(xd), row(zc)].astype(np.int32)], False, (0, 160, 0) if ok.all() else (0, 200, 230), 2, cv2.LINE_AA)
        for i in range(len(zc) - 1):
            if v[i] and v[i + 1]:
                cv2.line(vis, (int(col(xm[i])), int(row(zc[i]))), (int(col(xm[i + 1])), int(row(zc[i + 1]))), (220, 0, 0), 1, cv2.LINE_AA)
    for z in range(0, 191, 10):
        cv2.line(vis, (0, int(row(z))), (30, int(row(z))), (90, 90, 90), 2)
    cv2.putText(vis, f"{title}  red=model outline  green=drawn rib (yellow=unreliable)  blue=model rib", (15, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (20, 20, 20), 2, cv2.LINE_AA)
    cv2.imwrite(path, vis)


def overlay_v34(shape, st, cam, path, built=True, title=''):
    src = cv2.imread(os.path.join(TDIR, 'view34', 'image.png'), cv2.IMREAD_UNCHANGED)
    if src.shape[2] == 4:
        a = src[:, :, 3:4].astype(float) / 255
        src = (src[:, :, :3] * a + 255 * (1 - a)).astype(np.uint8)
    vis = (src * 0.5 + 255 * 0.5).astype(np.uint8)
    e = SC.v34_edges(SC.points3d(shape, st, built), cam)
    v = T.view34()
    for side in 'LR':
        for r, c in zip(v['rows'], e[side][0]):
            if np.isfinite(c):
                cv2.circle(vis, (int(round(c)), int(r)), 1, (0, 0, 230), -1)
    cv2.putText(vis, f"{title} red = model outline", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 20, 20), 1, cv2.LINE_AA)
    cv2.imwrite(path, vis)


def delta_lines(levels, key, path, title, ylabel):
    """levels: list of (label, seg list with key per segment), baseline included."""
    fig, ax = plt.subplots(figsize=(9, 4.2))
    x = np.arange(1, 20)
    for lab, seg in levels:
        y = [np.nan if s.get(key) is None else s[key] for s in seg]
        ax.plot(x, y, marker='o', ms=3, label=lab)
    ax.axhline(0, color='#888', lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels([f"S{i:02d}" for i in x], rotation=90, fontsize=7)
    ax.set_title(title, fontsize=10); ax.set_ylabel(ylabel); ax.legend(fontsize=7, ncol=3)
    fig.tight_layout(); fig.savefig(path, dpi=110); plt.close(fig)


def influence_map(M, path, title, unit):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    im = ax.imshow(M, aspect='auto', cmap='viridis', origin='lower')
    ax.set_xlabel('segment (S01..S19)'); ax.set_ylabel('bumped knot z (0..190 step 10)')
    ax.set_xticks(range(19)); ax.set_xticklabels([f"{i+1}" for i in range(19)], fontsize=7)
    ax.set_yticks(range(20)); ax.set_yticklabels([f"{10*i}" for i in range(20)], fontsize=7)
    fig.colorbar(im, label=f'mean |change| per segment ({unit})')
    ax.set_title(title, fontsize=10)
    fig.tight_layout(); fig.savefig(path, dpi=110); plt.close(fig)
