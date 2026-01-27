# RUN_REPORT — Path A scan-from-n (C5, W=50): N=4 vs N=8

## Purpose
Replicate the Path A scan-from-n result at a second coherence horizon (W=50) to test robustness of two-step emergence.
Compare N=4 and N=8 with 8 seeds and n ∈ {0,0.2,0.4,0.6,0.8}.

## Method
- Engine: `engine.mode=v_glue` (BCQM V direct-ancestor glue kernels + clock metric)
- Space: Path A event graph with `space.p_reuse_mode=from_n` (p_reuse := n, clipped)
- V_active: recency window of length W plus frontier events
- Islands: F_max(w*) at w* ∈ {0.10,0.20,0.30}
- Seeds: 8 (56791–56798)

## Results

### N=4 (W=50)

| n | count | Q_clock med [Q1,Q3] | S_perc med [Q1,Q3] | S_junc_w med [Q1,Q3] | Fmax0.10 | Fmax0.20 | Fmax0.30 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 8 | 0.536 [0.494,0.614] | 0.25 [0.25,0.25] | 0 [0,0] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] |
| 0.2 | 8 | 0.646 [0.56,0.738] | 0.834 [0.733,0.862] | 0.15 [0.11,0.201] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] |
| 0.4 | 8 | 0.519 [0.464,0.598] | 0.908 [0.881,0.926] | 0.562 [0.465,0.58] | 0.5 [0.25,0.5] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] |
| 0.6 | 8 | 0.622 [0.567,0.649] | 0.935 [0.904,0.94] | 1.71 [1.61,1.78] | 1 [1,1] | 0.25 [0.25,0.25] | 0.25 [0.25,0.25] |
| 0.8 | 8 | 0.604 [0.556,0.655] | 0.99 [0.976,1] | 4.62 [4.21,4.92] | 1 [1,1] | 1 [1,1] | 0.75 [0.688,0.812] |

### N=8 (W=50)

| n | count | Q_clock med [Q1,Q3] | S_perc med [Q1,Q3] | S_junc_w med [Q1,Q3] | Fmax0.10 | Fmax0.20 | Fmax0.30 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 8 | 0.637 [0.524,0.836] | 0.125 [0.125,0.125] | 0 [0,0] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] |
| 0.2 | 8 | 0.653 [0.639,0.668] | 0.834 [0.826,0.859] | 0.168 [0.134,0.198] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] |
| 0.4 | 8 | 0.618 [0.491,0.817] | 0.883 [0.869,0.907] | 0.455 [0.422,0.488] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] |
| 0.6 | 8 | 0.594 [0.545,0.674] | 0.936 [0.911,0.956] | 1.57 [1.45,1.68] | 0.438 [0.375,0.906] | 0.125 [0.125,0.125] | 0.125 [0.125,0.125] |
| 0.8 | 8 | 0.544 [0.52,0.663] | 0.983 [0.973,0.99] | 4.51 [4.2,5.07] | 1 [1,1] | 0.562 [0.25,0.812] | 0.125 [0.125,0.125] |

## Interpretation
- W=50 reproduces the same qualitative **two-step emergence** seen at W=100:
  1) S_perc rises sharply by n≈0.2–0.4 while F_max remains at its disconnected baseline.
  2) F_max rises later (n≈0.6–0.8), first at w*=0.10, then at stricter thresholds.
- N dependence is consistent with W=100:
  - N=4 becomes coherent at stricter thresholds by n=0.8 (Fmax0.30 median 0.75).
  - N=8 remains threshold-sensitive at n=0.8 (full at w*=0.10, mixed at w*=0.20, fragmented at w*=0.30).

## Next step
Combine W=50 and W=100 into a single robustness statement in the lab note, then decide whether to (i) map W-dependence further (e.g. W=20), or (ii) proceed to ablations that decouple glue from space to test coupling hypotheses.
