# Create AI Skill Package

Scaffolds a new `.aiskill` package with a complete repository structure, git init, GitHub remote, all required template files, and the `pack.py` packaging script.

**Version:** 1.0.0
**License:** MIT
**Author:** Anthony Harrison
**Homepage:** https://openaiskillpackage.com/

---

## Prerequisites

- Python 3.8+
- git
- gh CLI (optional — required only for `gh release create` in Step 6)

---

## Quick Start

```bash
python3 assets/scripts/scaffold.py \
  --aiskills-root /Volumes/ai-skill-packages/aiskills \
  --name "My Skill Name" \
  --description "One-line purpose statement." \
  --author "Your Name" \
  --author-email "you@example.com" \
  --type procedural \
  --id-domain com.yourdomain \
  --github-org YourGitHubOrg
```

This creates `/Volumes/ai-skill-packages/aiskills/AISKILL-MY-SKILL-NAME/` with the full
directory tree, substitutes all template tokens, and runs `git init` + `git remote add`.

---

## Inputs

See `inputs/schema.json` for the full JSON Schema definition.

| Argument | Required | Description |
|---|---|---|
| `--aiskills-root` | yes | Absolute path to the folder containing all AISKILL repos |
| `--name` | yes | Human-readable skill name (slug auto-derived) |
| `--description` | yes | One-line purpose statement |
| `--author` | yes | Author name or organisation |
| `--author-email` | yes | Contact email |
| `--type` | yes | `procedural`, `analytical`, or `generative` |
| `--id-domain` | yes | Reverse-domain prefix for the manifest `id` |
| `--github-org` | yes | GitHub org/user (used to build remote URL) |
| `--license` | no | SPDX identifier, `Proprietary`, or `UNLICENSED` (default: `UNLICENSED`) — see `SKILL.md` Step 1 for the required conversation before setting this |
| `--capabilities` | no | Comma-separated capability tokens |
| `--slug` | no | Override the auto-derived UPPER-KEBAB-CASE slug |

---

## Output

Running `scaffold.py` produces:

```
{aiskills_root}/AISKILL-{SLUG}/
├── README.md
├── CHANGELOG.md
├── .gitignore
├── skill/
│   ├── manifest.yaml          ← identity and metadata
│   ├── SKILL.md               ← AI entry point (fill this in)
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── checksums.yaml         ← placeholder; overwritten by pack.py
│   ├── assets/
│   │   ├── scripts/           ← place your Python scripts here
│   │   ├── templates/         ← reusable templates for your skill
│   │   └── tests/             ← place test_*.py files here
│   └── inputs/
│       └── schema.json
└── dist/                      ← pack.py writes the .aiskill archive here
```

After scaffold, edit `skill/SKILL.md` then run `pack.py` to produce the `.aiskill` archive.

---

## Source Repository

https://github.com/PenrithBeacon/AISKILL-CREATE-AISKILL
