# Create AI Skill Package

**Skill:** `CREATE-AISKILL-2.2.0.aiskill`
**UUID:** `a1805527-85e9-4002-9ab3-770084e9b45c`
**Type:** Procedural
**Homepage:** https://openaiskillpackage.com/

This is the meta-skill — the `.aiskill` package for creating `.aiskill` packages. Run it
once to scaffold a complete, spec-compliant repository for a new skill. The scaffolded
repo contains everything needed: directory structure, filled-in templates, git init,
GitHub remote, and the `pack.py` script to package future versions.

---

## Prerequisites

- Python 3.8 or later
- `git` installed and on PATH
- `gh` CLI (optional — only needed for creating GitHub releases)
- The target GitHub repository must already exist before pushing (create it in GitHub UI
  or with `gh repo create AISKILL-{SLUG} --private`)

---

## Inputs

All inputs are passed as command-line arguments to `assets/scripts/scaffold.py`.
The full JSON Schema is at `inputs/schema.json`.

| Argument | Required | Default | Description |
|---|---|---|---|
| `--aiskills-root` | yes | — | Absolute path to the folder that contains all AISKILL repos, e.g. `/Volumes/ai-skill-packages/aiskills` |
| `--name` | yes | — | Human-readable skill name, e.g. `"WCAG Contrast Audit"` |
| `--description` | yes | — | One-line purpose statement |
| `--author` | yes | — | Author name or organisation |
| `--author-email` | yes | — | Contact email address |
| `--type` | yes | — | `procedural` \| `analytical` \| `generative` |
| `--id-domain` | yes | — | Reverse-domain prefix, e.g. `com.openaiskillpackage` |
| `--github-org` | yes | — | GitHub organisation or user, e.g. `YourGitHubOrg` |
| `--license` | no | `UNLICENSED` | SPDX identifier, `Proprietary`, or `UNLICENSED` — decided via the conversation in Step 1, not guessed |
| `--capabilities` | no | `filesystem.read,filesystem.write,process.exec` | Comma-separated capability tokens |
| `--slug` | no | auto | UPPER-KEBAB-CASE slug (auto-derived from `--name` if omitted) |

---

## Execution

### Step 1 — Choose a license

Before scaffolding anything, ask the person creating the package what license
they want the new `.aiskill` package released under. This decision feeds the
`--license` argument in Step 2 — never guess it, and never silently default
to a permissive license the person didn't actually choose.

- **If they already know** (e.g. `MIT`, `Apache-2.0`, `GPL-3.0`, `Proprietary`),
  use that value directly.
- **If they don't know and want help deciding**, ask whether they'd like a
  short list of common possibilities. If yes:
  - Search the internet for the licenses commonly used in the open-source
    community.
  - Always list **MIT** first.
  - For every license offered, include a direct link to its full text (e.g.
    choosealicense.com or the SPDX license list) so the person can read it
    themselves before deciding.
  - Explicitly say this is **not an exhaustive list** — just the licenses
    commonly seen in open source — and that **choosing is the person's own
    responsibility**. Point them to doing their own research (or seeking
    legal advice) rather than recommending one on their behalf beyond
    listing MIT first.
- **If the person still doesn't choose one**, do not default to MIT and do
  not leave the field blank. Use `--license UNLICENSED`. This means:
  - `manifest.yaml`: `license: UNLICENSED`
  - `skill/LICENSE.txt`: a short statement that no license was selected by
    the author, so the package defaults to standard copyright protection —
    all rights reserved, no permissions granted beyond default statutory
    rights in whatever jurisdiction the package is used.
  - This is a deliberate, valid outcome, not a placeholder to fix later.
    Packages are not required to be open source — never silently substitute
    a real open-source license for a choice the person didn't make.

### Step 2 — Run scaffold.py

```bash
python3 assets/scripts/scaffold.py \
  --aiskills-root /Volumes/ai-skill-packages/aiskills \
  --name "My Skill Name" \
  --description "One-line purpose statement" \
  --author "Your Name" \
  --author-email "you@example.com" \
  --type procedural \
  --id-domain com.yourdomain \
  --github-org YourGitHubOrg \
  --license MIT \
  --capabilities "filesystem.read,filesystem.write,process.exec"
```

