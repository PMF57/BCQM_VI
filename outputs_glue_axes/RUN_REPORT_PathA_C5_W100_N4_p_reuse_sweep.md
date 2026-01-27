# RUN_REPORT — Path A (cross-links on top of v_glue): C5, W=100, N=4, p_reuse sweep

## Purpose
Quantify the interaction of **space/connectivity** and **time/clock coherence** when cross-links are enabled on top of the BCQM V glue engine (v_glue).
This report summarises an 8-seed sweep at fixed W=100, N=4 for three cross-link pressures (p_reuse = 0.20, 0.50, 0.80).

## Method
- Engine: `engine.mode = v_glue` (ported BCQM V state + kernels + metrics)
- Space layer: Path A event graph bookkeeping + reuse probability `p_reuse` (fixed per batch)
- V_active: events created within last W ticks, plus current frontier events
- No snapshots; end-of-run spatial/island observables computed post-hoc

## Results: space/islands (8 seeds each)

### p_reuse = 0.20
- S_perc mean±std: 0.822±0.072 (median 0.826 [0.772, 0.885])
- S_junc_w mean±std: 0.145±0.012 (median 0.147 [0.138, 0.153])
- hubshare mean±std: 0.00834±0.00012; max_indegree: 3
- islands: F_max = 0.25 (all seeds); bundle_hist {"1":4} in 8/8

### p_reuse = 0.50
- S_perc mean±std: 0.901±0.035 (median 0.901 [0.881, 0.916])
- S_junc_w mean±std: 0.857±0.082 (median 0.853 [0.815, 0.887])
- hubshare mean±std: 0.0156±0.0024; max_indegree mean±std 4.75±0.66 (max 6)
- islands: F_max = 0.25 (all seeds); bundle_hist {"1":4} in 8/8

### p_reuse = 0.80
- S_perc mean±std: 0.968±0.027 (median 0.979 [0.958, 0.982])
- S_junc_w mean±std: 4.50±0.57 (median 4.64 [4.2, 4.74])
- hubshare mean±std: 0.0351±0.0049; max_indegree mean±std 8.62±1.1 (max 10)
- clustering mean±std: 0.0491±0.023
- islands: F_max mean±std 0.875±0.22; median 1.0 [0.875,1.0]
  - bundle_hist {"4":1} in 6/8; {"2":2} in 1/8; {"1":2,"2":1} in 1/8

## Clock coherence (from the same batches)
Using `sweetspot_check.py` on each batch directory (N fixed at 4):
- p_reuse=0.20: Q_clock mean±std ≈ 0.875±0.21; median ≈ 0.902
- p_reuse=0.50: Q_clock mean±std ≈ 1.00±0.32; median ≈ 0.967
- p_reuse=0.80: Q_clock mean±std ≈ 0.986±0.16; median ≈ 0.997

## Interpretation
- Spatial connectivity increases smoothly with p_reuse (S_perc rises; junction density rises).
- Island formation is **not** gradual: F_max stays at 0.25 (four singles) for p_reuse=0.20 and 0.50, then jumps at p_reuse=0.80 (dominant bundle in 6/8 seeds).
- The clock survives across the sweep and is broadly stable; in this slice it does not collapse when space percolates.
- This is the first quantitative realisation of the “spacetime islands” picture: at moderate cross-link pressure the system is connected but not yet a single coherent island; at higher pressure a dominant island nucleates.

## Next step
Repeat the same p_reuse sweep for additional N (e.g. N=8) or additional W, and add a small ablation with `space.enabled=false` vs `true` at matched seeds to quantify clock survival relative to a no-space baseline.
