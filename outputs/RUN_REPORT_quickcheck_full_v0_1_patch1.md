# RUN_REPORT — quickcheck_full_v0_1_patch1

## Purpose
Quickcheck re-run after applying the anti-collapse patch. Goal: verify pipeline outputs and confirm the **star/self-loop collapse** seen previously is eliminated.

## Configuration (common)
- experiment_id: `quickcheck_full_v0_1_patch1`
- variant: `full`
- N: `[32]` (this quickcheck uses N=32)
- n values: `[0.0, 0.5, 1.0]`
- steps_total: `5000` (burn_in=1000, measure=4000)
- W_coh: `256`
- active_window: `recency` (hops=256)
- snapshots: enabled=True, cadence={'every': 2500, 'start': 2500}
- time-series: write_timeseries=False

## Outputs present
- Per n-point: `RUN_CONFIG_<run_id>.json`, `RUN_METRICS_<run_id>.json`
- Snapshots: edge CSV + node JSON at epoch 2500, and `*_final` (no duplicate final/cadence snapshot).

## Key metrics summary
| n | Q_clock | L=Q/√N | ell_lock | S_perc | S_junc_w | max_indeg | hubshare | clustering | flags |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0.000 | 0.0 | 0 | 0 | 0.306265 | 0.0522044 | 3 | 0.000439046 | 0.0 | none |
| 0.500 | 0.0 | 0 | 0 | 0.988462 | 1.00661 | 11 | 0.00144168 | 0.0 | none |
| 1.000 | 3.1805772429465513 | 0.562252 | 6 | 0.996207 | 21.2714 | 32 | 0.00398953 | 0.15670664371712092 | none |

## Interpretation
- The previous failure mode (**self-loop / star collapse**) is **fixed**:
  - `max_indegree` stays O(N) (32 at n=1.0), `hubshare` stays small (~0.004), and both anomaly flags remain **False**.
  - Spot-check: the n=1.0 final edge list contains **0 self-loops** (`u==v`).
- Connectivity now rises strongly with n (as intended for a scaffold), but note:
  - `S_perc` is already high at n=0.5 while `L` is still 0. This means spatial connectivity can appear before the current lockstep/tick proxy switches on.
  - That’s acceptable for quickcheck, but for the VI coupled-transition goal we will likely need to tune either (i) how `S_perc` depends on synchrony, or (ii) how lockstep is detected, so their transitions can coincide.

## QC status
**PASS** for bring-up and collapse guard-rails.

## Next step recommendation
Proceed to **Phase 0 bring-up sanity** (N=64, coarse n grid) now that collapse is fixed.
After Phase 0, if `S_perc` still turns on far earlier than `L`, we adjust the placeholder selection rule to make cross-link formation depend more sharply on synchrony (e.g. make existing-choice probability scale like `p_sync^2` or similar), while keeping the anti-hub guard-rail.
