#!/bin/bash
set -euo pipefail
TS=$(date +"%Y%m%d_%H%M%S")
ANADIR="outputs/analysis"
mkdir -p "$ANADIR"
OUTFILE="$ANADIR/${TS}_geometry_diagnosis_W100.txt"

echo "BCQM VI Geometry diagnosis — $(date)" | tee "$OUTFILE"
echo "" | tee -a "$OUTFILE"

CFG="configs/generated_vreg_C5_subset/geometry_diagnosis_C5_W100_N8_n0p6_seed56796.yml"
echo "== RUN: $CFG ==" | tee -a "$OUTFILE"
python3 -m bcqm_vi_spacetime.cli run --config "$CFG" 2>&1 | tee -a "$OUTFILE"
echo "" | tee -a "$OUTFILE"

echo "== DIAGNOSIS ==" | tee -a "$OUTFILE"
python3 bcqm_vi_spacetime/analysis/geometry_diagnosis.py outputs_glue_axes/geometry_diagnosis_C5/W100/N8/n0p6_seed56796 2>&1 | tee -a "$OUTFILE"

echo "" | tee -a "$OUTFILE"
echo "DONE. Wrote: $OUTFILE" | tee -a "$OUTFILE"
