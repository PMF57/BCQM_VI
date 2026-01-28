#!/usr/bin/env python3
"""
ball_growth_ensemble_summary.py (v0.1)

Reads RUN_METRICS for the 4 ball-growth ensemble runs (N=4/8 × n=0.4/0.8),
and produces:
- CSV tables of median/Q1/Q3 fraction-covered curves vs r
- 2 PDF figures (N=4 and N=8) comparing n=0.4 vs n=0.8 with IQR shading.

Run from Desktop:
  python3 bcqm_vi_spacetime/analysis/ball_growth_ensemble_summary.py
"""
from __future__ import annotations
import json
from pathlib import Path
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

W = 100
SEEDS = list(range(56791, 56796))

RUNS = [
    ("N8_n0p4", 8, 0.4, "outputs_glue_axes/ball_growth_ens_C5/W100/N8/n0p4_s56791_56795"),
    ("N8_n0p8", 8, 0.8, "outputs_glue_axes/ball_growth_ens_C5/W100/N8/n0p8_s56791_56795"),
    ("N4_n0p4", 4, 0.4, "outputs_glue_axes/ball_growth_ens_C5/W100/N4/n0p4_s56791_56795"),
    ("N4_n0p8", 4, 0.8, "outputs_glue_axes/ball_growth_ens_C5/W100/N4/n0p8_s56791_56795"),
]

def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.minorticks_on()
    ax.grid(True, which="major", linestyle="--", linewidth=0.8)

def qstats(x):
    x = np.asarray(x, dtype=float)
    return np.nanmedian(x), np.nanpercentile(x, 25), np.nanpercentile(x, 75)

def load_metrics(folder: Path):
    files = sorted(Path(p) for p in glob(str(folder / "RUN_METRICS_*.json")))
    if not files:
        raise SystemExit(f"No RUN_METRICS_*.json in {folder}")
    return [json.loads(f.read_text(encoding="utf-8")) for f in files]

def extract_curve(m):
    g = (m.get("geometry") or {})
    bg = (g.get("ball_growth") or {})
    mb = bg.get("mean_ball", None)
    comp = bg.get("comp_size", g.get("comp_size", None))
    if mb is None or comp is None or comp == 0:
        return None
    mb = np.asarray(mb, dtype=float)
    frac = mb / float(comp)
    return frac, int(comp)

def band(ax, r, med, q1, q3, label):
    r = np.asarray(r, dtype=float)
    med = np.asarray(med, dtype=float)
    q1 = np.asarray(q1, dtype=float)
    q3 = np.asarray(q3, dtype=float)
    line, = ax.plot(r, med, label=label)
    ax.fill_between(r, q1, q3, alpha=0.25, color=line.get_color())

def main():
    out_csv = Path("outputs") / "ball_growth_ensemble"
    out_fig = Path("figs")
    out_csv.mkdir(parents=True, exist_ok=True)
    out_fig.mkdir(parents=True, exist_ok=True)

    # Build per-run CSVs
    run_curves = {}
    for tag, N, nval, rel in RUNS:
        mets = load_metrics(Path(rel))
        curves = []
        comps = []
        for m in mets:
            ec = extract_curve(m)
            if ec is None:
                continue
            frac, comp = ec
            curves.append(frac)
            comps.append(comp)
        if not curves:
            raise SystemExit(f"No usable ball_growth curves in {rel}")
        # align by r index
        L = min(len(c) for c in curves)
        curves = [c[:L] for c in curves]
        r = np.arange(L)
        mat = np.vstack(curves)  # seeds x r
        med = np.nanmedian(mat, axis=0)
        q1 = np.nanpercentile(mat, 25, axis=0)
        q3 = np.nanpercentile(mat, 75, axis=0)
        run_curves[(N, nval)] = (r, med, q1, q3)
        pd.DataFrame({"r": r, "frac_med": med, "frac_q1": q1, "frac_q3": q3}).to_csv(
            out_csv / f"ball_growth_frac_{tag}_W{W}.csv", index=False
        )

    # Figures: N=8 and N=4 comparisons
    for N in (8, 4):
        plt.figure(figsize=(8.5, 5.5))
        ax = plt.gca()
        r, med, q1, q3 = run_curves[(N, 0.4)]
        band(ax, r, med, q1, q3, f"n=0.4 (median±IQR)")
        r, med, q1, q3 = run_curves[(N, 0.8)]
        band(ax, r, med, q1, q3, f"n=0.8 (median±IQR)")
        ax.set_title(f"Fig. 5  Ball growth fraction (ensemble) (W={W}, N={N})")
        ax.set_xlabel("Graph radius r")
        ax.set_ylabel("Fraction covered |B(r)| / |C|")
        ax.set_ylim(-0.02, 1.02)
        style_axes(ax)
        ax.legend(frameon=False, fontsize=9)
        plt.tight_layout()
        plt.savefig(out_fig / f"fig_ball_growth_frac_ensemble_W{W}_N{N}.pdf", format="pdf")
        plt.close()

    print("Wrote outputs/ball_growth_ensemble/*.csv and figs/fig_ball_growth_frac_ensemble_W100_N*.pdf")

if __name__ == "__main__":
    main()
