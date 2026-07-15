# Changelog — Create AI Skill Package

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [2.5.2] — 2026-07-15

### Fixed
- **Breaking.** `build_card.py`'s `CARD_TEMPLATE` reordered to match v2.5.1's hand-authored
  reference exactly: properties block (UUID/Package ID/Version/Type/Author/Author
  Email/License/Homepage/Tags) directly under the H1, before description/synopsis. New
  `detect_kind()`/`uuid_label()` — checks for `assets/`/`inputs/` under `--skill-dir` (same
  rule `main.js`'s `validatePackageFile()` uses) and picks **AI Skill UUID** or **MD Skill
  UUID** accordingly, so the same script correctly serves both `.aiskill` and `.mdskill`
  packages (confirmed: regenerating this package's own `CARD.md` now produces `kind=package`
  / AI Skill UUID; regenerating `MDSKILL-ALERT-PROTOCOL`'s produces `kind=md` / MD Skill UUID,
  byte-identical to its hand-authored v1.1.2).
- `render_tags()` added; `type`/`authorEmail`/`tags` now read from `manifest.yaml`.
- `scaffold.py`/`convert.py`: new `TAGS_LIST` token (plain comma-joined tag list, for README
  prose) alongside the existing YAML-list-formatted `TAGS` token.
- `README.repo.md.template` / `README.repo.md.converted.template`: same structural change —
  properties block under the H1 (new tokens: `UUID`, `ID`, `TYPE`, `AUTHOR_EMAIL`,
  `TAGS_LIST`, all of which already existed in both scripts' token dicts except `TAGS_LIST`),
  H1 now `<<<NAME>>>` on both tracks (was `AISKILL-<<<SLUG>>>` / `<<<REPO_NAME>>>`), old
  Name/Description line and properties table removed.
- Fixed a real bug this caught: this package's own `CARD.md`, hand-authored in v2.5.1, still
  read `**Version:** 2.5.0` after `manifest.yaml` had already been bumped to `2.5.1` in that
  same release — caught by regenerating via the fixed tool and diffing against the hand-
  authored file (the only diff was this line).
- `SKILL.md`'s Step 6 wording, Template Token Reference, and Pre-Release Checklist still
  describe the pre-v2.5.1 structure — not yet updated, follow-up needed.

---

## [2.5.1] — 2026-07-15

### Changed
- `CARD.md` and `README.md` restructured: the manifest-derived properties block (previously
  `**Version:**`/`**Author:**`/`**License:**`/`**Package ID:**`/`**Package UUID:**`/
  `**Homepage:**`, positioned after the description/synopsis, right before
  Capabilities/Permissions) moved to directly under the H1, before the description
  paragraph — a reader wants identity/provenance (who made this, what version, under what
  license) before the prose, not after it.
- Properties block gains three fields it previously lacked: `Type`, `Author Email`, `Tags`.
  `Package UUID` renamed to `AI Skill UUID` for this package's kind — kept format-specific
  (an `.mdskill` package's own generator will use `MD Skill UUID` instead) rather than a
  single generic label, so a reader can tell which kind of package they're looking at without
  checking the file extension.
- `Name` deliberately not duplicated into the block — the H1 immediately above it already
  shows it. `repository` deliberately excluded — a registry-side repo change could otherwise
  mislead a reader relying on it. `description` stays a separate paragraph, not folded into
  the block.
- `README.md`'s H1 now renders the real skill name (e.g. `# Create AI Skill Package`) instead
  of the repo slug.
- This release hand-applies the new structure to this package's own `CARD.md`/`README.md`
  only, as the reference implementation. `build_card.py` and both README templates
  (`README.repo.md.template`, `README.repo.md.converted.template`) still generate the old
  v2.5.0 structure and will be updated in a follow-up release so every future package gets
  the new layout by default — see the Pre-Release Checklist and Template Token Reference in
  `SKILL.md`, not yet updated to match.

---

## [2.5.0] — 2026-07-15

### Changed
- **Breaking** (`.aiskill` spec v2.4.0): `README.repo.md.template` and
  `README.repo.md.converted.template` restructured to open with three standardized headings,
  in order — `## Synopsis` (the `synopsis` field, verbatim), `## How It Works (Behavior)`,
  and `## What's in this .aiskill package?` — before the existing Prerequisites/Quick
  Start/Development Workflow/Version History/License/Contact sections, which are unchanged in
  content, just relocated after. Written for a reader browsing a skill library, not a
  repository.
- `build_card.py`: added a `GENERATING_SKILL` constant and referenced it explicitly in
  `CARD.md`'s footer — previously every `CARD.md` this script wrote said "re-run
  build_card.py" with no indication of which skill's script that was, meaningless for anyone
  reading any package other than this one.
- `SKILL.md` Pre-Release Checklist (Track A) updated to check for the three standardized
  README headings by name, replacing the old generic "describes purpose, prerequisites, quick
  start" check.

## [2.4.2] — 2026-07-11

### Fixed
- `manifest.yaml`'s `name`/`description` substitution is now YAML-safely quoted --
  a source skill title containing a colon (e.g. "TransformerLens: Mechanistic
  Interpretability for Transformers") previously broke `manifest.yaml` parsing
  entirely, since the bare unquoted substitution let YAML read `X: Y` as a
  nested mapping key/value rather than plain text. Fixed in both `convert.py`
  and `scaffold.py` with a new `yaml_quote()` helper in each, applied only to
  the `manifest.yaml` substitution -- `README.md`/`CHANGELOG.md` keep the same
  tokens unquoted, since a colon in markdown prose is harmless there.

## [2.4.1] — 2026-07-11

### Fixed
- `copy_skill_assets` no longer silently drops top-level source directories or
  loose files that fall outside the fixed `scripts`/`references`/`examples`/
  `templates`/`assets` `DIR_MAP` — caught converting `claude-api` (per-language
  subdirectories), `slack-gif-creator` (a bare `core/` module plus
  `requirements.txt`), and `theme-factory` (`themes/` plus a loose showcase
  PDF): all 3 were shipping with zero bundled files despite their `SKILL.md`
  explicitly referencing that content, because `copy_skill_assets` only ever
  looked at 5 fixed names. Unrecognized directories now copy through to
  `assets/templates/<original-name>/`, unrecognized loose files copy straight
  into `assets/templates/`, and `rewrite_path_references` was updated to take
  `(src_name, dest_rel)` pairs instead of relying on `DIR_MAP` lookups, since
  catch-all entries aren't in `DIR_MAP` at all.

## [2.4.0] — 2026-07-10

### Added
- **BREAKING** (`.aiskill` spec v2.3.0): new required manifest field `synopsis`
  — a multi-paragraph, hand-authored expansion of `description`, feeding both
  `README.md`'s opening and `CARD.md`'s rendering (`build_card.py` updated
  accordingly)

### Changed
- Retired `README.skill.md.template` and `README.skill.md.converted.template`
  — there is now exactly one README template per track
  (`README.repo.md.template` / `.converted.template`), rendered once and
  written identically to both the repo root and `skill/README.md`
- `scaffold.py` and `convert.py` both now require `--synopsis` (`convert.py`:
  required only in single-skill `--source-path` mode; batch/cherry-pick runs
  get a TODO placeholder per skill, to be hand-authored afterward, same as
  capabilities/permissions)
- `pack.py` gained a new pre-flight check, `verify_readme_matches_root` —
  refuses to package if the repo-root `README.md` and `skill/README.md`
  aren't byte-identical, matching the `.aiskill` spec v2.3.0 requirement
  enforced independently by the Cup and Ring Registry at registration
- `SKILL.md`: Track A gained a new Step 2 (Write a synopsis), renumbering
  Steps 2–8 to 3–9; Track B's Steps 2 and 5 updated to cover synopsis
  generation and hand-authoring; Manifest Field Reference, Template Token
  Reference, and both Pre-Release Checklists updated to match
- This package's own README rewritten to include a synopsis and made
  byte-identical between the repo root and `skill/`, dogfooding the new rule

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
