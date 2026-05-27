from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"


def load_knowledge_base(docs_dir: Path = DOCS_DIR) -> str:
    """Load all .md files from docs_dir and assemble into a single context string."""
    if not docs_dir.exists():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    md_files = sorted(docs_dir.glob("*.md"))
    if not md_files:
        return ""

    sections = []
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        sections.append(f"## {md_file.stem}\n\n{content}")

    return "\n\n---\n\n".join(sections)
