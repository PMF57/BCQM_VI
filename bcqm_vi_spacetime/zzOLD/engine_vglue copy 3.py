from __future__ import annotations

"""
engine_vglue.py (BCQM VI)

V-glue engine runner using direct-ancestor BCQM V modules (state/kernels/metrics).

Patch v0.1.1 (2026-01-22): add glue-state diagnostic logging to RUN_METRICS:
- cadence state summary (mean/var if available; otherwise active-mask stats)
- phase coherence (Kuramoto order parameter R) from thread phases
- domain occupancy histogram and entropy

Assumes the **package layout**:
  ~/Desktop/bcqm_vi_spacetime/engine_vglue.py
and sibling modules are imported via relative imports (e.g. .io, .state, etc.).
"""

import math
import os
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, Optional

import numpy as np

from .io import ensure_dir, write_json
from .state import ThreadState, BundleState
from .glue_dynamics import (
    hop_coherence_step,
    shared_bias_step,
    phase_lock_step,
    domain_glue_step,
    initialise_cadence,
    cadence_step,
)
from .metrics import compute_lockstep_metrics


_DEFAULT_HOP = {"form": "power_law", "alpha": 1.0, "k_prefactor": 2.0, "memory_depth": 1}
_DEFAULT_SHARED = {"enabled": False, "lambda_bias": 0.0}
_DEFAULT_PHASE = {"enabled": False, "lambda_phase": 0.0, "theta_join": 0.3, "theta_break": 1.5, "omega_0": 0.1, "noise_sigma": 0.0}
_DEFAULT_DOMAINS = {"enabled": False, "n_initial_domains": 1, "lambda_domain": 0.0, "merge_threshold": 0.8, "split_threshold": 0.3, "min_domain_size": 1}
_DEFAULT_CADENCE = {"enabled": False, "distribution": "lognormal", "mean_T": 1.0, "sigma_T": 0.0, "lambda_cadence": 0.0}

_FALLBACK_C5 = {
    "hop_coherence": {"form": "power_law", "alpha": 1.0, "k_prefactor": 2.0, "memory_depth": 1},
    "shared_bias": {"enabled": False, "lambda_bias": 0.0},
    "phase_lock": {"enabled": True, "lambda_phase": 0.25, "omega_0": 0.1},
    "domains": {"enabled": False, "n_initial_domains": 1, "lambda_domain": 0.0},
    "cadence": {"enabled": True, "distribution": "lognormal", "mean_T": 1.0, "sigma_T": 0.2, "lambda_cadence": 0.15},
}


def _run_id(experiment_id: str, variant: str, N: int, n: float, seed: int) -> str:
    return f"{experiment_id}__{variant}__N{N}__n{n:.3f}__seed{seed}"


def _ns(block: Optional[Dict[str, Any]], defaults: Dict[str, Any]) -> SimpleNamespace:
    d = dict(defaults)
    if block:
        d.update(block)
    return SimpleNamespace(**d)


def _compute_q_base(cfg_hop: SimpleNamespace, W_coh: float) -> float:
    form = getattr(cfg_hop, "form", "power_law")
    alpha = float(getattr(cfg_hop, "alpha", 1.0))
    k_pref = float(getattr(cfg_hop, "k_prefactor", 2.0))
    if form == "power_law":
        return float(min(0.5, k_pref / (float(W_coh) ** alpha)))
    if form == "exp":
        return float(min(0.5, k_pref * math.exp(-float(W_coh))))
    return float(min(0.5, k_pref / max(float(W_coh), 1.0)))


