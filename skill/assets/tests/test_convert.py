"""Unit tests for convert.py — license-tier classification, converted-package
naming (v2.2.1 lowercase-origin rule), and the assets/-prefix path-reference
rewrite. License text fixtures below are real fragments captured from the
actual source repos during the first conversion batch (Phase B) — not
synthetic examples — including the real anthropics/skills docx/pdf/xlsx
proprietary notice that originally motivated the tier-3 gate.
"""
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from convert import (
    slug_from_path,
    origin_segment,
    repo_name_from_origin_and_slug,
    id_from_dest_and_slug,
    classify_license_tier,
    copy_skill_assets,
    rewrite_path_references,
    synopsis_to_yaml_block,
    yaml_quote,
    SYNOPSIS_PLACEHOLDER,
)


# ── Real license text fixtures ────────────────────────────────────────────

MIT_TEXT = """MIT License

Copyright (c) 2025 Corey Haines

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software..."""

APACHE_TEXT = """
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
"""

# Real text from anthropics/skills/skills/docx/LICENSE.txt — the exact case
# that motivated the tier-3 gate in the first place.
PROPRIETARY_TEXT = """© 2025 Anthropic, PBC. All rights reserved.

LICENSE: Use of these materials (including all code, prompts, assets, files,
and other components of this Skill) is governed by your agreement with
Anthropic regarding use of Anthropic's services. If no separate agreement
exists, use is governed by Anthropic's Consumer Terms of Service or
Commercial Terms of Service, as applicable:
https://www.anthropic.com/legal/consumer-terms
https://www.anthropic.com/legal/commercial-terms
"""

AMBIGUOUS_TEXT = "This project is licensed for internal use only. Contact us for details."


# ── License-tier classification ──────────────────────────────────────────

def test_mit_is_tier_1():
    tier, label = classify_license_tier(MIT_TEXT)
    assert tier == 1
    assert label == "MIT"


def test_apache_is_tier_1():
    tier, label = classify_license_tier(APACHE_TEXT)
    assert tier == 1
    assert label == "Apache-2.0"


def test_real_anthropic_proprietary_notice_is_tier_3():
    tier, label = classify_license_tier(PROPRIETARY_TEXT)
    assert tier == 3
    assert "proprietary" in label.lower() or "all-rights-reserved" in label.lower()


def test_absent_license_is_tier_2():
    tier, label = classify_license_tier(None)
    assert tier == 2
    assert "no license file found" in label


def test_ambiguous_text_is_tier_2():
    tier, label = classify_license_tier(AMBIGUOUS_TEXT)
    assert tier == 2


# ── Naming: v2.2.1 lowercase-origin rule ─────────────────────────────────

def test_origin_segment_is_always_lowercase():
    # Orchestra-Research/AI-Research-SKILLs is mixed-case on GitHub -- the
    # exact case that shipped wrong in v1.0.0 of the nanogpt package and had
    # to be fixed in v1.0.1.
    assert origin_segment("Orchestra-Research", "AI-Research-SKILLs") == "orchestra-research_ai-research-skills"


def test_origin_segment_already_lowercase_unaffected():
    assert origin_segment("anthropics", "skills") == "anthropics_skills"
    assert origin_segment("coreyhaines31", "marketingskills") == "coreyhaines31_marketingskills"


def test_slug_from_path_flat():
    assert slug_from_path("skills/seo-audit") == "SEO-AUDIT"


def test_slug_from_path_nested_uses_basename_only():
    # nanogpt's real source path is nested two levels deep -- the slug must be
    # just the skill's own directory name, not the full path (this was the
    # second bug in the same v1.0.0 mistake: the repo name included
    # "MODEL-ARCHITECTURE-" from the parent directory, which pack.py's own
    # slug_from_id convention never would have produced).
    assert slug_from_path("01-model-architecture/nanogpt") == "NANOGPT"


