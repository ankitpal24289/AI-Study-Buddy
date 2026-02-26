import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.chat import get_ai_response, build_history
from utils.pdf_reader import extract_text

st.set_page_config(page_title="Study Chat", page_icon="💬", layout="wide")

st.title("💬 Study Chat")
st.markdown("Chat with your AI tutor. Ask anything, follow up, and get clear answers.")
st.divider()

# ── State ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_context" not in st.session_state:
    st.session_state.chat_context = ""

# ── Sidebar: Context Upload ──
with st.sidebar:
    st.subheader("📚 Study Context (Optional)")
    st.markdown("Upload your notes so the AI can answer questions about your specific material.")

    context_method = st.radio("Add Context", ["None", "Paste Text", "Upload File"])

    if context_method == "Paste Text":
        ctx = st.text_area("Paste Notes", height=200, placeholder="Your study notes...")
        if st.button("Set Context"):
            st.session_state.chat_context = ctx
            st.success("✅ Context set!")

    elif context_method == "Upload File":
        uploaded = st.file_uploader("Upload File", type=["pdf", "docx", "txt"])
        if uploaded:
            with st.spinner("Extracting..."):
                try:
                    st.session_state.chat_context = extract_text(uploaded)
                    st.success(f"✅ Loaded `{uploaded.name}`")
                except Exception as e:
                    st.error(str(e))

    if st.session_state.chat_context:
        wc = len(st.session_state.chat_context.split())
        st.info(f"📄 Context loaded: {wc:,} words")
        if st.button("🗑️ Clear Context"):
            st.session_state.chat_context = ""
            st.rerun()

    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("**Suggested starters:**")
    starters = [
        "Explain this concept simply",
        "What are the key points?",
        "Give me an example",
        "Why is this important?",
        "How does X relate to Y?",
    ]
    for s in starters:
        st.caption(f"• {s}")

# ── Chat Display ──
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding:3rem; color:#64748b;">
        <div style="font-size:3rem;">🤖</div>
        <div style="font-size:1.1rem; margin-top:1rem;">Hi! I'm your AI study tutor.</div>
        <div style="font-size:0.9rem; margin-top:0.5rem;">Ask me anything — a concept, a question about your notes, or for examples and explanations.</div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat Input ──
user_input = st.chat_input("Ask your study question...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                history = build_history(st.session_state.messages[:-1])  # exclude last user msg
                response = get_ai_response(
                    conversation_history=history,
                    user_message=user_input,
                    study_context=st.session_state.chat_context,
                )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"❌ Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# ── Export Chat ──
if len(st.session_state.messages) > 2:
    with st.expander("⬇️ Export Chat"):
        chat_text = "\n\n".join([
            f"{'You' if m['role'] == 'user' else 'AI Tutor'}: {m['content']}"
            for m in st.session_state.messages
        ])
        st.download_button(
            "Download Conversation (.txt)",
            data=chat_text,
            file_name="study_chat.txt",
            mime="text/plain",
        )
