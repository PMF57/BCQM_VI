# RUN_REPORT — timeseries_probe_50bins_v0_1

## Purpose
Baseline binned time-series probe (50 bins, nosnaps) to characterise regime stability across n using duty-cycle and mean-over-bins metrics.

## Configuration (resolved)
- experiment_id: `timeseries_probe_50bins_v0_1`
- variant: `full`
- N: `[64]` (this probe uses N=64)
- seeds: `[1]`
- n values: `[0.2, 0.4, 0.6, 0.8, 1.0]`
- steps_total: `20000` (burn_in=8000, measure=12000)
- active_window: `recency` (hops=256)
- snapshots.enabled: `False`
- write_timeseries: `True`, bins=50

## Summary (seed=1)
| n | Sperc_mean | DC(S>0.5) | DC(S>0.8) | S min–max | Sjuncw_mean | L_last10_mean | L_nonzero_frac | hubshare_max_ts | elapsed (s) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.2 | 0.329 | 25.5% | 11.8% | 0.103–0.997 | 0.146 | 0 | 0.0% | 0.000579 | 407.2 |
| 0.4 | 0.332 | 23.5% | 7.8% | 0.157–0.945 | 0.216 | 0 | 0.0% | 0.000883 | 353.2 |
| 0.6 | 0.352 | 17.6% | 7.8% | 0.201–0.997 | 0.396 | 0 | 0.0% | 0.00175 | 304.6 |
| 0.8 | 0.433 | 15.7% | 7.8% | 0.275–0.987 | 1 | 0 | 0.0% | 0.00432 | 233.0 |
| 1.0 | 0.805 | 96.1% | 68.6% | 0.486–1 | 9.87 | 0.0393 | 98.0% | 0.00767 | 129.5 |

## Interpretation
- Use **Sperc_mean** and duty-cycles (DC thresholds) as the regime indicator when intermittency is present; the end-of-run scalar can overstate connectivity.
- n=1.0 remains the most robust high-connectivity regime and is the only point where the current L-proxy is persistently nonzero.
- This 50-bin probe is the recommended lightweight baseline for future tuning loops.