scaffold.py will:
1. Derive the slug: `MY-SKILL-NAME` (UPPER-KEBAB-CASE from `--name`)
2. Generate a UUID4 for the new skill
3. Create `/Volumes/ai-skill-packages/aiskills/AISKILL-MY-SKILL-NAME/` with full tree
4. Write all template files with tokens substituted
5. Copy `SYSTEM.md` into `skill/SYSTEM.md` **verbatim, with no substitution** —
   this file is spec-mandated to be byte-identical across every `.aiskill`
   package in existence (see the `.aiskill` spec v2.2.0). It is never
   authored or edited per-skill; `pack.py` (Step 7) refuses to package a
   copy that doesn't match exactly.
6. Set `manifest.yaml`'s `system_protocol_version` to match `SYSTEM.md`'s own
   Protocol Version header
7. Run `git init` and `git remote add origin https://github.com/{github-org}/AISKILL-MY-SKILL-NAME.git`
8. Create the initial git commit
9. Print a next-steps summary

The scaffolded tree will be:
```
AISKILL-MY-SKILL-NAME/
├── README.md              ← repo-level, elaborate
├── CHANGELOG.md           ← repo-level
├── .gitignore
├── skill/                 ← zip this → MY-SKILL-NAME-1.0.0.aiskill
│   ├── manifest.yaml      ← pre-filled, uuid generated, includes system_protocol_version
│   ├── SKILL.md           ← skeleton — YOU MUST FILL THIS IN (Step 3)
│   ├── SYSTEM.md          ← copied verbatim from the canonical source (Step 2) — never edit this
│   ├── README.md          ← skill-level
│   ├── CHANGELOG.md
│   ├── CARD.md            ← placeholder — regenerated by build_card.py (Step 5)
│   ├── checksums.yaml     ← written by pack.py (Step 7)
│   ├── assets/
│   │   ├── scripts/       ← YOUR SCRIPTS GO HERE (Step 4)
│   │   ├── templates/     ← YOUR TEMPLATES GO HERE (Step 4)
│   │   └── tests/         ← YOUR TESTS GO HERE (Step 4)
│   └── inputs/
│       └── schema.json    ← pre-filled skeleton
└── dist/                  ← pack.py writes MY-SKILL-NAME-1.0.0.aiskill here
```

### Step 3 — Author skill/SKILL.md

This is the most important step. `skill/SKILL.md` is the entry point the AI reads
when executing your new skill. The scaffolded file contains a skeleton — replace every
placeholder section with the real content for your skill:

- **Purpose** — what the skill does and when to use it
- **Prerequisites** — runtime dependencies (Python version, pip packages, system tools)
- **Inputs** — what arguments or files the skill expects, matching `inputs/schema.json`
- **Step-by-step execution** — exactly what commands to run, in what order, with what arguments
- **Expected output** — what the AI should see and how to interpret it
- **Error handling** — what to do if execution fails

The skill is only as deterministic as its SKILL.md is precise. Ambiguous instructions
produce ambiguous AI behaviour. Be exhaustive.

### Step 4 — Write the assets

Write your skill's actual computation into `skill/assets/scripts/`. Write unit tests
in `skill/assets/tests/`. Tests must cover:
- The happy path (known input → known output)
- Boundary conditions
- Any algorithm-specific edge cases

Asset scripts must be pure source files (Python, shell, JavaScript, etc.) — no compiled
binaries. The runtime provides the interpreter.

### Step 5 — Generate CARD.md

```bash
python3 skill/assets/scripts/build_card.py --skill-dir skill/
```

`CARD.md` is a **required** file (alongside `manifest.yaml` and `SKILL.md`) — it's what a
consuming runtime shows a human when they select the package, before deciding whether to use
it. It is generated deterministically from `skill/manifest.yaml` — the same manifest always
produces the same `CARD.md`. **Never hand-edit `CARD.md`.** If `manifest.yaml`'s `name`,
`description`, `version`, `capabilities`, or `permissions` change for any reason, re-run this
step before packaging — do not package a `CARD.md` that's stale relative to the manifest it
was generated from.

### Step 6 — Run tests

```bash
cd /Volumes/ai-skill-packages/aiskills/AISKILL-MY-SKILL-NAME
python3 -m pytest skill/assets/tests/ -v
```