def test_repo_name_matches_actual_shipped_packages():
    # Real, currently-live repo names -- regression cases, not hypotheticals.
    assert repo_name_from_origin_and_slug(
        origin_segment("coreyhaines31", "marketingskills"), "SEO-AUDIT"
    ) == "AISKILL-coreyhaines31_marketingskills-SEO-AUDIT"
    assert repo_name_from_origin_and_slug(
        origin_segment("anthropics", "skills"), "WEBAPP-TESTING"
    ) == "AISKILL-anthropics_skills-WEBAPP-TESTING"
    assert repo_name_from_origin_and_slug(
        origin_segment("Orchestra-Research", "AI-Research-SKILLs"), "NANOGPT"
    ) == "AISKILL-orchestra-research_ai-research-skills-NANOGPT"


def test_id_matches_actual_shipped_packages():
    assert id_from_dest_and_slug("Xamtastic", "marketingskills", "SEO-AUDIT") == "com.xamtastic.marketingskills.seo-audit"
    assert id_from_dest_and_slug("Xamtastic", "AI-Research-SKILLs", "NANOGPT") == "com.xamtastic.ai-research-skills.nanogpt"


# ── Path-reference rewriting (the bug caught by hand in 5 of 6 packages) ──

def test_rewrites_bare_references_path():
    body = "See [International SEO](references/international-seo.md) for details."
    result = rewrite_path_references(body, [("references", "assets/references")])
    assert "assets/references/international-seo.md" in result
    assert "](references/" not in result


def test_rewrites_bare_scripts_path():
    # Real sentence from webapp-testing's actual source SKILL.md.
    body = '- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)'
    result = rewrite_path_references(body, [("scripts", "assets/scripts")])
    assert "assets/scripts/with_server.py" in result


def test_rewrites_examples_to_references_mapping():
    # examples/ maps to assets/references/, not assets/examples/ -- examples/
    # doesn't survive as its own destination directory name.
    body = "- **examples/** - Examples showing common patterns:"
    result = rewrite_path_references(body, [("examples", "assets/references")])
    assert "assets/references/" in result


def test_rewrites_catch_all_directory_mapping():
    # Not one of DIR_MAP's fixed 5 names -- copy_skill_assets's catch-all sends
    # unrecognized directories to assets/templates/<original-name>/ (the bug
    # that dropped claude-api/slack-gif-creator/theme-factory's real content
    # entirely before this fix).
    body = "Load the builder from `core/gif_builder.py`."
    result = rewrite_path_references(body, [("core", "assets/templates/core")])
    assert "assets/templates/core/gif_builder.py" in result


def test_does_not_touch_unrelated_text():
    body = "This skill has no bundled scripts or references at all."
    result = rewrite_path_references(body, [])
    assert result == body


# ── copy_skill_assets catch-all (the claude-api/slack-gif-creator/theme-factory
# bug: non-standard top-level dirs/files silently dropped entirely) ──────────

def test_copy_skill_assets_preserves_known_dirs(tmp_path):
    src = tmp_path / "source-skill"
    (src / "scripts").mkdir(parents=True)
    (src / "scripts" / "run.py").write_text("print('hi')")
    dest = tmp_path / "dest-skill"

    mapped = copy_skill_assets(src, dest)

    assert ("scripts", "assets/scripts") in mapped
    assert (dest / "assets" / "scripts" / "run.py").read_text() == "print('hi')"


def test_copy_skill_assets_catch_all_preserves_unrecognized_directory(tmp_path):
    # Reproduces slack-gif-creator's actual source layout: a bare core/ module
    # with no scripts/references/templates wrapper -- before this fix,
    # copy_skill_assets silently produced zero files for this package.
    src = tmp_path / "source-skill"
    (src / "core").mkdir(parents=True)
    (src / "core" / "gif_builder.py").write_text("class GIFBuilder: pass")
    dest = tmp_path / "dest-skill"

    mapped = copy_skill_assets(src, dest)

    assert ("core", "assets/templates/core") in mapped
    assert (dest / "assets" / "templates" / "core" / "gif_builder.py").read_text() == "class GIFBuilder: pass"


