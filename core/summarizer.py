"""
Core module: Note Summarizer
Summarizes study notes or uploaded document text using an LLM.
Handles chunking for long documents automatically.
"""

from utils.config import chat_completion
from utils.prompts import (
    SUMMARIZER_SYSTEM,
    summarizer_user_prompt,
    summarizer_chunk_prompt,
    merge_summaries_prompt,
)
from utils.pdf_reader import chunk_text

# Max words per chunk before we split the document
CHUNK_THRESHOLD_WORDS = 2500


def summarize_notes(notes: str, style: str = "structured") -> str:
    """
    Summarize the provided text. Automatically handles long documents
    by chunking and merging partial summaries.

    Args:
        notes: Raw text of the study notes
        style: "structured" | "concise" | "detailed"

    Returns:
        A formatted summary string (markdown)
    """
    if not notes.strip():
        raise ValueError("Notes cannot be empty.")

    word_count = len(notes.split())

    # Short document: single API call
    if word_count <= CHUNK_THRESHOLD_WORDS:
        messages = [
            {"role": "system", "content": SUMMARIZER_SYSTEM},
            {"role": "user", "content": summarizer_user_prompt(notes, style)},
        ]
        return chat_completion(messages, temperature=0.4)

    # Long document: chunk → summarize each → merge
    chunks = chunk_text(notes, max_tokens=2500, overlap=150)
    partial_summaries = []

    for i, chunk in enumerate(chunks):
        messages = [
            {"role": "system", "content": SUMMARIZER_SYSTEM},
            {"role": "user", "content": summarizer_chunk_prompt(chunk, i + 1, len(chunks))},
        ]
        partial_summary = chat_completion(messages, temperature=0.3)
        partial_summaries.append(partial_summary)

    # Merge all partial summaries into one final summary
    merge_messages = [
        {"role": "system", "content": SUMMARIZER_SYSTEM},
        {"role": "user", "content": merge_summaries_prompt(partial_summaries)},
    ]
    return chat_completion(merge_messages, temperature=0.4)


def get_word_count(text: str) -> int:
    """Return approximate word count of a string."""
    return len(text.split())
