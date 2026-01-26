# BCQM VI — Spacetime (Path A) reference implementation

This repository contains the reference **code + configs** to reproduce the BCQM VI Stage‑1 results.

**Workflow note:** as in earlier BCQM repos, the *paper sources and figures* are kept locally/cloud; the paper itself is archived on Zenodo as a PDF. This repo is intended to be rerunnable end‑to‑end and to regenerate the reported results.

## Quick start

### Install
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

### Selftest
From repo root:
```bash
bash bcqm_vi_spacetime/pipelines/run_selftest.sh
```

Selftest verifies:
- all **VI** YAML configs under `configs/` validate,
- the major runtime paths execute (nospace / space‑on / glue‑off / geometry hook).

## Reproducing results
See:
- `REPRODUCIBILITY.md` (commands / pipelines)
- `FIGURE_MAP.md` (locked mapping of figure numbers to filenames and pipelines)

## Repo layout
- `bcqm_vi_spacetime/` — code (package)
- `configs/` — YAML configs
- `.github/workflows/` — optional CI selftest
