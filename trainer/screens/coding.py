from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Markdown, Static, TextArea

from trainer.models import CodingTask
from trainer.storage import get_or_create_progress, save_progress


class CodingScreen(Screen):
    """Coding task mode: read task, write solution in editor, reveal answer."""

    BINDINGS = [
        ("ctrl+h", "show_hint", "Подсказка"),
        ("ctrl+s", "show_solution", "Решение"),
        ("ctrl+r", "reset_code", "Сбросить"),
        ("ctrl+n", "next_task", "Следующая"),
        ("escape", "back", "Назад"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._tasks: list[CodingTask] = []
        self._index: int = 0
        self._hint_index: int = 0
        self._solution_visible: bool = False

    def on_mount(self) -> None:
        self._tasks = list(self.app.questions["coding"])
        self._load_task()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Static(id="coding-layout"):
            with Static(id="task-panel"):
                yield Label("", id="task-meta")
                with Static(id="qa-why-box"):
                    yield Label("🧪 Зачем QA это знать:", classes="card-title")
                    yield Markdown("", id="qa-why-text")
                yield Label("Задача:", classes="card-title")
                yield Markdown("", id="task-description")
                yield Label("", id="hint-text")
                with Static(id="solution-box"):
                    yield Label("Решение:", classes="card-title")
                    yield TextArea("", id="solution-text", language="python", read_only=True)
            with Static(id="editor-panel"):
                yield Label("Твоё решение (редактируй тут):", classes="card-title")
                yield TextArea("", id="code-editor", language="python")
                with Static(id="coding-controls"):
                    yield Button("Подсказка [^H]", id="btn-hint", variant="warning")
                    yield Button("Решение [^S]", id="btn-solution", variant="success")
                    yield Button("Сбросить [^R]", id="btn-reset", variant="error")
                    yield Button("Далее [^N]", id="btn-next", variant="primary")
                    yield Button("← Назад", id="btn-back", variant="default")

    def _load_task(self) -> None:
        if not self._tasks:
            return

        self._solution_visible = False
        self._hint_index = 0
        task = self._tasks[self._index]
        total = len(self._tasks)

        diff = {"easy": "✅ easy", "medium": "⚠️ medium", "hard": "🔴 hard"}.get(task.difficulty, task.difficulty)
        p = self.app.progress.get(task.id)
        seen_info = f" | Попыток: {p.seen}" if p else ""
        self.query_one("#task-meta", Label).update(
            f"Задача {self._index + 1}/{total} | Тема: {task.topic.upper()} | {diff}{seen_info}"
        )

        qa_why = task.qa_context or "_Задача из реальной практики QA-автоматизатора_"
        self.query_one("#qa-why-text", Markdown).update(qa_why)

        self.query_one("#task-description", Markdown).update(task.description)
        self.query_one("#hint-text", Label).update("")

        editor = self.query_one("#code-editor", TextArea)
        editor.load_text(task.starter_code)

        solution_box = self.query_one("#solution-box")
        solution_box.remove_class("visible")

        solution_ta = self.query_one("#solution-text", TextArea)
        solution_ta.load_text(task.solution)

    def action_show_hint(self) -> None:
        task = self._tasks[self._index]
        if not task.hints:
            self.query_one("#hint-text", Label).update("💡 Подсказок нет для этой задачи.")
            return

        hint = task.hints[self._hint_index % len(task.hints)]
        hint_num = self._hint_index % len(task.hints) + 1
        self.query_one("#hint-text", Label).update(f"💡 Подсказка {hint_num}/{len(task.hints)}: {hint}")
        self._hint_index += 1

    def action_show_solution(self) -> None:
        task = self._tasks[self._index]
        p = get_or_create_progress(self.app.progress, task.id)
        p.mark_seen(False)
        save_progress(self.app.progress)

        solution_box = self.query_one("#solution-box")
        solution_box.add_class("visible")
        self._solution_visible = True

    def action_reset_code(self) -> None:
        task = self._tasks[self._index]
        editor = self.query_one("#code-editor", TextArea)
        editor.load_text(task.starter_code)
        self.query_one("#hint-text", Label).update("")

    def action_next_task(self) -> None:
        if not self._solution_visible:
            task = self._tasks[self._index]
            p = get_or_create_progress(self.app.progress, task.id)
            p.mark_seen(True)
            save_progress(self.app.progress)
        self._index = (self._index + 1) % len(self._tasks)
        self._load_task()

    def action_back(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "btn-hint":
            self.action_show_hint()
        elif btn_id == "btn-solution":
            self.action_show_solution()
        elif btn_id == "btn-reset":
            self.action_reset_code()
        elif btn_id == "btn-next":
            self.action_next_task()
        elif btn_id == "btn-back":
            self.action_back()
