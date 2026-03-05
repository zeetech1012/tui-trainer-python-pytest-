from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Markdown, Static

from trainer.models import TheoryCard
from trainer.storage import get_or_create_progress, save_progress

DIFFICULTY_ICONS = {"easy": "✅ easy", "medium": "⚠️ medium", "hard": "🔴 hard"}
PRIORITY_LABELS = {1: "🔥 MUST KNOW", 2: "⭐ IMPORTANT", 3: "💡 ADVANCED"}

TOPIC_ICONS: dict[str, str] = {
    "list": "📋",
    "dict": "📖",
    "set": "🔵",
    "tuple": "📦",
    "comprehensions": "🔄",
    "generators": "⚡",
    "strings": "🔤",
    "oop": "🏗️",
    "decorators": "🎨",
    "async": "🚀",
    "algorithms": "🧮",
    "api_testing": "🌐",
    "pytest": "🧪",
    "python_internals": "⚙️",
    "errors": "⚠️",
    "collections": "🗂️",
    "functools": "🔧",
    "itertools": "🔗",
    "typing": "📝",
    "patterns": "🏛️",
}


def _extract_trap(answer: str) -> str | None:
    """Extract 'ловушка на собесе' hint from answer text."""
    lower = answer.lower()
    markers = ["на собесе:", "ловушка:", "типичная ошибка:", "антипаттерн:"]
    for marker in markers:
        idx = lower.find(marker)
        if idx != -1:
            snippet = answer[idx : idx + 200].split("\n")[0]
            return snippet.strip()
    return None


