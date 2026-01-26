#!/usr/bin/env python3
"""
merge_glueoff_into_engine.py (v0.2.1)

More robust merger for the glue-off ablation hook into the CURRENT engine_vglue.py.

Improvements vs v0.2:
- Detects _load_v_blocks by `def _load_v_blocks(` regardless of type annotations.
- Locates the first `return {` inside that function and uses its indentation.
- Works with either "hop" or 'hop' keys in the return dict.
- Inserts q_base_override application after any `cfg_hop.q_base = _compute_q_base(...)` assignment.
- Inserts v_glue["ablation"] after the "W_coh" field if possible.

Run from Desktop:
  python3 bcqm_vi_spacetime/analysis/merge_glueoff_into_engine.py
"""
from __future__ import annotations

import re
import time
from pathlib import Path


def backup_file(src: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    dst = backup_dir / f"{src.name}.{ts}.bak"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dst


def find_load_v_blocks_region(text: str) -> tuple[int, int]:
    m = re.search(r"^def\s+_load_v_blocks\s*\(", text, flags=re.MULTILINE)
    if not m:
        raise RuntimeError("Couldn't find def _load_v_blocks(")
    start = m.start()
    # heuristic end: next top-level def after start
    m2 = re.search(r"^\s*def\s+", text[m.end():], flags=re.MULTILINE)
    if not m2:
        return start, len(text)
    end = m.end() + m2.start()
    return start, end


def insert_ablation_block(text: str) -> str:
    if "glue_decohere" in text:
        return text

    start, end = find_load_v_blocks_region(text)
    block_text = text[start:end]

    # find first return dict in this function
    mret = re.search(r"^\s*return\s*\{\s*$", block_text, flags=re.MULTILINE)
    if not mret:
        # alternative: return { on same line
        mret = re.search(r"^\s*return\s*\{", block_text, flags=re.MULTILINE)
    if not mret:
        raise RuntimeError("Couldn't find return { inside _load_v_blocks")
    # indentation is leading whitespace of the return line
    line_start = block_text.rfind("\n", 0, mret.start()) + 1
    indent = re.match(r"\s*", block_text[line_start:mret.start()]).group(0)

    insert_lines = [
        "",
        indent + "# Ablation hook: optionally destroy glue coherence while keeping space enabled.",
        indent + "# Controlled by YAML:",
        indent + "#   ablation:",
        indent + "#     glue_decohere: true",
        indent + "abl = cfg.get('ablation', {}) or {}",
        indent + "if bool(abl.get('glue_decohere', False)):",
        indent + "    # Disable phase lock and cadence coupling (keep other params for provenance).",
        indent + "    try:",
        indent + "        phase.enabled = False",
        indent + "    except Exception:",
        indent + "        pass",
        indent + "    try:",
        indent + "        phase.lambda_phase = 0.0",
        indent + "    except Exception:",
        indent + "        pass",
        indent + "    try:",
        indent + "        cadence.lambda_cadence = 0.0",
        indent + "    except Exception:",
        indent + "        pass",
        indent + "    # Disable shared bias and domains (conservative).",
        indent + "    try:",
        indent + "        shared.enabled = False",
        indent + "    except Exception:",
        indent + "        pass",
        indent + "    try:",
        indent + "        shared.lambda_bias = 0.0",
        indent + "    except Exception:",
        indent + "        pass",
        indent + "    try:",
        indent + "        domains.enabled = False",
        indent + "    except Exception:",
        indent + "        pass",
        indent + "    try:",
        indent + "        domains.lambda_domain = 0.0",
        indent + "    except Exception:",
        indent + "        pass",
        indent + "    # Increase hop-noise by overriding q_base unless overridden by YAML.",
        indent + "    try:",
        indent + "        hop.q_base_override = float(abl.get('q_base_override', 0.45))",
        indent + "    except Exception:",
        indent + "        hop.q_base_override = 0.45",
        "",
    ]
    ins = "\n".join(insert_lines)

    # insert immediately before the return line
    block_text2 = block_text[:line_start] + ins + block_text[line_start:]
    return text[:start] + block_text2 + text[end:]


def insert_q_base_override(text: str) -> str:
    if "q_base_override" in text and "hasattr(cfg_hop, 'q_base_override')" in text:
        return text
    # find first assignment line
    m = re.search(r"^\s*cfg_hop\.q_base\s*=\s*_compute_q_base\(cfg_hop,\s*W_coh\)\s*$", text, flags=re.MULTILINE)
    if not m:
        return text  # don't fail hard; some variants may name differently
    line_start = text.rfind("\n", 0, m.start()) + 1
    indent = re.match(r"\s*", text[line_start:m.start()]).group(0)
    insert = "\n".join([
        m.group(0),
        indent + "if hasattr(cfg_hop, 'q_base_override'):",
        indent + "    cfg_hop.q_base = float(getattr(cfg_hop, 'q_base_override'))",
    ])
    # replace the matched line with itself + override block
    return text[:line_start] + insert + text[m.end():]


def insert_cfgobj_ablation(text: str) -> str:
    if '"ablation": cfg.get("ablation", {})' in text:
        return text
    # try to locate v_glue block: look for '"W_coh": int(W_coh),' and insert after it.
    m = re.search(r'("W_coh"\s*:\s*int\(W_coh\)\s*,\s*\n)', text)
    if not m:
        return text
    insert = m.group(1) + '            "ablation": cfg.get("ablation", {}),\n'
    return text[:m.start(1)] + insert + text[m.end(1):]


def main() -> None:
    desktop = Path.cwd()
    code = desktop / "bcqm_vi_spacetime"
    eng = code / "engine_vglue.py"
    if not eng.exists():
        raise SystemExit("Expected bcqm_vi_spacetime/engine_vglue.py in current directory.")
    backup_dir = desktop / "outputs" / "analysis" / "backups"
    bak = backup_file(eng, backup_dir)

    text = eng.read_text(encoding="utf-8")
    text2 = insert_ablation_block(text)
    text2 = insert_q_base_override(text2)
    text2 = insert_cfgobj_ablation(text2)

    eng.write_text(text2, encoding="utf-8")
    print(f"Backed up to: {bak}")
    print("Patched: bcqm_vi_spacetime/engine_vglue.py")


if __name__ == "__main__":
    main()
