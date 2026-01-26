PIPELINE: Timeseries ensemble (W=100, N=8, n={0.4,0.8}, 5 seeds)

Adds:
- 2 YAMLs (n=0.4 and n=0.8; seeds 56791–56795; timeseries_bins=80)
- analysis/timeseries_ensemble_summary.py (writes CSV + figures with median±IQR bands)
- pipelines/run_timeseries_ensemble_W100.sh (just run + analysis-to-file)

Manual copy:
- YAMLs -> configs/generated_vreg_C5_subset/
- analysis script -> bcqm_vi_spacetime/analysis/
- pipeline -> bcqm_vi_spacetime/pipelines/

Run:
  bash bcqm_vi_spacetime/pipelines/run_timeseries_ensemble_W100.sh

Outputs:
- outputs/analysis/<timestamp>_timeseries_ensemble_W100.txt
- outputs/timeseries_ensemble/timeseries_ensemble_n0p4_*.csv and n0p8_*.csv
- figs/fig_timeseries_ensemble_space_vs_islands_*.pdf
