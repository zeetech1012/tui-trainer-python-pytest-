from __future__ import annotations

import random

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Markdown, Static

from trainer.models import QuizQuestion
from trainer.storage import get_or_create_progress, save_progress


class QuizScreen(Screen):
    """Quiz mode: multiple choice, 4 options, track score."""

    BINDINGS = [
        ("1", "pick_0", "Вариант 1"),
        ("2", "pick_1", "Вариант 2"),
        ("3", "pick_2", "Вариант 3"),
        ("4", "pick_3", "Вариант 4"),
        ("n", "next_question", "Следующий"),
        ("escape", "back", "Назад"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._questions: list[QuizQuestion] = []
        self._index: int = 0
        self._answered: bool = False
        self._session_correct: int = 0
        self._session_total: int = 0

    def on_mount(self) -> None:
        self._questions = list(self.app.questions["quiz"])
        random.shuffle(self._questions)
        self._show_question()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Static(id="flashcard-screen"):
            with Static(id="quiz-container"):
                yield Label("", id="quiz-meta")
                with Static(id="quiz-question", classes="card"):
                    yield Label("", id="quiz-topic", classes="card-title")
                    yield Markdown("", id="quiz-text")
                yield Button("", id="opt-0", classes="option-btn", variant="default")
                yield Button("", id="opt-1", classes="option-btn", variant="default")
                yield Button("", id="opt-2", classes="option-btn", variant="default")
                yield Button("", id="opt-3", classes="option-btn", variant="default")
                yield Label("", id="quiz-result")
                with Static(id="quiz-qa"):
                    yield Label("🧪 QA-контекст:", classes="card-title")
                    yield Markdown("", id="quiz-qa-text")
                with Static(id="flashcard-controls"):
                    yield Button("Следующий [N]", id="btn-next", classes="fc-btn", variant="primary", disabled=True)
                    yield Button("← Назад", id="btn-back", classes="fc-btn", variant="default")

    def _show_question(self) -> None:
        self._answered = False
        q = self._questions[self._index]
        total = len(self._questions)

        self.query_one("#quiz-meta", Label).update(
            f"Вопрос {self._index + 1}/{total} | "
            f"Сессия: {self._session_correct}/{self._session_total} ✓ | "
            f"Тема: {q.topic}"
        )
        diff = {"easy": "✅ easy", "medium": "⚠️ medium", "hard": "🔴 hard"}.get(q.difficulty, q.difficulty)
        self.query_one("#quiz-topic", Label).update(f"{q.topic.upper()} — {diff}")
        self.query_one("#quiz-text", Markdown).update(q.question)

        for i, opt_text in enumerate(q.options):
            btn = self.query_one(f"#opt-{i}", Button)
            btn.label = f"[{i + 1}]  {opt_text}"
            btn.variant = "default"
            btn.disabled = False
            btn.remove_class("correct")
            btn.remove_class("wrong")

        self.query_one("#quiz-result", Label).update("")
        self.query_one("#quiz-qa").remove_class("visible")
        self.query_one("#btn-next", Button).disabled = True

    def _pick(self, option_index: int) -> None:
        if self._answered:
            return

        self._answered = True
        self._session_total += 1
        q = self._questions[self._index]
        is_correct = option_index == q.correct

        if is_correct:
            self._session_correct += 1

        p = get_or_create_progress(self.app.progress, q.id)
        p.mark_seen(is_correct)
        save_progress(self.app.progress)

        for i in range(len(q.options)):
            btn = self.query_one(f"#opt-{i}", Button)
            btn.disabled = True
            if i == q.correct:
                btn.variant = "success"
            elif i == option_index and not is_correct:
                btn.variant = "error"

        result_label = self.query_one("#quiz-result", Label)
        if is_correct:
            result_label.update("✅ Правильно!")
        else:
            result_label.update(f"❌ Неверно. Правильный ответ: {q.options[q.correct]}")
        result_label.add_class("visible")

        if q.qa_context:
            self.query_one("#quiz-qa-text", Markdown).update(q.qa_context)
            self.query_one("#quiz-qa").add_class("visible")

        self.query_one("#btn-next", Button).disabled = False

    def action_pick_0(self) -> None:
        self._pick(0)

    def action_pick_1(self) -> None:
        self._pick(1)

    def action_pick_2(self) -> None:
        self._pick(2)

    def action_pick_3(self) -> None:
        self._pick(3)

    def action_next_question(self) -> None:
        if not self._answered:
            return
        self._index = (self._index + 1) % len(self._questions)
        self._show_question()

    def action_back(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "btn-next":
            self.action_next_question()
        elif btn_id == "btn-back":
            self.action_back()
        elif btn_id and btn_id.startswith("opt-"):
            idx = int(btn_id.split("-")[1])
            self._pick(idx)
