#!/bin/bash
set -euo pipefail

# Run from Desktop. No cd required.
# Runs Path A scan-from-n for W=100 at N=4 and N=8, with and without space layer.
# Writes analysis outputs to outputs/analysis/<timestamp>_ablation_suite_W100.txt

TS=$(date +"%Y%m%d_%H%M%S")
ANADIR="outputs/analysis"
mkdir -p "$ANADIR"
OUTFILE="$ANADIR/${TS}_ablation_suite_W100.txt"

echo "BCQM VI Ablation Suite (W=100) — $(date)" | tee "$OUTFILE"
echo "" | tee -a "$OUTFILE"

run_cfg () {
  local cfg="$1"
  echo "== RUN: $cfg ==" | tee -a "$OUTFILE"
  python3 -m bcqm_vi_spacetime.cli run --config "$cfg" 2>&1 | tee -a "$OUTFILE"
  echo "" | tee -a "$OUTFILE"
}

summarise_scan () {
  local scanroot="$1"
  echo "== SUMMARY: $scanroot ==" | tee -a "$OUTFILE"
  python3 bcqm_vi_spacetime/analysis/scan_from_n_summary.py "$scanroot" 2>&1 | tee -a "$OUTFILE"
  echo "" | tee -a "$OUTFILE"
}

# Config paths (relative to Desktop)
CFG4_ON="configs/generated_vreg_C5_subset/pathA_scan_C5_W100_N4_from_n_s56791_56798.yml"
CFG4_OFF="configs/generated_vreg_C5_subset/pathA_scan_C5_W100_N4_from_n_s56791_56798_nospace.yml"
CFG8_ON="configs/generated_vreg_C5_subset/pathA_scan_C5_W100_N8_from_n_s56791_56798.yml"
CFG8_OFF="configs/generated_vreg_C5_subset/pathA_scan_C5_W100_N8_from_n_s56791_56798_nospace.yml"

# Run scans
run_cfg "$CFG4_OFF"
run_cfg "$CFG4_ON"
run_cfg "$CFG8_OFF"
run_cfg "$CFG8_ON"

# Summaries (paths must match output.out_dir in the YAMLs)
summarise_scan "outputs_glue_axes/run_C5_phase_plus_cadence_vglue_pathA/W100/N4/scan_from_n_nospace_s56791_56798"
summarise_scan "outputs_glue_axes/run_C5_phase_plus_cadence_vglue_pathA/W100/N4/scan_from_n_s56791_56798"
summarise_scan "outputs_glue_axes/run_C5_phase_plus_cadence_vglue_pathA/W100/N8/scan_from_n_nospace_s56791_56798"
summarise_scan "outputs_glue_axes/run_C5_phase_plus_cadence_vglue_pathA/W100/N8/scan_from_n_s56791_56798"

echo "DONE. Wrote: $OUTFILE" | tee -a "$OUTFILE"
