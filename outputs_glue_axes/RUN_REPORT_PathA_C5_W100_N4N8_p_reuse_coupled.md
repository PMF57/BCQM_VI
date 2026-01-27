# RUN_REPORT — Path A coupled time–space–islands sweep (C5, W=100)

## Scope
8 seeds (56791–56798), W=100, p_reuse ∈ {0.20, 0.50, 0.80}, with N=4 and N=8.
Clock: v_glue (BCQM V kernels+metrics). Space: Path A event-graph cross-links.
Islands: overlap bundles; report F_max at w* ∈ {0.10,0.20,0.30}.

## Key findings
- For N=4, islands remain fragmented through p=0.50 then jump at p=0.80 (F_max median 1.0 at w*=0.30).
- For N=8, percolation rises with p, but island coherence is threshold-sensitive: at p=0.80, F_max medians are 1.0 (w*=0.10), 0.562 (w*=0.20), 0.125 (w*=0.30).
- Clock survives across the sweep; for N=8 at p=0.80, Q_clock is broad (median 0.938 with wide IQR), consistent with bursty lock episodes.

## Batch-level summary (medians)

### N=4

| p_reuse | Q_clock | S_perc | S_junc_w | F_max(w=0.30) |
|---:|---:|---:|---:|---:|
| 0.20 | 0.902 | 0.826 | 0.147 | 0.25 |
| 0.50 | 0.967 | 0.901 | 0.853 | 0.25 |
| 0.80 | 0.997 | 0.979 | 4.64 | 1.00 |

### N=8

| p_reuse | Q_clock | S_perc | S_junc_w | F_max(0.10) | F_max(0.20) | F_max(0.30) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.20 | 1.01 | 0.879 | 0.145 | 0.125 | 0.125 | 0.125 |
| 0.50 | 1.39 | 0.901 | 0.884 | 0.125 | 0.125 | 0.125 |
| 0.80 | 0.938 | 0.962 | 4.71 | 1.00 | 0.562 | 0.125 |

## Next step
Extend to additional N or W, then transition to the coupled-transition/ablation programme with v_glue supplying the temporal order parameter.
