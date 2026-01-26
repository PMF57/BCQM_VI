PIPELINE: Timeseries ensemble (W=100, N=4, n={0.4,0.8}, 5 seeds)

Adds:
- 2 YAMLs (N=4; n=0.4 and n=0.8; seeds 56791–56795; timeseries_bins=80)
- analysis/timeseries_ensemble_summary_N4.py (writes CSV + figures; Fig. 3c/3d titles)
- pipelines/run_timeseries_ensemble_W100_N4.sh (just run + analysis-to-file)

Manual copy:
- YAMLs -> configs/generated_vreg_C5_subset/
- analysis script -> bcqm_vi_spacetime/analysis/
- pipeline -> bcqm_vi_spacetime/pipelines/

Run:
  bash bcqm_vi_spacetime/pipelines/run_timeseries_ensemble_W100_N4.sh

Outputs:
- outputs/analysis/<timestamp>_timeseries_ensemble_W100_N4.txt
- outputs/timeseries_ensemble/timeseries_ensemble_n0p4_W100_N4.csv and n0p8_W100_N4.csv
- figs/fig_n0p4_space_vs_islands_ensemble_W100_N4.pdf and fig_n0p8_space_vs_islands_ensemble_W100_N4.pdf
