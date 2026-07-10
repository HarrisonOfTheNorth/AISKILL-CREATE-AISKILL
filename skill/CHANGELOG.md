# Changelog — Create AI Skill Package

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [2.3.1] — 2026-07-10

### Fixed
- `convert.py`'s `str | None` annotations were unguarded and would raise a
  `TypeError` on Python 3.8/3.9 — added `from __future__ import
  annotations`. Caught while fact-checking the README's own "Python 3.8+"
  claim
- README's claim that `gh` CLI is "only needed to publish a GitHub
  release" was incomplete — it's also used to create the repository
  itself, and both steps have a manual web-UI alternative

### Changed
- Rewrote the README's Prerequisites, Under the Bonnet, This Skill in
  Particular, On Public Distribution, and Specification sections to
  properly cover the conversion capability — previously only Quick Start
  and the Independence Day callout had been updated
- Dropped the Python version prerequisite entirely — the spec requires
  only "scripts", not Python specifically, and the AI agent handles
  runtime needs invisibly
- Named and linked the Cup and Ring Registry explicitly in Prerequisites,
  and explained why publishing requires a real GitHub account
  (accountability, not a technical format requirement)

## [2.3.0] — 2026-07-10

### Added
- **Track B: convert an existing skill from a foreign Agent Skills repo.**
  `SKILL.md` gains a Step 0 gateway (original vs. converted); new
  `convert.py` discovers a single skill, a cherry-picked list, or a full
  batch (every `SKILL.md` in the repo), resolves each skill's own license
  (never assumed from the repo as a whole), classifies a provisional tier,
  maps source directories to `.aiskill` conventions, rewrites bare path
  references to their `assets/`-prefixed form automatically, and generates
  the package
- Three-tier license gate, always per-skill: tier 1 (permissive) converts
  immediately; tier 2 (absent/ambiguous) and tier 3 (explicit
  proprietary/all-rights-reserved) require a human attestation, logged in
  both `manifest.yaml` (`license_attestation`) and `README.md` (`## License
  Attestation`) — tier 3 requires a fresh attestation every time, never a
  standing authorization
- Batch/cherry-pick runs convert every tier-1 skill immediately and defer
  every tier-2/3 skill to one list, resolved afterward via `convert.py
  --attestation-for`
- New manifest fields `origin`, `source_owner`, `source_repo`,
  `source_path`, `converted_at`, `license_attestation`; new
  `manifest.yaml.converted.template`, `README.*.converted.template`,
  `CHANGELOG.md.converted.template`
- New converted-package repo-naming pattern, `AISKILL-{origin}-{SLUG}` with
  the origin segment always lowercased (`.aiskill` spec v2.2.1) — computed
  correctly from the start instead of fixed after shipping
- `test_convert.py` (15 tests) using real license-text fixtures from the
  first conversion batch, including the actual `anthropics/skills`
  proprietary notice that motivated the tier-3 gate

### Fixed
- `scaffold.py`/`build_card.py` docstring headers were still stamped
  `v2.0.0`, never bumped alongside their actual v2.1.0/v2.2.0 behavior
  changes
- `inputs/schema.json`'s `license` field still defaulted to `MIT`,
  inconsistent with `scaffold.py`'s real `UNLICENSED` default since the
  v2.1.0 license-gate work

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
