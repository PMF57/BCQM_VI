PIPELINE: Geometry probe W=100 (spectral dimension estimate)

This bundle provides:
- engine_vglue.py (patched): adds optional geometry.ds_est computation when geometry.enabled=true and S_perc >= require_sperc.
- event_graph.py (replacement): includes estimate_spectral_dimension on V_active.
- analysis/geometry_summary.py: summarises ds_est across outputs.
- two YAMLs for N=4 and N=8 at n=0.8 (p_reuse from_n), 8 seeds.
- pipelines/run_geometry_probe_W100.sh: runs both and writes analysis to outputs/analysis/<timestamp>_geometry_probe_W100.txt

Manual copy workflow:
1) Back up bcqm_vi_spacetime.
2) Copy engine_vglue.py and event_graph.py into bcqm_vi_spacetime/ (replace).
3) Copy analysis/geometry_summary.py into bcqm_vi_spacetime/analysis/
4) Copy the two YAMLs into configs/generated_vreg_C5_subset/
5) Copy pipelines/run_geometry_probe_W100.sh into bcqm_vi_spacetime/pipelines/
6) Run: bash bcqm_vi_spacetime/pipelines/run_geometry_probe_W100.sh
