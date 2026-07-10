# Changelog — Create AI Skill Package

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [2.2.0] — 2026-07-10

### Added
- `SYSTEM.md` promoted to a fourth REQUIRED package file (`.aiskill` spec
  v2.2.0) — an invariant, versioned verification protocol, identical across
  every compliant package, that an AI agent must follow before executing
  `SKILL.md`. **BREAKING:** packages built before this version lack it and
  no longer conform
- New required manifest field `system_protocol_version`, declaring which
  `SYSTEM.md` version the package ships — must match `SYSTEM.md`'s own
  Protocol Version header
- `scaffold.py` copies `SYSTEM.md` verbatim from `assets/templates/SYSTEM.md`
  into every new package (this repo's own `skill/SYSTEM.md` is a synced copy
  of that same source, since this meta-skill is itself a `.aiskill` package)
- `pack.py` refuses to package if `skill/SYSTEM.md` doesn't byte-match the
  canonical template exactly

## [2.1.0] — 2026-07-10

### Added
- `SKILL.md` new Step 1 — "Choose a license": a mandatory gated conversation
  before scaffolding. Asks the person what license they want; if unsure and
  they want help, offers common open-source options (MIT always listed
  first, with links, explicitly non-exhaustive, choosing is their own
  responsibility); if still undecided, falls back to `license: UNLICENSED`
  rather than silently defaulting to a permissive license. Remaining steps
  renumbered 2–8 (previously 1–7)
- Bundled `skill/LICENSE.txt` (MIT) — conforms to the v2.1.0 `.aiskill` spec's
  optional bundled license file
- `UNLICENSED` documented as a recognized `license` manifest value, alongside
  SPDX identifiers and `Proprietary`

### Changed
- `scaffold.py --license` default changed from `MIT` to `UNLICENSED` — the
  tool itself no longer silently assumes a permissive license if invoked
  without the Step 1 conversation happening first

## [2.0.0] — 2026-07-07

### Added
- `build_card.py` — deterministically generates `CARD.md` from `manifest.yaml`; same manifest always produces the same `CARD.md`, never hand-edited
- `SKILL.md` Step 4 — "Generate CARD.md", run before testing and packaging
- `scaffold.py` now seeds a placeholder `CARD.md` (overwritten by `build_card.py` before packaging)

### Changed
- **BREAKING:** `CARD.md` is now a third REQUIRED package file, alongside `manifest.yaml` and `SKILL.md` — packages built before this version lack it and no longer conform to the spec
- `pack.py`'s documented usage no longer includes `--dashboard-dir` — each repo's own `dist/` folder is the only source of truth for a finished `.aiskill`; the legacy dashboard drop-zone copy is retired

## [1.0.0] — 2026-07-03

### Added
- Initial release — the meta-skill for creating `.aiskill` packages
- `scaffold.py` — creates a complete `AISKILL-{SLUG}` repo structure, substitutes all template tokens, runs `git init` and sets the GitHub remote
- `pack.py` — computes SHA-256 checksums, writes `checksums.yaml`, packages the `.aiskill` archive, and optionally copies to website and dashboard directories
- Seven template files: `manifest.yaml`, `SKILL.md`, `README.repo.md`, `README.skill.md`, `CHANGELOG.md`, `.gitignore`, `schema.json`
- Unit tests for all scaffold utility functions (`test_scaffold.py`)
- JSON Schema definition for `scaffold.py` inputs (`inputs/schema.json`)
