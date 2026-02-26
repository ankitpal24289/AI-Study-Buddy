import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.quiz_gen import generate_quiz, score_quiz
from utils.pdf_export import export_quiz_pdf
from utils.pdf_reader import extract_text

st.set_page_config(page_title="Quiz Generator", page_icon="📝", layout="wide")

st.title("📝 Quiz Generator")
st.markdown("Generate interactive quizzes from any topic or your own study notes.")
st.divider()

# ── State initialization ──
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# ── Configuration Panel ──
with st.expander("⚙️ Quiz Settings", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        source_type = st.radio("Source", ["Topic Name", "My Notes / File"], horizontal=True)
    with col2:
        quiz_type = st.selectbox("Question Type", ["MCQ", "True/False"])
    with col3:
        num_questions = st.slider("Number of Questions", min_value=3, max_value=15, value=5)

    if source_type == "Topic Name":
        quiz_input = st.text_input(
            "Topic",
            placeholder="e.g., World War II, Photosynthesis, Python OOP...",
            value=st.session_state.quiz_topic,
        )
    else:
        input_method = st.radio("Provide Notes As", ["Paste Text", "Upload File"], horizontal=True)
        if input_method == "Paste Text":
            quiz_input = st.text_area("Paste Notes", height=150,
                                       placeholder="Paste your study notes here...")
        else:
            uploaded = st.file_uploader("Upload File", type=["pdf", "docx", "txt"])
            quiz_input = ""
            if uploaded:
                with st.spinner("Extracting text..."):
                    try:
                        quiz_input = extract_text(uploaded)
                        st.success(f"✅ Loaded `{uploaded.name}`")
                    except Exception as e:
                        st.error(str(e))

    generate_btn = st.button("🎲 Generate Quiz", type="primary", use_container_width=True)

# ── Generate Quiz ──
if generate_btn:
    if not quiz_input.strip():
        st.warning("Please enter a topic or provide notes.")
    else:
        with st.spinner("Generating your quiz..."):
            try:
                questions = generate_quiz(quiz_input, num_questions, quiz_type)
                st.session_state.quiz_questions = questions
                st.session_state.quiz_topic = quiz_input[:60]
                st.session_state.quiz_submitted = False
                st.session_state.user_answers = {}
                st.success(f"✅ Generated {len(questions)} questions!")
            except Exception as e:
                st.error(f"Quiz generation failed: {e}")

st.divider()

# ── Interactive Quiz ──
questions = st.session_state.quiz_questions

if questions:
    st.subheader(f"📋 Quiz — {len(questions)} Questions")

    if not st.session_state.quiz_submitted:
        with st.form("quiz_form"):
            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}. {q['question']}**")

                if quiz_type == "MCQ" and "options" in q:
                    answer = st.radio(
                        f"q_{i}",
                        options=q["options"],
                        key=f"q_{i}",
                        label_visibility="collapsed",
                    )
                else:
                    answer = st.radio(
                        f"q_{i}",
                        options=["True", "False"],
                        key=f"q_{i}",
                        label_visibility="collapsed",
                    )

                st.session_state.user_answers[i] = answer
                st.markdown("---")

            submitted = st.form_submit_button("✅ Submit Quiz", use_container_width=True, type="primary")

        if submitted:
            st.session_state.quiz_submitted = True
            st.rerun()

    else:
        # ── Results ──
        score_data = score_quiz(questions, st.session_state.user_answers)
        pct = score_data["percentage"]

        # Score banner
        if pct >= 80:
            st.success(f"🎉 Excellent! You scored **{score_data['score']}/{score_data['total']} ({pct}%)**")
        elif pct >= 60:
            st.warning(f"📚 Good effort! You scored **{score_data['score']}/{score_data['total']} ({pct}%)**")
        else:
            st.error(f"📖 Keep studying! You scored **{score_data['score']}/{score_data['total']} ({pct}%)**")

        st.progress(pct / 100)
        st.markdown("---")

        # Question-by-question review
        st.subheader("📊 Detailed Results")
        for i, result in enumerate(score_data["results"]):
            icon = "✅" if result["correct"] else "❌"
            with st.expander(f"{icon} Q{i+1}: {result['question'][:80]}..."):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Your Answer:** {result['your_answer']}")
                with col2:
                    st.markdown(f"**Correct Answer:** :green[{result['correct_answer']}]")
                if result.get("explanation"):
                    st.info(f"💡 {result['explanation']}")

        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Retake Quiz", use_container_width=True):
                st.session_state.quiz_submitted = False
                st.session_state.user_answers = {}
                st.rerun()
        with col2:
            if st.button("🎲 New Quiz", use_container_width=True):
                st.session_state.quiz_questions = []
                st.session_state.quiz_submitted = False
                st.rerun()
        with col3:
            try:
                pdf_bytes = export_quiz_pdf(
                    st.session_state.quiz_topic,
                    questions,
                    include_answers=True,
                    score_data=score_data,
                )
                st.download_button(
                    "⬇️ Download Results PDF",
                    data=pdf_bytes,
                    file_name="quiz_results.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"PDF export error: {e}")
