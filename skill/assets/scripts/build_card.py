#!/usr/bin/env python3
"""
build_card.py — CREATE-AISKILL v2.5.2
Deterministically generates CARD.md from manifest.yaml.
Same inputs always produce the same output — CARD.md is never hand-edited.
"""

import argparse
import sys
from pathlib import Path

# Named explicitly so every CARD.md this script produces can say, in its own footer, which
# skill's build_card.py generated it -- a CARD.md travels inside the *target* package (e.g.
# MDSKILL-ALERT-PROTOCOL's), not the skill that made it, so without this the footer's "do
# not hand-edit, re-run build_card.py" instruction pointed at nothing findable for anyone
# reading any package other than this one.
GENERATING_SKILL = "AISKILL-CREATE-AISKILL"

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ── Human-readable capability/permission/tags rendering ───────────────────────

def render_capabilities(capabilities: list) -> str:
    if not capabilities:
        return "_None declared._"
    return "\n".join(f"- `{c}`" for c in capabilities)


def render_permissions(permissions: dict) -> str:
    if not permissions:
        return "_None declared._"
    lines = []
    for key in sorted(permissions.keys()):
        scope = permissions[key]
        if isinstance(scope, dict):
            for scope_key in sorted(scope.keys()):
                values = scope[scope_key]
                if isinstance(values, list):
                    joined = ", ".join(f"`{v}`" for v in values)
                    lines.append(f"- **`{key}`** — {scope_key}: {joined}")
                else:
                    lines.append(f"- **`{key}`** — {scope_key}: `{values}`")
        else:
            lines.append(f"- **`{key}`** — `{scope}`")
    return "\n".join(lines)


def render_tags(tags: list) -> str:
    return ", ".join(str(t) for t in tags) if tags else ""


# ── Kind detection ─────────────────────────────────────────────────────────────
# A package is .mdskill (markdown-only, no bundled code/tests/schemas) unless it has an
# assets/ or inputs/ directory, in which case it's .aiskill -- same rule main.js's
# validatePackageFile() uses on the Task Master side (hasNonMdAssets check), kept in sync
# deliberately so a package's kind is never something an author declares by hand, only ever
# something derived from its actual file set. Determines which UUID label CARD.md/README.md
# use: .mdskill packages are markdown-only by nature, .aiskill packages bundle real assets
# (scripts, tests, templates) -- the label should tell a reader which kind they're looking at
# without needing to check the file extension.

def detect_kind(skill_dir: Path) -> str:
    if (skill_dir / "assets").is_dir() or (skill_dir / "inputs").is_dir():
        return "package"
    return "md"


def uuid_label(kind: str) -> str:
    return "AI Skill UUID" if kind == "package" else "MD Skill UUID"


# ── CARD.md rendering ─────────────────────────────────────────────────────────
# Sourced from manifest.yaml alone — README.md is not consulted. In practice a package's
# README.md opening paragraph is usually a near-restatement of manifest.description (both are
# typically written from the same source), so pulling both produced visible, pointless
# duplication in testing. manifest.yaml is the single normative source for CARD.md.
#
# Properties block sits directly under the H1, before description/synopsis -- a reader wants
# identity/provenance (UUID, version, type, author, license) before the prose, not buried
# after it and right before Capabilities/Permissions (the pre-v2.5.1 position). Field order:
# UUID and Package ID together (both identifiers), then Version/Type, then Author/Author
# Email/License (who made it, under what terms), then Homepage/Tags (discovery metadata)
# last. `name` is deliberately not repeated here -- the H1 immediately above already shows
# it. `repository` is deliberately excluded -- a registry-side repo change could otherwise
# mislead a reader relying on it here.

CARD_TEMPLATE = """# {name}

**{uuid_label}:** `{uuid}`
**Package ID:** `{id}`
**Version:** {version}
**Type:** {type}
**Author:** {author}
**Author Email:** {author_email}
**License:** {license}
**Homepage:** {homepage}
**Tags:** {tags}

{description}

{synopsis}

---

## Capabilities

{capabilities}

## Permissions

{permissions}

---

*Generated deterministically by `build_card.py`, part of the **{generating_skill}** skill,
from this package's own `manifest.yaml` — do not hand-edit. Re-run `build_card.py` after any
`manifest.yaml` change, before packaging.*
"""


def build_card(manifest: dict, kind: str) -> str:
    description = str(manifest.get("description", "")).strip()
    synopsis = str(manifest.get("synopsis", "")).strip()
    return CARD_TEMPLATE.format(
        name=manifest.get("name", ""),
        description=description,
        synopsis=synopsis,
        version=manifest.get("version", ""),
        type=manifest.get("type", ""),
        author=manifest.get("author", ""),
        author_email=manifest.get("authorEmail", ""),
        license=manifest.get("license", ""),
        id=manifest.get("id", ""),
        uuid=manifest.get("uuid", ""),
        uuid_label=uuid_label(kind),
        homepage=manifest.get("homepage", ""),
        tags=render_tags(manifest.get("tags", [])),
        generating_skill=GENERATING_SKILL,
        capabilities=render_capabilities(manifest.get("capabilities", [])),
        permissions=render_permissions(manifest.get("permissions", {})),
    )


# ── Main ─────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="Deterministically generate CARD.md from manifest.yaml."
    )
    p.add_argument("--skill-dir", required=True,
                   help="Path to the skill/ directory (contains manifest.yaml)")
    return p.parse_args()


def main():
    args = parse_args()
    skill_dir = Path(args.skill_dir).expanduser().resolve()

    if not skill_dir.is_dir():
        print(f"Error: --skill-dir does not exist: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    manifest_path = skill_dir / "manifest.yaml"
    if not manifest_path.exists():
        print(f"Error: manifest.yaml not found in {skill_dir}", file=sys.stderr)
        sys.exit(1)

    with open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    kind = detect_kind(skill_dir)
    card_content = build_card(manifest, kind)

    card_path = skill_dir / "CARD.md"
    card_path.write_text(card_content, encoding="utf-8")
    print(f"  wrote  {card_path}  ({len(card_content)} bytes, kind={kind})")


if __name__ == "__main__":
    main()
