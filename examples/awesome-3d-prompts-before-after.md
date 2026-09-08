# Awesome 3D Prompts: real README before and after

This comparison uses two immutable commits from the public
[`BeatAPI/awesome-3d-prompts`](https://github.com/BeatAPI/awesome-3d-prompts)
repository. It is a reference for README Refiner's quality bar, not a claim that
README Refiner authored the historical change.

## Fixed snapshots

- **Before:** [`a591c0ffee88fb5d529f4da0931465ce37980a25`](https://github.com/BeatAPI/awesome-3d-prompts/blob/a591c0ffee88fb5d529f4da0931465ce37980a25/README.md)
- **After:** [`ac37217b7b723fbe38095503e06e3b818fbb1a85`](https://github.com/BeatAPI/awesome-3d-prompts/blob/ac37217b7b723fbe38095503e06e3b818fbb1a85/README.md)
- **README diff:** [`a591c0f...ac37217`](https://github.com/BeatAPI/awesome-3d-prompts/compare/a591c0ffee88fb5d529f4da0931465ce37980a25...ac37217b7b723fbe38095503e06e3b818fbb1a85)

## Evidence ledger

| Signal | Before | After |
| --- | --- | --- |
| README length | 80 lines | 949 lines |
| Catalog size | 29 accepted cases | 306 source-backed cases |
| Opening visual | None | Repository-owned hero image |
| Result proof | Text tables link to detail pages | Featured entries show visible result media in the README |
| Navigation | Category headings | Six workflow links with counts |
| Trust cues | Source and rights explanation | Source attribution, prompt-fidelity labels, evidence notes, and rights links |
| Media summary | No media summary | 250 WebM videos and 56 WebP images |

Counts above are read from the two committed READMEs and their committed prompt
data. The comparison does not change or reinterpret the source prompts.

## What changed in the reading experience

The earlier README is accurate, but a visitor must read tables and open detail
pages before seeing why the collection is useful. The later README leads with a
clear promise, visible output, workflow-level navigation, and evidence labels.
The underlying source discipline remains intact; the presentation makes that
discipline easier to understand and trust.

This is the pattern README Refiner should reproduce on other repositories:

1. preserve repository truth;
2. move the strongest real proof forward;
3. establish a project-native visual system;
4. improve scanning without hiding detail;
5. keep every important claim traceable to source.

## Reproduce the comparison

From a clone of the 3D prompt repository:

```bash
git show a591c0ffee88fb5d529f4da0931465ce37980a25:README.md
git show ac37217b7b723fbe38095503e06e3b818fbb1a85:README.md
git diff a591c0ffee88fb5d529f4da0931465ce37980a25..ac37217b7b723fbe38095503e06e3b818fbb1a85 -- README.md
```
