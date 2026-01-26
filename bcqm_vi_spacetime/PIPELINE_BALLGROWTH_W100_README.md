PIPELINE: Ball-growth ensemble (W=100; N={4,8}; n={0.4,0.8}; 5 seeds)

Uses geometry.mode = ball_growth_only (skips ds fitting; always attaches ball-growth profile).

Manual copy workflow:
- Copy bcqm_vi_spacetime/engine_vglue.py and bcqm_vi_spacetime/event_graph.py into production bcqm_vi_spacetime/ (replace).
- Copy YAMLs into configs/generated_vreg_C5_subset/
- Copy analysis/ball_growth_ensemble_summary.py into bcqm_vi_spacetime/analysis/
- Copy pipelines/run_ball_growth_ensemble_W100.sh into bcqm_vi_spacetime/pipelines/

Run (from Desktop):
  bash bcqm_vi_spacetime/pipelines/run_ball_growth_ensemble_W100.sh

Outputs:
- outputs/analysis/<timestamp>_ball_growth_ensemble_W100.txt
- outputs/ball_growth_ensemble/*.csv
- figs/fig_ball_growth_frac_ensemble_W100_N4.pdf and figs/fig_ball_growth_frac_ensemble_W100_N8.pdf
