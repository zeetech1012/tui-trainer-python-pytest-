# Subagent: Notion / Jira Sync

## Цель
Синхронизация контента тренажера с Notion и Jira: экспорт вопросов, импорт задач, создание тест-кейсов.

## Триггеры
- "Экспортируй вопросы в Notion"
- "Импортируй задачи из Notion в тренажер"
- "Создай Jira тикет для задачи [ID]"
- "Покажи мои Jira задачи"

---

## Notion: Экспорт вопросов

### Структура Notion базы данных
Создай базу данных "Python Interview Questions" со свойствами:
- `ID` (title)
- `Topic` (select)
- `Type` (select: theory/quiz/coding)
- `Difficulty` (select: easy/medium/hard)
- `Question` (rich_text)
- `Answer` (rich_text)
- `Status` (select: new/learning/mastered)

### Алгоритм экспорта
```python
import json

with open('data/questions.json') as f:
    data = json.load(f)

# Подготовить записи для Notion API
for q in data['theory']:
    notion_page = {
        "parent": {"database_id": "YOUR_DATABASE_ID"},
        "properties": {
            "ID": {"title": [{"text": {"content": q['id']}}]},
            "Topic": {"select": {"name": q['topic']}},
            "Type": {"select": {"name": "theory"}},
            "Difficulty": {"select": {"name": q['difficulty']}},
            "Question": {"rich_text": [{"text": {"content": q['question']}}]},
            "Answer": {"rich_text": [{"text": {"content": q['answer']}}]},
            "Status": {"select": {"name": "new"}}
        }
    }
    # Использовать Notion MCP: create_page
```

### Использование Notion MCP
Через MCP сервер `notion`:
1. `list_databases` — найти или создать базу данных
2. `create_page` — добавить вопрос
3. `update_page` — обновить статус (new → learning → mastered)
4. `query_database` — получить все вопросы для импорта

---

## Jira: Создание задач из вопросов

### Когда использовать
- Трекинг прогресса обучения через Jira Sprint
- Каждый раздел курса = Epic
- Каждая задача = Story/Task

### Структура Jira
```
Epic: "Python Interview Prep"
├── Story: "День 1: List Operations" (10 задач)
├── Story: "День 5: Comprehensions" (10 задач)
├── Story: "LeetCode Easy" (c013-c016)
└── Story: "API Testing" (c018-c019)
```

### Алгоритм через Jira MCP
```python
# Использовать MCP jira:
# 1. get_projects — найти проект
# 2. create_issue — создать задачу:
issue = {
    "project": {"key": "PYINT"},
    "summary": f"[{q['id']}] {q['topic']}: {q['description'][:50]}",
    "description": q['description'],
    "issuetype": {"name": "Task"},
    "labels": [q['topic'], q['difficulty'], "python-interview"],
    "priority": {"name": "Medium" if q['difficulty'] == 'medium' else "Low"}
}
```

---

## Импорт из Notion в questions.json

### Алгоритм
1. `query_database` — получить все страницы базы данных
2. Парсить свойства: id, topic, question, answer, difficulty
3. Создать Python объекты и добавить в questions.json
4. Проверить на дубликаты по ID

```python
def import_from_notion(pages: list[dict]) -> None:
    with open('data/questions.json') as f:
        data = json.load(f)
    
    existing_ids = {q['id'] for q in data['theory']}
    
    new_questions = []
    for page in pages:
        props = page['properties']
        q_id = props['ID']['title'][0]['text']['content']
        if q_id not in existing_ids:
            new_questions.append({
                "id": q_id,
                "topic": props['Topic']['select']['name'],
                "question": props['Question']['rich_text'][0]['text']['content'],
                "answer": props['Answer']['rich_text'][0]['text']['content'],
                "difficulty": props['Difficulty']['select']['name']
            })
    
    data['theory'].extend(new_questions)
    with open('data/questions.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Импортировано: {len(new_questions)} вопросов")
```

---

## Настройка (замени placeholders)
- Notion: `YOUR_NOTION_TOKEN` → Integration token из notion.so/my-integrations
- Notion: `YOUR_DATABASE_ID` → ID базы данных из URL
- Jira: `YOUR_SITE.atlassian.net` → твой Jira домен
- Jira: `YOUR_JIRA_API_TOKEN` → API token из id.atlassian.com