**All tests must pass before packaging.** A failing test is a packaging blocker.
The test suite is what separates a verified, trustworthy package from an ephemeral prompt.

### Step 7 — Run pack.py

```bash
python3 skill/assets/scripts/pack.py \
  --skill-dir skill/ \
  --dist-dir dist/ \
  --website-skills-dir /Volumes/websites/sites/aiskill_website/src/ai-skills
```

pack.py will:
1. Verify `skill/SYSTEM.md` byte-matches the canonical source at
   `assets/templates/SYSTEM.md` — **refuses to package if it doesn't**, since
   unlike `CARD.md`, `SYSTEM.md` should never legitimately vary at all
2. Walk `skill/`, compute SHA-256 of every file except `checksums.yaml`
3. Write `skill/checksums.yaml`
4. ZIP the entire `skill/` directory into `dist/MY-SKILL-NAME-1.0.0.aiskill`
5. Optionally copy the `.aiskill` to the website directory
6. Print the git tag and `gh release create` commands to run next

The `dist/` folder inside this repo is the only source of truth for a finished `.aiskill` —
there is no longer a separate dashboard drop-zone copy step.

### Step 8 — Commit, tag, and release

```bash
cd /Volumes/ai-skill-packages/aiskills/AISKILL-MY-SKILL-NAME

# Push the final source
git add -A
git commit -m "feat: complete MY-SKILL-NAME v1.0.0"
git push origin main

# Tag and release
git tag v1.0.0
git push origin v1.0.0
gh release create v1.0.0 dist/MY-SKILL-NAME-1.0.0.aiskill \
  --title "v1.0.0 — Initial release" \
  --notes "Initial release of MY-SKILL-NAME."
```

---

## Naming Conventions

| Artifact | Convention | Example |
|---|---|---|
| Skill slug | UPPER-KEBAB-CASE | `WCAG-CONTRAST-AUDIT` |
| Local repo folder | `AISKILL-{SLUG}` | `AISKILL-WCAG-CONTRAST-AUDIT` |
| GitHub repo name | `AISKILL-{SLUG}` | `AISKILL-WCAG-CONTRAST-AUDIT` |
| `.aiskill` filename | `{SLUG}-{VERSION}.aiskill` | `WCAG-CONTRAST-AUDIT-1.0.0.aiskill` |
| Manifest `id` | `{reverse-domain}.{lowercase-slug}` | `com.openaiskillpackage.wcag-contrast-audit` |
| Manifest `uuid` | UUID4, generated once at scaffold time | (auto-generated by scaffold.py) |

---

## Manifest Field Reference

All fields below are defined by the Open AI Skill Package specification at
https://openaiskillpackage.com/

| Field | Required | Type | Description |
|---|---|---|---|
| `name` | yes | string | Human-readable skill name |
| `id` | yes | string | Reverse-domain ownership identifier. Encodes authorship; verifiable via DNS TXT for registry submission. |
| `uuid` | yes | string | UUID4 — globally unique, collision-safe across registries and file systems. Generated once; never changes across versions. |
| `version` | yes | semver | Package version (Semantic Versioning 2.0). Always a quoted string, e.g. `"1.0.0"`. |
| `description` | yes | string | One-line purpose statement |
| `author` | yes | string | Author name or organisation |
| `entry` | yes | string | Relative path to SKILL.md, always `SKILL.md` |
| `system_protocol_version` | yes | string | Which `SYSTEM.md` protocol version this package ships — must match `SYSTEM.md`'s own Protocol Version header exactly |
| `license` | yes | string | SPDX identifier (`MIT`, `Apache-2.0`), `Proprietary`, or `UNLICENSED` (no license selected — see Step 1) |
| `minimum_runtime` | yes | semver string | Minimum AI Skill runtime version, quoted, e.g. `"1.0.0"` |
| `capabilities` | yes | list | Capability tokens: `filesystem.read`, `filesystem.write`, `process.exec`, `network.fetch` |
| `permissions` | optional | object | Capability-specific path or scope constraints |
| `homepage` | optional | string | Canonical URL for the skill |
| `repository` | optional | string | GitHub repo URL |
| `authorEmail` | optional | string | Contact email |
| `tags` | optional | list | Discovery tags for registries |
| `type` | optional | string | `procedural` \| `analytical` \| `generative` |
| `changelog` | optional | list | Version history entries, newest first |