def test_copy_skill_assets_catch_all_preserves_loose_file(tmp_path):
    # Reproduces theme-factory's actual source layout: a loose showcase PDF
    # sitting next to SKILL.md with no containing directory at all.
    src = tmp_path / "source-skill"
    src.mkdir(parents=True)
    (src / "theme-showcase.pdf").write_bytes(b"%PDF-fake")
    dest = tmp_path / "dest-skill"

    mapped = copy_skill_assets(src, dest)

    assert ("theme-showcase.pdf", "assets/templates/theme-showcase.pdf") in mapped
    assert (dest / "assets" / "templates" / "theme-showcase.pdf").read_bytes() == b"%PDF-fake"


def test_copy_skill_assets_skips_known_non_asset_files(tmp_path):
    src = tmp_path / "source-skill"
    src.mkdir(parents=True)
    (src / "SKILL.md").write_text("# Skill")
    (src / "LICENSE.txt").write_text("MIT")
    dest = tmp_path / "dest-skill"

    mapped = copy_skill_assets(src, dest)

    assert mapped == []
    assert not (dest / "assets").exists()


def test_copy_skill_assets_skips_evals(tmp_path):
    src = tmp_path / "source-skill"
    (src / "evals").mkdir(parents=True)
    (src / "evals" / "evals.json").write_text("[]")
    dest = tmp_path / "dest-skill"

    mapped = copy_skill_assets(src, dest)

    assert mapped == []
    assert not (dest / "assets").exists()


# ── synopsis handling (.aiskill spec v2.3.0) ─────────────────────────────────

def test_synopsis_to_yaml_block_indents():
    result = synopsis_to_yaml_block("First.\n\nSecond.")
    assert result.split("\n") == ["  First.", "", "  Second."]


def test_synopsis_placeholder_is_nonempty_and_flags_todo():
    # Batch/cherry-pick conversions with no --synopsis get this placeholder --
    # must be obviously a TODO, never mistaken for a real synopsis.
    assert "TODO" in SYNOPSIS_PLACEHOLDER
    assert len(SYNOPSIS_PLACEHOLDER) > 0


def test_readme_converted_template_has_synopsis_token():
    tmpl_path = Path(__file__).parent.parent / "templates" / "README.repo.md.converted.template"
    content = tmpl_path.read_text(encoding="utf-8")
    assert "<<<SYNOPSIS>>>" in content


# ── yaml_quote (the transformer-lens bug: an unquoted "name:" substitution whose
# own value contains a colon breaks manifest.yaml's YAML parsing entirely) ──────

def test_yaml_quote_real_transformer_lens_title():
    # The actual title that broke manifest.yaml parsing in production.
    name = "TransformerLens: Mechanistic Interpretability for Transformers"
    quoted = yaml_quote(name)
    parsed = yaml.safe_load(f"name: {quoted}")
    assert parsed == {"name": name}


def test_yaml_quote_plain_string_still_parses_correctly():
    quoted = yaml_quote("Simple Skill Name")
    parsed = yaml.safe_load(f"name: {quoted}")
    assert parsed == {"name": "Simple Skill Name"}


def test_yaml_quote_handles_embedded_double_quotes():
    quoted = yaml_quote('Has a "quoted" word')
    parsed = yaml.safe_load(f"name: {quoted}")
    assert parsed == {"name": 'Has a "quoted" word'}


def test_yaml_quote_handles_hash_character():
    # A bare "#" mid-scalar can also be read as a comment start in some contexts --
    # confirm the quoted form round-trips regardless.
    quoted = yaml_quote("Skill for #trending topics")
    parsed = yaml.safe_load(f"name: {quoted}")
    assert parsed == {"name": "Skill for #trending topics"}


def test_yaml_quote_does_not_wrap_output_across_lines():
    # PyYAML's default line-wrapping (~80 chars) would corrupt a single-line
    # substitution if not disabled -- confirm a long description stays one line.
    long_description = "A " + ("very " * 30) + "long description with a colon: right here."
    quoted = yaml_quote(long_description)
    assert "\n" not in quoted
    parsed = yaml.safe_load(f"description: {quoted}")
    assert parsed == {"description": long_description}
