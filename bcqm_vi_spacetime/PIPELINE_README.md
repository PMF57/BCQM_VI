PIPELINE: Ablation Suite W=100 (Path A scan-from-n)

Goal:
- One-command run of the recommended ablation suite:
  - N=4 and N=8
  - space disabled vs enabled
  - n-grid (0,0.2,0.4,0.6,0.8) with p_reuse := n (from_n mode)
- Automatically writes scan summaries to an output text file.

How to use (from Desktop):
1) Copy YAMLs into your Desktop configs/generated_vreg_C5_subset/
2) Copy pipelines/run_ablation_suite_W100.sh into your Desktop bcqm_vi_spacetime/pipelines/
3) Run:
   bash bcqm_vi_spacetime/pipelines/run_ablation_suite_W100.sh

Outputs:
- outputs/analysis/<timestamp>_ablation_suite_W100.txt
