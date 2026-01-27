# RUN_REPORT — timeseries_probe_v0_1

## Purpose
Binned time-series probe (nosnaps) to distinguish steady-state vs intermittent/transient behaviour in the provisional order parameters.
Probe points: N=64, seed=1, n ∈ {0.2, 0.6, 1.0}, 120 bins over the measurement window.

## Configuration (resolved)
- experiment_id: `timeseries_probe_v0_1`
- variant: `full`
- N: `[64]` (this probe uses N=64)
- seeds: `[1]`
- n values: `[0.2, 0.6, 1.0]`
- steps_total: `20000` (burn_in=8000, measure=12000)
- active_window: `recency` (hops=256)
- snapshots.enabled: `False`
- write_timeseries: `True`, bins=120

## Time-series summary (per n)
| n | Sperc_mean | Sperc duty-cycle >0.5 | Sperc duty-cycle >0.8 | Sperc min–max | L_last10_mean | L min–max (clean) | hubshare_max |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.2 | 0.335 | 25.4% | 10.7% | 0.11–0.997 | 0 | 0–0 | 0.000642 |
| 0.6 | 0.35 | 19.7% | 9.8% | 0.196–0.986 | 0 | 0–0 | 0.00199 |
| 1.0 | 0.804 | 98.4% | 72.1% | 0.481–1 | 0.0393 | 0–0.399 | 0.00873 |

## Interpretation
- **n=0.2:** Sperc is *intermittent/non-stationary* within the measurement window (low duty-cycle of strong percolation), while L remains identically 0.
- **n=0.6:** fragmented regime persists; Sperc remains low most of the time, and L remains identically 0.
- **n=1.0:** high-percolation regime is robust (very high duty-cycle of Sperc>0.5; substantial fraction >0.8). L becomes nonzero and stabilises (last-10-bin mean close to the final scalar).
- **Key lesson:** for n ≤ 0.6, the *final* scalar S_perc can be misleading; scan-level summaries should use time-averaged Sperc (or duty-cycle thresholds) when timeseries is enabled.

## Recommendation
For Phase-1 scans, keep timeseries off by default, but when used for diagnostics near candidate transitions, record and report:
- `Sperc_mean_over_bins`, `Sperc_frac_gt_0p5`, and `Sperc_frac_gt_0p8` (duty-cycle metrics)
- `L_last10_mean` as a stable temporal proxy, to avoid early-bin instability when tick counts are small.
