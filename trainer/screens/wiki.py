from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Markdown, Static
from textual.containers import ScrollableContainer


WIKI_ROOT = Path(__file__).parent.parent.parent / "wiki"

# Структура ВИКИ: (id_раздела, заголовок, иконка, [(id_статьи, название_файла, заголовок)])
WIKI_STRUCTURE: list[tuple[str, str, str, list[tuple[str, str, str]]]] = [
    (
        "basics",
        "Основы Python",
        "🐍",
        [
            ("functions", "01_basics/functions.md", "Функции"),
            ("strings", "01_basics/strings.md", "Строки"),
            ("control_flow", "01_basics/control_flow.md", "Управление потоком"),
        ],
    ),
    (
        "collections",
        "Коллекции",
        "📦",
        [
            ("lists", "02_collections/lists.md", "Списки (list)"),
            ("dicts", "02_collections/dicts.md", "Словари (dict)"),
            ("sets_tuples", "02_collections/sets_tuples.md", "Множества и кортежи"),
            ("comprehensions", "02_collections/comprehensions.md", "Comprehensions"),
        ],
    ),
    (
        "oop",
        "ООП",
        "🏗️",
        [
            ("classes", "03_oop/classes.md", "Классы"),
            ("inheritance", "03_oop/inheritance.md", "Наследование"),
            ("encapsulation", "03_oop/encapsulation.md", "Инкапсуляция"),
            ("polymorphism", "03_oop/polymorphism.md", "Полиморфизм"),
            ("magic_methods", "03_oop/magic_methods.md", "Магические методы"),
        ],
    ),
    (
        "pytest_section",
        "Pytest",
        "🧪",
        [
            ("pytest_basics", "04_pytest/basics.md", "Основы pytest"),
            ("fixtures", "04_pytest/fixtures.md", "Фикстуры"),
            ("parametrize", "04_pytest/parametrize.md", "Параметризация"),
            ("mocking", "04_pytest/mocking.md", "Моки"),
            ("markers", "04_pytest/markers.md", "Маркеры"),
        ],
    ),
    (
        "api_testing",
        "API-тестирование",
        "🌐",
        [
            ("requests_basics", "05_api_testing/requests_basics.md", "Requests — основы"),
            ("assertions", "05_api_testing/assertions.md", "Assertions для API"),
            ("mock_api", "05_api_testing/mock_api.md", "Моки для API"),
        ],
    ),
]

# Плоский список всех статей для навигации
ALL_ARTICLES: list[tuple[str, str, str, str]] = [
    (article_id, filepath, title, section_title)
    for _sec_id, section_title, _icon, articles in WIKI_STRUCTURE
    for article_id, filepath, title in articles
]


class WikiMenuScreen(Screen):
    """Оглавление ВИКИ — выбор раздела и статьи."""

    BINDINGS = [
        ("escape", "back", "← Назад"),
        ("j", "scroll_down", "↓"),
        ("k", "scroll_up", "↑"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with ScrollableContainer(id="wiki-menu-container"):
            yield Label("📖  Python Wiki для QA-автотестера", id="wiki-menu-title")
            yield Label(
                "Выбери статью нажав на кнопку. Клавиша [Esc] — назад в меню.",
                id="wiki-menu-subtitle",
            )
            for sec_id, section_title, icon, articles in WIKI_STRUCTURE:
                yield Label(f"{icon}  {section_title}", classes="wiki-section-header")
                with Static(classes="wiki-section-list"):
                    for article_id, _filepath, title in articles:
                        yield Button(
                            f"  {title}",
                            id=f"wiki-article-{article_id}",
                            classes="wiki-article-btn",
                            variant="default",
                        )
            yield Static(id="wiki-menu-spacer")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id or ""
        if btn_id.startswith("wiki-article-"):
            article_id = btn_id.removeprefix("wiki-article-")
            for aid, filepath, title, section_title in ALL_ARTICLES:
                if aid == article_id:
                    self.app.push_screen(WikiArticleScreen(filepath, title, section_title))
                    return

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_scroll_down(self) -> None:
        self.query_one("#wiki-menu-container", ScrollableContainer).scroll_down()

    def action_scroll_up(self) -> None:
        self.query_one("#wiki-menu-container", ScrollableContainer).scroll_up()


class WikiArticleScreen(Screen):
    """Экран чтения статьи ВИКИ."""

    BINDINGS = [
        ("escape", "back", "← Назад"),
        ("j", "scroll_down", "↓ Вниз"),
        ("k", "scroll_up", "↑ Вверх"),
        ("n", "next_article", "→ След статья"),
        ("p", "prev_article", "← Пред статья"),
        ("m", "wiki_menu", "📖 Меню"),
    ]

    def __init__(self, filepath: str, title: str, section: str) -> None:
        super().__init__()
        self._filepath = filepath
        self._title = title
        self._section = section
        self._article_index = self._find_index()

    def _find_index(self) -> int:
        for i, (_, fp, _, _) in enumerate(ALL_ARTICLES):
            if fp == self._filepath:
                return i
        return 0

    def _load_content(self) -> str:
        path = WIKI_ROOT / self._filepath
        if path.exists():
            return path.read_text(encoding="utf-8")
        return f"# Статья не найдена\n\nФайл `{path}` не существует."

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Static(id="wiki-article-layout"):
            # Навигационная строка сверху
            with Static(id="wiki-article-nav"):
                yield Label(
                    f"📖 Wiki  ›  {self._section}  ›  {self._title}",
                    id="wiki-breadcrumb",
                )
                idx = self._article_index
                total = len(ALL_ARTICLES)
                yield Label(
                    f"[{idx + 1}/{total}]  [P] Пред  [N] След  [M] Меню  [Esc] Назад",
                    id="wiki-nav-hint",
                )
            # Основное содержимое
            with ScrollableContainer(id="wiki-article-scroll"):
                yield Markdown(self._load_content(), id="wiki-article-content")

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_wiki_menu(self) -> None:
        self.app.pop_screen()

    def action_scroll_down(self) -> None:
        self.query_one("#wiki-article-scroll", ScrollableContainer).scroll_down(animate=False)

    def action_scroll_up(self) -> None:
        self.query_one("#wiki-article-scroll", ScrollableContainer).scroll_up(animate=False)

    def action_next_article(self) -> None:
        next_idx = (self._article_index + 1) % len(ALL_ARTICLES)
        aid, fp, title, section = ALL_ARTICLES[next_idx]
        self.app.switch_screen(WikiArticleScreen(fp, title, section))

    def action_prev_article(self) -> None:
        prev_idx = (self._article_index - 1) % len(ALL_ARTICLES)
        aid, fp, title, section = ALL_ARTICLES[prev_idx]
        self.app.switch_screen(WikiArticleScreen(fp, title, section))
