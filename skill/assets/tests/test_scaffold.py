"""Unit tests for scaffold.py utility functions."""
import sys
import re
import uuid as uuid_module
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from scaffold import (
    slug_from_name,
    repo_name_from_slug,
    id_from_domain_and_slug,
    tags_from_slug,
    capabilities_to_yaml_list,
    synopsis_to_yaml_block,
    substitute,
)


def test_slug_from_name_basic():
    assert slug_from_name("WCAG Contrast Audit") == "WCAG-CONTRAST-AUDIT"


def test_slug_from_name_mixed_case():
    assert slug_from_name("My Cool Skill") == "MY-COOL-SKILL"


def test_slug_strips_specials():
    assert slug_from_name("My Cool Skill!") == "MY-COOL-SKILL"


def test_slug_collapses_spaces():
    assert slug_from_name("Too  Many   Spaces") == "TOO-MANY-SPACES"


def test_repo_name():
    assert repo_name_from_slug("CREATE-AISKILL") == "AISKILL-CREATE-AISKILL"


def test_repo_name_wcag():
    assert repo_name_from_slug("WCAG-CONTRAST-AUDIT") == "AISKILL-WCAG-CONTRAST-AUDIT"


def test_id_from_domain_and_slug():
    result = id_from_domain_and_slug("com.openaiskillpackage", "CREATE-AISKILL")
    assert result == "com.openaiskillpackage.create-aiskill"


def test_id_lowercase():
    result = id_from_domain_and_slug("com.example", "MY-SKILL-NAME")
    assert result == "com.example.my-skill-name"


def test_tags_from_slug():
    assert tags_from_slug("WCAG-CONTRAST-AUDIT") == ["wcag", "contrast", "audit"]


def test_capabilities_yaml_list():
    result = capabilities_to_yaml_list("filesystem.read,filesystem.write,process.exec")
    assert "  - filesystem.read" in result
    assert "  - filesystem.write" in result
    assert "  - process.exec" in result


def test_template_substitution():
    tmpl = "name: <<<NAME>>>\nid: <<<ID>>>"
    result = substitute(tmpl, {"NAME": "My Skill", "ID": "com.example.my-skill"})
    assert result == "name: My Skill\nid: com.example.my-skill"


def test_template_substitution_unknown_token_left_intact():
    tmpl = "value: <<<KNOWN>>>, other: <<<UNKNOWN>>>"
    result = substitute(tmpl, {"KNOWN": "hello"})
    assert "<<<UNKNOWN>>>" in result


def test_uuid_is_v4():
    generated = str(uuid_module.uuid4())
    parsed = uuid_module.UUID(generated, version=4)
    assert parsed.version == 4
    assert re.match(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
        generated
    )


def test_manifest_template_has_required_fields():
    tmpl_path = Path(__file__).parent.parent / "templates" / "manifest.yaml.template"
    content = tmpl_path.read_text(encoding="utf-8")
    required = ["<<<NAME>>>", "<<<ID>>>", "<<<UUID>>>", "<<<VERSION>>>",
                "<<<DESCRIPTION>>>", "<<<SYNOPSIS_BLOCK>>>", "<<<AUTHOR>>>",
                "<<<AUTHOR_EMAIL>>>", "<<<LICENSE>>>", "<<<MINIMUM_RUNTIME>>>",
                "<<<CAPABILITIES_LIST>>>", "<<<TYPE>>>"]
    for token in required:
        assert token in content, f"Missing token {token} in manifest.yaml.template"


# ── synopsis handling (.aiskill spec v2.3.0) ─────────────────────────────────

def test_synopsis_to_yaml_block_indents_every_line():
    result = synopsis_to_yaml_block("Paragraph one.\n\nParagraph two.")
    lines = result.split("\n")
    assert lines[0] == "  Paragraph one."
    assert lines[1] == ""
    assert lines[2] == "  Paragraph two."


def test_synopsis_to_yaml_block_strips_outer_blank_lines():
    result = synopsis_to_yaml_block("\n\nSome text.\n\n")
    assert result == "  Some text."


def test_readme_template_has_synopsis_token():
    tmpl_path = Path(__file__).parent.parent / "templates" / "README.repo.md.template"
    content = tmpl_path.read_text(encoding="utf-8")
    assert "<<<SYNOPSIS>>>" in content


def test_readme_skill_templates_are_retired():
    templates_dir = Path(__file__).parent.parent / "templates"
    assert not (templates_dir / "README.skill.md.template").exists()
    assert not (templates_dir / "README.skill.md.converted.template").exists()
