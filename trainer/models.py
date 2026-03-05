from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class TheoryCard:
    id: str
    topic: str
    question: str
    answer: str
    difficulty: str = "medium"
    priority: int = 2
    qa_context: str = ""


@dataclass
class CodingTask:
    id: str
    topic: str
    description: str
    starter_code: str
    solution: str
    hints: list[str] = field(default_factory=list)
    difficulty: str = "medium"
    priority: int = 2
    qa_context: str = ""


@dataclass
class QuizQuestion:
    id: str
    topic: str
    question: str
    options: list[str]
    correct: int
    difficulty: str = "medium"
    priority: int = 2
    qa_context: str = ""


@dataclass
class QuestionProgress:
    seen: int = 0
    correct: int = 0
    last_seen: Optional[str] = None

    def mark_seen(self, is_correct: bool) -> None:
        self.seen += 1
        if is_correct:
            self.correct += 1
        self.last_seen = datetime.now().isoformat(timespec="seconds")

    @property
    def accuracy(self) -> float:
        if self.seen == 0:
            return 0.0
        return round(self.correct / self.seen * 100, 1)
