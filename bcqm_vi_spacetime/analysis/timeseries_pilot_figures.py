#!/usr/bin/env python3
"""
timeseries_pilot_figures.py (v0.1)

Regenerates the pilot figure set from:
- timeseries_pilot_W100_N8_n0p8_seed56796_spaceon.csv

Outputs PDFs to the repo-root folder `figures/` with the locked filenames:
- fig_timeseries_islands_W100_N8_n0p8_seed56796.pdf         (Fig. 2)
- fig_2a_islands_only_W100_N8_n0p8_seed56796.pdf            (Fig. 2a)
- fig_2b_space_vs_islands_W100_N8_n0p8_seed56796.pdf        (Fig. 2b)

Important:
- Titles are descriptive and contain NO embedded figure numbering.
- Colours are locked to the Fig. 2 base palette:
  S_perc=C0, comp_frac=C1, S_junc_w=C2, Fmax_0.10=C3, Fmax_0.20=C4, Fmax_0.30=C5

Run from repo root:
  python3 bcqm_vi_spacetime/analysis/timeseries_pilot_figures.py
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CSV = Path("figures/timeseries_pilot_W100_N8_n0p8_seed56796_spaceon.csv")  # allow placing at repo root or adjust path

COL = {
    "S_perc": "C0",
    "comp_frac": "C1",
    "S_junc_w": "C2",
    "Fmax_0.10": "C3",
    "Fmax_0.20": "C4",
    "Fmax_0.30": "C5",
}

def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.minorticks_on()
    ax.grid(True, which="major", linestyle="--", linewidth=0.8)

def main():
    if not CSV.exists():
        # fallback: common location in your archive layout
        alt = Path("timeseries_pilot_W100_N8_n0p8_seed56796_spaceon.csv")
        raise SystemExit(f"Pilot CSV not found: {CSV}")

    df = pd.read_csv(CSV)
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    outdir = Path("figures")
    outdir.mkdir(parents=True, exist_ok=True)

    # Fig. 2 (full overlay)
    plt.figure(figsize=(8.5, 5.5))
    ax = plt.gca()
    ax.plot(df["t"], df["S_perc"], label="S_perc(t)", color=COL["S_perc"])
    ax.plot(df["t"], df["comp_frac"], label="|C|/|V_active|", color=COL["comp_frac"])
    ax.plot(df["t"], df["S_junc_w"], label="S_junc_w(t)", color=COL["S_junc_w"])
    ax.plot(df["t"], df["Fmax_0.10"], label="F_max(w=0.10)", color=COL["Fmax_0.10"])
    ax.plot(df["t"], df["Fmax_0.20"], label="F_max(w=0.20)", color=COL["Fmax_0.20"])
    ax.plot(df["t"], df["Fmax_0.30"], label="F_max(w=0.30)", color=COL["Fmax_0.30"])
    ax.set_title("Dynamic islands and connectivity (pilot: W=100, N=8, n=0.8, seed=56796)")
    ax.set_xlabel("Tick t (binned)")
    ax.set_ylabel("Value (unitless)")
    style_axes(ax)
    ax.legend(frameon=False, ncols=2, fontsize=9)
    plt.tight_layout()
    plt.savefig(outdir / "fig_timeseries_islands_W100_N8_n0p8_seed56796.pdf", format="pdf")
    plt.close()

    # Fig. 2a (islands only)
    plt.figure(figsize=(8.5, 5.5))
    ax = plt.gca()
    ax.plot(df["t"], df["Fmax_0.10"], label="F_max(w=0.10)", color=COL["Fmax_0.10"])
    ax.plot(df["t"], df["Fmax_0.20"], label="F_max(w=0.20)", color=COL["Fmax_0.20"])
    ax.plot(df["t"], df["Fmax_0.30"], label="F_max(w=0.30)", color=COL["Fmax_0.30"])
    ax.set_title("Island coherence over time (pilot: W=100, N=8, n=0.8, seed=56796)")
    ax.set_xlabel("Tick t (binned)")
    ax.set_ylabel("F_max (0–1)")
    ax.set_ylim(-0.02, 1.05)
    style_axes(ax)
    ax.legend(frameon=False, ncols=3, fontsize=9)
    plt.tight_layout()
    plt.savefig(outdir / "fig_2a_islands_only_W100_N8_n0p8_seed56796.pdf", format="pdf")
    plt.close()

    # Fig. 2b (space vs islands, w=0.20)
    plt.figure(figsize=(8.5, 5.5))
    ax = plt.gca()
    ax.plot(df["t"], df["S_perc"], label="S_perc(t)", color=COL["S_perc"])
    ax.plot(df["t"], df["Fmax_0.20"], label="F_max(w=0.20)", color=COL["Fmax_0.20"])
    ax.set_title("Space stays on while islands fluctuate (pilot: W=100, N=8, n=0.8, seed=56796)")
    ax.set_xlabel("Tick t (binned)")
    ax.set_ylabel("Order parameter (0–1)")
    ax.set_ylim(-0.02, 1.05)
    style_axes(ax)
    ax.legend(frameon=False, fontsize=9)
    plt.tight_layout()
    plt.savefig(outdir / "fig_2b_space_vs_islands_W100_N8_n0p8_seed56796.pdf", format="pdf")
    plt.close()

    print("Wrote pilot figures to figures/")

if __name__ == "__main__":
    main()
