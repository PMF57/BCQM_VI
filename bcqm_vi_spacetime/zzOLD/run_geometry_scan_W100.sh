#!/bin/bash
set -euo pipefail

TS=$(date +"%Y%m%d_%H%M%S")
ANADIR="outputs/analysis"
mkdir -p "$ANADIR"
OUTFILE="$ANADIR/${TS}_geometry_scan_W100.txt"

echo "BCQM VI Geometry scan (W=100; n={0.2,0.6,0.8}) — $(date)" | tee "$OUTFILE"
echo "" | tee -a "$OUTFILE"

run_cfg () {
  local cfg="$1"
  echo "== RUN: $cfg ==" | tee -a "$OUTFILE"
  python3 -m bcqm_vi_spacetime.cli run --config "$cfg" 2>&1 | tee -a "$OUTFILE"
  echo "" | tee -a "$OUTFILE"
}

run_cfg "configs/generated_vreg_C5_subset/geometry_scan_C5_W100_N4.yml"
run_cfg "configs/generated_vreg_C5_subset/geometry_scan_C5_W100_N8.yml"

echo "== SUMMARY: ds_est by (N,n) ==" | tee -a "$OUTFILE"
python3 bcqm_vi_spacetime/analysis/geometry_scan_summary.py outputs_glue_axes/geometry_scan_C5/W100 2>&1 | tee -a "$OUTFILE"
echo "" | tee -a "$OUTFILE"

echo "DONE. Wrote: $OUTFILE" | tee -a "$OUTFILE"
