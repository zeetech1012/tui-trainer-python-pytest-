# Pytest — основы

> **Зачем автотестеру:** pytest — стандарт де-факто для тестирования Python-кода. Это основной инструмент работы QA-автотестера. Без глубокого понимания pytest невозможно пройти собеседование в WB, Ozon или Яндекс.

---

## Установка и запуск

```bash
pip install pytest

# Запуск всех тестов
pytest

# Запуск конкретного файла
pytest test_users.py

# Запуск конкретного теста
pytest test_users.py::test_create_user

# Запуск с выводом (verbose)
pytest -v

# Остановиться на первом падении
pytest -x

# Показать локальные переменные при падении
pytest -l

# Запуск тестов с определённым маркером
pytest -m smoke

# Показать print() в тестах
pytest -s
```

---

## Структура тестового файла

```python
# test_orders.py

# Соглашения:
# - Файл: test_*.py или *_test.py
# - Функция: test_*
# - Класс: Test* (без __init__)

def test_simple_assertion():
    assert 2 + 2 == 4


def test_string_contains():
    message = "Order created successfully"
    assert "created" in message


class TestOrderCalculation:
    """Группировка связанных тестов в класс."""

    def test_total_calculation(self):
        price = 100.0
        quantity = 3
        total = price * quantity
        assert total == 300.0

    def test_total_with_discount(self):
        price = 100.0
        discount = 0.1
        total = price * (1 - discount)
        assert total == 90.0
```

---

## Assert — проверки

pytest автоматически показывает подробную информацию о падении assert.

```python
# Базовые проверки
assert value == expected
assert value != unexpected
assert value > 0
assert value is None
assert value is not None

# Строки
assert "keyword" in response_text
assert response.startswith("OK")

# Коллекции
assert len(items) == 3
assert item in collection
assert list1 == list2

# Числа с допуском
import pytest
assert result == pytest.approx(3.14159, rel=1e-4)
assert 0.1 + 0.2 == pytest.approx(0.3)

# Исключения
with pytest.raises(ValueError):
    int("not a number")

with pytest.raises(ValueError, match="invalid literal"):
    int("abc")

# Исключение с проверкой атрибутов
with pytest.raises(HTTPError) as exc_info:
    raise_for_status_if_error(response)
assert exc_info.value.response.status_code == 404

# Пользовательское сообщение при провале
assert user["role"] == "admin", f"Expected admin, got: {user['role']}"
```

---

## conftest.py — общие фикстуры и конфигурация

```
project/
├── conftest.py          ← фикстуры доступны во всём проекте
├── tests/
│   ├── conftest.py      ← фикстуры для папки tests/
│   ├── test_users.py
│   └── api/
│       ├── conftest.py  ← фикстуры для папки api/
│       └── test_orders.py
```

```python
# conftest.py
import pytest
import requests


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://api.example.com"


@pytest.fixture(scope="session")
def admin_token(base_url: str) -> str:
    response = requests.post(
        f"{base_url}/auth/login",
        json={"username": "admin", "password": "secret"},
    )
    return response.json()["token"]


@pytest.fixture
def api_client(base_url: str, admin_token: str) -> requests.Session:
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {admin_token}"
    session.headers["Content-Type"] = "application/json"
    return session
```

---

## Именование тестов

```python
# Паттерн: test_<функция>_<сценарий>

def test_create_user_success():
    ...

def test_create_user_duplicate_email_returns_409():
    ...

def test_get_user_not_found_returns_404():
    ...

def test_update_user_invalid_age_raises_value_error():
    ...

def test_delete_user_removes_from_database():
    ...
```

---

## pytest.ini / pyproject.toml — конфигурация

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    smoke: Быстрые проверки основной функциональности
    regression: Полная регрессия
    slow: Медленные тесты (>5 сек)
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
markers = [
    "smoke: быстрые тесты",
    "slow: медленные тесты",
]
```

---

## Структура реального тест-файла

```python
"""Тесты для API пользователей."""
import pytest
import requests


BASE_URL = "https://api.example.com"


@pytest.fixture
def new_user_payload() -> dict:
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "SecurePass123",
    }


@pytest.fixture
def created_user(api_client: requests.Session, new_user_payload: dict) -> dict:
    """Создаёт пользователя и удаляет после теста."""
    response = api_client.post(f"{BASE_URL}/users", json=new_user_payload)
    user = response.json()
    yield user
    # teardown — удаление после теста
    api_client.delete(f"{BASE_URL}/users/{user['id']}")


class TestCreateUser:
    def test_returns_201(self, api_client, new_user_payload):
        response = api_client.post(f"{BASE_URL}/users", json=new_user_payload)
        assert response.status_code == 201

    def test_returns_user_id(self, api_client, new_user_payload):
        response = api_client.post(f"{BASE_URL}/users", json=new_user_payload)
        assert "id" in response.json()

    def test_duplicate_email_returns_409(self, api_client, created_user, new_user_payload):
        response = api_client.post(f"{BASE_URL}/users", json=new_user_payload)
        assert response.status_code == 409


class TestGetUser:
    def test_returns_200_for_existing_user(self, api_client, created_user):
        user_id = created_user["id"]
        response = api_client.get(f"{BASE_URL}/users/{user_id}")
        assert response.status_code == 200

    def test_returns_404_for_missing_user(self, api_client):
        response = api_client.get(f"{BASE_URL}/users/999999")
        assert response.status_code == 404
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| `assert func()` | Функция возвращает None — всегда падает | Присвой результат переменной |
| `assert a == b` с float | `0.1 + 0.2 != 0.3` из-за IEEE 754 | Используй `pytest.approx()` |
| Один тест — несколько assert | Сложно понять где упало | Предпочитай один assert на тест |
| Тест зависит от другого теста | Хрупкая связность | Каждый тест должен быть независим |

---

## Вопрос на собесе

**Q: В чём отличие pytest от unittest?**

> pytest использует обычные функции и `assert` вместо методов класса и `self.assertEqual()`. pytest автоматически ищет тесты, обеспечивает детальный вывод при падении, имеет богатую экосистему плагинов. `unittest` встроен в stdlib и использует ООП-подход.

**Q: Как запустить только smoke-тесты?**

> Пометить тесты декоратором `@pytest.mark.smoke`, зарегистрировать маркер в `pytest.ini`, запустить `pytest -m smoke`.
