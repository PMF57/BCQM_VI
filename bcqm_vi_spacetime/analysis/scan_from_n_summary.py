#!/usr/bin/env python3
"""
scan_from_n_summary.py (v0.1)

Summarise a Path A scan where n_values are used (e.g. p_reuse_mode=from_n).

Assumes the scan root contains RUN_METRICS_*.json across multiple n values.
We group by the top-level "n" field in RUN_METRICS.

Outputs a compact table (median [Q1,Q3]) per n for:
- Q_clock
- S_perc
- S_junc_w
- F_max_by_wstar at w in {0.10,0.20,0.30} if present (else falls back to islands.F_max)

Usage:
  python3 analysis/scan_from_n_summary.py <scan_root_dir>
"""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List


def load_metrics(root: Path) -> List[Dict[str, Any]]:
    files = list(root.rglob("RUN_METRICS_*.json"))
    if not files:
        raise SystemExit(f"No RUN_METRICS_*.json found under {root}")
    return [json.loads(p.read_text(encoding="utf-8")) for p in files]


def median(xs):
    xs = sorted(float(x) for x in xs if x is not None and x != "inf")
    n = len(xs)
    if n == 0:
        return float("nan")
    mid = n // 2
    if n % 2 == 1:
        return xs[mid]
    return 0.5 * (xs[mid - 1] + xs[mid])


def quantile(xs, q):
    xs = sorted(float(x) for x in xs if x is not None and x != "inf")
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


def get_fmax(ms: List[Dict[str, Any]], wkey: str):
    out = []
    for m in ms:
        isl = m.get("islands", {})
        fws = isl.get("F_max_by_wstar", {})
        if isinstance(fws, dict) and wkey in fws:
            out.append(fws[wkey])
        elif "F_max" in isl:
            out.append(isl.get("F_max"))
    return out


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 analysis/scan_from_n_summary.py <scan_root_dir>")
    root = Path(sys.argv[1])
    ms = load_metrics(root)

    byn = defaultdict(list)
    for m in ms:
        n = float(m.get("n", 0.0))
        byn[n].append(m)

    nvals = sorted(byn.keys())
    print(f"Found n values: {nvals}")
    print()
    header = ("n | count | Q_clock (med[IQR]) | S_perc (med[IQR]) | "
              "S_junc_w (med[IQR]) | Fmax0.10 | Fmax0.20 | Fmax0.30")
    print(header)
    print("-" * len(header))

    for n in nvals:
        grp = byn[n]
        Q = [m.get("Q_clock") for m in grp]
        S = [m.get("S_perc") for m in grp]
        J = [m.get("S_junc_w") for m in grp]
        f10 = get_fmax(grp, "0.10")
        f20 = get_fmax(grp, "0.20")
        f30 = get_fmax(grp, "0.30")

        line = (f"{n:.3g} | {len(grp):>5} | {fmt_med(Q):>17} | {fmt_med(S):>16} | "
                f"{fmt_med(J):>18} | {fmt_med(f10):>8} | {fmt_med(f20):>8} | {fmt_med(f30):>8}")
        print(line)


if __name__ == "__main__":
    main()
