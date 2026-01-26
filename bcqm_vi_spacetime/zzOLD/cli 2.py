\
from __future__ import annotations

import argparse
from pathlib import Path

from .io import load_yaml
from .runner import run_from_config, scan_from_config


def main() -> None:
    parser = argparse.ArgumentParser(prog="bcqmvi", description="bcqm_vi_spacetime CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Run a config (may include scan lists)")
    p_run.add_argument("--config", required=True, type=str, help="Path to YAML config")

    p_scan = sub.add_parser("scan", help="Run a scan over n, sizes, seeds as defined in YAML")
    p_scan.add_argument("--config", required=True, type=str, help="Path to YAML config")

    args = parser.parse_args()
    cfg = load_yaml(Path(args.config))

    if args.cmd == "run":
        run_from_config(cfg)
    elif args.cmd == "scan":
        scan_from_config(cfg)
    else:
        raise SystemExit(f"Unknown command: {args.cmd}")


if __name__ == "__main__":
    main()
