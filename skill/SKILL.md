# Create AI Skill Package

**Skill:** `CREATE-AISKILL-2.3.0.aiskill`
**UUID:** `a1805527-85e9-4002-9ab3-770084e9b45c`
**Type:** Procedural
**Homepage:** https://openaiskillpackage.com/

This is the meta-skill — the `.aiskill` package for creating `.aiskill` packages. It has
two tracks: authoring a brand-new, originally-authored skill from scratch (Track A), or
converting an existing skill from a foreign "Agent Skills" format repo (agentskills.io)
into one or more `.aiskill` packages (Track B). Step 0 below determines which track
applies before anything else happens.

---

## Prerequisites

- Python 3.8 or later
- `git` installed and on PATH
- `gh` CLI (optional — only needed for creating GitHub releases)
- The target GitHub repository must already exist before pushing (create it in GitHub UI
  or with `gh repo create AISKILL-{SLUG} --private`) — this applies once a package is
  ready to publish, at the very end of either track, never before
- Track B additionally needs read access to the source repo being converted (public
  repos need nothing extra — `convert.py` shells out to a plain `git clone --depth 1`)

---

## Step 0 — Original or converted?

Before anything else, determine which track applies. Ask, or read it from
already-supplied session context if it's already clear — never re-ask for
something already established in the conversation.

- **Track A — Author a new, original skill.** The person wants to create a skill
  that doesn't exist anywhere else yet. Go to **Track A** below.
- **Track B — Convert an existing skill.** The person wants to bring a skill that
  already exists in another format (typically Agent Skills — SKILL.md with YAML
  frontmatter, e.g. from `anthropics/skills`, `coreyhaines31/marketingskills`, or
  any similar repo) into the `.aiskill` format. Go to **Track B** below.

Everything from here is organized under whichever track applies. The two tracks
share `build_card.py` and `pack.py` at their tails, but their manifest fields,
license handling, and generation scripts (`scaffold.py` vs. `convert.py`)
are otherwise distinct — do not mix steps between them.

---

# Track A: Author a New Original Skill

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
| `--type` | yes | — | `procedural` \| `analytical` \| `generative` \| `instructional` |
| `--id-domain` | yes | — | Reverse-domain prefix, e.g. `com.openaiskillpackage` |
| `--github-org` | yes | — | GitHub organisation or user, e.g. `YourGitHubOrg` |
| `--license` | no | `UNLICENSED` | SPDX identifier, `Proprietary`, or `UNLICENSED` — decided via the conversation in Step 1, not guessed |
| `--capabilities` | no | `filesystem.read,filesystem.write,process.exec` | Comma-separated capability tokens |
| `--slug` | no | auto | UPPER-KEBAB-CASE slug (auto-derived from `--name` if omitted) |

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
   package in existence (see the `.aiskill` spec). It is never
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

# Track B: Convert an Existing Skill from Another Format

## Inputs

All inputs are passed as command-line arguments to `assets/scripts/convert.py`.

| Argument | Required | Default | Description |
|---|---|---|---|
| `--aiskills-root` | yes | — | Same as Track A |
| `--source-repo` | yes | — | `owner/repo` of the foreign Agent Skills repo, e.g. `anthropics/skills` |
| `--source-path` | no | — | Single skill's path within the repo. Mutually exclusive with `--skills` |
| `--skills` | no | — | Comma-separated cherry-picked skill paths. Mutually exclusive with `--source-path` |
| (neither given) | — | — | **Batch mode** — every directory in the repo containing a `SKILL.md` is discovered and converted |
| `--dest-account` | yes | — | Destination account the package is published under, e.g. `Xamtastic` |
| `--author-email` | yes | — | Contact email recorded in the manifest |
| `--github-org` | no | `--dest-account` | GitHub org/user for the destination repo URL, if different from `--dest-account` |
| `--scratch-dir` | no | `/tmp/aiskill-convert-scratch` | Where the source repo is cloned |
| `--attestation-for` | no | — | Re-invocation only: finalizes one previously-deferred skill (see Step 4) |
| `--attestation-by` | no | — | Required with `--attestation-for` |
| `--attestation-reasoning` | no | — | Required with `--attestation-for` |

## Execution

### Step 1 — Gather the target specification

Determine the target before running anything — ask, or read it from
already-supplied session context if it's already clear:

- **A single skill**: you have `--source-repo` and `--source-path`.
- **A cherry-picked set**: you have `--source-repo` and a list of paths for `--skills`.
- **A full batch**: you have `--source-repo` alone. Every skill in the repo will be
  discovered and attempted. Only do this when the person has actually asked for
  the whole repo, not as a default when a narrower request would do.

