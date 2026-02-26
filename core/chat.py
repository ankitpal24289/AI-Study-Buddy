"""
Core module: Study Chat
Maintains conversation history and sends messages to the LLM.
Uses a system prompt tuned for tutoring.
"""

from utils.config import chat_completion, get_client, get_model
from utils.prompts import CHAT_SYSTEM


def get_ai_response(
    conversation_history: list[dict],
    user_message: str,
    study_context: str = "",
) -> str:
    """
    Get the next AI response in a study conversation.

    Args:
        conversation_history: List of {"role": "user"/"assistant", "content": str} dicts
        user_message: The latest message from the student
        study_context: Optional context (e.g., uploaded notes) to inject into system prompt

    Returns:
        The assistant's reply as a markdown string.
    """
    system_prompt = CHAT_SYSTEM
    if study_context.strip():
        system_prompt += f"\n\nThe student has provided the following study material for context:\n\n{study_context[:3000]}"

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    return chat_completion(messages, temperature=0.7)


def build_history(messages: list[dict]) -> list[dict]:
    """
    Filter a Streamlit session_state messages list into the format
    expected by the OpenAI API (role + content only).
    Limits to the last 20 messages to avoid hitting context limits.
    """
    filtered = [
        {"role": m["role"], "content": m["content"]}
        for m in messages
        if m["role"] in ("user", "assistant")
    ]
    # Keep last 20 messages (10 turns)
    return filtered[-20:]
