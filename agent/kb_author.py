import base64
from io import BytesIO
from pathlib import Path

import anthropic
import pdfplumber
from docx import Document as DocxDocument

DOCS_DIR = Path(__file__).parent.parent / "docs"

KB_AUTHOR_SYSTEM_PROMPT = """\
You are helping build a structured AIMS knowledge base. Review the provided content \
and draft a clean markdown document.
Include:
- A descriptive title as a level-1 heading
- A one-paragraph summary
- Organized sections with level-2 headings
- Tables where appropriate for structured data
Focus on information useful for AIMS implementation and troubleshooting. \
Write in a reference style suitable for quick lookup during a support call.
End your response with this line exactly:
SUGGESTED_FILENAME: <kebab-case-name-without-extension>"""


def extract_pdf_text(file_bytes: bytes) -> str:
    """Extract all text from a PDF file."""
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n\n".join(pages)


def extract_docx_text(file_bytes: bytes) -> str:
    """Extract all text from a Word .docx file."""
    doc = DocxDocument(BytesIO(file_bytes))
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n\n".join(paragraphs)


def draft_article(
    client: anthropic.Anthropic,
    text_content: str = "",
    uploaded_files: list[dict] | None = None,
) -> tuple[str, str]:
    """
    Draft a KB markdown article from text and/or uploaded files.
    uploaded_files: list of {"name": str, "type": str, "bytes": bytes}
    Returns: (draft_markdown, suggested_filename)
    """
    content: list[dict] = []

    if text_content.strip():
        content.append({"type": "text", "text": f"Raw content to convert:\n\n{text_content}"})

    for f in uploaded_files or []:
        if f["type"].startswith("image/"):
            b64 = base64.standard_b64encode(f["bytes"]).decode()
            content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": f["type"], "data": b64},
            })
        elif f["type"] == "application/pdf":
            text = extract_pdf_text(f["bytes"])
            content.append({"type": "text", "text": f"PDF content from {f['name']}:\n\n{text}"})
        elif f["type"] in (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
        ):
            text = extract_docx_text(f["bytes"])
            content.append({"type": "text", "text": f"Word document content from {f['name']}:\n\n{text}"})
        else:
            text = f["bytes"].decode("utf-8", errors="replace")
            content.append({"type": "text", "text": f"File content from {f['name']}:\n\n{text}"})

    content.append({
        "type": "text",
        "text": "Draft the knowledge base article from the content above.",
    })

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=KB_AUTHOR_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": content}],
    )

    raw = response.content[0].text.strip()
    suggested_filename = "new-aims-article"
    lines = raw.splitlines()
    if lines and lines[-1].startswith("SUGGESTED_FILENAME:"):
        suggested_filename = lines[-1].replace("SUGGESTED_FILENAME:", "").strip()
        raw = "\n".join(lines[:-1]).strip()

    return raw, suggested_filename


def save_article(content: str, filename: str, docs_dir: Path = DOCS_DIR) -> Path:
    """Write a markdown article to docs_dir. Appends .md if not present."""
    if not filename.endswith(".md"):
        filename = f"{filename}.md"
    output_path = docs_dir / filename
    output_path.write_text(content, encoding="utf-8")
    return output_path