### Step 2 — Run convert.py

```bash
python3 assets/scripts/convert.py \
  --aiskills-root /Volumes/ai-skill-packages/aiskills \
  --source-repo anthropics/skills \
  --source-path skills/webapp-testing \
  --dest-account Xamtastic \
  --author-email you@example.com
```

(Omit `--source-path` and pass `--skills path1,path2` for a cherry-picked set, or
omit both for a full batch.)

For every discovered skill, convert.py will:
1. Resolve the effective license: check the skill's own directory for a
   `LICENSE.txt`/`LICENSE` first, fall back to the repo root, and treat
   "genuinely absent" as its own outcome — **never per-repo**, since a single
   repo can and does mix licenses (`anthropics/skills` has 14 Apache-2.0
   skills and 3 explicitly proprietary/ToS-bound ones in the same repo).
2. Classify a **provisional** tier from that license text (see the table
   below) and print the actual evidence alongside the classification — review
   it, don't just trust it. Even a tier-1 classification can be wrong on an
   unusual license file.
3. Map source directories to `.aiskill` conventions (`scripts/`→`assets/scripts/`,
   `references/`→`assets/references/`, `examples/`→`assets/references/`,
   `templates/`/`assets/`→`assets/templates/`; `evals/` is excluded from the
   package entirely, same as every prior conversion).
4. Rewrite any bare path reference inside the fetched `SKILL.md` (e.g.
   `references/foo.md`, `scripts/bar.py`) to its `assets/`-prefixed
   equivalent automatically — this is the exact class of bug caught by hand
   in 5 of 6 packages during the first real conversion batch; it should never
   need a manual fix again.
5. Compute the repo name as `AISKILL-{source_owner}_{source_repo}-{SLUG}`,
   with the origin segment always lowercased regardless of the source's
   actual GitHub casing (the `.aiskill` spec's converted-package naming rule).
6. Generate `manifest.yaml` with `origin: converted` and the full provenance
   field group (`source_owner`, `source_repo`, `source_path`, `converted_at`),
   the required description suffix, and `capabilities`/`permissions` left as
   an explicit placeholder — **never auto-inferred**, always authored by hand
   in Step 5 below.
7. Copy `SYSTEM.md` canonical verbatim, same as Track A.
8. Generate `README.md` with the `## Origin` section, and — tier 2/3 only —
   a `## License Attestation` section marked `PENDING`.

**Tier-1 (clean) skills are committed locally immediately, one after another,
with no interruption.** Tier-2/3 skills are generated but left uncommitted and
collected into a **deferred list**, printed at the end of the run alongside
the exact command to resolve each one. Clean conversions are never held up
waiting on a license decision for an unrelated skill in the same batch.

| Tier | Meaning | What happens |
|---|---|---|
| 1 | Permissive (MIT, Apache-2.0, BSD, GPL, or another recognizable open license) | No gate. Convert and commit immediately. |
| 2 | Absent or ambiguous — no license file found, or unrecognized text | Disclose what was (and wasn't) found, get an attestation from the user, log it, proceed. A standing attestation given once may cover this tier for the rest of the session. |
| 3 | Explicit proprietary / "all rights reserved" / ToS-bound notice | Same disclosure-and-log flow, but **requires a fresh attestation every single time** — never covered by a standing authorization from earlier in the session. |

### Step 3 — Review the tier-1 (clean) conversions

These are already generated and locally committed. Spot-check at least one
against its source (content-fidelity: every instruction in the source
`SKILL.md` should be present in the converted version, `assets/`-prefixed
path references should resolve correctly) before moving on.

### Step 4 — Work the deferred (tier 2/3) list with the user

For each skill convert.py deferred, in order:
1. Show the user what was found: the skill, the license text (or its
   absence), and the tier.
2. Ask them to decide. For tier 2, a standing "yes, that covers this tier for
   the rest of this session" is acceptable. For tier 3, a fresh, specific
   attestation is required — ask them what their authorization actually is
   and why (e.g. "I work for the source's org and I'm cleared to do this" or
   "this is a personal/internal conversion, not for public redistribution").
   This is a logged, identity-backed public statement (attributed to the
   real name/email/GitHub account already on the package), not a request for
   unverifiable "evidence" — no ID, no email forward, nothing the AI could
   check anyway.
3. If they decline or don't respond, leave that skill as-is (uncommitted,
   `PENDING`) — do not silently proceed and do not silently discard it either.
4. If they authorize it, resolve it:
   ```bash
   python3 assets/scripts/convert.py \
     --aiskills-root /Volumes/ai-skill-packages/aiskills \
     --source-repo anthropics/skills \
     --attestation-for skills/docx \
     --attestation-by "Their Name <their@email>" \
     --attestation-reasoning "Exactly what they told you, verbatim or closely paraphrased"
   ```
   This fills in the `PENDING` placeholders in `manifest.yaml` and `README.md`
   and commits the skill locally.

End with one summary: converted / attested-and-converted / still blocked.

### Step 5 — Author capabilities and permissions by hand

No source format (Agent Skills or otherwise) declares an equivalent to
`.aiskill`'s capability tokens. Every generated `manifest.yaml` leaves
`capabilities`/`permissions` as an explicit placeholder — read what the
skill's `SKILL.md` actually does and author these yourself, the same as for
an originally-authored package. Never infer this automatically.

### Step 6 — Generate CARD.md, run tests, and pack — per completed skill

Identical to Track A's Steps 5–7, run once per finalized skill (tier-1
immediately, tier-2/3 once attested):

