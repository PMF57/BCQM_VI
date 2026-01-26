#!/usr/bin/env python3
"""
pathA_summary.py (v0.2)

Summarise Path A spatial + island observables for a directory containing RUN_METRICS_*.json.

Adds:
- If islands.F_max_by_wstar and islands.bundle_hist_by_wstar are present:
  - prints mean/median/IQR for F_max at each threshold
  - prints bundle_hist frequency per threshold

Usage:
  python3 analysis/pathA_summary.py <run_root_dir>
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path


def load_metrics(root: Path):
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


def fmt(mu, sd, digits=3):
    if math.isnan(mu):
        return "nan"
    return f"{mu:.{digits}g}±{sd:.{max(1,digits-1)}g}"


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 analysis/pathA_summary.py <run_root_dir>")
    root = Path(sys.argv[1])
    ms = load_metrics(root)

    Sperc, Sj, hub, maxdeg, clust, Fmax = [], [], [], [], [], []
    bundle_hist_counter = Counter()

    # Multi-wstar collectors
    f_by_w = defaultdict(list)  # w -> list of F_max
    bh_by_w = defaultdict(Counter)  # w -> Counter of bundle_hist json strings

    for m in ms:
        sp = m.get("space_state", {})
        if sp and sp.get("enabled", False):
            Sperc.append(sp.get("S_perc", m.get("S_perc")))
            Sj.append(sp.get("S_junc_w", m.get("S_junc_w")))
            hub.append(sp.get("hubshare", m.get("hubshare")))
            maxdeg.append(sp.get("max_indegree", m.get("max_indegree")))
            clust.append(sp.get("clustering", m.get("clustering")))
        else:
            Sperc.append(m.get("S_perc"))
            Sj.append(m.get("S_junc_w"))
            hub.append(m.get("hubshare"))
            maxdeg.append(m.get("max_indegree"))
            clust.append(m.get("clustering"))

        isl = m.get("islands", {})
        if isinstance(isl, dict):
            if "F_max" in isl:
                Fmax.append(isl.get("F_max"))
            bh = isl.get("bundle_hist")
            if isinstance(bh, dict):
                key = json.dumps(bh, sort_keys=True)
                bundle_hist_counter[key] += 1

            # Multi-wstar
            fws = isl.get("F_max_by_wstar")
            if isinstance(fws, dict):
                for w, val in fws.items():
                    f_by_w[w].append(val)
            bws = isl.get("bundle_hist_by_wstar")
            if isinstance(bws, dict):
                for w, bhdict in bws.items():
                    if isinstance(bhdict, dict):
                        bh_by_w[w][json.dumps(bhdict, sort_keys=True)] += 1

    n = len(ms)
    print(f"count: {n}")
    print()

    mu, sd = mean_std(Sperc); med = median(Sperc); q1 = quantile(Sperc,0.25); q3 = quantile(Sperc,0.75)
    print(f"S_perc: mean±std {fmt(mu,sd)}; median {med:.3g} [Q1,Q3]=[{q1:.3g},{q3:.3g}]")

    mu, sd = mean_std(Sj); med = median(Sj); q1 = quantile(Sj,0.25); q3 = quantile(Sj,0.75)
    print(f"S_junc_w: mean±std {fmt(mu,sd)}; median {med:.3g} [Q1,Q3]=[{q1:.3g},{q3:.3g}]")

    mu, sd = mean_std(hub)
    hmax = max(float(x) for x in hub if x is not None) if any(x is not None for x in hub) else float("nan")
    print(f"hubshare: mean±std {fmt(mu,sd)}; max {hmax:.3g}")

    mu, sd = mean_std(maxdeg)
    dmax = max(int(x) for x in maxdeg if x is not None) if any(x is not None for x in maxdeg) else None
    print(f"max_indegree: mean±std {fmt(mu,sd)}; max {dmax}")

    if any(x is not None for x in clust):
        mu, sd = mean_std(clust)
        print(f"clustering: mean±std {fmt(mu,sd)}")
    else:
        print("clustering: (not present)")

    if Fmax:
        mu, sd = mean_std(Fmax); med = median(Fmax); q1 = quantile(Fmax,0.25); q3 = quantile(Fmax,0.75)
        print(f"F_max: mean±std {fmt(mu,sd)}; median {med:.3g} [Q1,Q3]=[{q1:.3g},{q3:.3g}]")
    else:
        print("F_max: (not present)")

    if bundle_hist_counter:
        print()
        print("bundle_hist frequency (configured w_star):")
        for k, c in bundle_hist_counter.most_common():
            print(f"  {k}: {c}")

    if f_by_w:
        print()
        print("F_max_by_wstar summary:")
        for w in sorted(f_by_w.keys(), key=lambda x: float(x)):
            mu, sd = mean_std(f_by_w[w]); med = median(f_by_w[w]); q1 = quantile(f_by_w[w],0.25); q3 = quantile(f_by_w[w],0.75)
            print(f"  w={w}: mean±std {fmt(mu,sd)}; median {med:.3g} [Q1,Q3]=[{q1:.3g},{q3:.3g}]")

    if bh_by_w:
        print()
        print("bundle_hist_by_wstar frequency:")
        for w in sorted(bh_by_w.keys(), key=lambda x: float(x)):
            print(f"  w={w}:")
            for k, c in bh_by_w[w].most_common():
                print(f"    {k}: {c}")


if __name__ == "__main__":
    main()
