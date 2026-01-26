#!/usr/bin/env python3
"""
geometry_summary.py

Summarise geometry.ds_est across a directory tree of RUN_METRICS_*.json.

Groups by (N,n) if present, printing count and ds median/IQR (and mean/std).
"""
from __future__ import annotations
import json, math, sys
from collections import defaultdict
from pathlib import Path

def load(root: Path):
    files = list(root.rglob("RUN_METRICS_*.json"))
    if not files:
        raise SystemExit(f"No RUN_METRICS_*.json under {root}")
    return [json.loads(p.read_text(encoding="utf-8")) for p in files]

def median(xs):
    xs = sorted(xs)
    n=len(xs)
    if n==0: return float("nan")
    return xs[n//2] if n%2==1 else 0.5*(xs[n//2-1]+xs[n//2])

def quantile(xs,q):
    xs = sorted(xs); n=len(xs)
    if n==0: return float("nan")
    pos=(n-1)*q; lo=int(math.floor(pos)); hi=int(math.ceil(pos))
    if lo==hi: return xs[lo]
    w=pos-lo
    return xs[lo]*(1-w)+xs[hi]*w

def mean_std(xs):
    if not xs: return (float("nan"), float("nan"))
    mu=sum(xs)/len(xs)
    var=sum((x-mu)**2 for x in xs)/len(xs)
    return (mu, math.sqrt(var))

def main():
    if len(sys.argv)!=2:
        raise SystemExit("Usage: python3 analysis/geometry_summary.py <root_dir>")
    root=Path(sys.argv[1])
    ms=load(root)
    by=defaultdict(list)
    for m in ms:
        N=int(m.get("N",-1))
        n=float(m.get("n",0.0))
        g=m.get("geometry",{})
        ds=g.get("ds_est") if isinstance(g,dict) else None
        if ds is None: 
            continue
        by[(N,n)].append(float(ds))
    for key in sorted(by.keys()):
        xs=by[key]
        mu,sd=mean_std(xs)
        med=median(xs); q1=quantile(xs,0.25); q3=quantile(xs,0.75)
        print(f"N={key[0]} n={key[1]:.3g} count={len(xs)} ds mean {mu:.3g}±{sd:.2g} median {med:.3g} [{q1:.3g},{q3:.3g}]")
if __name__=="__main__":
    main()
