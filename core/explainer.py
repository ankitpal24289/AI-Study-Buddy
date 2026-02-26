"""
Core module: Concept Explainer
Explains any topic at a specified difficulty level using an LLM.
"""

from utils.config import chat_completion
from utils.prompts import EXPLAINER_SYSTEM, explainer_user_prompt


DIFFICULTY_LEVELS = {
    "ELI5 (Explain Like I'm 5)": "ELI5 — use very simple words and relatable analogies a 5-year-old would understand",
    "Middle School": "middle school level — assume basic knowledge, use simple vocabulary and everyday examples",
    "High School": "high school level — include relevant terminology and slightly technical explanations",
    "University / Advanced": "university/advanced level — use proper technical terminology, depth, and academic rigor",
}


def explain_concept(topic: str, level: str, extra_context: str = "") -> str:
    """
    Generate an explanation of `topic` at the given difficulty `level`.

    Args:
        topic: The concept or topic to explain (e.g., "Photosynthesis")
        level: One of the keys in DIFFICULTY_LEVELS
        extra_context: Optional additional context from the student

    Returns:
        A formatted explanation string (markdown)
    """
    if not topic.strip():
        raise ValueError("Topic cannot be empty.")

    level_description = DIFFICULTY_LEVELS.get(level, level)

    messages = [
        {"role": "system", "content": EXPLAINER_SYSTEM},
        {"role": "user", "content": explainer_user_prompt(topic, level_description, extra_context)},
    ]

    return chat_completion(messages, temperature=0.7)
