from pathlib import Path
from unittest.mock import MagicMock
from kb_author import save_article, draft_article


def test_save_article_creates_file(tmp_path):
    path = save_article("# Title\nContent", "test-article", docs_dir=tmp_path)
    assert path.exists()
    assert path.read_text(encoding="utf-8") == "# Title\nContent"


def test_save_article_appends_md_extension(tmp_path):
    path = save_article("# Title", "my-article", docs_dir=tmp_path)
    assert path.name == "my-article.md"


def test_save_article_accepts_existing_md_extension(tmp_path):
    path = save_article("# Title", "my-article.md", docs_dir=tmp_path)
    assert path.name == "my-article.md"


def test_draft_article_returns_draft_without_filename_line():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="# Article\nContent here\n\nSUGGESTED_FILENAME: my-article")]
    )
    draft, _ = draft_article(mock_client, text_content="raw text")
    assert "# Article" in draft
    assert "Content here" in draft
    assert "SUGGESTED_FILENAME" not in draft


def test_draft_article_extracts_suggested_filename():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="# Article\nContent\n\nSUGGESTED_FILENAME: my-new-article")]
    )
    _, filename = draft_article(mock_client, text_content="raw text")
    assert filename == "my-new-article"


def test_draft_article_fallback_filename_when_none_suggested():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="# Article\nNo filename line here")]
    )
    _, filename = draft_article(mock_client, text_content="raw text")
    assert filename == "new-aims-article"


def test_draft_article_includes_text_content_in_request():
    mock_client = MagicMock()
    mock_client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="# Draft\nSUGGESTED_FILENAME: draft")]
    )
    draft_article(mock_client, text_content="some email content")
    call_kwargs = mock_client.messages.create.call_args.kwargs
    messages = call_kwargs["messages"]
    content_texts = [
        block["text"] for block in messages[0]["content"]
        if block.get("type") == "text"
    ]
    combined = " ".join(content_texts)
    assert "some email content" in combined
