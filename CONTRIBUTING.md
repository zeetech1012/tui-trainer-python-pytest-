# Как добавить вопросы и статьи

## Добавить вопрос в базу

Все вопросы хранятся в `data/questions.json`. Файл содержит три секции: `theory`, `quiz`, `coding`.

### Теория (флэшкарточка)

```json
{
  "id": "theory_unique_id",
  "topic": "pytest",
  "difficulty": "medium",
  "priority": 1,
  "question": "Что такое фикстура в pytest?",
  "answer": "Фикстура — функция с декоратором @pytest.fixture...",
  "qa_context": "В API-тестах фикстуры используются для...",
  "tags": ["pytest", "fixtures"]
}
```

**Допустимые значения:**
- `topic`: `list`, `dict`, `set`, `comprehensions`, `strings`, `functions`, `oop`, `pytest`, `api_testing`, `algorithms`, `decorators`, `async`, `generators`
- `difficulty`: `easy`, `medium`, `hard`
- `priority`: `1` (must know), `2` (important), `3` (advanced)

### Квиз (мультичойс)

```json
{
  "id": "quiz_unique_id",
  "topic": "oop",
  "difficulty": "medium",
  "priority": 2,
  "question": "Что делает super().__init__()?",
  "options": [
    "Создаёт новый объект",
    "Вызывает __init__ родительского класса",
    "Удаляет объект",
    "Возвращает None"
  ],
  "correct": 1,
  "explanation": "super().__init__() вызывает конструктор родителя...",
  "qa_context": "В Page Object Model super().__init__() используется..."
}
```

`correct` — индекс правильного варианта (0-based).

### Кодинг (задача)

```json
{
  "id": "coding_unique_id",
  "topic": "comprehensions",
  "difficulty": "medium",
  "priority": 1,
  "title": "Фильтр активных пользователей",
  "description": "Напиши функцию, которая принимает список пользователей...",
  "starter_code": "def get_active_users(users: list[dict]) -> list[dict]:\n    pass",
  "hint": "Используй list comprehension с условием",
  "solution": "def get_active_users(users: list[dict]) -> list[dict]:\n    return [u for u in users if u.get('is_active')]",
  "qa_context": "В тестах такие функции используются для фильтрации..."
}
```

---

## Добавить статью в Wiki

1. Создай `.md` файл в нужной папке:
   ```
   wiki/
   ├── 01_basics/
   ├── 02_collections/
   ├── 03_oop/
   ├── 04_pytest/
   └── 05_api_testing/
   ```

2. Используй шаблон статьи:
   ```markdown
   # Название темы

   > **Зачем автотестеру:** ...

   ## Концепция
   ...

   ## Базовый синтаксис
   ...

   ## Как это выглядит в pytest
   ...

   ## Edge-кейсы
   ...

   ## Вопрос на собесе
   **Q: ...**
   > Ответ...
   ```

3. Зарегистрируй статью в `trainer/screens/wiki.py` в списке `WIKI_STRUCTURE`:
   ```python
   ("my_article", "04_pytest/my_article.md", "Название статьи"),
   ```

---

## Запуск и проверка

```bash
# Установить зависимости
pip install -r requirements.txt

# Запустить тренажёр
python3 -m trainer

# Проверить что все файлы Wiki существуют
python3 -c "
from trainer.screens.wiki import ALL_ARTICLES, WIKI_ROOT
missing = [fp for _, fp, _, _ in ALL_ARTICLES if not (WIKI_ROOT / fp).exists()]
print('Missing:', missing or 'None')
"
```
