from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Footer, Header, Label, Static


TOPIC_LABELS: dict[str, str] = {
    # === PRIORITY 1: MUST KNOW ===
    "list":             "🔥 [P1] List — срезы, sort, методы",
    "dict":             "🔥 [P1] Dict — get, setdefault, comprehension",
    "set":              "🔥 [P1] Set — операции, frozenset",
    "comprehensions":   "🔥 [P1] Comprehensions — list/dict/set",
    "strings":          "🔥 [P1] Strings — split, strip, парсинг",
    "errors":           "🔥 [P1] Errors — try/except, raise",
    "functions":        "🔥 [P1] Functions — *args, **kwargs, замыкания",
    "modules":          "🔥 [P1] Modules — import, __name__, пакеты",
    "files":            "🔥 [P1] Files — with open, pathlib, csv",
    # === PRIORITY 2: IMPORTANT ===
    "oop":              "⭐ [P2] ООП — классы, наследование, dunder",
    "pytest":           "⭐ [P2] Pytest — fixtures, conftest, parametrize",
    "api_testing":      "⭐ [P2] API Testing — requests, mock",
    "algorithms":       "⭐ [P2] Algorithms — LeetCode, Two Sum, Sliding Window",
    "generators":       "⭐ [P2] Generators — yield, lazy eval",
    "python_internals": "⭐ [P2] Python Internals — GIL, mutable, iterators",
    "datetime":         "⭐ [P2] Datetime — strftime, timedelta",
    "scope":            "⭐ [P2] Scope — LEGB, global, nonlocal",
    # === PRIORITY 3: ADVANCED ===
    "decorators":       "💡 [P3] Decorators — @wraps, retry, параметры",
    "async":            "💡 [P3] Async/Await — asyncio, gather, tasks",
    "collections":      "💡 [P3] Collections — Counter, deque, namedtuple",
    "functools":        "💡 [P3] Functools — lru_cache, partial, reduce",
    "itertools":        "💡 [P3] Itertools — chain, groupby, combinations",
    "typing":           "💡 [P3] Typing — Optional, Union, TypeVar",
    "pattern_matching": "💡 [P3] Pattern Matching — match/case, guards",
    "patterns":         "💡 [P3] Design Patterns — Singleton, Strategy",
    "tuple":            "💡 [P3] Tuple — namedtuple, распаковка",
}


class TopicFilterScreen(Screen):
    """Topic selection screen — filter questions by topic."""

    BINDINGS = [
        ("a", "select_all", "Все темы"),
        ("c", "clear_all", "Очистить"),
        ("enter", "confirm", "Подтвердить"),
        ("escape", "back", "Назад"),
    ]

    def __init__(self, mode: str, callback) -> None:
        super().__init__()
        self._mode = mode
        self._callback = callback

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Static(id="flashcard-screen"):
            with Static(id="flashcard-container"):
                yield Label(f"Выбери темы для режима: {self._mode.upper()}", classes="card-title")
                yield Label("(пробел — переключить, A — все, C — очистить, Enter — начать)", id="flashcard-meta")
                with Static(id="question-box", classes="card"):
                    for topic_id, topic_label in TOPIC_LABELS.items():
                        yield Checkbox(topic_label, value=True, id=f"topic-{topic_id}")
                with Static(id="flashcard-controls"):
                    yield Button("▶  Начать [Enter]", id="btn-confirm", variant="primary", classes="fc-btn")
                    yield Button("Все темы [A]", id="btn-all", variant="default", classes="fc-btn")
                    yield Button("← Назад", id="btn-back", variant="default", classes="fc-btn")

    def _get_selected_topics(self) -> list[str]:
        selected = []
        for topic_id in TOPIC_LABELS:
            cb = self.query_one(f"#topic-{topic_id}", Checkbox)
            if cb.value:
                selected.append(topic_id)
        return selected

    def action_select_all(self) -> None:
        for topic_id in TOPIC_LABELS:
            self.query_one(f"#topic-{topic_id}", Checkbox).value = True

    def action_clear_all(self) -> None:
        for topic_id in TOPIC_LABELS:
            self.query_one(f"#topic-{topic_id}", Checkbox).value = False

    def action_confirm(self) -> None:
        selected = self._get_selected_topics()
        if not selected:
            selected = list(TOPIC_LABELS.keys())
        self.app.pop_screen()
        self._callback(selected)

    def action_back(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-confirm":
            self.action_confirm()
        elif event.button.id == "btn-all":
            self.action_select_all()
        elif event.button.id == "btn-back":
            self.action_back()
