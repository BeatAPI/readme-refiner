---
name: refine-readme
description: Redesign, generate, or audit a GitHub repository README using real repository evidence, a required project-native cover, maintainable Markdown, proof media, diagrams, and factual/GitHub rendering checks. Use when a user asks to beautify, improve, generate, restructure, review, fact-check, or create visual assets for a repository README, including README covers, SVG heroes, screenshots, workflows, before/after examples, and GitHub-safe previews.
---

# Refine README

Turn a real repository into a clear, polished, truthful, and maintainable
GitHub homepage. Treat the README as a product landing page constrained by
GitHub rendering, not as a poster or a generic generated document.

## Choose the operating mode

Infer the mode when the request is explicit. Otherwise ask whether the user
wants `audit`, `cover`, `beautify`, or `check`.

- `audit`: inspect and report only; do not edit files.
- `cover`: create visual assets only; do not edit README content or references.
- `beautify`: execute the complete project-native workflow and propose a README diff.
- `check`: validate facts and GitHub rendering without redesigning.

Reading repository files does not grant permission to edit, commit, push, open a
pull request, or publish. Always preview first. Require separate explicit
approval for commit, push, PR, and publication actions.

## Run the project-native workflow

1. Establish repository truth.
   - Inspect the current README, manifests, package scripts, public routes,
     configuration examples, docs, tests, and existing visual assets.
   - Run `scripts/inspect_repository.py <repository>` for a deterministic first
     inventory.
   - Build a fact ledger that separates confirmed evidence, reasonable
     inference, user-supplied claims, and unsupported claims.

2. Pass the project-native direction gate.
   - Resolve the audience, one-sentence value, primary proof, first successful
     action, and native visual material before selecting a style.
   - Run `scripts/plan_directions.py <repository>` for three evidence-led
     candidates, then sharpen them with repository-specific reasoning.
   - If the planner reports a blocked gate, request repository evidence instead
     of returning arbitrary zero-evidence styles.
   - For every direction, explain why it fits, its project-native motif, its
     real proof, construction mode, hero composition, and primary risk.
   - Treat bundled styles as seeds and constraints, not immutable templates.
   - Read `references/project-native-directions.md` before recommending styles.

3. Rebuild the story and Markdown hierarchy.
   - Make the first screen answer what the project is, who it is for, what proof
     exists, and how to try it.
   - Move real screenshots, outputs, examples, or a minimal command ahead of
     internal architecture when they are the clearest proof.
   - Keep installation, configuration, API, contribution, and license sections
     precise and scannable.
   - Read `references/five-layer-workflow.md` for the default section logic.

4. Create the cover and visual identity.
   - In `beautify` mode, create a cover unless the user explicitly opts out.
   - Default to `1200x400` SVG. Use `1200x320` for compact technical projects
     and `1200x480` for proof-rich showcases.
   - When no direction is selected, recommend exactly three evidence-led
     directions and ask the user to choose. Auto-select only when the user says
     to decide automatically.
   - Choose one coherent direction. Adapt one style seed to the project instead
     of applying a fixed template or mixing unrelated decorative traits.
   - Use `scripts/render_cover.py` for deterministic exact-text SVG covers.
   - If generated imagery is needed, generate only the subject, texture, or
     background. Add project names, commands, metrics, and labels through SVG.
   - Read `references/cover-system.md` before creating or reviewing a cover.

5. Add proof and explanation.
   - Prefer real screenshots, outputs, input/output comparisons, terminal
     captures, or diagrams over decorative images.
   - Use SVG for exact diagrams and coordinated section transitions; use
     Mermaid for relationships that benefit from maintainable text source.
   - Keep explanations and commands in Markdown so they remain searchable and
     copyable.

6. Validate and deliver.
   - Run `scripts/check_readme.py <repository>`.
   - Review factual claims against the ledger and `references/fact-check.md`.
   - Apply the GitHub rendering rules in `references/github-rendering.md`.
   - Show the changed README, source assets, warnings, and a diff.
   - Do not claim completion when broken paths, unsupported commands, unreadable
     cover text, or invented claims remain.

## Output locations

Use these defaults unless the repository already has a documented convention:

```text
assets/readme/cover.svg
assets/readme/cover.webp
assets/readme/architecture.svg
.readme-refiner/report.json
.readme-refiner/preview/
```

Do not create a raster derivative unless the current run produced a real source
artifact. Do not scan unrelated generation folders and guess which image belongs
to the run.

## Quality gates

- The first screen communicates one concrete promise and one real proof.
- The cover uses exact, readable text and survives narrow rendering.
- The title, palette, motifs, and proof feel native to this repository.
- Removing the project name would not make the visual fit an unrelated project.
- Claims, commands, paths, versions, ports, and public interfaces match source.
- Images have meaningful alt text and do not replace essential body content.
- Relative paths and heading anchors resolve.
- The result remains useful with images disabled.
- The user can review every change before anything is published.
- Do not place README Refiner branding in user assets by default; attribution is
  optional and belongs outside the project hero.
