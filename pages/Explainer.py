import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.explainer import explain_concept, DIFFICULTY_LEVELS

st.set_page_config(page_title="Concept Explainer", page_icon="💡", layout="wide")

st.title("💡 Concept Explainer")
st.markdown("Enter any topic and get a clear, structured explanation at your preferred level.")
st.divider()

# ── Input Form ──
col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_input(
        "📚 Topic to Explain",
        placeholder="e.g., Quantum Entanglement, The French Revolution, Recursion in Programming...",
        help="Be specific for better results. E.g., 'Mitosis vs Meiosis' is better than 'Cell Division'."
    )

with col2:
    level = st.selectbox(
        "🎯 Difficulty Level",
        options=list(DIFFICULTY_LEVELS.keys()),
        index=2,  # Default: High School
    )

extra_context = st.text_area(
    "💬 Additional Context (optional)",
    placeholder="e.g., I already know about atoms, explain in the context of chemistry...",
    height=80,
)

explain_btn = st.button("✨ Explain This Topic", type="primary", use_container_width=True)

st.divider()

# ── Output ──
if explain_btn:
    if not topic.strip():
        st.warning("Please enter a topic to explain.")
    else:
        with st.spinner(f"Generating explanation for **{topic}** at {level} level..."):
            try:
                explanation = explain_concept(topic, level, extra_context)
                st.session_state["last_explanation"] = {"topic": topic, "level": level, "content": explanation}
            except Exception as e:
                st.error(f"Error generating explanation: {e}")
                st.stop()

if "last_explanation" in st.session_state:
    exp = st.session_state["last_explanation"]
    st.subheader(f"📖 {exp['topic']} — {exp['level']}")
    st.markdown(exp["content"])
    st.divider()

    # Download as text
    st.download_button(
        label="⬇️ Download Explanation (.txt)",
        data=exp["content"],
        file_name=f"explanation_{exp['topic'].replace(' ', '_')}.txt",
        mime="text/plain",
    )

    st.info("💡 Tip: Copy this explanation to the **Summarizer** or **Quiz Generator** for further study!")
