#!/usr/bin/env python3
"""Check a README for local paths, image alt text, hierarchy, and package scripts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote


LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)]+)\)")
HTML_IMG_RE = re.compile(r"<img\b(?P<attrs>[^>]+)>", re.IGNORECASE)
HTML_ATTR_RE = re.compile(r"(?P<name>[a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*([\"'])(?P<value>.*?)\2")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
PNPM_RE = re.compile(r"\bpnpm\s+(?:run\s+)?([a-zA-Z0-9:_-]+)")


def find_readme(root: Path) -> Path | None:
    if root.is_file():
        return root
    for name in ("README.md", "readme.md", "README.MD"):
        candidate = root / name
        if candidate.is_file():
            return candidate
    return None


def clean_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def package_scripts(root: Path) -> set[str]:
    path = root / "package.json"
    if not path.is_file():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return set((data.get("scripts") or {}).keys())


def check(readme: Path) -> dict:
    text = readme.read_text(encoding="utf-8", errors="replace")
    root = readme.parent
    findings: list[dict[str, str]] = []
    local_images = 0

    for match in LINK_RE.finditer(text):
        is_image = bool(match.group(1))
        alt = match.group(2).strip()
        target = clean_target(match.group(3))
        if is_image and not alt:
            findings.append({"severity": "warning", "code": "empty-image-alt", "target": target})
        if target.startswith(("http://", "https://", "mailto:", "#", "data:")):
            continue
        path_part = unquote(target.split("#", 1)[0])
        if not path_part:
            continue
        if is_image:
            local_images += 1
        if not (root / path_part).resolve().exists():
            findings.append({"severity": "error", "code": "missing-local-path", "target": target})

    html_images: list[dict[str, str]] = []
    for match in HTML_IMG_RE.finditer(text):
        attrs = {
            item.group("name").lower(): item.group("value")
            for item in HTML_ATTR_RE.finditer(match.group("attrs"))
        }
        source = attrs.get("src", "").strip()
        alt = attrs.get("alt", "").strip()
        html_images.append({"src": source, "alt": alt})
        if not alt:
            findings.append({"severity": "warning", "code": "empty-image-alt", "target": source})
        if not source or source.startswith(("http://", "https://", "data:")):
            continue
        local_images += 1
        path_part = unquote(source.split("#", 1)[0])
        if path_part and not (root / path_part).resolve().exists():
            findings.append({"severity": "error", "code": "missing-local-path", "target": source})

    headings = [(len(m.group(1)), m.group(2).strip()) for m in HEADING_RE.finditer(text)]
    for previous, current in zip(headings, headings[1:]):
        if current[0] > previous[0] + 1:
            findings.append({
                "severity": "warning",
                "code": "heading-level-skip",
                "target": f"{previous[1]} -> {current[1]}",
            })

    scripts = package_scripts(root)
    if scripts:
        for command in sorted(set(PNPM_RE.findall(text))):
            if command in {"install", "add", "dlx", "exec"}:
                continue
            if command not in scripts:
                findings.append({"severity": "warning", "code": "unknown-pnpm-script", "target": command})

    first_h2 = text.find("\n## ")
    opening = text if first_h2 == -1 else text[:first_h2]
    has_opening_cover = bool(re.search(r"!\[[^\]]+\]\([^)]*(?:cover|hero)[^)]*\)", opening, re.IGNORECASE))
    if not has_opening_cover:
        has_opening_cover = any(
            ("cover" in image["src"].lower() or "hero" in image["src"].lower())
            and match.start() < (first_h2 if first_h2 != -1 else len(text))
            for match, image in zip(HTML_IMG_RE.finditer(text), html_images)
        )
    if not has_opening_cover:
        findings.append({"severity": "warning", "code": "no-opening-cover", "target": readme.name})

    errors = sum(item["severity"] == "error" for item in findings)
    warnings = sum(item["severity"] == "warning" for item in findings)
    return {
        "readme": str(readme),
        "ok": errors == 0,
        "summary": {"errors": errors, "warnings": warnings, "local_images": local_images},
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".")
    parser.add_argument("--output")
    args = parser.parse_args()

    target = Path(args.repository).expanduser().resolve()
    readme = find_readme(target)
    if not readme:
        parser.error(f"README.md not found under {target}")
    payload = check(readme)
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