class FlashcardScreen(Screen):
    """Flashcard mode: question → Space to reveal answer → mark as known/unknown."""

    BINDINGS = [
        ("space", "reveal", "Показать ответ"),
        ("k", "mark_correct", "Знаю ✓"),
        ("n", "mark_wrong", "Не знаю ✗"),
        ("s", "skip", "Пропустить"),
        ("left", "prev_card", "← Пред"),
        ("right", "next_direct", "→ След"),
        ("t", "toggle_trap", "Подсказка собес"),
        ("q", "toggle_qa", "QA-контекст"),
        ("escape", "back", "Назад"),
    ]

    def __init__(self, topic_filter: list[str] | None = None) -> None:
        super().__init__()
        self._topic_filter = topic_filter
        self._cards: list[TheoryCard] = []
        self._index: int = 0
        self._answer_visible: bool = False
        self._trap_visible: bool = False
        self._qa_visible: bool = False

    def on_mount(self) -> None:
        all_cards = list(self.app.questions["theory"])
        if self._topic_filter:
            filtered = [c for c in all_cards if c.topic in self._topic_filter]
            all_cards = filtered if filtered else all_cards
        self._cards = all_cards
        self._sort_cards()
        self._show_card()

    def _sort_cards(self) -> None:
        """Sort by: priority ASC → unseen first → lowest accuracy first."""
        progress = self.app.progress
        diff_order = {"easy": 0, "medium": 1, "hard": 2}

        def sort_key(card: TheoryCard) -> tuple[int, int, int, float]:
            p = progress.get(card.id)
            seen = p.seen if p else 0
            accuracy = p.accuracy if p else 0.0
            unseen_first = 0 if seen == 0 else 1
            return (
                card.priority,                          # P1 first
                diff_order.get(card.difficulty, 1),    # easy before hard
                unseen_first,                           # unseen first
                accuracy,                               # lowest accuracy first
            )

        self._cards.sort(key=sort_key)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Static(id="flashcard-screen"):
            with Static(id="flashcard-container"):
                yield Label("", id="flashcard-meta")
                with Static(id="question-box", classes="card"):
                    yield Label("", classes="card-title", id="fc-topic")
                    yield Markdown("", id="fc-question")
                with Static(id="answer-box", classes="card"):
                    yield Label("Ответ:", classes="card-title")
                    yield Markdown("", id="fc-answer")
                with Static(id="fc-extra"):
                    yield Markdown("", id="fc-trap-text")
                with Static(id="fc-qa"):
                    yield Label("🧪 Применение в автотестах:", classes="card-title")
                    yield Markdown("", id="fc-qa-text")
                with Static(id="flashcard-controls"):
                    yield Button("Показать ответ [Space]", id="btn-reveal", classes="fc-btn", variant="primary")
                    yield Button("Знаю ✓ [K]", id="btn-correct", classes="fc-btn", variant="success", disabled=True)
                    yield Button("Не знаю ✗ [N]", id="btn-wrong", classes="fc-btn", variant="error", disabled=True)
                    yield Button("← [←]", id="btn-prev", classes="fc-btn", variant="default")
                    yield Button("Пропустить [S]", id="btn-skip", classes="fc-btn", variant="default")
                    yield Button("→ [→]", id="btn-next-direct", classes="fc-btn", variant="default")
                    yield Button("← Меню", id="btn-back", classes="fc-btn", variant="default")

    def _show_card(self) -> None:
        if not self._cards:
            return

        self._answer_visible = False
        self._trap_visible = False
        card = self._cards[self._index]
        total = len(self._cards)
        progress = self.app.progress.get(card.id)

        topic_icon = TOPIC_ICONS.get(card.topic, "•")
        diff_icon = DIFFICULTY_ICONS.get(card.difficulty, card.difficulty)
        priority_label = PRIORITY_LABELS.get(card.priority, "")

        meta_parts = [
            f"[{self._index + 1}/{total}]",
            priority_label,
            f"{topic_icon} {card.topic.upper()}",
            diff_icon,
        ]
        if progress and progress.seen > 0:
            meta_parts.append(f"👁 {progress.seen}x  ✓ {progress.accuracy}%")

        self.query_one("#flashcard-meta", Label).update("  |  ".join(meta_parts))
        self.query_one("#fc-topic", Label).update(
            f"{priority_label}  {topic_icon} {card.topic.upper()} — {diff_icon}"
        )
        self.query_one("#fc-question", Markdown).update(f"### {card.question}")
        self.query_one("#fc-answer", Markdown).update(card.answer)

        # Trap hint extraction
        trap = _extract_trap(card.answer)
        if trap:
            self.query_one("#fc-trap-text", Markdown).update(f"**На собесе:** {trap}")
        else:
            self.query_one("#fc-trap-text", Markdown).update("")

        # QA context
        qa_text = card.qa_context or "_QA-контекст не заполнен для этой карточки_"
        self.query_one("#fc-qa-text", Markdown).update(qa_text)

        # Reset visibility
        self._qa_visible = False
        self.query_one("#answer-box").remove_class("visible")
        self.query_one("#fc-extra").remove_class("visible")
        self.query_one("#fc-qa").remove_class("visible")

        self.query_one("#btn-reveal", Button).disabled = False
        self.query_one("#btn-correct", Button).disabled = True
        self.query_one("#btn-wrong", Button).disabled = True

    def action_reveal(self) -> None:
        if self._answer_visible:
            return
        self._answer_visible = True
        self.query_one("#answer-box").add_class("visible")
        self.query_one("#btn-reveal", Button).disabled = True
        self.query_one("#btn-correct", Button).disabled = False
        self.query_one("#btn-wrong", Button).disabled = False

    def action_toggle_trap(self) -> None:
        """Show/hide 'на собесе' section."""
        if not self._answer_visible:
            self.action_reveal()
        extra = self.query_one("#fc-extra")
        if self._trap_visible:
            extra.remove_class("visible")
            self._trap_visible = False
        else:
            extra.add_class("visible")
            self._trap_visible = True

    def action_toggle_qa(self) -> None:
        """Show/hide QA automation context section."""
        if not self._answer_visible:
            self.action_reveal()
        qa_box = self.query_one("#fc-qa")
        if self._qa_visible:
            qa_box.remove_class("visible")
            self._qa_visible = False
        else:
            qa_box.add_class("visible")
            self._qa_visible = True

    def action_mark_correct(self) -> None:
        if not self._answer_visible:
            return
        self._record(correct=True)
        self._advance()

    def action_mark_wrong(self) -> None:
        if not self._answer_visible:
            return
        self._record(correct=False)
        self._advance()

    def action_skip(self) -> None:
        self._advance()

    def action_prev_card(self) -> None:
        self._index = (self._index - 1) % len(self._cards)
        self._show_card()

    def action_next_direct(self) -> None:
        self._index = (self._index + 1) % len(self._cards)
        self._show_card()

    def _record(self, correct: bool) -> None:
        card = self._cards[self._index]
        p = get_or_create_progress(self.app.progress, card.id)
        p.mark_seen(correct)
        save_progress(self.app.progress)

    def _advance(self) -> None:
        self._index = (self._index + 1) % len(self._cards)
        self._show_card()

    def action_back(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        mapping = {
            "btn-reveal": self.action_reveal,
            "btn-correct": self.action_mark_correct,
            "btn-wrong": self.action_mark_wrong,
            "btn-skip": self.action_skip,
            "btn-prev": self.action_prev_card,
            "btn-next-direct": self.action_next_direct,
            "btn-back": self.action_back,
        }
        action = mapping.get(event.button.id or "")
        if action:
            action()
