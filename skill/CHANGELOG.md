# Changelog — Create AI Skill Package

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-07-03

### Added
- Initial release — the meta-skill for creating `.aiskill` packages
- `scaffold.py` — creates a complete `AISKILL-{SLUG}` repo structure, substitutes all template tokens, runs `git init` and sets the GitHub remote
- `pack.py` — computes SHA-256 checksums, writes `checksums.yaml`, packages the `.aiskill` archive, and optionally copies to website and dashboard directories
- Seven template files: `manifest.yaml`, `SKILL.md`, `README.repo.md`, `README.skill.md`, `CHANGELOG.md`, `.gitignore`, `schema.json`
- Unit tests for all scaffold utility functions (`test_scaffold.py`)
- JSON Schema definition for `scaffold.py` inputs (`inputs/schema.json`)