def _load_v_blocks(cfg: Dict[str, Any], n: float) -> Dict[str, SimpleNamespace]:
    prov = cfg.get("provenance", {})
    vcfg = prov.get("v_config", None)
    scaled = False

    if isinstance(vcfg, dict):
        blocks = vcfg
    else:
        blocks = _FALLBACK_C5
        scaled = True

    hop = _ns(blocks.get("hop_coherence"), _DEFAULT_HOP)
    shared = _ns(blocks.get("shared_bias"), _DEFAULT_SHARED)
    phase = _ns(blocks.get("phase_lock"), _DEFAULT_PHASE)
    domains = _ns(blocks.get("domains"), _DEFAULT_DOMAINS)
    cadence = _ns(blocks.get("cadence"), _DEFAULT_CADENCE)

    if not hasattr(phase, "theta_join"):
        phase.theta_join = _DEFAULT_PHASE["theta_join"]
    if not hasattr(phase, "theta_break"):
        phase.theta_break = _DEFAULT_PHASE["theta_break"]
    if not hasattr(phase, "noise_sigma"):
        phase.noise_sigma = _DEFAULT_PHASE["noise_sigma"]

    if scaled:
        if getattr(phase, "enabled", False):
            phase.lambda_phase = float(n) * float(getattr(phase, "lambda_phase", 0.0))
        if getattr(cadence, "enabled", False):
            cadence.lambda_cadence = float(n) * float(getattr(cadence, "lambda_cadence", 0.0))

    return {
        "hop": hop,
        "shared": shared,
        "phase": phase,
        "domains": domains,
        "cadence": cadence,
        "used_provenance": bool(isinstance(vcfg, dict)),
        "scaled_fallback_by_n": scaled,
    }


def _kuramoto_R(theta: np.ndarray) -> float:
    if theta.size == 0:
        return 0.0
    z = np.mean(np.exp(1j * theta))
    return float(np.abs(z))


def _domain_stats(domain: np.ndarray) -> Dict[str, Any]:
    if domain.size == 0:
        return {"counts": {}, "entropy": 0.0}
    vals, counts = np.unique(domain, return_counts=True)
    total = float(np.sum(counts))
    p = counts / total
    entropy = float(-np.sum(p * np.log(p + 1e-12)))
    return {"counts": {str(int(v)): int(c) for v, c in zip(vals, counts)}, "entropy": entropy}


def _cadence_stats(threads: ThreadState) -> Dict[str, Any]:
    # Try common cadence attribute names in V state
    for name in ("T", "L", "cadence", "tau"):
        if hasattr(threads, name):
            arr = np.asarray(getattr(threads, name), dtype=float)
            return {"field": name, "mean": float(arr.mean()), "var": float(arr.var())}
    # Cadence gating mask is also useful
    if hasattr(threads, "active"):
        act = np.asarray(getattr(threads, "active")).astype(bool)
        return {"field": "active", "mean": float(act.mean()), "var": float(act.var())}
    return {"field": None, "mean": None, "var": None}


