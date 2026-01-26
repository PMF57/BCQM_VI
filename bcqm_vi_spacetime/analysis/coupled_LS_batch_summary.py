#!/usr/bin/env python3
"""
coupled_LS_batch_summary.py (v0.1)

Summarise coupled time–space–islands metrics for one or more batch folders.

For each folder:
- Q_clock: mean±std, median [Q1,Q3]
- S_perc, S_junc_w: mean±std, median [Q1,Q3]
- islands.F_max_by_wstar at w in {0.10,0.20,0.30}: mean±std, median [Q1,Q3]
- counts and basic sanity fields

Usage:
  python3 analysis/coupled_LS_batch_summary.py <folder1> [folder2 folder3 ...]

Example:
  python3 analysis/coupled_LS_batch_summary.py \
    outputs_glue_axes/run_C5_phase_plus_cadence_vglue_pathA/W100/N4/batch_p0p20_s56791_56798 \
    outputs_glue_axes/run_C5_phase_plus_cadence_vglue_pathA/W100/N4/batch_p0p50_s56791_56798
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import List, Dict, Any


def load_metrics(root: Path) -> List[Dict[str, Any]]:
    files = list(root.rglob("RUN_METRICS_*.json"))
    if not files:
        raise SystemExit(f"No RUN_METRICS_*.json found under {root}")
    return [json.loads(p.read_text(encoding="utf-8")) for p in files]


def mean_std(xs):
    xs = [float(x) for x in xs if x is not None]
    if not xs:
        return (float("nan"), float("nan"))
    mu = sum(xs) / len(xs)
    var = sum((x - mu) ** 2 for x in xs) / len(xs)
    return (mu, math.sqrt(var))


def median(xs):
    xs = sorted(float(x) for x in xs if x is not None)
    n = len(xs)
    if n == 0:
        return float("nan")
    mid = n // 2
    if n % 2 == 1:
        return xs[mid]
    return 0.5 * (xs[mid - 1] + xs[mid])


def quantile(xs, q):
    xs = sorted(float(x) for x in xs if x is not None)
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


def fmt_med(xs) -> str:
    med = median(xs)
    q1 = quantile(xs, 0.25)
    q3 = quantile(xs, 0.75)
    if math.isnan(med):
        return "nan"
    return f"{med:.3g} [{q1:.3g},{q3:.3g}]"


def fmt_mean(xs) -> str:
    mu, sd = mean_std(xs)
    if math.isnan(mu):
        return "nan"
    return f"{mu:.3g}±{sd:.2g}"


def get_fmax_by_w(ms, wkey: str):
    out = []
    for m in ms:
        isl = m.get("islands", {})
        fws = isl.get("F_max_by_wstar", {})
        if isinstance(fws, dict) and wkey in fws:
            out.append(fws[wkey])
        elif "F_max" in isl:
            # fallback to configured threshold if per-w missing
            out.append(isl.get("F_max"))
    return out


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python3 analysis/coupled_LS_batch_summary.py <folder1> [folder2 ...]")

    folders = [Path(p) for p in sys.argv[1:]]
    for root in folders:
        ms = load_metrics(root)
        n = len(ms)

        Q = [m.get("Q_clock") for m in ms]
        L = [m.get("L") for m in ms]
        Sperc = [m.get("S_perc") for m in ms]
        Sj = [m.get("S_junc_w") for m in ms]

        # multi-wstar
        F10 = get_fmax_by_w(ms, "0.10")
        F20 = get_fmax_by_w(ms, "0.20")
        F30 = get_fmax_by_w(ms, "0.30")

        # print
        print(f"== {root} ==")
        print(f"count: {n}")
        print(f"Q_clock mean {fmt_mean(Q)}; median {fmt_med(Q)}")
        print(f"L mean {fmt_mean(L)}; median {fmt_med(L)}")
        print(f"S_perc mean {fmt_mean(Sperc)}; median {fmt_med(Sperc)}")
        print(f"S_junc_w mean {fmt_mean(Sj)}; median {fmt_med(Sj)}")

        if F10:
            print(f"F_max(w=0.10) mean {fmt_mean(F10)}; median {fmt_med(F10)}")
        if F20:
            print(f"F_max(w=0.20) mean {fmt_mean(F20)}; median {fmt_med(F20)}")
        if F30:
            print(f"F_max(w=0.30) mean {fmt_mean(F30)}; median {fmt_med(F30)}")

        print()

if __name__ == "__main__":
    main()
