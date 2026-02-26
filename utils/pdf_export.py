"""
Utility: Export quiz questions and results to a downloadable PDF.
Uses fpdf2 library.
"""

from fpdf import FPDF
import io


class QuizPDF(FPDF):
    """Custom PDF class with header and footer for quiz exports."""

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_fill_color(15, 23, 42)   # dark navy
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, "  AI Study Buddy — Quiz Export", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def export_quiz_pdf(
    topic: str,
    questions: list[dict],
    include_answers: bool = True,
    score_data: dict = None,
) -> bytes:
    """
    Generate a PDF of quiz questions (and optionally answers/results).

    Args:
        topic: The quiz topic label
        questions: List of question dicts from quiz_gen.generate_quiz()
        include_answers: Whether to include correct answers and explanations
        score_data: Optional score dict from quiz_gen.score_quiz() — adds a results section

    Returns:
        PDF file as bytes for Streamlit download button.
    """
    pdf = QuizPDF()
    pdf.set_margins(20, 20, 20)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── Title ──
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(0, 8, f"Quiz: {topic}", align="L")
    pdf.ln(2)

    if score_data:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(0, 100, 0)
        pdf.cell(
            0, 8,
            f"Your Score: {score_data['score']} / {score_data['total']}  ({score_data['percentage']}%)",
            new_x="LMARGIN", new_y="NEXT"
        )
        pdf.ln(4)

    pdf.set_draw_color(200, 200, 200)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(4)

    # ── Questions ──
    for i, q in enumerate(questions):
        # Question number + text
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 7, f"Q{i + 1}. {q['question']}")
        pdf.ln(1)

        # Options (MCQ)
        if "options" in q:
            pdf.set_font("Helvetica", "", 10)
            for opt in q["options"]:
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(0, 6, f"    {opt}")

        # Score result highlight
        if score_data:
            result = score_data["results"][i]
            if result["correct"]:
                pdf.set_text_color(0, 128, 0)
                pdf.set_font("Helvetica", "B", 10)
                pdf.cell(0, 6, "  ✓ Correct", new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.set_text_color(200, 0, 0)
                pdf.set_font("Helvetica", "B", 10)
                pdf.multi_cell(0, 6, f"  ✗ Incorrect — Your answer: {result['your_answer']}")

        # Answer + explanation
        if include_answers:
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(0, 90, 160)
            pdf.multi_cell(0, 6, f"  Answer: {q.get('answer', 'N/A')}")
            if q.get("explanation"):
                pdf.set_text_color(80, 80, 80)
                pdf.multi_cell(0, 6, f"  Explanation: {q['explanation']}")

        pdf.ln(4)
        pdf.set_draw_color(230, 230, 230)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(3)

    # Return PDF as bytes
    return bytes(pdf.output())