def run_single_v_glue(cfg: Dict[str, Any], N: int, n: float, seed: int) -> None:
    variant = cfg["variant"]
    experiment_id = cfg["experiment_id"]
    out_dir = Path(cfg["output"]["out_dir"])
    ensure_dir(out_dir)

    run_id = _run_id(experiment_id, variant, N, n, seed)

    steps_total = int(cfg["steps_total"])
    burn_in = int(cfg["burn_in_epochs"])
    measure = int(cfg["measure_epochs"])
    if burn_in + measure != steps_total:
        raise ValueError("burn_in_epochs + measure_epochs must equal steps_total")
    T_eff = steps_total - burn_in
    if T_eff <= 0:
        raise ValueError("burn_in must be < steps_total")

    W_coh = int(cfg.get("W_coh", cfg.get("active_window", {}).get("hops", 256)))

    rng = np.random.default_rng(int(seed))

    blocks = _load_v_blocks(cfg, n)
    cfg_hop = blocks["hop"]
    cfg_shared = blocks["shared"]
    cfg_phase = blocks["phase"]
    cfg_domains = blocks["domains"]
    cfg_cadence = blocks["cadence"]

    cfg_hop.q_base = _compute_q_base(cfg_hop, W_coh)

    n_domains = int(getattr(cfg_domains, "n_initial_domains", 1))
    if n_domains < 1:
        n_domains = 1

    v0 = rng.choice([-1.0, 1.0], size=N)
    theta0 = rng.uniform(0.0, 2.0 * np.pi, size=N)
    domain0 = rng.integers(0, n_domains, size=N, endpoint=False)

    threads = ThreadState(v=v0, theta=theta0, domain=domain0, history_v=None)
    initialise_cadence(rng, threads, cfg_cadence)

    bundle = BundleState(X=0.0, m=float(np.mean(threads.v)),
                         theta_mean=float(np.angle(np.mean(np.exp(1j * threads.theta)))))

    m_all = np.zeros((1, T_eff), dtype=float)
    dX_all = np.zeros((1, T_eff), dtype=float)

    t_eff = 0
    t0_wall = time.time()

    for t in range(steps_total):
        cadence_step(rng, threads, cfg_cadence)
        hop_coherence_step(rng, threads, cfg_hop)

        bundle.m = float(np.mean(threads.v))
        bundle.theta_mean = float(np.angle(np.mean(np.exp(1j * threads.theta))))

        shared_bias_step(rng, threads, bundle, cfg_shared)
        phase_lock_step(rng, threads, bundle, cfg_phase)
        domain_glue_step(rng, threads, cfg_domains)

        bundle.m = float(np.mean(threads.v))
        bundle.theta_mean = float(np.angle(np.mean(np.exp(1j * threads.theta))))
        dX = float(np.mean(threads.v))
        bundle.X += dX

        if t >= burn_in:
            m_all[0, t_eff] = bundle.m
            dX_all[0, t_eff] = dX
            t_eff += 1

    elapsed = time.time() - t0_wall
    assert t_eff == T_eff

    met = compute_lockstep_metrics(m_all, dX_all)
    Q_clock = float(met.get("Q_clock", 0.0))
    ell_lock = float(met.get("ell_lock", 0.0))
    L_inst = float(met.get("L_inst", 0.0))
    L = Q_clock / (math.sqrt(N) if N > 0 else 1.0)

    diag = {
        "cadence": _cadence_stats(threads),
        "phase": {"R": _kuramoto_R(np.asarray(threads.theta, dtype=float))},
        "domains": _domain_stats(np.asarray(threads.domain)),
    }

    metrics_obj: Dict[str, Any] = {
        "run_id": run_id,
        "variant": variant,
        "engine_mode": "v_glue",
        "N": int(N),
        "n": float(n),
        "seed": int(seed),
        "steps_total": steps_total,
        "burn_in_epochs": burn_in,
        "measure_epochs": measure,
        "Q_clock": Q_clock,
        "L": float(L),
        "ell_lock": ell_lock,
        "L_inst": L_inst,
        "glue_state": diag,
        # Spatial placeholders (not computed in v_glue engine yet)
        "S_perc": 0.0,
        "S_junc_w": 0.0,
        "hubshare": 0.0,
        "max_indegree": 0,
        "clustering": None,
        "anomaly_flags": {
            "star_collapse": False,
            "runaway_hubbing": False,
            "tierB_evaluated": False,
        },
        "elapsed_seconds": float(elapsed),
    }

    cfg_obj: Dict[str, Any] = {
        "run_id": run_id,
        "schema_version": cfg.get("schema_version"),
        "experiment_id": experiment_id,
        "description": cfg.get("description"),
        "variant": variant,
        "engine_mode": "v_glue",
        "N": int(N),
        "n": float(n),
        "seed": int(seed),
        "resolved": cfg,
        "v_glue": {
            "used_provenance_v_config": bool(blocks["used_provenance"]),
            "scaled_fallback_by_n": bool(blocks["scaled_fallback_by_n"]),
            "W_coh": int(W_coh),
            "hop_coherence": vars(cfg_hop),
            "shared_bias": vars(cfg_shared),
            "phase_lock": vars(cfg_phase),
            "domains": vars(cfg_domains),
            "cadence": vars(cfg_cadence),
        },
        "platform": {"python": os.sys.version.split()[0]},
    }

    write_json(out_dir / f"RUN_CONFIG_{run_id}.json", cfg_obj)
    write_json(out_dir / f"RUN_METRICS_{run_id}.json", metrics_obj)
