# RUN_REPORT — BCQM V parity regression (C9 phase+domains+cadence) via v_glue engine

## Purpose
Quantify the effect of adding the **domains** glue axis (C9: phase+domains+cadence) relative to C5, using the v_glue engine in bcqm_vi_spacetime (direct descendant of BCQM V).
We report robust statistics (mean, std, median, IQR, 10% trimmed mean) and a local-peak heuristic at N=4 vs neighbours {2,6} for N={2,4,6,8}.

## Method
- Engine: `engine.mode = v_glue` (ported BCQM V state + kernels + metrics)
- Config provenance: parameters from `provenance.v_config` (original BCQM V C9 YAML)
- Seeds: 16 (random_seed base from C9, contiguous 16-seed batch)
- W slices: W_coh ∈ {20,50,100}
- N set: {2,4,6,8} (N=6 is an additional evaluation point)
- Summary tool: `analysis/sweetspot_check.py` v0.3 (generic heuristic for N={2,4,6})

## Results

### W_coh = 20

| N | count | Q_clock mean±std | median [Q1,Q3] | trim10 | ell_lock mean±std | L mean±std |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 16 | 0.309±0.053 | 0.308 [0.289,0.318] | 0.31 | 42.2±5.2 | 0.218±0.037 |
| 4 | 16 | 0.305±0.053 | 0.307 [0.28,0.333] | 0.308 | 44.3±3 | 0.152±0.026 |
| 6 | 16 | 0.297±0.059 | 0.303 [0.252,0.341] | 0.301 | 50.3±5.3 | 0.121±0.024 |
| 8 | 16 | 0.283±0.059 | 0.273 [0.24,0.323] | 0.282 | 54.6±4.7 | 0.0999±0.021 |

- Local-peak heuristic at N=4 vs {2,6}: **FAIL** (mean) and **FAIL** (median).

### W_coh = 50

| N | count | Q_clock mean±std | median [Q1,Q3] | trim10 | ell_lock mean±std | L mean±std |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 16 | 0.567±0.11 | 0.573 [0.501,0.633] | 0.565 | 64.8±6.8 | 0.401±0.081 |
| 4 | 16 | 0.605±0.13 | 0.628 [0.578,0.652] | 0.607 | 80.9±11 | 0.303±0.064 |
| 6 | 16 | 0.552±0.2 | 0.579 [0.41,0.661] | 0.537 | 97.6±13 | 0.225±0.08 |
| 8 | 16 | 0.508±0.12 | 0.521 [0.433,0.583] | 0.509 | 131±23 | 0.18±0.042 |

- Local-peak heuristic at N=4 vs {2,6}: **PASS** (mean) and **PASS** (median).

### W_coh = 100

| N | count | Q_clock mean±std | median [Q1,Q3] | trim10 | ell_lock mean±std | L mean±std |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 16 | 0.932±0.2 | 0.86 [0.806,1.05] | 0.921 | 80.8±13 | 0.659±0.14 |
| 4 | 16 | 0.982±0.3 | 1.01 [0.837,1.29] | 0.999 | 109±20 | 0.491±0.15 |
| 6 | 16 | 0.862±0.51 | 0.795 [0.508,1.1] | 0.818 | 174±63 | 0.352±0.21 |
| 8 | 16 | 1.31±1.2 | 0.984 [0.714,1.31] | 1.17 | 196±89 | 0.465±0.41 |

- Local-peak heuristic at N=4 vs {2,6}: **PASS** (mean) and **PASS** (median).

## Interpretation
- Domains remain a **secondary modulator**, not the primary clock engine: the phase+cadence mechanism still sets the overall scale of Q_clock.
- However, domains can **reshape the N-dependence** of clock quality:
  - At W=20, adding domains does not create a sweet spot at N=4 (N=2 marginally best).
  - At W=50 and W=100, the local-peak-at-4 heuristic is satisfied (mean and median), indicating a stabilised moderate-N optimum relative to neighbours.
- Variability increases at larger N and larger W (notably W=100, N=8), consistent with intermittent high-lock episodes.

## Next step
Write a short comparison note (C5 vs C9) and decide whether to (i) proceed to additional C-series checks, or (ii) return to VI proper: reintroduce cross-links and run coupled L–S transition tests using L from the authentic V glue mechanism.
