# Fact-check contract

## Verify from current source

- Project and package names.
- Package manager, install commands, script names, ports, and runtime versions.
- Environment variables and whether they are required or optional.
- Public routes, API methods, CLI flags, configuration keys, and return shapes.
- Supported platforms, providers, databases, frameworks, and deployment targets.
- License, maturity, release status, and production-readiness wording.
- Screenshots, outputs, benchmarks, customer names, usage counts, and comparisons.

## Evidence priority

1. Current executable source and manifests.
2. Current tests and generated public contracts.
3. Current configuration templates and maintained docs.
4. User-supplied evidence.
5. Historical documents, comments, and plans.

Lower-priority evidence cannot silently override higher-priority contradictions.

## Never infer

- A feature is shipped because code or a TODO exists.
- A test pass proves a paid provider or production funnel works.
- A configured provider is currently accessible.
- An internal benchmark is representative or independently verified.
- A logo, testimonial, or customer relationship exists without approval.

Record unresolved contradictions in the report. Remove unsupported claims from
the proposed README or label them accurately as planned, experimental, mock, or
unverified.
