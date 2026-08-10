# Contributing

README Studio accepts fixes, new repository fixtures, new project-native cover
styles, and public before/after examples.

## Before opening a pull request

```bash
python -m unittest discover -s tests -v
python skills/beautify-readme/scripts/validate_skill.py
python skills/beautify-readme/scripts/check_readme.py .
```

## Adding a style

Add one entry to `skills/beautify-readme/assets/styles/presets.json` and include:

- a stable lowercase ID;
- the repository types it serves;
- one visual center and one composition rule;
- a restrained palette and exact typography behavior;
- proof slots when real screenshots or outputs are appropriate;
- negative constraints that prevent generic AI-cover failures.

Do not copy a company's logo, wordmark, or fixed brand layout. A visual lineage
may inspire a neutral project style, but the public preset must stand on its own.

## Adding a showcase

Only submit repositories you own or have permission to feature. Include the
original README, the proposed README, source assets, and a short fact ledger.
Attribution inside a user's README must remain optional.
