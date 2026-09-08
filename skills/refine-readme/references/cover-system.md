# README cover system

## Standard formats

| Format | Size | Use |
| --- | --- | --- |
| Standard | `1200x400` | Default repository hero |
| Compact | `1200x320` | CLI, library, and documentation projects |
| Showcase | `1200x480` | SaaS, creative projects, and proof-rich galleries |

Keep a separate `1200x630` Open Graph image. Do not assume a social card will
work as a README hero.

## Construction modes

### Deterministic SVG

Use for APIs, SDKs, CLIs, libraries, infrastructure, diagrams, and projects with
strong symbolic or typographic identities. Keep all factual text in SVG source.

### Proof composite

Use real screenshots, terminal output, generated results, or prompt cards inside
a deterministic SVG frame. Do not invent dashboard data or polished outputs.
Use a single-board hero only when the proof remains readable at the target
GitHub width. Otherwise make the cover simple and place proof immediately below.

### Hybrid generated subject

Use image generation only for a character, organic material, cinematic setting,
or texture that is cumbersome to draw. Generate it without important text, then
place it under exact SVG typography. Preserve a source prompt and editable SVG.

## Safe layout

- Keep important content inside an 8% outer safe area.
- Use one visual center and one primary reading path.
- Keep the project name legible when rendered near 900 CSS pixels wide.
- Use no more than one short supporting line in the cover.
- Avoid tiny fake UI, dense diagrams, long feature lists, and decorative badges.
- Test the cover on light and dark GitHub themes and near 360 CSS pixels wide.
- Keep project attribution separate from tool attribution. User covers contain
  no README Refiner branding or watermark by default.

## Required checks

- Exact spelling and casing of project name.
- No cropped title, key proof, logo, face, or semantic contact point.
- Sufficient contrast without relying on a page background.
- Meaningful alt text in the README.
- SVG source remains editable and uses no unsupported remote dependencies.
