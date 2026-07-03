#!/usr/bin/env python3
"""
pack.py — CREATE-AISKILL v1.0.0
Generates checksums.yaml and packages the skill/ directory into a .aiskill archive.
"""

import argparse
import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ── Slug derivation ──────────────────────────────────────────────────────────

def slug_from_id(skill_id: str) -> str:
    """'com.openaiskillpackage.create-aiskill' → 'CREATE-AISKILL'"""
    return skill_id.split(".")[-1].upper()


# ── Checksum generation ──────────────────────────────────────────────────────

EXCLUDE_NAMES = {".DS_Store", ".AppleDouble", ".LSOverride"}
EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", ".eggs"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}


def _should_include(p: Path) -> bool:
    if p.name in EXCLUDE_NAMES:
        return False
    if p.suffix in EXCLUDE_SUFFIXES:
        return False
    for part in p.parts:
        if part in EXCLUDE_DIRS:
            return False
    return True


def compute_checksums(skill_dir: Path) -> dict:
    files = {}
    for p in sorted(skill_dir.rglob("*")):
        if p.is_file() and p.name != "checksums.yaml" and _should_include(p):
            rel = str(p.relative_to(skill_dir))
            files[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return files


def write_checksums(skill_dir: Path, files: dict) -> None:
    content = yaml.dump(
        {"algorithm": "sha256", "files": files},
        default_flow_style=False,
        sort_keys=True
    )
    (skill_dir / "checksums.yaml").write_text(content, encoding="utf-8")


# ── Packaging ────────────────────────────────────────────────────────────────

def build_aiskill(skill_dir: Path, dist_dir: Path, slug: str, version: str) -> Path:
    dist_dir.mkdir(parents=True, exist_ok=True)
    archive_name = f"{slug}-{version}.aiskill"
    archive_path = dist_dir / archive_name

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(skill_dir.rglob("*")):
            if p.is_file() and _should_include(p):
                arcname = str(p.relative_to(skill_dir))
                zf.write(p, arcname)

    return archive_path


# ── Main ─────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="Generate checksums and package a skill/ directory into a .aiskill archive."
    )
    p.add_argument("--skill-dir", required=True,
                   help="Path to the skill/ directory (contains manifest.yaml)")
    p.add_argument("--dist-dir", required=True,
                   help="Path to the dist/ output directory (created if absent)")
    p.add_argument("--website-skills-dir",
                   help="Optional: copy .aiskill to this directory (website ai-skills/)")
    p.add_argument("--dashboard-dir",
                   help="Optional: copy .aiskill to this directory (dashboard packages)")
    return p.parse_args()


def main():
    args = parse_args()
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    dist_dir = Path(args.dist_dir).expanduser().resolve()

    if not skill_dir.is_dir():
        print(f"Error: --skill-dir does not exist: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    manifest_path = skill_dir / "manifest.yaml"
    if not manifest_path.exists():
        print(f"Error: manifest.yaml not found in {skill_dir}", file=sys.stderr)
        sys.exit(1)

    with open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    name = manifest.get("name", "")
    version = manifest.get("version", "1.0.0")
    skill_id = manifest.get("id", "")
    slug = slug_from_id(skill_id) if skill_id else name.upper().replace(" ", "-")

    print(f"\nPacking {slug}-{version}.aiskill")
    print(f"  skill dir: {skill_dir}")

    # ── Checksums ──
    print("  computing checksums...")
    files = compute_checksums(skill_dir)
    write_checksums(skill_dir, files)
    print(f"  checksummed {len(files)} files → skill/checksums.yaml")

    # ── Package ──
    archive_path = build_aiskill(skill_dir, dist_dir, slug, version)
    size_kb = archive_path.stat().st_size // 1024
    file_count = len(files) + 1  # +1 for checksums.yaml itself
    print(f"  packaged   {archive_path.name} ({size_kb}K, {file_count} files)")

    # ── Optional copies ──
    copies = []
    if args.website_skills_dir:
        dest = Path(args.website_skills_dir) / archive_path.name
        shutil.copy2(archive_path, dest)
        copies.append(str(dest))
        print(f"  copied  →  {dest}")
    if args.dashboard_dir:
        dest = Path(args.dashboard_dir) / archive_path.name
        shutil.copy2(archive_path, dest)
        copies.append(str(dest))
        print(f"  copied  →  {dest}")

    print(f"""
{'='*60}
Archive: {archive_path}

Next steps:
  git add -A
  git commit -m "feat: complete {slug} v{version}"
  git push origin main
  git tag v{version}
  git push origin v{version}
  gh release create v{version} {archive_path} \\
    --title "v{version} — Initial release" \\
    --notes "Initial release of {name}."
{'='*60}
""")


if __name__ == "__main__":
    main()