```bash
python3 skill/assets/scripts/build_card.py --skill-dir skill/
python3 -m pytest skill/assets/tests/ -v   # if any assets/scripts/ exist
python3 skill/assets/scripts/pack.py --skill-dir skill/ --dist-dir dist/
```

### Step 7 — Stop. Review with the user before creating any GitHub repo or pushing.

`convert.py` never creates a GitHub repo and never pushes — every converted
skill ends at a local commit. Present what was converted (and what's still
deferred) and get an explicit go-ahead before `gh repo create`, `git push`,
or `gh release create` touch anything.

---

## Naming Conventions

| Artifact | Convention | Example |
|---|---|---|
| Skill slug | UPPER-KEBAB-CASE | `WCAG-CONTRAST-AUDIT` |
| Local repo folder (Track A) | `AISKILL-{SLUG}` | `AISKILL-WCAG-CONTRAST-AUDIT` |
| Local repo folder (Track B) | `AISKILL-{origin}-{SLUG}`, origin always lowercase | `AISKILL-anthropics_skills-WEBAPP-TESTING` |
| GitHub repo name | Same as the local repo folder | (as above) |
| `.aiskill` filename | `{SLUG}-{VERSION}.aiskill` | `WCAG-CONTRAST-AUDIT-1.0.0.aiskill` |
| Manifest `id` (Track A) | `{reverse-domain}.{lowercase-slug}` | `com.openaiskillpackage.wcag-contrast-audit` |
| Manifest `id` (Track B) | `com.{dest-account}.{source-repo}.{lowercase-slug}` | `com.xamtastic.skills.webapp-testing` |
| Manifest `uuid` | UUID4, generated once at scaffold/conversion time | (auto-generated) |

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
| `description` | yes | string | One-line purpose statement. Track B: gets the `... Upgraded from a skill originally authored by @{owner} on GitHub.` suffix. |
| `author` | yes | string | Author name or organisation (Track A) / destination account (Track B) |
| `entry` | yes | string | Relative path to SKILL.md, always `SKILL.md` |
| `system_protocol_version` | yes | string | Which `SYSTEM.md` protocol version this package ships — must match `SYSTEM.md`'s own Protocol Version header exactly |
| `license` | yes | string | SPDX identifier (`MIT`, `Apache-2.0`), `Proprietary`, or `UNLICENSED`. Track A: decided via Step 1. Track B: carried forward verbatim from the source — never re-litigated. |
| `minimum_runtime` | yes | semver string | Minimum AI Skill runtime version, quoted, e.g. `"1.0.0"` |
| `capabilities` | yes | list | Capability tokens: `filesystem.read`, `filesystem.write`, `process.exec`, `network.fetch`. Always hand-authored, never auto-inferred, in both tracks. |
| `permissions` | optional | object | Capability-specific path or scope constraints |
| `homepage` | optional | string | Canonical URL for the skill |
| `repository` | optional | string | GitHub repo URL |
| `authorEmail` | optional | string | Contact email |
| `tags` | optional | list | Discovery tags for registries |
| `type` | optional | string | `procedural` \| `analytical` \| `generative` \| `instructional` |
| `changelog` | optional | list | Version history entries, newest first |
| `origin` | Track B only | string | `converted` — set when the package is derived from another format |
| `source_owner` | Track B only | string | GitHub account/org owning the original repo |
| `source_repo` | Track B only | string | Name of the original repository |
| `source_path` | Track B only | string | Path to the skill within the original repository |
| `converted_at` | Track B only | date | ISO 8601 date the conversion was performed |
| `license_attestation` | Track B, tier 2/3 only | object | `by`, `reasoning`, `date` — a logged, identity-backed record of the human decision to proceed despite an absent/ambiguous/proprietary license finding |

