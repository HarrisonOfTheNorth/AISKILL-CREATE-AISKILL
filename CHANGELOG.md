# Changelog — AISKILL-CREATE-AISKILL

All notable changes to this repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [2.4.0] — 2026-07-10

### Added
- **BREAKING** (`.aiskill` spec v2.3.0): required manifest field `synopsis`,
  feeding both `README.md` and `CARD.md`

### Changed
- One README template per track — rendered once, written identically to
  repo root and `skill/README.md`; `pack.py` now refuses to package if they
  diverge
- `scaffold.py`/`convert.py` require `--synopsis` (batch/cherry-pick: TODO
  placeholder per skill, hand-authored afterward)
- `SKILL.md` renumbered (Track A gains a new Step 2); reference tables and
  checklists updated to match

## [2.3.1] — 2026-07-10

### Fixed
- `convert.py` Python 3.8/3.9 compatibility bug (unguarded `str | None`
  annotations)
- README's `gh` CLI prerequisite claim, incomplete as previously worded

### Changed
- Comprehensive README revision covering the conversion capability across
  every section, not just Quick Start

## [2.3.0] — 2026-07-10

### Added
- Track B: `convert.py` turns an existing skill from a foreign Agent Skills
  repo into one or more `.aiskill` packages, with a per-skill three-tier
  license gate (permissive / needs-attestation / needs-fresh-attestation-
  every-time) and automatic `assets/`-prefixed path-reference rewriting
- New converted-package repo-naming pattern (`AISKILL-{origin}-{SLUG}`,
  origin always lowercased) computed correctly by the tool itself
- `test_convert.py` (15 tests) with real license-text fixtures

### Fixed
- Stale `v2.0.0` docstring headers in `scaffold.py`/`build_card.py`
- `inputs/schema.json`'s stale `MIT` license default (now `UNLICENSED`)

## [2.2.0] — 2026-07-10

### Added
- `SYSTEM.md` — invariant, fourth REQUIRED package file, an external verification protocol every AI agent follows before executing `SKILL.md`
- New required manifest field `system_protocol_version`
- `scaffold.py` copies `SYSTEM.md` verbatim into every new package; `pack.py` refuses to package if it's been hand-edited

### Changed
- **BREAKING:** packages built before this version lack `SYSTEM.md` and no longer conform

## [2.1.0] — 2026-07-10

### Added
- `SKILL.md` Step 1 — mandatory license-selection gate before scaffolding (falls back to `license: UNLICENSED`, never silently defaults to a permissive license)
- Bundled `skill/LICENSE.txt`

### Changed
- `scaffold.py --license` default changed from `MIT` to `UNLICENSED`

## [2.0.0] — 2026-07-07

### Added
- `build_card.py` — deterministic `CARD.md` generator, sourced from `manifest.yaml` alone
- New `SKILL.md` Step 4 ("Generate CARD.md"), remaining steps renumbered

### Changed
- **BREAKING:** `CARD.md` promoted to a third REQUIRED package file (`manifest.yaml`, `SKILL.md`, `CARD.md`)
- Retired the `--dashboard-dir` legacy drop-zone copy from `pack.py`'s documented usage

## [1.0.0] — 2026-07-03

### Added
- Initial release — the meta-skill for creating `.aiskill` packages
- `scaffold.py` — scaffolds a complete `AISKILL-{SLUG}` repository from CLI arguments
- `pack.py` — computes SHA-256 checksums and packages the `.aiskill` archive
- Seven template files covering all required skill artifacts
- `test_scaffold.py` — 13 unit tests for all scaffold utility functions
- `inputs/schema.json` — JSON Schema Draft-07 definition for `scaffold.py` inputs
- Naming conventions baked in as constants: `AISKILL-` repo prefix, UPPER-KEBAB-CASE slugs
