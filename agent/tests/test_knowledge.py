from pathlib import Path
import pytest
from knowledge import load_knowledge_base


def test_load_reads_all_md_files(tmp_path):
    (tmp_path / "a.md").write_text("# Doc A\nContent A", encoding="utf-8")
    (tmp_path / "b.md").write_text("# Doc B\nContent B", encoding="utf-8")
    result = load_knowledge_base(tmp_path)
    assert "Content A" in result
    assert "Content B" in result


def test_load_missing_dir_raises(tmp_path):
    missing = tmp_path / "nonexistent"
    with pytest.raises(FileNotFoundError):
        load_knowledge_base(missing)


def test_load_empty_dir_returns_empty_string(tmp_path):
    result = load_knowledge_base(tmp_path)
    assert result == ""


def test_load_includes_filename_as_section_header(tmp_path):
    (tmp_path / "aims-overview.md").write_text("Some content", encoding="utf-8")
    result = load_knowledge_base(tmp_path)
    assert "aims-overview" in result


def test_load_ignores_non_md_files(tmp_path):
    (tmp_path / "readme.txt").write_text("Not markdown", encoding="utf-8")
    (tmp_path / "data.json").write_text("{}", encoding="utf-8")
    result = load_knowledge_base(tmp_path)
    assert result == ""
