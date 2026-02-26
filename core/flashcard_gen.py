"""
Core module: Flashcard Generator
Generates term-definition flashcard pairs from any topic or notes.
Also provides export to CSV (Anki-compatible).
"""

import json
import re
import io
import csv
from utils.config import chat_completion
from utils.prompts import FLASHCARD_SYSTEM, flashcard_user_prompt


def _clean_json(raw: str) -> str:
    """Strip markdown code fences from raw LLM response."""
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return raw.strip()


def generate_flashcards(
    topic_or_notes: str,
    num_cards: int = 10,
) -> list[dict]:
    """
    Generate flashcards as a list of dicts with 'front', 'back', 'category'.

    Args:
        topic_or_notes: A topic name (e.g., "Photosynthesis") or raw study notes
        num_cards: Number of flashcards to generate (1-30)

    Returns:
        List of dicts: [{"front": str, "back": str, "category": str}, ...]

    Raises:
        ValueError: If the model response cannot be parsed.
    """
    if not topic_or_notes.strip():
        raise ValueError("Topic or notes cannot be empty.")

    num_cards = max(1, min(30, num_cards))  # clamp 1-30

    messages = [
        {"role": "system", "content": FLASHCARD_SYSTEM},
        {"role": "user", "content": flashcard_user_prompt(topic_or_notes, num_cards)},
    ]

    raw = chat_completion(messages, temperature=0.6)
    cleaned = _clean_json(raw)

    try:
        cards = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        if match:
            cards = json.loads(match.group())
        else:
            raise ValueError(
                f"Could not parse flashcard JSON from model response.\nRaw:\n{raw}"
            )

    if not isinstance(cards, list):
        raise ValueError("Expected a JSON array of flashcards.")

    # Ensure all cards have the required keys
    normalized = []
    for card in cards:
        normalized.append({
            "front": card.get("front", ""),
            "back": card.get("back", ""),
            "category": card.get("category", "General"),
        })

    return normalized


def export_flashcards_csv(cards: list[dict]) -> bytes:
    """
    Export flashcards to a CSV file (bytes) compatible with Anki.

    Anki import format: Front, Back, Tags (optional)

    Returns:
        CSV content as bytes for Streamlit download button.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Front", "Back", "Category"])
    for card in cards:
        writer.writerow([card["front"], card["back"], card.get("category", "")])
    return output.getvalue().encode("utf-8")
