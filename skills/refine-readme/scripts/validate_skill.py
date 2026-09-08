#!/usr/bin/env python3
"""Validate the bundled Skill metadata and required resources."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REQUIRED = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/five-layer-workflow.md",
    "references/cover-system.md",
    "references/project-native-directions.md",
    "references/style-catalog.md",
    "references/fact-check.md",
    "references/github-rendering.md",
    "assets/styles/presets.json",
)


def main() -> int:
    errors: list[str] = []
    skill = ROOT / "SKILL.md"
    text = skill.read_text(encoding="utf-8") if skill.is_file() else ""
    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter:
        errors.append("SKILL.md is missing YAML frontmatter")
    else:
        header = frontmatter.group(1)
        if not re.search(r"^name:\s*refine-readme\s*$", header, re.MULTILINE):
            errors.append("frontmatter name must be refine-readme")
        if not re.search(r"^description:\s*\S.+$", header, re.MULTILINE):
            errors.append("frontmatter description is required")

    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    if (ROOT / "README.md").exists():
        errors.append("README.md belongs at repository root, not inside the Skill")

    try:
        presets = json.loads((ROOT / "assets/styles/presets.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid presets.json: {error}")
        presets = {}
    required_fields = {"name", "best_for", "canvas", "background", "foreground", "accent", "support", "motif", "layout", "proof_slots", "negative"}
    for style_id, preset in presets.items():
        if not re.fullmatch(r"[a-z0-9-]+", style_id):
            errors.append(f"invalid style id: {style_id}")
        missing = required_fields - set(preset)
        if missing:
            errors.append(f"{style_id} missing fields: {', '.join(sorted(missing))}")
    if len(presets) < 3:
        errors.append("at least three style presets are required")

    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1
    print(f"Skill valid: refine-readme ({len(presets)} style presets)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
