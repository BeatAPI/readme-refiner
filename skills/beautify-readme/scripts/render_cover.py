#!/usr/bin/env python3
"""Render an exact-text SVG README cover from a bundled style preset."""

from __future__ import annotations

import argparse
import json
import textwrap
from html import escape
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRESETS_PATH = HERE.parent / "assets" / "styles" / "presets.json"


def load_presets() -> dict:
    return json.loads(PRESETS_PATH.read_text(encoding="utf-8"))


def motif(style: str, accent: str, support: str, foreground: str) -> str:
    if style == "protocol-grid":
        return f'''<g transform="translate(760 76)">
  <rect width="360" height="248" rx="18" fill="#111820" stroke="{support}" stroke-opacity=".45"/>
  <text x="24" y="42" fill="{accent}" class="mono small">POST /v1/tasks</text>
  <path d="M24 64H336" stroke="{support}" stroke-opacity=".35"/>
  <rect x="24" y="88" width="132" height="40" rx="8" fill="{accent}" fill-opacity=".12" stroke="{accent}"/>
  <text x="42" y="114" fill="{accent}" class="mono tiny">REQUEST</text>
  <path d="M162 108H218" stroke="{accent}" stroke-width="2"/><path d="M210 101l9 7-9 7" fill="none" stroke="{accent}" stroke-width="2"/>
  <rect x="224" y="88" width="112" height="40" rx="8" fill="{accent}" fill-opacity=".12" stroke="{accent}"/>
  <text x="246" y="114" fill="{accent}" class="mono tiny">OUTPUT</text>
  <circle cx="36" cy="180" r="6" fill="{accent}"/><path d="M48 180H310" stroke="{support}" stroke-width="2" stroke-dasharray="7 8"/>
  <circle cx="324" cy="180" r="6" fill="{accent}"/>
  <text x="24" y="222" fill="{support}" class="mono tiny">truth → design → proof → check</text>
</g>'''
    if style == "product-proof":
        return f'''<g transform="translate(770 56)">
  <rect x="0" y="36" width="300" height="250" rx="18" fill="#fff" stroke="{foreground}" stroke-opacity=".16"/>
  <rect x="38" y="0" width="300" height="250" rx="18" fill="#fff" stroke="{foreground}" stroke-opacity=".16"/>
  <rect x="62" y="24" width="252" height="126" rx="12" fill="{accent}" fill-opacity=".1"/>
  <path d="M86 116l48-42 38 30 42-55 68 67z" fill="{accent}" fill-opacity=".75"/>
  <circle cx="254" cy="58" r="13" fill="{support}"/>
  <rect x="62" y="174" width="150" height="11" rx="5" fill="{foreground}" fill-opacity=".75"/>
  <rect x="62" y="199" width="214" height="9" rx="4" fill="{foreground}" fill-opacity=".22"/>
</g>'''
    if style == "research-field":
        return f'''<g transform="translate(790 62)" fill="none" stroke="{foreground}" stroke-width="5" stroke-linecap="round">
  <path d="M22 254C82 238 58 134 126 126s70 90 132 50 22-118 100-136"/>
  <circle cx="22" cy="254" r="12" fill="{accent}"/><circle cx="126" cy="126" r="9" fill="{accent}"/>
  <circle cx="258" cy="176" r="14" fill="{accent}"/><circle cx="358" cy="40" r="10" fill="{accent}"/>
</g>'''
    if style == "ink-archive":
        dots = "".join(
            f'<circle cx="{x}" cy="{y}" r="{3 + ((x + y) // 20) % 3}" fill="{foreground}"/>'
            for y in range(88, 260, 24)
            for x in range(820, 1084, 24)
            if ((x // 24) + (y // 24)) % 3 != 0
        )
        return f'<g opacity=".9">{dots}</g>'
    if style == "modular-build":
        return f'''<g transform="translate(790 64)">
  <rect x="0" y="176" width="84" height="84" fill="{accent}"/><rect x="92" y="132" width="84" height="128" fill="{support}"/>
  <rect x="184" y="82" width="84" height="178" fill="{accent}" fill-opacity=".75"/><rect x="276" y="28" width="84" height="232" fill="{support}" fill-opacity=".78"/>
  <path d="M42 164L134 120 226 70 318 16" fill="none" stroke="{foreground}" stroke-width="5" stroke-dasharray="9 9"/>
  <circle cx="42" cy="164" r="9" fill="{foreground}"/><circle cx="318" cy="16" r="9" fill="{foreground}"/>
</g>'''
    return f'''<g transform="translate(792 92)">
  <rect x="0" y="58" width="112" height="112" rx="28" fill="{accent}" fill-opacity=".16" stroke="{accent}" stroke-width="3"/>
  <rect x="248" y="58" width="112" height="112" rx="28" fill="{support}" fill-opacity=".16" stroke="{support}" stroke-width="3"/>
  <path d="M112 114C156 72 204 156 248 114" fill="none" stroke="url(#connector)" stroke-width="8" stroke-linecap="round"/>
  <circle cx="180" cy="114" r="12" fill="{foreground}"/>
  <text x="56" y="126" text-anchor="middle" fill="{accent}" class="sans symbol">A</text>
  <text x="304" y="126" text-anchor="middle" fill="{support}" class="sans symbol">B</text>
</g>'''


def render(style_id: str, title: str, tagline: str, accent_override: str | None = None) -> str:
    presets = load_presets()
    if style_id not in presets:
        raise KeyError(f"unknown style: {style_id}; choose from {', '.join(sorted(presets))}")
    preset = presets[style_id]
    width, height = (int(value) for value in preset["canvas"].split("x"))
    background = preset["background"]
    foreground = preset["foreground"]
    accent = accent_override or preset["accent"]
    support = preset["support"]
    safe_title = escape(title)
    safe_tagline = escape(textwrap.shorten(tagline, width=78, placeholder="…"))
    style_name = escape(preset["name"])
    font_size = 76 if len(title) <= 18 else 60 if len(title) <= 30 else 48

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{safe_title}</title>
  <desc id="desc">{safe_tagline}</desc>
  <defs>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{support}" stroke-opacity=".12"/></pattern>
    <linearGradient id="connector"><stop stop-color="{accent}"/><stop offset="1" stop-color="{support}"/></linearGradient>
  </defs>
  <style>
    .sans {{ font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .mono {{ font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace; }}
    .serif {{ font-family: Georgia, "Times New Roman", serif; }}
    .small {{ font-size: 18px; font-weight: 700; }} .tiny {{ font-size: 14px; font-weight: 600; }} .symbol {{ font-size: 34px; font-weight: 800; }}
  </style>
  <rect width="{width}" height="{height}" rx="24" fill="{background}"/>
  <rect width="{width}" height="{height}" rx="24" fill="url(#grid)" opacity="{'.45' if style_id == 'protocol-grid' else '.08'}"/>
  <text x="72" y="72" fill="{accent}" class="mono small" letter-spacing="2">AWESOME README STUDIO · {style_name.upper()}</text>
  <text x="72" y="190" fill="{foreground}" class="{'serif' if style_id == 'research-field' else 'sans'}" font-size="{font_size}" font-weight="800" letter-spacing="-2">{safe_title}</text>
  <text x="76" y="242" fill="{support}" class="sans" font-size="22" font-weight="600">{safe_tagline}</text>
  <rect x="72" y="292" width="188" height="42" rx="21" fill="{accent}"/>
  <text x="166" y="319" text-anchor="middle" fill="{background}" class="mono" font-size="15" font-weight="800">BEAUTIFUL · TRUE</text>
  {motif(style_id, accent, support, foreground)}
</svg>'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--style")
    parser.add_argument("--title")
    parser.add_argument("--tagline", default="A beautiful, truthful, GitHub-safe README")
    parser.add_argument("--accent", help="Optional CSS color override")
    parser.add_argument("--output")
    parser.add_argument("--list-styles", action="store_true")
    args = parser.parse_args()

    presets = load_presets()
    if args.list_styles:
        print("\n".join(sorted(presets)))
        return 0
    if not args.style or not args.title or not args.output:
        parser.error("--style, --title, and --output are required unless --list-styles is used")
    try:
        svg = render(args.style, args.title, args.tagline, args.accent)
    except KeyError as error:
        parser.error(str(error))
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
