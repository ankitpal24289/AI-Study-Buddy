import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.summarizer import summarize_notes, get_word_count
from utils.pdf_reader import extract_text

st.set_page_config(page_title="Note Summarizer", page_icon="📄", layout="wide")

st.title("📄 Note Summarizer")
st.markdown("Paste your notes or upload a file (PDF, DOCX, TXT) to get a structured AI summary.")
st.divider()

# ── Input Method Toggle ──
input_method = st.radio(
    "Input Method",
    ["✍️ Paste Text", "📁 Upload File"],
    horizontal=True,
)

notes_text = ""

if input_method == "✍️ Paste Text":
    notes_text = st.text_area(
        "Your Study Notes",
        placeholder="Paste your notes, lecture slides text, or any study material here...",
        height=250,
    )
else:
    uploaded_file = st.file_uploader(
        "Upload File",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX, TXT",
    )
    if uploaded_file:
        with st.spinner("Extracting text from file..."):
            try:
                notes_text = extract_text(uploaded_file)
                st.success(f"✅ Extracted **{get_word_count(notes_text):,} words** from `{uploaded_file.name}`")
                with st.expander("Preview extracted text"):
                    st.text(notes_text[:1500] + ("..." if len(notes_text) > 1500 else ""))
            except Exception as e:
                st.error(f"Error reading file: {e}")

# ── Summary Style ──
col1, col2 = st.columns([1, 1])
with col1:
    style = st.selectbox(
        "Summary Style",
        options=["structured", "concise", "detailed"],
        format_func=lambda x: {
            "structured": "📋 Structured (headings + bullets)",
            "concise": "⚡ Concise (max 150 words)",
            "detailed": "📚 Detailed (all important info)",
        }[x],
    )

with col2:
    if notes_text:
        wc = get_word_count(notes_text)
        st.metric("Word Count", f"{wc:,}", delta="Long doc — will chunk" if wc > 2500 else "Normal length")

summarize_btn = st.button("📝 Summarize Notes", type="primary", use_container_width=True)
st.divider()

# ── Output ──
if summarize_btn:
    if not notes_text.strip():
        st.warning("Please provide notes to summarize.")
    else:
        wc = get_word_count(notes_text)
        msg = f"Summarizing {wc:,} words..."
        if wc > 2500:
            msg += " (splitting into chunks for long document)"

        with st.spinner(msg):
            try:
                summary = summarize_notes(notes_text, style)
                st.session_state["last_summary"] = summary
            except Exception as e:
                st.error(f"Summarization failed: {e}")
                st.stop()

if "last_summary" in st.session_state:
    st.subheader("📋 Summary")
    st.markdown(st.session_state["last_summary"])
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇️ Download Summary (.txt)",
            data=st.session_state["last_summary"],
            file_name="summary.txt",
            mime="text/plain",
        )
    with col2:
        if st.button("🃏 Generate Flashcards from this Summary"):
            st.session_state["prefill_flashcard"] = st.session_state["last_summary"]
            st.switch_page("pages/4_🃏_Flashcards.py")
