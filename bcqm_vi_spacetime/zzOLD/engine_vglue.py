from __future__ import annotations


"""
engine_vglue.py

V-glue engine runner (Phase P1–P3 wiring).

This module is the dispatch target when config `engine.mode: v_glue`.

Current status:
- The direct-ancestor files `state.py`, `glue_dynamics.py`, and `metrics.py` exist in the package.
- This engine will be filled in to call the ported BCQM V state + kernels + metrics.

For now, it provides a clear error if invoked before wiring is complete.
"""
from typing import Any, Dict


def run_single_v_glue(cfg: Dict[str, Any], N: int, n: float, seed: int) -> None:
    raise NotImplementedError(
        "engine.mode=v_glue selected, but V-glue engine is not yet wired into the runner. "
        "Next patch will implement state initialisation + kernel stepping + metrics using the "
        "ported BCQM V ancestor modules."
    )
