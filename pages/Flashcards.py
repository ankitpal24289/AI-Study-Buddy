import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.flashcard_gen import generate_flashcards, export_flashcards_csv
from utils.pdf_reader import extract_text

st.set_page_config(page_title="Flashcard Maker", page_icon="🃏", layout="wide")

# ── Flashcard CSS ──
st.markdown("""
<style>
.flashcard-container {
    perspective: 1000px;
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    cursor: pointer;
}
.flashcard {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 2px solid #334155;
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: box-shadow 0.3s;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.flashcard:hover { box-shadow: 0 12px 48px rgba(56,189,248,0.2); border-color: #38bdf8; }
.card-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #64748b;
    margin-bottom: 1rem;
}
.card-front-text {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.5rem;
}
.card-back-text {
    font-size: 1.1rem;
    color: #94a3b8;
    line-height: 1.6;
}
.card-category {
    margin-top: 1rem;
    font-size: 0.72rem;
    padding: 0.2rem 0.7rem;
    background: rgba(56,189,248,0.1);
    color: #38bdf8;
    border-radius: 999px;
    border: 1px solid rgba(56,189,248,0.3);
}
.progress-text {
    text-align: center;
    color: #64748b;
    font-size: 0.9rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

st.title("🃏 Flashcard Maker")
st.markdown("Generate, study, and export interactive flashcard decks.")
st.divider()

# ── State ──
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "card_index" not in st.session_state:
    st.session_state.card_index = 0
if "show_back" not in st.session_state:
    st.session_state.show_back = False

# Prefill from summarizer if available
prefill = st.session_state.pop("prefill_flashcard", "")

# ── Configuration ──
with st.expander("⚙️ Flashcard Settings", expanded=not bool(st.session_state.flashcards)):
    source_type = st.radio("Source", ["Topic Name", "My Notes / File"], horizontal=True)

    if source_type == "Topic Name":
        fc_input = st.text_input(
            "Topic",
            placeholder="e.g., The Solar System, French Vocabulary, Python Data Types...",
            value=prefill[:100] if prefill else "",
        )
    else:
        input_method = st.radio("Notes As", ["Paste Text", "Upload File"], horizontal=True)
        if input_method == "Paste Text":
            fc_input = st.text_area(
                "Paste Notes",
                value=prefill,
                height=150,
                placeholder="Paste your study notes...",
            )
        else:
            uploaded = st.file_uploader("Upload File", type=["pdf", "docx", "txt"])
            fc_input = ""
            if uploaded:
                with st.spinner("Extracting text..."):
                    try:
                        fc_input = extract_text(uploaded)
                        st.success(f"✅ Loaded `{uploaded.name}`")
                    except Exception as e:
                        st.error(str(e))

    num_cards = st.slider("Number of Cards", min_value=5, max_value=30, value=10)
    generate_btn = st.button("🃏 Generate Flashcards", type="primary", use_container_width=True)

if generate_btn:
    if not fc_input.strip():
        st.warning("Please enter a topic or provide notes.")
    else:
        with st.spinner("Creating your flashcard deck..."):
            try:
                cards = generate_flashcards(fc_input, num_cards)
                st.session_state.flashcards = cards
                st.session_state.card_index = 0
                st.session_state.show_back = False
                st.success(f"✅ Created {len(cards)} flashcards!")
            except Exception as e:
                st.error(f"Flashcard generation failed: {e}")

st.divider()

# ── Flashcard Viewer ──
cards = st.session_state.flashcards

if cards:
    idx = st.session_state.card_index
    card = cards[idx]
    showing_back = st.session_state.show_back

    st.markdown(f'<div class="progress-text">Card {idx + 1} of {len(cards)}</div>', unsafe_allow_html=True)
    st.progress((idx + 1) / len(cards))

    # ── Card Display ──
    if not showing_back:
        st.markdown(f"""
        <div class="flashcard-container">
            <div class="flashcard">
                <div class="card-label">📖 Front — Term / Question</div>
                <div class="card-front-text">{card['front']}</div>
                <div class="card-category">{card.get('category', 'General')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="flashcard-container">
            <div class="flashcard" style="border-color: #a78bfa;">
                <div class="card-label" style="color: #a78bfa;">✨ Back — Answer / Definition</div>
                <div class="card-back-text">{card['back']}</div>
                <div class="card-category" style="background: rgba(167,139,250,0.1); color: #a78bfa; border-color: rgba(167,139,250,0.3);">{card.get('category', 'General')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Navigation Buttons ──
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1.5, 1, 1])

    with col1:
        if st.button("⬅️ Prev", use_container_width=True, disabled=(idx == 0)):
            st.session_state.card_index = max(0, idx - 1)
            st.session_state.show_back = False
            st.rerun()

    with col2:
        if st.button("➡️ Next", use_container_width=True, disabled=(idx == len(cards) - 1)):
            st.session_state.card_index = min(len(cards) - 1, idx + 1)
            st.session_state.show_back = False
            st.rerun()

    with col3:
        flip_label = "👁️ Show Answer" if not showing_back else "🔄 Show Term"
        if st.button(flip_label, type="primary", use_container_width=True):
            st.session_state.show_back = not showing_back
            st.rerun()

    with col4:
        if st.button("🔀 Shuffle", use_container_width=True):
            import random
            random.shuffle(st.session_state.flashcards)
            st.session_state.card_index = 0
            st.session_state.show_back = False
            st.rerun()

    with col5:
        if st.button("🔁 Restart", use_container_width=True):
            st.session_state.card_index = 0
            st.session_state.show_back = False
            st.rerun()

    st.divider()

    # ── All Cards Table ──
    with st.expander(f"📋 View All {len(cards)} Cards"):
        for i, c in enumerate(cards):
            col_a, col_b, col_c = st.columns([2, 3, 1])
            with col_a:
                st.markdown(f"**{c['front']}**")
            with col_b:
                st.markdown(c['back'])
            with col_c:
                st.caption(c.get("category", ""))
            if i < len(cards) - 1:
                st.divider()

    # ── Export ──
    st.subheader("⬇️ Export Flashcards")
    col1, col2 = st.columns(2)
    with col1:
        csv_bytes = export_flashcards_csv(cards)
        st.download_button(
            "📥 Download as CSV (Anki compatible)",
            data=csv_bytes,
            file_name="flashcards.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col2:
        # Plain text export
        txt_content = "\n\n".join([f"Q: {c['front']}\nA: {c['back']}" for c in cards])
        st.download_button(
            "📄 Download as TXT",
            data=txt_content,
            file_name="flashcards.txt",
            mime="text/plain",
            use_container_width=True,
        )
