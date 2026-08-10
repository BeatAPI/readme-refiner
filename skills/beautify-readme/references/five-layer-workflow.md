# Five-layer workflow

## 1. Repository truth

Confirm the project name, audience, purpose, package scripts, installation path,
configuration requirements, public interfaces, proof assets, license, and status.
Do not treat a TODO, test fixture, unused adapter, or historical document as a
shipped capability.

Classify every claim as one of:

- `confirmed`: directly supported by current source or user-approved evidence;
- `inferred`: a conservative conclusion from multiple current files;
- `supplied`: provided by the user but not independently verified;
- `unsupported`: missing or contradicted evidence; exclude or flag it.

## 2. Story and Markdown

Default reading order:

1. Cover
2. One-sentence project promise
3. Real proof or minimal example
4. Why it is useful or different
5. Quick Start
6. Core capabilities
7. Workflow or architecture
8. Configuration and reference details
9. Contribution, status, and license

Change the order when repository evidence shows a better first-use path. Avoid
long tables of contents for short READMEs, repeated feature claims, and directory
trees before the reader understands the project.

## 3. Cover and identity

Create one cover system, not unrelated decorative assets. Reuse its palette,
typography logic, spacing, line treatment, and motifs in diagrams or section
transitions only when those assets improve comprehension.

## 4. Proof and explanation

Rank proof in this order:

1. a real working output;
2. a product screenshot or terminal result;
3. a minimal input/output example;
4. a verified architecture or workflow diagram;
5. an externally verifiable adoption signal;
6. descriptive prose.

Never manufacture proof for visual impact.

## 5. GitHub QA

Validate relative links, image paths, alt text, heading order, command names,
copyability, cover readability, light/dark contrast, and mobile behavior. Deliver
warnings and a diff even when the visual result looks finished.
