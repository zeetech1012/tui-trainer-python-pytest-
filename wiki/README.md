# Python Wiki для QA-автотестера

> Справочник в стиле Metanit — каждая статья объясняет концепцию, показывает её в коде и демонстрирует, как она применяется в реальных pytest-тестах.

---

## Как пользоваться

Каждая статья строится по единому шаблону:
1. **Зачем знать автотестеру** — контекст применения
2. **Концепция** — объяснение простым языком
3. **Синтаксис и примеры** — минимальный рабочий код
4. **Применение в pytest** — реальный тест с данной концепцией
5. **Edge-кейсы** — что ломается и как защититься
6. **Вопрос на собесе** — типичная формулировка + короткий ответ

---

## 01. Основы Python

| Статья | Темы |
|--------|------|
| [Функции](01_basics/functions.md) | def, аргументы, `*args`, `**kwargs`, type hints, lambda |
| [Строки](01_basics/strings.md) | методы строк, f-strings, `split` / `strip` / `join`, срезы |
| [Управление потоком](01_basics/control_flow.md) | `if/elif/else`, циклы `for/while`, `try/except/finally` |

---

## 02. Коллекции

| Статья | Темы |
|--------|------|
| [Списки (list)](02_collections/lists.md) | методы, срезы, сортировка, `copy`, `sort` vs `sorted` |
| [Словари (dict)](02_collections/dicts.md) | методы, вложенные словари, `get`, `setdefault`, merge |
| [Множества и кортежи](02_collections/sets_tuples.md) | `set`, `frozenset`, `tuple`, операции над множествами |
| [Comprehensions](02_collections/comprehensions.md) | list / dict / set comprehensions, генераторы, `yield` |

---

## 03. ООП — Объектно-ориентированное программирование

| Статья | Темы |
|--------|------|
| [Классы](03_oop/classes.md) | `class`, `__init__`, `self`, атрибуты класса и экземпляра |
| [Наследование](03_oop/inheritance.md) | `super()`, MRO, Page Object паттерн |
| [Инкапсуляция](03_oop/encapsulation.md) | `@property`, `private` / `protected`, геттеры и сеттеры |
| [Полиморфизм](03_oop/polymorphism.md) | duck typing, переопределение методов, абстрактные классы |
| [Магические методы](03_oop/magic_methods.md) | `__str__`, `__eq__`, `__len__`, `__repr__`, `__contains__` |

---

## 04. Pytest

| Статья | Темы |
|--------|------|
| [Основы pytest](04_pytest/basics.md) | `assert`, структура теста, запуск, именование |
| [Фикстуры](04_pytest/fixtures.md) | `@pytest.fixture`, scope, `yield`, `conftest.py` |
| [Параметризация](04_pytest/parametrize.md) | `@pytest.mark.parametrize`, комбинации, ids |
| [Моки](04_pytest/mocking.md) | `unittest.mock`, `MagicMock`, `patch`, `monkeypatch` |
| [Маркеры](04_pytest/markers.md) | `skip`, `xfail`, `slow`, кастомные маркеры, `pytest.ini` |

---

## 05. API-тестирование

| Статья | Темы |
|--------|------|
| [Requests — основы](05_api_testing/requests_basics.md) | `GET/POST/PUT/DELETE`, headers, JSON, session |
| [Assertions для API](05_api_testing/assertions.md) | статус-коды, схема JSON, время ответа, `jsonschema` |
| [Моки для API](05_api_testing/mock_api.md) | `responses`, `httpretty`, `pytest-mock`, `respx` |

---

## Необходимые библиотеки

```bash
pip install pytest pytest-mock requests responses jsonschema pydantic httpx respx
```

| Библиотека | Зачем |
|------------|-------|
| `pytest` | основной фреймворк для тестов |
| `pytest-mock` | удобная обёртка над `unittest.mock` |
| `requests` | HTTP-клиент для API-тестов |
| `responses` | мокирование requests без реальных запросов |
| `jsonschema` | валидация JSON-ответов по схеме |
| `pydantic` | валидация данных через модели |
| `httpx` | async HTTP-клиент |
| `respx` | мокирование httpx |
