PIPELINE: Ablation Suite W=100 with glue-off condition (v0.1.1)

Fixes:
- Correct indentation for the ablation hook (prevents SyntaxError).
- Correct CFG8_GOFF path in the pipeline script.

Provides:
- Patched engine_vglue.py supporting:
    ablation:
      glue_decohere: true
      q_base_override: 0.45
- Two new YAML configs (N=4 and N=8) for glueoff scans.
- Pipeline script that runs:
    nospace, space-on, glueoff
  for N=4 and N=8, then writes scan summaries to a single log file.

Use:
1) Back up bcqm_vi_spacetime.
2) Copy engine_vglue.py into bcqm_vi_spacetime/ (replace current).
3) Copy YAMLs into configs/generated_vreg_C5_subset/
4) Copy pipelines/run_ablation_suite_W100_glueoff.sh into bcqm_vi_spacetime/pipelines/
5) Run: bash bcqm_vi_spacetime/pipelines/run_ablation_suite_W100_glueoff.sh
