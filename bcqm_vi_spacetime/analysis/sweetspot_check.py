#!/usr/bin/env python3
"""
sweetspot_check.py (v0.3)

Summarise Q_clock (and related metrics) vs N for a given run directory containing RUN_METRICS_*.json.

Robust statistics:
- mean±std
- median and IQR (Q1,Q3)
- 10% trimmed mean

Heuristics:
- If N includes {1,2,4,8}: report mean/median heuristics at N=4 vs N=1 and N=8 (as before).
- Otherwise: report a generic local-peak-at-4 heuristic if {2,4,6} are present:
    compare Q(4) vs max(Q(2), Q(6)) using mean and median.
- Always report the available N set and counts.

Usage:
  python3 analysis/sweetspot_check.py <run_root_dir>
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


def median(xs):
    xs = sorted(float(x) for x in xs)
    n = len(xs)
    if n == 0:
        return float("nan")
    mid = n // 2
    if n % 2 == 1:
        return xs[mid]
    return 0.5 * (xs[mid - 1] + xs[mid])


def quantile(xs, q):
    xs = sorted(float(x) for x in xs)
    n = len(xs)
    if n == 0:
        return float("nan")
    pos = (n - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return xs[lo]
    w = pos - lo
    return xs[lo] * (1 - w) + xs[hi] * w


def trimmed_mean(xs, trim_frac=0.10):
    xs = sorted(float(x) for x in xs)
    n = len(xs)
    if n == 0:
        return float("nan")
    k = int(math.floor(n * trim_frac))
    xs2 = xs[k:n - k] if n - 2 * k > 0 else xs
    return sum(xs2) / len(xs2)


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

    Nset = sorted(byN.keys())
    print(f"Found N values: {Nset}")
    print()
    print("N | count | Q_clock mean±std | Q_clock median [Q1,Q3] | Q_clock trim10% | ell_lock mean±std | L mean±std")
    print("--|------:|------------------|------------------------|---------------:|------------------|----------")

    stats_mean = {}
    stats_med = {}

    for N in Nset:
        Qs = [float(x["Q_clock"]) for x in byN[N] if "Q_clock" in x and x["Q_clock"] != "inf"]
        els = [float(x.get("ell_lock", 0.0)) for x in byN[N]]
        Ls = [float(x["L"]) for x in byN[N] if "L" in x and x["L"] != "inf"]

        qmu, qsd = mean_std(Qs)
        qmed = median(Qs)
        q1 = quantile(Qs, 0.25)
        q3 = quantile(Qs, 0.75)
        qtrim = trimmed_mean(Qs, 0.10)

        emu, esd = mean_std(els)
        lmu, lsd = mean_std(Ls)

        stats_mean[N] = qmu
        stats_med[N] = qmed

        print(f"{N:>2} | {len(byN[N]):>5} | {qmu:>6.3g}±{qsd:<6.2g} | {qmed:>6.3g} [{q1:>6.3g},{q3:<6.3g}] | {qtrim:>13.3g} | {emu:>6.3g}±{esd:<6.2g} | {lmu:>6.3g}±{lsd:<6.2g}")

    # Heuristic A: {1,2,4,8}
    target = [1, 2, 4, 8]
    if all(t in stats_mean for t in target):
        print()
        print("Sweet-spot heuristic (mean Q_clock) at N=4 vs {1,8}:")
        print(f"  Qmean(1)={stats_mean[1]:.3g}, Qmean(4)={stats_mean[4]:.3g}, Qmean(8)={stats_mean[8]:.3g}")
        if stats_mean[4] > stats_mean[1] and stats_mean[4] > stats_mean[8]:
            print("  PASS: local maximum at N=4 (mean).")
        else:
            print("  FAIL/INCONCLUSIVE: not a local maximum at N=4 (mean).")

    if all(t in stats_med for t in target):
        print()
        print("Sweet-spot heuristic (median Q_clock) at N=4 vs {1,8}:")
        print(f"  Qmed(1)={stats_med[1]:.3g}, Qmed(4)={stats_med[4]:.3g}, Qmed(8)={stats_med[8]:.3g}")
        if stats_med[4] > stats_med[1] and stats_med[4] > stats_med[8]:
            print("  PASS: local maximum at N=4 (median).")
        else:
            print("  FAIL/INCONCLUSIVE: not a local maximum at N=4 (median).")
    else:
        # Heuristic B: {2,4,6}
        if 2 in stats_mean and 4 in stats_mean and 6 in stats_mean:
            print()
            print("Sweet-spot heuristic (mean Q_clock) local peak at N=4 vs neighbours {2,6}:")
            q2, q4, q6 = stats_mean[2], stats_mean[4], stats_mean[6]
            print(f"  Qmean(2)={q2:.3g}, Qmean(4)={q4:.3g}, Qmean(6)={q6:.3g}")
            if q4 > max(q2, q6):
                print("  PASS: N=4 exceeds both N=2 and N=6 (mean).")
            else:
                print("  FAIL/INCONCLUSIVE: N=4 not above both neighbours (mean).")

        if 2 in stats_med and 4 in stats_med and 6 in stats_med:
            print()
            print("Sweet-spot heuristic (median Q_clock) local peak at N=4 vs neighbours {2,6}:")
            q2, q4, q6 = stats_med[2], stats_med[4], stats_med[6]
            print(f"  Qmed(2)={q2:.3g}, Qmed(4)={q4:.3g}, Qmed(6)={q6:.3g}")
            if q4 > max(q2, q6):
                print("  PASS: N=4 exceeds both N=2 and N=6 (median).")
            else:
                print("  FAIL/INCONCLUSIVE: N=4 not above both neighbours (median).")

if __name__ == "__main__":
    main()
