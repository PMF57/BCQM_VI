#!/usr/bin/env python3
"""
geometry_diagnosis.py (v0.1)

Reads one RUN_METRICS_*.json (or a folder) and prints:
- comp_size, plateau_est, 1/comp_size
- ds_est, ds_valid, r2, fit window, notes
- P0_downsample
- ball_growth mean_ball (if present)

Usage:
  python3 bcqm_vi_spacetime/analysis/geometry_diagnosis.py <path_to_RUN_METRICS.json OR folder>
"""
from __future__ import annotations
import json, sys, math
from pathlib import Path
from glob import glob

def load_one(path: Path):
    if path.is_dir():
        files = sorted(Path(p) for p in glob(str(path / "RUN_METRICS_*.json")))
        if not files:
            raise SystemExit(f"No RUN_METRICS_*.json in {path}")
        path = files[0]
    m = json.loads(path.read_text(encoding="utf-8"))
    return path, m

def main():
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python3 bcqm_vi_spacetime/analysis/geometry_diagnosis.py <metrics.json|folder>")
    path = Path(sys.argv[1])
    f, m = load_one(path)
    print(f"FILE: {f}")
    print(f"N={m.get('N')} n={m.get('n')} seed={m.get('seed')}")
    g = m.get("geometry", {}) or {}
    if not isinstance(g, dict):
        print("No geometry block.")
        return
    comp = g.get("comp_size", None)
    plateau = g.get("plateau_est", None)
    ds = g.get("ds_est", None)
    r2 = g.get("r2", None)
    notes = g.get("notes", "")
    tmin = g.get("fit_t_min", None)
    tmax = g.get("fit_t_max", None)
    print(f"comp_size={comp} 1/comp_size={(1.0/comp) if isinstance(comp,int) and comp>0 else None}")
    print(f"plateau_est={plateau}")
    print(f"ds_est={ds} ds_valid={g.get('ds_valid')} r2={r2} fit=[{tmin},{tmax}] notes={notes}")
    print("")
    p0 = g.get("P0_downsample", None)
    if p0:
        print("P0_downsample:")
        for t,val in p0:
            print(f"  t={t:>4}  P0={val}")
        print("")
    bg = g.get("ball_growth", None)
    if isinstance(bg, dict) and "mean_ball" in bg:
        print(f"ball_growth: comp_size={bg.get('comp_size')} samples={bg.get('samples')} r_max={bg.get('r_max')}")
        mb = bg.get("mean_ball", [])
        # print first 15 and last 5
        if mb:
            print("  mean_ball(r) first 15:")
            for r,val in list(enumerate(mb))[:15]:
                print(f"    r={r:>2} |B|={val:.3g}")
            print("  mean_ball(r) last 5:")
            for r in range(max(0,len(mb)-5), len(mb)):
                print(f"    r={r:>2} |B|={mb[r]:.3g}")
    else:
        print("No ball_growth in geometry.")
if __name__=="__main__":
    main()
