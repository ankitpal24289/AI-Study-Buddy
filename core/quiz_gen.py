"""
Core module: Quiz Generator
Generates MCQ or True/False quizzes from any topic or notes.
Returns structured JSON that the UI layer renders interactively.
"""

import json
import re
from utils.config import chat_completion
from utils.prompts import QUIZ_SYSTEM, quiz_user_prompt


def _clean_json(raw: str) -> str:
    """
    Strip markdown code fences and whitespace from a raw LLM response
    so it can be safely parsed as JSON.
    """
    raw = raw.strip()
    # Remove ```json ... ``` or ``` ... ``` fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return raw.strip()


def generate_quiz(
    topic_or_notes: str,
    num_questions: int = 5,
    quiz_type: str = "MCQ",
) -> list[dict]:
    """
    Generate a quiz as a list of question dicts.

    Args:
        topic_or_notes: A topic name or raw study notes
        num_questions: Number of questions to generate (1-20)
        quiz_type: "MCQ" or "True/False"

    Returns:
        List of question dicts. MCQ format:
            {"question": str, "options": list[str], "answer": str, "explanation": str}
        True/False format:
            {"question": str, "answer": str, "explanation": str}

    Raises:
        ValueError: If the LLM response cannot be parsed as JSON.
    """
    if not topic_or_notes.strip():
        raise ValueError("Topic or notes cannot be empty.")

    num_questions = max(1, min(20, num_questions))  # clamp to 1-20

    messages = [
        {"role": "system", "content": QUIZ_SYSTEM},
        {"role": "user", "content": quiz_user_prompt(topic_or_notes, num_questions, quiz_type)},
    ]

    raw = chat_completion(messages, temperature=0.6)
    cleaned = _clean_json(raw)

    try:
        questions = json.loads(cleaned)
    except json.JSONDecodeError:
        # Attempt to extract a JSON array from the response
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        if match:
            questions = json.loads(match.group())
        else:
            raise ValueError(
                f"Could not parse quiz JSON from model response.\nRaw response:\n{raw}"
            )

    if not isinstance(questions, list):
        raise ValueError("Expected a JSON array of questions.")

    return questions


def score_quiz(questions: list[dict], user_answers: dict[int, str]) -> dict:
    """
    Score a completed quiz.

    Args:
        questions: The list of question dicts from generate_quiz()
        user_answers: {question_index: selected_answer_string}

    Returns:
        {
            "score": int,
            "total": int,
            "percentage": float,
            "results": [{"question": str, "correct": bool, "correct_answer": str, "your_answer": str}]
        }
    """
    total = len(questions)
    score = 0
    results = []

    for i, q in enumerate(questions):
        user_ans = user_answers.get(i, "")
        correct_ans = q.get("answer", "")
        is_correct = user_ans.strip() == correct_ans.strip()
        if is_correct:
            score += 1
        results.append({
            "question": q["question"],
            "correct": is_correct,
            "correct_answer": correct_ans,
            "your_answer": user_ans,
            "explanation": q.get("explanation", ""),
        })

    return {
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 1) if total > 0 else 0,
        "results": results,
    }
