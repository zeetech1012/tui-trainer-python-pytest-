from __future__ import annotations

from pathlib import Path

from textual.app import App

from trainer.screens.menu import MenuScreen
from trainer.screens.flashcards import FlashcardScreen
from trainer.screens.quiz import QuizScreen
from trainer.screens.coding import CodingScreen
from trainer.screens.stats import StatsScreen
from trainer.storage import load_questions, load_progress, save_progress


class TrainerApp(App):
    """Python Interview Trainer — TUI study app."""

    CSS_PATH = Path(__file__).parent / "app.tcss"

    SCREENS = {
        "menu": MenuScreen,
        "flashcards": FlashcardScreen,
        "quiz": QuizScreen,
        "coding": CodingScreen,
        "stats": StatsScreen,
    }

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.questions = load_questions()
        self.progress = load_progress()
        self.push_screen("menu")

    def on_unmount(self) -> None:
        save_progress(self.progress)


def main() -> None:
    app = TrainerApp()
    app.run()


if __name__ == "__main__":
    main()
