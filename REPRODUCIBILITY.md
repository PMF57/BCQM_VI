# Reproducibility

## Selftest
```bash
bash bcqm_vi_spacetime/pipelines/run_selftest.sh
```

## Pipelines used to generate reported results

### Dynamic islands: ensemble (N=8)
```bash
bash bcqm_vi_spacetime/pipelines/run_timeseries_ensemble_W100.sh
python3 bcqm_vi_spacetime/analysis/timeseries_ensemble_summary.py
```

### Dynamic islands: ensemble (N=4)
```bash
bash bcqm_vi_spacetime/pipelines/run_timeseries_ensemble_W100_N4.sh
python3 bcqm_vi_spacetime/analysis/timeseries_ensemble_summary_N4.py
```

### Ball-growth geometry: ensemble
```bash
bash bcqm_vi_spacetime/pipelines/run_ball_growth_ensemble_W100.sh
```

All pipelines write a timestamped log to `outputs/analysis/` (ignored by git by default).
