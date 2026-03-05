from __future__ import annotations

from collections import defaultdict

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Header, Label, Static


class StatsScreen(Screen):
    """Progress statistics screen — shows per-topic and per-mode stats."""

    BINDINGS = [
        ("r", "reset_progress", "Сбросить прогресс"),
        ("escape", "back", "Назад"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Static(id="flashcard-screen"):
            with Static(id="stats-container"):
                yield Label("Статистика прогресса", classes="card-title")
                yield Label("", id="stats-summary")
                yield DataTable(id="stats-table")
                with Static(id="flashcard-controls"):
                    yield Button("🗑  Сбросить прогресс [R]", id="btn-reset", variant="error")
                    yield Button("← Назад", id="btn-back", variant="default")

    def on_mount(self) -> None:
        self._build_table()

    def _build_table(self) -> None:
        progress = self.app.progress
        questions = self.app.questions

        table = self.query_one("#stats-table", DataTable)
        table.clear(columns=True)
        table.add_columns("Раздел", "Всего", "Просмотрено", "Правильно", "Точность %")

        sections = {
            "📚 Теория": questions.get("theory", []),
            "✅ Квиз": questions.get("quiz", []),
            "💻 Кодинг": questions.get("coding", []),
        }

        total_all = 0
        seen_all = 0
        correct_all = 0

        for section_name, items in sections.items():
            total = len(items)
            seen = sum(1 for item in items if item.id in progress and progress[item.id].seen > 0)
            correct = sum(
                progress[item.id].correct for item in items if item.id in progress
            )
            total_attempts = sum(
                progress[item.id].seen for item in items if item.id in progress
            )
            accuracy = round(correct / total_attempts * 100, 1) if total_attempts > 0 else 0.0

            table.add_row(section_name, str(total), str(seen), str(correct), f"{accuracy}%")

            total_all += total
            seen_all += seen
            correct_all += correct

        table.add_row("─" * 12, "─" * 6, "─" * 12, "─" * 10, "─" * 10)

        total_attempts_all = sum(p.seen for p in progress.values())
        correct_attempts_all = sum(p.correct for p in progress.values())
        overall_accuracy = (
            round(correct_attempts_all / total_attempts_all * 100, 1)
            if total_attempts_all > 0
            else 0.0
        )
        table.add_row(
            "ИТОГО",
            str(total_all),
            str(seen_all),
            str(correct_attempts_all),
            f"{overall_accuracy}%",
        )

        topics: dict[str, dict[str, int]] = defaultdict(lambda: {"seen": 0, "correct": 0, "total": 0})
        for category in questions.values():
            for item in category:
                topics[item.topic]["total"] += 1
                if item.id in progress:
                    topics[item.topic]["seen"] += progress[item.id].seen
                    topics[item.topic]["correct"] += progress[item.id].correct

        weakest = sorted(
            topics.items(),
            key=lambda x: x[1]["correct"] / max(x[1]["seen"], 1),
        )

        weak_str = " | ".join(
            f"{t} ({d['correct']}/{d['seen']})" for t, d in weakest[:3] if d["seen"] > 0
        )
        summary = f"Всего карточек: {total_all} | Активных сессий: {total_attempts_all}"
        if weak_str:
            summary += f"\nСлабые темы: {weak_str}"
        self.query_one("#stats-summary", Label).update(summary)

    def action_reset_progress(self) -> None:
        self.app.progress.clear()
        from trainer.storage import save_progress
        save_progress(self.app.progress)
        self._build_table()

    def action_back(self) -> None:
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-reset":
            self.action_reset_progress()
        elif event.button.id == "btn-back":
            self.action_back()
