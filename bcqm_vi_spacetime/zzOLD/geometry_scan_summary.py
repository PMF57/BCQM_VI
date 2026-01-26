#!/usr/bin/env python3
"""
geometry_scan_summary.py (v0.1)

Summarise spectral dimension estimates ds_est from a geometry scan output tree.

Expects RUN_METRICS_*.json with fields:
- N, n
- geometry.ds_est (float)

Usage:
  python3 analysis/geometry_scan_summary.py outputs_glue_axes/geometry_scan_C5/W100
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
from collections import defaultdict

def median(xs):
    xs = sorted(float(x) for x in xs if x is not None)
    n = len(xs)
    if n == 0: return float("nan")
    mid = n//2
    return xs[mid] if n%2==1 else 0.5*(xs[mid-1]+xs[mid])

def quantile(xs,q):
    xs = sorted(float(x) for x in xs if x is not None)
    n=len(xs)
    if n==0: return float("nan")
    pos=(n-1)*q
    lo=int(math.floor(pos)); hi=int(math.ceil(pos))
    if lo==hi: return xs[lo]
    w=pos-lo
    return xs[lo]*(1-w)+xs[hi]*w

def mean_std(xs):
    xs=[float(x) for x in xs if x is not None]
    if not xs: return (float("nan"), float("nan"))
    mu=sum(xs)/len(xs)
    var=sum((x-mu)**2 for x in xs)/len(xs)
    return (mu, math.sqrt(var))

def main():
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python3 analysis/geometry_scan_summary.py <root_dir>")
    root=Path(sys.argv[1])
    files=list(root.rglob("RUN_METRICS_*.json"))
    if not files:
        raise SystemExit(f"No RUN_METRICS_*.json under {root}")
    by = defaultdict(list)  # (N,n)->ds
    for f in files:
        m=json.loads(f.read_text(encoding="utf-8"))
        N=int(m.get("N",-1))
        n=float(m.get("n",0.0))
        g=m.get("geometry",{}) or {}
        ds=g.get("ds_est", None)
        if ds is None: 
            continue
        by[(N,n)].append(ds)
    keys=sorted(by.keys(), key=lambda x:(x[0], x[1]))
    print("N | n | count | ds mean±std | ds median [Q1,Q3]")
    print("--|---|------:|------------|------------------")
    for N,n in keys:
        xs=by[(N,n)]
        mu,sd=mean_std(xs)
        med=median(xs); q1=quantile(xs,0.25); q3=quantile(xs,0.75)
        print(f"{N:>1} | {n:.1f} | {len(xs):>5} | {mu:.3g}±{sd:.2g} | {med:.3g} [{q1:.3g},{q3:.3g}]")

if __name__=="__main__":
    main()
