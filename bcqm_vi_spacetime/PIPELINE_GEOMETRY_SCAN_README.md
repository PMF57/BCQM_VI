PIPELINE: Geometry scan W=100 (n={0.2,0.6,0.8})

Adds:
- configs/generated_vreg_C5_subset/geometry_scan_C5_W100_N4.yml
- configs/generated_vreg_C5_subset/geometry_scan_C5_W100_N8.yml
- analysis/geometry_scan_summary.py
- pipelines/run_geometry_scan_W100.sh

Assumes:
- Your current engine_vglue.py + event_graph.py already support cfg.geometry.enabled and write RUN_METRICS['geometry']['ds_est'].

Run:
  bash bcqm_vi_spacetime/pipelines/run_geometry_scan_W100.sh

Output:
- outputs/analysis/<timestamp>_geometry_scan_W100.txt
