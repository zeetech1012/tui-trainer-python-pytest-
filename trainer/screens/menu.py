from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static

from trainer.screens.topic_filter import TopicFilterScreen
from trainer.screens.wiki import WikiMenuScreen


LOGO = r"""
 ____  _  _  ____  _  _  ____  ____
(  _ \( \/ )(_  _)( \/ )(  _ \( ___)
 )___/ \  /  _)(_  )  (  )___/ )__)
(__)   (__) (____)(_/\_)(__)   (____)
  Python Interview Trainer  v1.0
"""

STATS_LINE = "73 теория  |  42 квиз  |  40 кодинг  |  QA-контекст [Q]  |  P1→P2→P3"


class MenuScreen(Screen):
    """Main menu — choose training mode."""

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Static(id="menu-container"):
            yield Static(LOGO, id="logo")
            yield Label(STATS_LINE, id="menu-title")
            with Static(id="menu-list"):
                yield Button("📚  Флэшкарточки (теория)", id="btn-flashcards", classes="menu-btn", variant="primary")
                yield Button("✅  Квиз (мультичойс)", id="btn-quiz", classes="menu-btn", variant="success")
                yield Button("💻  Задачи (кодинг)", id="btn-coding", classes="menu-btn", variant="warning")
                yield Button("🎯  По теме (фильтр)", id="btn-filter", classes="menu-btn", variant="primary")
                yield Button("📖  Wiki — справочник", id="btn-wiki", classes="menu-btn", variant="default")
                yield Button("📊  Статистика прогресса", id="btn-stats", classes="menu-btn", variant="default")
                yield Button("❌  Выйти", id="btn-quit", classes="menu-btn", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "btn-flashcards":
            self.app.push_screen("flashcards")
        elif button_id == "btn-quiz":
            self.app.push_screen("quiz")
        elif button_id == "btn-coding":
            self.app.push_screen("coding")
        elif button_id == "btn-filter":
            self.app.push_screen(
                TopicFilterScreen("flashcards", self._start_filtered_flashcards)
            )
        elif button_id == "btn-wiki":
            self.app.push_screen(WikiMenuScreen())
        elif button_id == "btn-stats":
            self.app.push_screen("stats")
        elif button_id == "btn-quit":
            self.app.exit()

    def _start_filtered_flashcards(self, topics: list[str]) -> None:
        from trainer.screens.flashcards import FlashcardScreen
        screen = FlashcardScreen(topic_filter=topics)
        self.app.push_screen(screen)

    def action_quit(self) -> None:
        self.app.exit()
