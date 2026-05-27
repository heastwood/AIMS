import os
from pathlib import Path

import anthropic
import streamlit as st
from dotenv import load_dotenv

from chat import send_message, trim_history
from kb_author import draft_article, save_article
from knowledge import load_knowledge_base
from PIL import Image

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
_icon = Image.open(Path(__file__).parent / "aims360_icon.png")
st.set_page_config(page_title="AIMS Agent", page_icon=_icon, layout="wide")
svg_logo = (Path(__file__).parent / "Logo_AIMS_RGB_gb.svg").read_text()
st.markdown(f'<div style="width:350px">{svg_logo}</div>', unsafe_allow_html=True)


# ── Claude client ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("ANTHROPIC_API_KEY not found. Add it to AIMS/agent/.env")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)


# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "knowledge" not in st.session_state:
    st.session_state.knowledge = load_knowledge_base()

client = get_client()

# ── Tabs ──────────────────────────────────────────────────────────────────────
chat_tab, kb_tab = st.tabs(["💬 Chat", "📚 Knowledge Base"])

# ── Chat tab ──────────────────────────────────────────────────────────────────
with chat_tab:
    with st.expander("How to use Chat"):
        st.markdown("""
**Chatting with the AIMS Knowledge Base**
- Type your question below and press **Enter**
- The agent knows AIMS500/1000 configuration, JAF/JCF/JRF file formats,
  Impress Automate integration, AD/service account setup, firewall requirements,
  and third-party OMS field mapping (Ricoh Process Director, Pitney Bowes MRDF)
- Ask in plain language — e.g. *"What ports does AIMS need open in the firewall?"*
  or *"How do I set up an AD group for AIMS login?"*
- Click **Reload Knowledge Base** after adding new articles to pick them up in this session
""")

    if st.button("🔄 Reload Knowledge Base"):
        st.session_state.knowledge = load_knowledge_base()
        st.success("Knowledge base reloaded.")

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question about AIMS..."):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = send_message(
                    client=client,
                    user_message=prompt,
                    history=st.session_state.history,
                    knowledge=st.session_state.knowledge,
                )
            st.markdown(response)

        st.session_state.history.append({"role": "user", "content": prompt})
        st.session_state.history.append({"role": "assistant", "content": response})
        st.session_state.history = trim_history(st.session_state.history)

# ── KB tab ────────────────────────────────────────────────────────────────────
with kb_tab:
    with st.expander("How to use the Knowledge Base"):
        st.markdown("""
**Adding to the Knowledge Base**
- Upload files using the uploader below — supported: images (PNG, JPG, GIF), PDFs, text/markdown
- You can also paste raw text (e.g. an email body) into the text area
- Mix and match — upload a screenshot and paste the accompanying email text together
- Click **Draft Article** and the agent will generate a structured markdown article
- Review and edit the draft, confirm the filename, then click **Save to Knowledge Base**
- Switch to the Chat tab and click **Reload Knowledge Base** to make the new article available
""")

    ALLOWED_TYPES = {"png", "jpg", "jpeg", "gif", "pdf", "txt", "md", "docx", "doc"}

    uploaded_files = st.file_uploader(
        "Upload files (images, PDFs, Word docs, text)",
        accept_multiple_files=True,
        key="kb_uploader",
    )

    invalid_files = [
        f.name for f in (uploaded_files or [])
        if Path(f.name).suffix.lstrip(".").lower() not in ALLOWED_TYPES
    ]
    if invalid_files:
        st.error(
            f"Unsupported file type(s): {', '.join(invalid_files)}. "
            "Please upload images (PNG, JPG, GIF), PDFs, Word documents, or text/markdown files only."
        )
        uploaded_files = [
            f for f in uploaded_files
            if Path(f.name).suffix.lstrip(".").lower() in ALLOWED_TYPES
        ]

    pasted_text = st.text_area(
        "Or paste text here (e.g. email body)",
        height=150,
        placeholder="Paste email content, notes, or any raw text to convert into a KB article...",
        key="kb_paste",
    )

    has_input = bool(uploaded_files or pasted_text.strip())

    if st.button("✍️ Draft Article", disabled=not has_input):
        files_data = [
            {"name": f.name, "type": f.type, "bytes": f.read()}
            for f in (uploaded_files or [])
        ]
        with st.spinner("Drafting article..."):
            draft, suggested_filename = draft_article(
                client=client,
                text_content=pasted_text,
                uploaded_files=files_data,
            )
        st.session_state["kb_draft"] = draft
        st.session_state["kb_filename"] = suggested_filename

    if "kb_draft" in st.session_state:
        st.subheader("Review Draft")
        st.caption("Edit the article below before saving.")
        edited_draft = st.text_area(
            "Article content (markdown)",
            value=st.session_state["kb_draft"],
            height=400,
            key="kb_draft_editor",
        )
        filename = st.text_input(
            "Filename (without .md):",
            value=st.session_state["kb_filename"],
            key="kb_filename_input",
        )
        col1, col2 = st.columns([1, 5])
        with col1:
            save_clicked = st.button("💾 Save to Knowledge Base", disabled=not filename.strip())
        with col2:
            if st.button("✖ Discard"):
                del st.session_state["kb_draft"]
                del st.session_state["kb_filename"]
                st.rerun()

        if save_clicked and filename.strip():
            saved_path = save_article(content=edited_draft, filename=filename.strip())
            st.success(
                f"Saved as `{saved_path.name}`. "
                "Go to the Chat tab and click **Reload Knowledge Base** to use it."
            )
            del st.session_state["kb_draft"]
            del st.session_state["kb_filename"]
