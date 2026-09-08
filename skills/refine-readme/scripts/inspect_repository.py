#!/usr/bin/env python3
"""Produce a small evidence inventory without executing repository code."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


MANIFESTS = (
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "Gemfile",
    "composer.json",
    "pom.xml",
    "build.gradle",
)
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build", ".output", ".venv", "venv"}


def read_text(path: Path, limit: int = 1_000_000) -> str:
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def find_readme(root: Path) -> Path | None:
    for name in ("README.md", "readme.md", "README.MD"):
        candidate = root / name
        if candidate.is_file():
            return candidate
    return None


def package_facts(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"parse_error": True}
    return {
        "name": data.get("name"),
        "description": data.get("description"),
        "package_manager": data.get("packageManager"),
        "scripts": sorted((data.get("scripts") or {}).keys()),
    }


def inventory(root: Path) -> dict:
    readme = find_readme(root)
    readme_text = read_text(readme) if readme else ""
    headings = [
        {"level": len(match.group(1)), "text": match.group(2).strip()}
        for match in re.finditer(r"^(#{1,6})\s+(.+)$", readme_text, re.MULTILINE)
    ]

    manifests: dict[str, dict | str] = {}
    for name in MANIFESTS:
        path = root / name
        if path.is_file():
            manifests[name] = package_facts(path) if name == "package.json" else "present"

    assets: list[str] = []
    for base_name in ("assets", "public", "docs", "media", "screenshots"):
        base = root / base_name
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.is_file() and path.suffix.lower() in ASSET_SUFFIXES:
                assets.append(path.relative_to(root).as_posix())
                if len(assets) >= 80:
                    break

    package = manifests.get("package.json") if isinstance(manifests.get("package.json"), dict) else {}
    project_name = package.get("name") if package else None
    if not project_name and headings:
        project_name = re.sub(r"[*_`]", "", headings[0]["text"])

    return {
        "root": str(root),
        "project_name": project_name or root.name,
        "readme": readme.name if readme else None,
        "headings": headings,
        "manifests": manifests,
        "existing_visual_assets": sorted(assets),
        "has_cover_hint": any("cover" in item.lower() or "hero" in item.lower() for item in assets),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".")
    parser.add_argument("--output", help="Write JSON to this path instead of stdout")
    args = parser.parse_args()

    root = Path(args.repository).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"repository is not a directory: {root}")

    payload = json.dumps(inventory(root), indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
