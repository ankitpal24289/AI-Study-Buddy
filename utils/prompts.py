"""
Centralized prompt templates for all AI features.
Keeping prompts here makes them easy to tweak and version.
"""

# ─────────────────────────────────────────────
# CONCEPT EXPLAINER
# ─────────────────────────────────────────────

EXPLAINER_SYSTEM = """You are an expert tutor skilled at explaining complex topics clearly.
Your explanations are accurate, engaging, and tailored to the requested difficulty level.
Use analogies, examples, and structured formatting (headings, bullet points) to maximize understanding.
Always end with a "Key Takeaways" section of 3-5 bullet points."""

def explainer_user_prompt(topic: str, level: str, extra_context: str = "") -> str:
    context_line = f"\nAdditional context from the student: {extra_context}" if extra_context else ""
    return f"""Explain the following topic at a {level} level:

Topic: {topic}{context_line}

Structure your response with:
1. A brief introduction
2. Core concept explanation with examples
3. Real-world applications
4. Key Takeaways (bullet points)"""


# ─────────────────────────────────────────────
# NOTE SUMMARIZER
# ─────────────────────────────────────────────

SUMMARIZER_SYSTEM = """You are an expert academic assistant that creates clear, concise summaries.
You identify the most important concepts, definitions, and relationships in study material.
Your summaries are structured, scannable, and study-friendly."""

def summarizer_user_prompt(notes: str, style: str = "structured") -> str:
    styles = {
        "structured": "a structured summary with headings, bullet points for key ideas, and a brief conclusion",
        "concise": "a concise paragraph summary (max 150 words) highlighting only the most critical points",
        "detailed": "a detailed summary preserving all important details, organized by topic/section",
    }
    style_instruction = styles.get(style, styles["structured"])
    return f"""Summarize the following study material as {style_instruction}.

STUDY MATERIAL:
{notes}

Also include at the end:
- **Important Terms**: List any key terms/definitions found
- **Study Tips**: 2-3 tips for mastering this material"""


def summarizer_chunk_prompt(chunk: str, chunk_num: int, total: int) -> str:
    return f"""Summarize the key points from this section (part {chunk_num} of {total}) of a study document.
Be concise. Focus on facts, definitions, and concepts.

SECTION:
{chunk}"""


def merge_summaries_prompt(partial_summaries: list[str]) -> str:
    combined = "\n\n---\n\n".join(
        [f"Section {i+1} Summary:\n{s}" for i, s in enumerate(partial_summaries)]
    )
    return f"""You have been given summaries of different sections of a study document.
Create a single, unified, well-structured final summary from these section summaries.

{combined}

Final summary should include:
- Main topics covered
- Key concepts and definitions
- Important Terms glossary
- Study Tips"""


# ─────────────────────────────────────────────
# QUIZ GENERATOR
# ─────────────────────────────────────────────

QUIZ_SYSTEM = """You are an expert educator who creates high-quality assessment questions.
You MUST return ONLY valid JSON — no explanations, no markdown fences, no extra text.
The JSON must exactly match the requested format."""

def quiz_user_prompt(topic_or_notes: str, num_questions: int, quiz_type: str) -> str:
    if quiz_type == "MCQ":
        format_desc = """[
  {
    "question": "What is ...?",
    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "answer": "A) ...",
    "explanation": "Brief explanation of why this is correct."
  }
]"""
    else:  # True/False
        format_desc = """[
  {
    "question": "Statement about the topic...",
    "answer": "True",
    "explanation": "Brief explanation."
  }
]"""

    return f"""Generate exactly {num_questions} {quiz_type} questions based on the following content.

CONTENT:
{topic_or_notes}

Return ONLY a JSON array in this exact format:
{format_desc}

Rules:
- Questions must be clear and unambiguous
- For MCQ, make all 4 options plausible
- Cover different aspects of the content
- Return ONLY the JSON array, nothing else"""


# ─────────────────────────────────────────────
# FLASHCARD GENERATOR
# ─────────────────────────────────────────────

FLASHCARD_SYSTEM = """You are an expert at creating study flashcards.
You MUST return ONLY valid JSON — no markdown, no extra text.
Create flashcards that are clear, concise, and memorable."""

def flashcard_user_prompt(topic_or_notes: str, num_cards: int) -> str:
    return f"""Create exactly {num_cards} flashcards based on the following content.

CONTENT:
{topic_or_notes}

Return ONLY a JSON array in this exact format:
[
  {{
    "front": "Term or question",
    "back": "Definition or answer",
    "category": "optional category/topic tag"
  }}
]

Rules:
- Front side should be a term, concept, or question
- Back side should be a concise definition or answer (max 2-3 sentences)
- Cover the most important concepts
- Return ONLY the JSON array, nothing else"""


# ─────────────────────────────────────────────
# STUDY CHAT
# ─────────────────────────────────────────────

CHAT_SYSTEM = """You are a friendly, knowledgeable AI study tutor.
Your goal is to help students understand their study material.
- Answer questions clearly with examples when helpful
- If a student seems confused, try a different explanation approach
- Encourage curiosity and deeper thinking
- Keep responses focused and educational
- Use formatting (bold, bullet points) to improve readability
- If you don't know something, say so honestly"""
