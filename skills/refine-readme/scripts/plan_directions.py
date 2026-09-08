#!/usr/bin/env python3
"""Recommend three evidence-led README directions without editing the repository."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from inspect_repository import inventory  # noqa: E402


STYLE_RULES = {
    "protocol-grid": {
        "terms": ("api", "sdk", "cli", "endpoint", "developer", "server", "infrastructure", "async", "asynchronous", "task", "request", "response"),
        "why": "The repository exposes a technical interface that can become the visual grammar.",
        "motif": "one real request, its task lifecycle, and the verified output",
        "proof": "a copyable command or real request/response",
    },
    "product-proof": {
        "terms": ("app", "dashboard", "web", "studio", "generator", "video", "image", "product", "gallery", "preview"),
        "why": "The result is easier to trust when real product output leads the visual system.",
        "motif": "one real product frame or output, not a generic device mockup",
        "proof": "a real screenshot, generated result, or before/after",
    },
    "research-field": {
        "terms": ("research", "model", "dataset", "benchmark", "paper", "analysis", "knowledge", "evidence"),
        "why": "The repository is better framed through its method and evidence than through decorative UI.",
        "motif": "one repository-specific method, signal, or data relationship",
        "proof": "a verified method, dataset, benchmark, or result",
    },
    "ink-archive": {
        "terms": ("database", "storage", "archive", "index", "query", "record", "catalog", "collection"),
        "why": "Records, queries, or indexed material provide a native restrained visual language.",
        "motif": "one real record, query, index, or catalog structure",
        "proof": "a real query, record, or indexed output",
    },
    "modular-build": {
        "terms": ("builder", "workflow", "automation", "pipeline", "template", "tutorial", "compose"),
        "why": "The project value is created through an understandable sequence of building blocks.",
        "motif": "the smallest real sequence from input to completed output",
        "proof": "a verified workflow, module path, or completed result",
    },
    "integration-bridge": {
        "terms": ("plugin", "integration", "mcp", "dify", "connector", "webhook", "provider"),
        "why": "The project connects two recognizable systems through one concrete action.",
        "motif": "the two real endpoints and the action that crosses between them",
        "proof": "a verified integration flow or successful action",
    },
}


def repository_text(data: dict) -> str:
    pieces = [str(data.get("project_name", "")), str(data.get("readme_excerpt", ""))]
    for heading in data.get("headings", []):
        pieces.append(str(heading.get("text", "")))
    for manifest in data.get("manifests", {}).values():
        if isinstance(manifest, dict):
            pieces.extend(str(manifest.get(key, "")) for key in ("name", "description"))
    pieces.extend(data.get("existing_visual_assets", []))
    return " ".join(pieces).lower()


def recommend(data: dict) -> dict:
    text = repository_text(data)
    tokens = set(re.findall(r"[a-z0-9]+", text))
    visual_markers = ("screenshot", "demo", "output", "result", "preview", "hero", "gallery")
    has_visual_proof = any(
        marker in asset.lower()
        for asset in data.get("existing_visual_assets", [])
        for marker in visual_markers
    )

    scored: list[tuple[int, str, list[str]]] = []
    for style, rule in STYLE_RULES.items():
        matched_terms = sorted(term for term in rule["terms"] if term in tokens)
        score = len(matched_terms) * 3
        if style == "product-proof" and has_visual_proof:
            score += 5
        scored.append((score, style, matched_terms))
    scored.sort(key=lambda item: (-item[0], item[1]))

    evidence_backed = [item for item in scored if item[0] > 0]
    directions = []
    if evidence_backed:
        for score, style, matched_terms in evidence_backed[:3]:
            rule = STYLE_RULES[style]
            directions.append({
                "style_seed": style,
                "evidence_score": score,
                "matched_terms": matched_terms,
                "why_it_fits": rule["why"],
                "project_native_motif": rule["motif"],
                "primary_proof": rule["proof"],
                "construction_mode": "proof-composite" if has_visual_proof else "deterministic-svg",
                "decision_status": "candidate; verify against repository facts before production",
            })

    gate_status = "ready" if len(directions) == 3 else "blocked"
    gate_reason = (
        "Repository evidence supports three candidate directions."
        if gate_status == "ready"
        else "Fewer than three evidence-backed directions were found. Add or identify a README, manifest description, public interface, workflow, or real visual proof before selecting a direction."
    )
    return {
        "repository": data.get("root"),
        "project_name": data.get("project_name"),
        "direction_gate": {"status": gate_status, "reason": gate_reason},
        "project_brief": {
            "audience": "verify from current docs, package metadata, and user evidence",
            "one_sentence_value": "derive from confirmed behavior, not the repository tagline alone",
            "primary_proof": "select the strongest real output before designing the hero",
            "first_successful_action": "identify the shortest verified path to a useful result",
            "native_visual_material": data.get("existing_visual_assets", [])[:12],
        },
        "directions": directions,
        "selection_rule": "Choose the direction with the strongest repository-specific motif and proof, not the highest score alone.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".")
    parser.add_argument("--output")
    args = parser.parse_args()

    root = Path(args.repository).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"repository is not a directory: {root}")
    payload = recommend(inventory(root))
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
