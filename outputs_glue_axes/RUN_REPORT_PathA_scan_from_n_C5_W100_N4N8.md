# RUN_REPORT — Path A scan-from-n (C5, W=100): N=4 vs N=8

## Purpose
Document the first true Path A coupled scan where the scan parameter `n` sets cross-link pressure (`p_reuse = n`) on top of the BCQM V v_glue clock engine.
We compare N=4 and N=8 at fixed W=100 with 8 seeds and n ∈ {0,0.2,0.4,0.6,0.8}.

## Method
- Engine: `engine.mode=v_glue` (BCQM V direct-ancestor glue kernels + V clock metric)
- Space: Path A event graph with `space.p_reuse_mode=from_n` (p_reuse := n, clipped ≤0.95)
- V_active: recency window of length W plus frontier events
- Islands: overlap bundles from per-thread event histories, reported as F_max(w*) at w* ∈ {0.10,0.20,0.30}
- Seeds: 8 (56791–56798)

## Results

### N=4 (from scan_from_n_summary)

| n | count | Q_clock med [Q1,Q3] | S_perc med [Q1,Q3] | S_junc_w med [Q1,Q3] | Fmax0.10 | Fmax0.20 | Fmax0.30 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 8 | 1.03 [0.768,1.13] | 0.25 [0.25,0.25] | 0 [0,0] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] |
| 0.2 | 8 | 0.902 [0.743,1.08] | 0.826 [0.772,0.885] | 0.147 [0.138,0.153] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] |
| 0.4 | 8 | 0.925 [0.719,1.08] | 0.878 [0.84,0.891] | 0.461 [0.436,0.642] | 0.25 [0.25,0.375] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] |
| 0.6 | 8 | 1.21 [1.02,1.37] | 0.932 [0.915,0.963] | 1.62 [1.57,1.76] | 1 [1,1] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] |
| 0.8 | 8 | 0.997 [0.908,1.08] | 0.979 [0.958,0.982] | 4.64 [4.2,4.74] | 1 [1,1] | 1 [1,1] | 1 [0.875,1] |

### N=8 (from scan_from_n_summary)

| n | count | Q_clock med [Q1,Q3] | S_perc med [Q1,Q3] | S_junc_w med [Q1,Q3] | Fmax0.10 | Fmax0.20 | Fmax0.30 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 8 | 0.924 [0.685,1.85] | 0.125 [0.125,0.125] | 0 [0,0] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] |
| 0.2 | 8 | 1.01 [0.697,1.31] | 0.879 [0.862,0.894] | 0.145 [0.14,0.169] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] |
| 0.4 | 8 | 1.06 [0.928,1.16] | 0.896 [0.887,0.906] | 0.448 [0.431,0.502] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] |
| 0.6 | 8 | 1.74 [1.03,2.1] | 0.913 [0.897,0.928] | 1.55 [1.31,1.58] | 0.312 [0.25,0.375] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] |
| 0.8 | 8 | 0.938 [0.681,1.99] | 0.962 [0.96,0.982] | 4.71 [4.47,5.43] | 1 [1,1] | 0.562 [0.312,0.75] | 0.125 [0.125,0.125] |

## Interpretation
- In both N=4 and N=8, the scan shows a **two-step emergence**:
  1) **Space percolation first**: S_perc jumps from the disconnected baseline at n=0 to large values by n≈0.2–0.4, while islands remain fragmented.
  2) **Island coherence later**: F_max rises only at higher n (≈0.6–0.8), and does so earlier at lenient overlap thresholds.
- N-dependence:
  - N=4: by n=0.8, islands are coherent even at strict w*=0.30 (median F_max=1.0).
  - N=8: by n=0.8, island coherence is **threshold-sensitive**: full at w*=0.10, mixed at w*=0.20, absent at w*=0.30.
- Clock survival: Q_clock remains viable across the scan; in these runs it does not collapse when space percolates.

## Next step
Repeat the scan at additional W values and/or larger N, and then perform ablations that decouple space formation from glue dynamics to test coupling hypotheses.
