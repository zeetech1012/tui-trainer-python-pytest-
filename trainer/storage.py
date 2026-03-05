from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from trainer.models import (
    CodingTask,
    QuestionProgress,
    QuizQuestion,
    TheoryCard,
)

DATA_DIR = Path(__file__).parent.parent / "data"
QUESTIONS_FILE = DATA_DIR / "questions.json"
PROGRESS_FILE = DATA_DIR / "progress.json"


def load_questions() -> dict[str, list[Any]]:
    with QUESTIONS_FILE.open(encoding="utf-8") as f:
        raw = json.load(f)

    theory = [TheoryCard(**item) for item in raw.get("theory", [])]
    coding = [CodingTask(**item) for item in raw.get("coding", [])]
    quiz = [QuizQuestion(**item) for item in raw.get("quiz", [])]

    return {"theory": theory, "coding": coding, "quiz": quiz}


def load_progress() -> dict[str, QuestionProgress]:
    if not PROGRESS_FILE.exists():
        return {}
    with PROGRESS_FILE.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {qid: QuestionProgress(**data) for qid, data in raw.items()}


def save_progress(progress: dict[str, QuestionProgress]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    data = {
        qid: {
            "seen": p.seen,
            "correct": p.correct,
            "last_seen": p.last_seen,
        }
        for qid, p in progress.items()
    }
    with PROGRESS_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_or_create_progress(
    progress: dict[str, QuestionProgress], qid: str
) -> QuestionProgress:
    if qid not in progress:
        progress[qid] = QuestionProgress()
    return progress[qid]
