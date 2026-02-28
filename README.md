#  AI Study Buddy - AICTE - Batch 7


An AI-powered study companion built with Python and Streamlit.

## Features
- 💡 **Concept Explainer** — Any topic at ELI5 → University level
- 📄 **Note Summarizer** — Structured summaries from notes or uploaded PDFs/DOCX
- 📝 **Quiz Generator** — Interactive MCQ or True/False quizzes with scoring
- 🃏 **Flashcard Maker** — Flashcard decks with Anki CSV export
- 💬 **Study Chat** — Multi-turn AI tutor with conversation memory

## Quick Start

### 1. Clone and set up
```bash
git clone <your-repo>
cd study_buddy
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set your API key
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run the app
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Project Structure
```
study_buddy/
├── app.py                  # Home page
├── pages/
│   ├── 1_💡_Explainer.py
│   ├── 2_📄_Summarizer.py
│   ├── 3_📝_Quiz.py
│   ├── 4_🃏_Flashcards.py
│   └── 5_💬_Chat.py
├── core/
│   ├── explainer.py
│   ├── summarizer.py
│   ├── quiz_gen.py
│   ├── flashcard_gen.py
│   └── chat.py
├── utils/
│   ├── config.py
│   ├── prompts.py
│   ├── pdf_reader.py
│   └── pdf_export.py
├── requirements.txt
└── .env.example
```

## Deployment (Streamlit Cloud)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set main file as `app.py`
4. Add `OPENAI_API_KEY` in the Secrets section
5. Deploy!

## Requirements
- Python 3.10+
- OpenAI API key (get one at platform.openai.com)
