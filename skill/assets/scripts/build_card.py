#!/usr/bin/env python3
"""
build_card.py — CREATE-AISKILL v2.0.0
Deterministically generates CARD.md from manifest.yaml.
Same inputs always produce the same output — CARD.md is never hand-edited.
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ── Human-readable capability/permission rendering ───────────────────────────

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


# ── CARD.md rendering ─────────────────────────────────────────────────────────
# Sourced from manifest.yaml alone — README.md is not consulted. In practice a package's
# README.md opening paragraph is usually a near-restatement of manifest.description (both are
# typically written from the same source), so pulling both produced visible, pointless
# duplication in testing. manifest.yaml is the single normative source for CARD.md.

CARD_TEMPLATE = """# {name}

{description}

**Version:** {version}
**Author:** {author}
**License:** {license}
**Package ID:** `{id}`
**Package UUID:** `{uuid}`
**Homepage:** {homepage}

---

## Capabilities

{capabilities}

## Permissions

{permissions}

---

*Generated deterministically by `build_card.py` from `manifest.yaml` — do not hand-edit.
Re-run `build_card.py` after any `manifest.yaml` change, before packaging.*
"""


def build_card(manifest: dict) -> str:
    description = str(manifest.get("description", "")).strip()
    return CARD_TEMPLATE.format(
        name=manifest.get("name", ""),
        description=description,
        version=manifest.get("version", ""),
        author=manifest.get("author", ""),
        license=manifest.get("license", ""),
        id=manifest.get("id", ""),
        uuid=manifest.get("uuid", ""),
        homepage=manifest.get("homepage", ""),
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

    card_content = build_card(manifest)

    card_path = skill_dir / "CARD.md"
    card_path.write_text(card_content, encoding="utf-8")
    print(f"  wrote  {card_path}  ({len(card_content)} bytes)")


if __name__ == "__main__":
    main()
