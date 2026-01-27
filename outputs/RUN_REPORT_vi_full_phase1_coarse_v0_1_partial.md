# RUN_REPORT — vi_full_phase1_coarse_v0_1 (prematurely terminated)

## Status
This dataset is **incomplete** (runs were stopped early). It contains **6 completed runs**: N=64 only, n in {0.0, 0.1}, seeds 1–3.

## Completed grid
- variant: `full`
- N: 64
- n: 0.0, 0.1
- seeds: 1, 2, 3

## Key metrics (completed runs)
| N | seed | n | Q_clock | L | ell_lock | S_perc | S_junc_w | max_indeg | hubshare | clustering | flags |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 64 | 1 | 0.0 | 0.0 | 0.0 | 0 | 0.636315 | 0.281042 | 6 | 0.000400909 | 0.0 | none |
| 64 | 2 | 0.0 | 0.0 | 0.0 | 0 | 0.668497 | 0.293643 | 8 | 0.000532623 | 0.000624512099921936 | none |
| 64 | 3 | 0.0 | 0.0 | 0.0 | 0 | 0.653558 | 0.275422 | 8 | 0.000533262 | 0.0024096385542168677 | none |
| 64 | 1 | 0.1 | 0.0 | 0.0 | 0 | 0.11555 | 0.0216962 | 3 | 0.000225683 | 0.0 | none |
| 64 | 2 | 0.1 | 0.0 | 0.0 | 0 | 0.144361 | 0.0246425 | 4 | 0.000301046 | 0.0 | none |
| 64 | 3 | 0.1 | 0.0 | 0.0 | 0 | 0.142639 | 0.0251132 | 4 | 0.00029967 | 0.0 | none |

## Interpretation (what this limited subset tells us)
- No lockstep signal yet at n=0.0 or 0.1 (`Q_clock=0`, `L=0`, `ell_lock=0` across seeds). This is expected at the low-n end.
- Spatial connectivity is **nontrivial even at n=0.0** (`S_perc≈0.64–0.67`). At n=0.1 it is smaller (`S_perc≈0.12–0.14`). With only two n-points, treat this as *non-diagnostic* (could be stochastic fluctuation or a genuine low-n structure); we need a broader scan.
- No hub pathologies in this subset (hubshare ~ 4e-4 to 5e-4, max_indeg <= 8; anomaly flags none).

## Practical issue observed: snapshot size
The run produced very large snapshot artefacts per run (tens of MB per file even at N=64), which will scale to hundreds of MB (or more) when N and the n-grid increase. This is consistent with your 500 MB/run observation.

## Recommendation before re-running Phase 1
1) For Phase-1 coarse scans, **disable snapshots entirely** (snapshots.enabled: false) to keep output small and avoid I/O bottlenecks.
2) After n_c is bracketed, do a dedicated **snapshot campaign** only at 3 points (below/near/above n_c) with compression (gz) and/or edges-only.
