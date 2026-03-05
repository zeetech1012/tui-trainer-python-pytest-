# 🧪 Python QA Interview Trainer

> Интерактивный тренажёр для подготовки к live coding собеседованиям на позицию **Python QA Automation Engineer** (middle уровень).
> Фокус: **WB / Ozon / X5 / Яндекс**. Цель: уверенно пройти технический экран за 295k+ в Москве.

---

## Что внутри

| Модуль | Описание |
|--------|----------|
| 📚 **Флэшкарточки** | 73 карточки по теории — вопрос → ответ → QA-контекст |
| ✅ **Квиз** | 42 вопроса с мультичойсом и объяснением |
| 💻 **Кодинг** | 40 задач как на реальном собесе с подсказками и решением |
| 📖 **Wiki** | 20 статей-справочников: от базового Python до API-тестирования |
| 📊 **Статистика** | Прогресс по темам, точность, слабые места |

---

## Скриншоты

```
 ____  _  _  ____  _  _  ____  ____
(  _ \( \/ )(_  _)( \/ )(  _ \( ___)
 )___/ \  /  _)(_  )  (  )___/ )__)
(__)   (__) (____)(_/\_)(__)   (____)
  Python Interview Trainer  v1.0

  📚  Флэшкарточки (теория)
  ✅  Квиз (мультичойс)
  💻  Задачи (кодинг)
  🎯  По теме (фильтр)
  📖  Wiki — справочник
  📊  Статистика прогресса
```

---

## Быстрый старт

### Требования

- Python 3.9+
- macOS / Linux / Windows

### Установка

```bash
git clone git@github.com:zeetech1012/tui-trainer-python-pytest-.git
cd tui-trainer-python-pytest-

# Создать виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt
```

### Запуск

```bash
# Вариант 1 — через скрипт
./run.sh

# Вариант 2 — напрямую
python3 -m trainer
```

---

## Wiki — справочник

Статьи написаны в формате Metanit: концепция → синтаксис → **как это выглядит в pytest** → edge-кейсы → вопрос на собесе.

```
wiki/
├── 01_basics/
│   ├── functions.md        — def, *args/**kwargs, type hints, lambda
│   ├── strings.md          — методы, f-strings, split/strip/join
│   └── control_flow.md     — if/else, циклы, try/except
├── 02_collections/
│   ├── lists.md            — методы, sort, срезы, copy
│   ├── dicts.md            — методы, вложенные словари, merge
│   ├── sets_tuples.md      — операции над множествами, namedtuple
│   └── comprehensions.md   — list/dict/set comprehensions, generators
├── 03_oop/
│   ├── classes.md          — class, __init__, @classmethod, dataclass
│   ├── inheritance.md      — super(), MRO, Page Object Model
│   ├── encapsulation.md    — @property, private attrs, API-клиент
│   ├── polymorphism.md     — duck typing, ABC, @abstractmethod
│   └── magic_methods.md    — __str__, __eq__, __len__, __enter__
├── 04_pytest/
│   ├── basics.md           — assert, conftest.py, pytest.ini
│   ├── fixtures.md         — scope, yield, autouse
│   ├── parametrize.md      — @pytest.mark.parametrize, ids
│   ├── mocking.md          — MagicMock, patch, monkeypatch, responses
│   └── markers.md          — skip, xfail, кастомные маркеры
└── 05_api_testing/
    ├── requests_basics.md  — GET/POST/PUT/DELETE, Session, timeout
    ├── assertions.md       — статус, схема, jsonschema, Pydantic
    └── mock_api.md         — responses, respx, pytest-mock
```

Статьи читаются прямо в TUI (кнопка **📖 Wiki**) или в любом Markdown-редакторе.

---

## Управление в TUI

### Главное меню
| Кнопка | Действие |
|--------|----------|
| `📚 Флэшкарточки` | Режим карточек |
| `✅ Квиз` | Мультичойс |
| `💻 Задачи` | Кодинг |
| `🎯 По теме` | Фильтр по топику |
| `📖 Wiki` | Справочник |
| `📊 Статистика` | Прогресс |

### Флэшкарточки
| Клавиша | Действие |
|---------|----------|
| `Space` | Показать ответ |
| `K` | Знаю ✓ |
| `N` | Не знаю ✗ |
| `T` | Подсказка на собесе |
| `Q` | QA-контекст |
| `←` / `→` | Предыдущая / следующая |
| `Esc` | Назад |

### Wiki
| Клавиша | Действие |
|---------|----------|
| `J` / `K` | Скролл вниз / вверх |
| `N` / `P` | Следующая / предыдущая статья |
| `M` | Меню Wiki |
| `Esc` | Назад |

---

## Темы

Вопросы расставлены по приоритетам:

| Приоритет | Темы |
|-----------|------|
| 🔥 **P1 — Must Know** | list, dict, set, comprehensions, strings, errors, functions |
| ⭐ **P2 — Important** | ООП, pytest, API testing, algorithms, generators |
| 💡 **P3 — Advanced** | decorators, async, collections, functools, typing |

---

## Стек

| Технология | Версия | Зачем |
|------------|--------|-------|
| Python | 3.9+ | основной язык |
| [Textual](https://github.com/Textualize/textual) | ≥0.50 | TUI-фреймворк |
| [Rich](https://github.com/Textualize/rich) | ≥13.7 | форматирование в терминале |

---

## Структура проекта

```
.
├── trainer/                  # TUI-приложение
│   ├── main.py               # точка входа, TrainerApp
│   ├── models.py             # TheoryCard, CodingTask, QuizQuestion
│   ├── storage.py            # JSON I/O (questions, progress)
│   ├── app.tcss              # стили Textual
│   └── screens/
│       ├── menu.py           # главное меню
│       ├── flashcards.py     # режим флэшкарт
│       ├── quiz.py           # режим квиза
│       ├── coding.py         # режим кодинга
│       ├── wiki.py           # Wiki-браузер
│       ├── stats.py          # статистика
│       └── topic_filter.py   # фильтр по темам
├── wiki/                     # 20 Markdown-статей
├── data/
│   └── questions.json        # база вопросов (155 шт.)
├── .cursorrules              # AI-правила для Cursor IDE
├── requirements.txt
└── run.sh
```

---

## Лицензия

MIT — используй свободно для личной подготовки.
