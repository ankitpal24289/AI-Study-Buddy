import streamlit as st

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a clean, modern look
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .feature-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s;
    }
    .feature-card:hover { border-color: #38bdf8; }
    .feature-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .feature-title { font-size: 1.1rem; font-weight: 700; color: #f1f5f9; }
    .feature-desc { font-size: 0.88rem; color: #94a3b8; margin-top: 0.3rem; }
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; color: white; }
</style>
""", unsafe_allow_html=True)

# --- Home Page ---
st.markdown('<div class="main-title">🎓 AI Study Buddy</div>', unsafe_allow_html=True)
st.markdown("#### Your personal AI-powered learning assistant — explain, summarize, quiz, and chat.")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💡</div>
        <div class="feature-title">Concept Explainer</div>
        <div class="feature-desc">Get any topic explained in simple terms, from ELI5 to university level.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <div class="feature-title">Note Summarizer</div>
        <div class="feature-desc">Paste your notes or upload a PDF and get a clean, structured summary instantly.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📝</div>
        <div class="feature-title">Quiz Generator</div>
        <div class="feature-desc">Auto-generate MCQs or true/false questions and test your knowledge interactively.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🃏</div>
        <div class="feature-title">Flashcard Maker</div>
        <div class="feature-desc">Create term-definition flashcard decks from any topic or uploaded material.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">Study Chat</div>
        <div class="feature-desc">Chat with an AI tutor that remembers your conversation and answers follow-up questions.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📤</div>
        <div class="feature-title">Export Anywhere</div>
        <div class="feature-desc">Download quizzes as PDF or flashcards as Anki-compatible CSV files.</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.info("👈 Use the **sidebar** to navigate between features. Make sure your OpenAI API key is set in the `.env` file.")