---

## Template Token Reference

All template files in `assets/templates/` use `<<<PLACEHOLDER>>>` substitution syntax.

### manifest.yaml.template (Track A)
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

### manifest.yaml.converted.template (Track B)
All of the above (naming adjusted per the Track B naming table), plus:
| Token | Value source |
|---|---|
| `<<<SOURCE_OWNER>>>` | Parsed from `--source-repo` |
| `<<<SOURCE_REPO>>>` | Parsed from `--source-repo` |
| `<<<SOURCE_PATH>>>` | `--source-path` / one entry of `--skills` / batch-discovered |
| `<<<CONVERTED_AT>>>` | Today's date |
| `<<<AISKILL_SPEC_VERSION>>>` | The `.aiskill` spec version this conversion targets |
| `<<<LICENSE_ATTESTATION_BLOCK>>>` | Empty for tier 1; a `license_attestation:` YAML block (possibly `PENDING`) for tier 2/3 |

### SKILL.md.template
| Token | Value source |
|---|---|
| `<<<SKILL_NAME>>>` | `--name` |
| `<<<SLUG>>>` | Derived slug |
| `<<<SKILL_VERSION>>>` | `1.0.0` |
| `<<<SKILL_DESCRIPTION>>>` | `--description` |

Track B does not use `SKILL.md.template` at all — the converted `SKILL.md`
body comes directly from the source skill (path-rewritten), not a skeleton.

### README.repo.md.template / README.skill.md.template (Track A)
| Token | Value source |
|---|---|
| `<<<SLUG>>>` | Derived slug |
| `<<<NAME>>>` | `--name` |
| `<<<DESCRIPTION>>>` | `--description` |
| `<<<AUTHOR>>>` | `--author` |
| `<<<GITHUB_ORG>>>` | `--github-org` |
| `<<<LICENSE>>>` | `--license` |
| `<<<VERSION>>>` | `1.0.0` |

### README.repo.md.converted.template / README.skill.md.converted.template (Track B)
All of the above, plus `<<<SOURCE_OWNER>>>`, `<<<SOURCE_REPO>>>`,
`<<<SOURCE_PATH>>>`, `<<<CONVERTED_AT>>>`, `<<<AISKILL_SPEC_VERSION>>>`, and
`<<<LICENSE_ATTESTATION_SECTION>>>` (empty for tier 1; a full `## License
Attestation` section, possibly marked `PENDING`, for tier 2/3).

### CHANGELOG.md.template (Track A) / CHANGELOG.md.converted.template (Track B)
| Token | Value source |
|---|---|
| `<<<DATE>>>` | Today's date (YYYY-MM-DD) |
| `<<<VERSION>>>` | `1.0.0` |
| `<<<NAME>>>` | `--name` |
| `<<<SOURCE_OWNER>>>` / `<<<SOURCE_REPO>>>` / `<<<SOURCE_PATH>>>` (Track B only) | Same as manifest |

### schema.json.template
| Token | Value source |
|---|---|
| `<<<SKILL_NAME>>>` | `--name` |
| `<<<SKILL_DESCRIPTION>>>` | `--description` |

---

## Pre-Release Checklist

### Track A

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

### Track B

- [ ] Every skill's license was resolved per-skill, never assumed from the
      repo as a whole or from a sibling skill's license
- [ ] No tier-2/3 skill was committed with a `PENDING` attestation still in
      its `manifest.yaml`/`README.md`
- [ ] Every tier-3 attestation is fresh — not reused from a standing
      authorization given for a different skill or an earlier session
- [ ] `capabilities`/`permissions` were hand-authored by reading the actual
      `SKILL.md` content — never left as the generated placeholder
- [ ] Every path reference inside the converted `SKILL.md` uses the
      `assets/`-prefixed form — spot-check against the source's own bare
      references (`references/`, `scripts/`, `examples/`, `templates/`)
- [ ] `skill/SYSTEM.md` byte-matches the canonical source (same as Track A)
- [ ] `manifest.yaml`'s `origin`, `source_owner`, `source_repo`, `source_path`,
      `converted_at` are all present and correct
- [ ] The repo name matches `AISKILL-{origin}-{SLUG}` with the origin segment
      lowercased, regardless of the source's actual GitHub casing
- [ ] `build_card.py`/`pytest`/`pack.py` have been run per finalized skill,
      same as Track A
- [ ] Nothing has been pushed or had a GitHub repo created without an
      explicit go-ahead from the user, per Step 7
