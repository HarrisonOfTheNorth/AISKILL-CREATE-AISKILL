# Changelog — AISKILL-CREATE-AISKILL

All notable changes to this repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-07-03

### Added
- Initial release — the meta-skill for creating `.aiskill` packages
- `scaffold.py` — scaffolds a complete `AISKILL-{SLUG}` repository from CLI arguments
- `pack.py` — computes SHA-256 checksums and packages the `.aiskill` archive
- Seven template files covering all required skill artifacts
- `test_scaffold.py` — 13 unit tests for all scaffold utility functions
- `inputs/schema.json` — JSON Schema Draft-07 definition for `scaffold.py` inputs
- Naming conventions baked in as constants: `AISKILL-` repo prefix, UPPER-KEBAB-CASE slugs