---

## Template Token Reference

All template files in `assets/templates/` use `<<<PLACEHOLDER>>>` substitution syntax.

### manifest.yaml.template
| Token | Value source |
|---|---|
| `<<<NAME>>>` | `--name` |
| `<<<ID>>>` | `{--id-domain}.{lowercase-slug}` |
| `<<<UUID>>>` | Generated UUID4 |
| `<<<VERSION>>>` | Always `1.0.0` for new skills |
| `<<<DESCRIPTION>>>` | `--description` |
| `<<<AUTHOR>>>` | `--author` |
| `<<<AUTHOR_EMAIL>>>` | `--author-email` |
| `<<<LICENSE>>>` | `--license` |
| `<<<MINIMUM_RUNTIME>>>` | Always `"1.0.0"` |
| `<<<CAPABILITIES_LIST>>>` | YAML list from `--capabilities` |
| `<<<HOMEPAGE>>>` | Always `https://openaiskillpackage.com/` |
| `<<<REPOSITORY>>>` | `https://github.com/{--github-org}/AISKILL-{SLUG}` |
| `<<<TAGS>>>` | Derived from slug words |
| `<<<TYPE>>>` | `--type` |
| `<<<SLUG>>>` | Derived slug |

### SKILL.md.template
| Token | Value source |
|---|---|
| `<<<SKILL_NAME>>>` | `--name` |
| `<<<SLUG>>>` | Derived slug |
| `<<<SKILL_VERSION>>>` | `1.0.0` |
| `<<<SKILL_DESCRIPTION>>>` | `--description` |

### README.repo.md.template / README.skill.md.template
| Token | Value source |
|---|---|
| `<<<SLUG>>>` | Derived slug |
| `<<<NAME>>>` | `--name` |
| `<<<DESCRIPTION>>>` | `--description` |
| `<<<AUTHOR>>>` | `--author` |
| `<<<GITHUB_ORG>>>` | `--github-org` |
| `<<<LICENSE>>>` | `--license` |
| `<<<VERSION>>>` | `1.0.0` |

### CHANGELOG.md.template
| Token | Value source |
|---|---|
| `<<<DATE>>>` | Today's date (YYYY-MM-DD) |
| `<<<VERSION>>>` | `1.0.0` |
| `<<<NAME>>>` | `--name` |

### schema.json.template
| Token | Value source |
|---|---|
| `<<<SKILL_NAME>>>` | `--name` |
| `<<<SKILL_DESCRIPTION>>>` | `--description` |

---

## Pre-Release Checklist

Before running pack.py and pushing, verify:

- [ ] A license was actually decided via Step 1's conversation — not defaulted
      without asking. `skill/LICENSE.txt` exists and matches `manifest.yaml`'s
      `license` field, whether that's a real SPDX license, `Proprietary`, or
      the deliberate `UNLICENSED` outcome
- [ ] `skill/SYSTEM.md` byte-matches `assets/templates/SYSTEM.md` exactly —
      `pack.py` enforces this and will refuse to package otherwise, but check
      it wasn't hand-edited before that point
- [ ] `manifest.yaml`'s `system_protocol_version` matches `SYSTEM.md`'s own
      Protocol Version header
- [ ] `skill/SKILL.md` has all placeholder sections replaced with real content
- [ ] At least one script exists in `skill/assets/scripts/`
- [ ] At least one test exists in `skill/assets/tests/`
- [ ] All tests pass: `python3 -m pytest skill/assets/tests/ -v`
- [ ] `skill/manifest.yaml` has `uuid` field present and is a valid UUID4
- [ ] `skill/CARD.md` has been (re)generated by `build_card.py` and reflects the current
      `manifest.yaml` — never hand-edited, never stale
- [ ] `skill/README.md` describes the skill purpose, prerequisites, and quick start
- [ ] `skill/CHANGELOG.md` has an entry for v1.0.0
- [ ] `skill/inputs/schema.json` accurately describes the inputs (if any)
- [ ] Repo-level `README.md` is complete and suitable for public viewing on GitHub
- [ ] pack.py has been run and `skill/checksums.yaml` is present
- [ ] `dist/{SLUG}-1.0.0.aiskill` exists and is the file to attach to the GitHub release
