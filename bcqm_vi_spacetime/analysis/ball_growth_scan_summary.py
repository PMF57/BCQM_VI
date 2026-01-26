#!/usr/bin/env python3
"""
ball_growth_scan_summary.py

Reads the three diagnostic run folders and prints:
- comp_size
- plateau_est and 1/comp_size
- key ball growth points (r=1,5,10,15,20,25,30) and fraction covered.

Usage:
  python3 bcqm_vi_spacetime/analysis/ball_growth_scan_summary.py
"""
from __future__ import annotations
import json
from pathlib import Path

ROOTS = [
    ("n=0.2", "outputs_glue_axes/ball_growth_diag_C5/W100/N8/n0p2_seed56796"),
    ("n=0.6", "outputs_glue_axes/ball_growth_diag_C5/W100/N8/n0p6_seed56796"),
    ("n=0.8", "outputs_glue_axes/ball_growth_diag_C5/W100/N8/n0p8_seed56796"),
]

def load_metrics(folder: Path):
    files = sorted(folder.glob("RUN_METRICS_*.json"))
    if not files:
        raise SystemExit(f"No RUN_METRICS in {folder}")
    return json.loads(files[0].read_text(encoding="utf-8"))

def main():
    pts = [1,5,10,15,20,25,30]
    for label, rel in ROOTS:
        folder = Path(rel)
        m = load_metrics(folder)
        g = m.get("geometry", {}) or {}
        comp = g.get("comp_size", None)
        plateau = g.get("plateau_est", None)
        inv = (1.0/comp) if isinstance(comp,int) and comp>0 else None
        bg = g.get("ball_growth", {}) or {}
        mb = bg.get("mean_ball", [])
        print(f"== {label} ==")
        print(f"comp_size={comp} 1/comp_size={inv} plateau_est={plateau} ds_est={g.get('ds_est')} ds_valid={g.get('ds_valid')} r2={g.get('r2')} notes={g.get('notes')}")
        if not mb:
            print("NO ball_growth mean_ball")
            print()
            continue
        for r in pts:
            if r < len(mb):
                frac = (mb[r]/comp) if isinstance(comp,int) and comp>0 else None
                print(f"  r={r:>2} |B|={mb[r]:>7.3f}  frac={frac}")
        print()
if __name__=="__main__":
    main()
