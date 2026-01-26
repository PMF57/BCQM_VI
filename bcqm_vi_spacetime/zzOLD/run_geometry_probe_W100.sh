#!/bin/bash
set -euo pipefail
TS=$(date +"%Y%m%d_%H%M%S")
ANADIR="outputs/analysis"
mkdir -p "$ANADIR"
OUTFILE="$ANADIR/${TS}_geometry_probe_W100.txt"

echo "BCQM VI Geometry probe (spectral dimension) — $(date)" | tee "$OUTFILE"
echo "" | tee -a "$OUTFILE"

run_cfg () {
  local cfg="$1"
  echo "== RUN: $cfg ==" | tee -a "$OUTFILE"
  python3 -m bcqm_vi_spacetime.cli run --config "$cfg" 2>&1 | tee -a "$OUTFILE"
  echo "" | tee -a "$OUTFILE"
}

summarise () {
  local root="$1"
  echo "== GEOMETRY SUMMARY: $root ==" | tee -a "$OUTFILE"
  python3 bcqm_vi_spacetime/analysis/geometry_summary.py "$root" 2>&1 | tee -a "$OUTFILE"
  echo "" | tee -a "$OUTFILE"
}

CFG4="configs/generated_vreg_C5_subset/geometry_probe_C5_W100_N4_n0p8.yml"
CFG8="configs/generated_vreg_C5_subset/geometry_probe_C5_W100_N8_n0p8.yml"

run_cfg "$CFG4"
run_cfg "$CFG8"

summarise "outputs_glue_axes/geometry_probe/W100"
echo "DONE. Wrote: $OUTFILE" | tee -a "$OUTFILE"
