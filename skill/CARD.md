# Create AI Skill Package

Scaffolds a new, originally-authored .aiskill package (Track A), or converts an existing skill from a foreign Agent Skills repo into one or more .aiskill packages with per-skill license gating (Track B).

**Version:** 2.3.0
**Author:** Anthony Harrison
**License:** MIT
**Package ID:** `com.openaiskillpackage.create-aiskill`
**Package UUID:** `a1805527-85e9-4002-9ab3-770084e9b45c`
**Homepage:** https://openaiskillpackage.com/

---

## Capabilities

- `filesystem.read`
- `filesystem.write`
- `process.exec`
- `network.fetch`

## Permissions

- **`filesystem.write`** — paths: `<aiskills_root>/AISKILL-*`
- **`network.fetch`** — hosts: `github.com`

---

*Generated deterministically by `build_card.py` from `manifest.yaml` — do not hand-edit.
Re-run `build_card.py` after any `manifest.yaml` change, before packaging.*
