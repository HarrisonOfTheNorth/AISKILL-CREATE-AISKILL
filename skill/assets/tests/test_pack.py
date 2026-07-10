"""Unit tests for pack.py's verify_readme_matches_root check (.aiskill spec
v2.3.0) -- pack.py only zips skill/, so skill/README.md is the only README
copy that ever travels with a distributed .aiskill file. The repo-root and
skill/ copies must be byte-identical, or packaging must refuse to proceed.
"""
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from pack import verify_readme_matches_root


def _make_repo(tmp_path: Path, root_content: str, skill_content: str) -> Path:
    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    (tmp_path / "README.md").write_text(root_content, encoding="utf-8")
    (skill_dir / "README.md").write_text(skill_content, encoding="utf-8")
    return skill_dir


def test_matching_readmes_pass(tmp_path):
    skill_dir = _make_repo(tmp_path, "Same content.\n", "Same content.\n")
    verify_readme_matches_root(skill_dir)  # should not raise / exit


def test_mismatched_readmes_exit(tmp_path):
    skill_dir = _make_repo(tmp_path, "Root version.\n", "Skill version.\n")
    with pytest.raises(SystemExit):
        verify_readme_matches_root(skill_dir)


def test_single_typo_difference_is_still_a_mismatch(tmp_path):
    # Even a one-character divergence must fail -- byte-identical, not "close enough".
    skill_dir = _make_repo(tmp_path, "Hello world.\n", "Hello wrold.\n")
    with pytest.raises(SystemExit):
        verify_readme_matches_root(skill_dir)


def test_missing_skill_readme_exits(tmp_path):
    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    (tmp_path / "README.md").write_text("Root only.\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        verify_readme_matches_root(skill_dir)


def test_missing_root_readme_exits(tmp_path):
    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    (skill_dir / "README.md").write_text("Skill only.\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        verify_readme_matches_root(skill_dir)
