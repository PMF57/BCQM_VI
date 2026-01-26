#!/usr/bin/env python3
"""
sweetspot_check.py

Summarise Q_clock (and related metrics) vs N for a given run directory containing RUN_METRICS_*.json.
Designed for BCQM V regression slices (v_glue engine).

Usage:
  python3 analysis/sweetspot_check.py <run_root_dir>

Example:
  python3 analysis/sweetspot_check.py outputs_glue_axes/run_C5_phase_plus_cadence_vglue/W100
"""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path


def load_metrics(root: Path):
    files = list(root.rglob("RUN_METRICS_*.json"))
    if not files:
        raise SystemExit(f"No RUN_METRICS_*.json found under {root}")
    return [json.loads(p.read_text(encoding="utf-8")) for p in files]


def mean_std(xs):
    xs = [float(x) for x in xs]
    if not xs:
        return (float("nan"), float("nan"))
    mu = sum(xs) / len(xs)
    var = sum((x - mu) ** 2 for x in xs) / len(xs)
    return (mu, math.sqrt(var))


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 analysis/sweetspot_check.py <run_root_dir>")
    root = Path(sys.argv[1])
    metrics = load_metrics(root)

    byN = defaultdict(list)
    for m in metrics:
        N = int(m.get("N", -1))
        if N >= 0:
            byN[N].append(m)

    print(f"Found N values: {sorted(byN.keys())}")
    print()
    print("N | count | Q_clock mean±std | ell_lock mean±std | L mean±std")
    print("--|------:|------------------|------------------|----------")
    stats = {}
    for N in sorted(byN.keys()):
        Qs = [float(x["Q_clock"]) for x in byN[N] if "Q_clock" in x and x["Q_clock"] != "inf"]
        els = [float(x.get("ell_lock", 0.0)) for x in byN[N]]
        Ls = [float(x["L"]) for x in byN[N] if "L" in x and x["L"] != "inf"]
        qmu, qsd = mean_std(Qs)
        emu, esd = mean_std(els)
        lmu, lsd = mean_std(Ls)
        stats[N] = (qmu, qsd)
        print(f"{N:>2} | {len(byN[N]):>5} | {qmu:>6.3g}±{qsd:<6.2g} | {emu:>6.3g}±{esd:<6.2g} | {lmu:>6.3g}±{lsd:<6.2g}")

    target = [1, 2, 4, 8]
    if all(t in stats for t in target):
        q4 = stats[4][0]
        q1 = stats[1][0]
        q8 = stats[8][0]
        print()
        print("Sweet-spot heuristic (mean Q_clock):")
        print(f"  Q(1)={q1:.3g}, Q(4)={q4:.3g}, Q(8)={q8:.3g}")
        if q4 > q1 and q4 > q8:
            print("  PASS: local maximum at N=4 (vs N=1 and N=8).")
        else:
            print("  FAIL/INCONCLUSIVE: not a local maximum at N=4 (need more seeds or different W).")
    else:
        print()
        print("Sweet-spot heuristic skipped (need N in {1,2,4,8}).")


if __name__ == "__main__":
    main()
