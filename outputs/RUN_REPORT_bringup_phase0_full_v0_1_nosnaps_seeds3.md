# RUN_REPORT — bringup_phase0_full_v0_1_nosnaps_seeds3

## Purpose
Phase-0 bring-up sanity scan for the **full** model (snapshots disabled) to verify stability and map qualitative behaviour of provisional order-parameter proxies across **n** with **3 seeds** at fixed **N=64**.

## Configuration (resolved)
- schema_version: `vi_spacetime_config_v0.1`
- experiment_id: `bringup_phase0_full_v0_1_nosnaps_seeds3`
- variant: `full`
- N: `[64]`
- seeds: `{'count': 3, 'start': 1}`
- n values: `[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]`
- steps_total: `20000` (burn_in=8000, measure=12000)
- active_window: `recency` (hops=256)
- W_coh: `256`
- snapshots.enabled: `False`
- beta_junc: `1.5`

## QC / anomaly status
- star_collapse flagged: **false**
- runaway_hubbing flagged: **false**
- hubshare remains small throughout; max indegree remains O(N).

## Summary by n (mean ± std over seeds)
| n | Q_clock | L=Q/√N | ell_lock | S_perc | S_junc_w | hubshare (mean/max) | max_indeg (mean/max) | clustering | elapsed (s) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0 ± 0 | 0 ± 0 | 0.00 ± 0 | 0.653 ± 0.013 | 0.283 ± 0.0076 | 0.000489/0.000533 | 7.3/8 | 0.00101 | 389.4 |
| 0.2 | 0 ± 0 | 0 ± 0 | 0.00 ± 0 | 0.855 ± 0.0049 | 0.501 ± 0.014 | 0.000512/0.000514 | 8.0/8 | 1.63e-05 | 380.3 |
| 0.4 | 0 ± 0 | 0 ± 0 | 0.00 ± 0 | 0.188 ± 0.0057 | 0.0532 ± 0.0022 | 0.000361/0.00042 | 4.3/5 | 0 | 353.8 |
| 0.6 | 0 ± 0 | 0 ± 0 | 0.00 ± 0 | 0.23 ± 0.017 | 0.119 ± 0.002 | 0.000515/0.000583 | 5.3/6 | 0 | 1446.9 |
| 0.8 | 0 ± 0 | 0 ± 0 | 0.00 ± 0 | 0.685 ± 0.062 | 1.91 ± 0.34 | 0.00358/0.00415 | 38.3/42 | 0.00261 | 3342.5 |
| 1.0 | 0.32 ± 0.0052 | 0.04 ± 0.00065 | 4.67 ± 0.94 | 0.82 ± 0.0057 | 18.8 ± 0.4 | 0.00431/0.0044 | 59.7/61 | 0.00615 | 2132.0 |

## Interpretation
- **Stability:** All 18 runs (6 n-points × 3 seeds) completed without hub/star collapse. Guard-rails behaved as intended.
- **Spatial regimes:** The spatial order proxy is **non-monotone** in n and reproducible across seeds:
  - High connectivity at **n=0.2** (S_perc ≈ 0.85–0.86)
  - Fragmented / low connectivity at **n=0.4–0.6** (S_perc ≈ 0.18–0.25)
  - Re-percolation at **n=0.8–1.0** (S_perc ≈ 0.62–0.83)
- **Temporal proxy:** The clock/lockstep proxy remains **0** through n=0.8 and turns on only weakly at **n=1.0** (small nonzero Q_clock/L and ell_lock).
- **Conclusion (Phase-0):** The pipeline is now usable in nosnaps mode and the spatial order parameter is sensitive. However, the current placeholder dynamics does **not** yet provide a clean monotone control knob or a single coupled L–S transition.

## Recommended next diagnostic
Enable **binned time-series** (still nosnaps) for a minimal probe set at n ∈ {0.2, 0.6, 1.0} with seed=1 to determine whether each regime is steady-state or a burn-in/measurement artefact, and to guide the minimal rule refinement needed for a cleaner phase diagram.
