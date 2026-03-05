# Assertions для API-тестов

> **Зачем автотестеру:** Правильные проверки API — это не просто `assert response.status_code == 200`. Нужно проверять структуру JSON, типы данных, схему ответа, время отклика. Это то, что отличает junior от middle QA.

---

## Концепция

Хорошая API-проверка охватывает несколько уровней:

1. **Транспортный** — статус-код, заголовки, время ответа
2. **Структурный** — наличие полей, типы данных
3. **Семантический** — бизнес-логика, корректность значений
4. **Схемный** — соответствие JSON-схеме или Pydantic-модели

---

## 1. Проверка статус-кодов

```python
import pytest
import requests

response = requests.get("https://api.example.com/users/1")

# Базовые проверки
assert response.status_code == 200
assert response.status_code == 201
assert response.status_code == 204

# Проверка диапазона
assert 200 <= response.status_code < 300, f"Expected 2xx, got {response.status_code}"

# Удобно использовать http.HTTPStatus
from http import HTTPStatus

assert response.status_code == HTTPStatus.OK
assert response.status_code == HTTPStatus.CREATED
assert response.status_code == HTTPStatus.NOT_FOUND

# Информативное сообщение при падении
assert response.status_code == 200, (
    f"Expected 200, got {response.status_code}. "
    f"URL: {response.url}. "
    f"Body: {response.text[:300]}"
)
```

---

## 2. Проверка заголовков

```python
# Content-Type
assert "application/json" in response.headers["Content-Type"]

# Кэширование
assert response.headers.get("Cache-Control") == "no-cache"

# Кастомные заголовки
assert "X-Request-ID" in response.headers

# Утилита для проверки заголовков
def assert_json_content_type(response: requests.Response) -> None:
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, (
        f"Expected JSON Content-Type, got: {content_type}"
    )
```

---

## 3. Проверка структуры JSON

```python
def test_user_response_structure(api_client):
    response = api_client.get("/users/1")
    assert response.status_code == 200
    data = response.json()

    # Проверка обязательных ключей
    required_keys = {"id", "name", "email", "created_at"}
    assert required_keys.issubset(data.keys()), (
        f"Missing keys: {required_keys - data.keys()}"
    )

    # Проверка типов
    assert isinstance(data["id"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["email"], str)
    assert isinstance(data["is_active"], bool)

    # Проверка значений
    assert data["id"] > 0
    assert len(data["name"]) > 0
    assert "@" in data["email"]
```

---

## 4. Валидация JSON-схемы через `jsonschema`

```bash
pip install jsonschema
```

```python
import jsonschema
import pytest

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "is_active"],
    "properties": {
        "id": {"type": "integer", "minimum": 1},
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "is_active": {"type": "boolean"},
        "created_at": {"type": "string"},
        "role": {"type": "string", "enum": ["admin", "user", "moderator"]},
    },
    "additionalProperties": False,
}

USERS_LIST_SCHEMA = {
    "type": "object",
    "required": ["items", "total", "page", "limit"],
    "properties": {
        "items": {
            "type": "array",
            "items": USER_SCHEMA,
        },
        "total": {"type": "integer", "minimum": 0},
        "page": {"type": "integer", "minimum": 1},
        "limit": {"type": "integer", "minimum": 1, "maximum": 100},
    },
}


def test_user_response_matches_schema(api_client):
    response = api_client.get("/users/1")
    assert response.status_code == 200
    try:
        jsonschema.validate(instance=response.json(), schema=USER_SCHEMA)
    except jsonschema.ValidationError as e:
        pytest.fail(f"Schema validation failed: {e.message}")


def test_users_list_matches_schema(api_client):
    response = api_client.get("/users")
    assert response.status_code == 200
    jsonschema.validate(instance=response.json(), schema=USERS_LIST_SCHEMA)
```

---

## 5. Валидация через Pydantic

```bash
pip install pydantic
```

```python
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
import pytest


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    role: str
    created_at: datetime

    @field_validator("role")
    @classmethod
    def role_must_be_valid(cls, v: str) -> str:
        valid_roles = {"admin", "user", "moderator"}
        if v not in valid_roles:
            raise ValueError(f"role must be one of {valid_roles}")
        return v


class UsersListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    limit: int


def test_user_response_is_valid(api_client):
    response = api_client.get("/users/1")
    assert response.status_code == 200

    # Pydantic бросит ValidationError если данные не соответствуют модели
    user = UserResponse(**response.json())
    assert user.id == 1
    assert user.is_active is True


def test_users_list_response_is_valid(api_client):
    response = api_client.get("/users?page=1&limit=10")
    assert response.status_code == 200
    data = UsersListResponse(**response.json())

    assert data.total >= 0
    assert 1 <= data.limit <= 100
    assert all(isinstance(u.id, int) for u in data.items)
```

---

## 6. Проверка времени ответа

```python
import pytest


def test_response_time_under_1s(api_client):
    response = api_client.get("/users")
    elapsed = response.elapsed.total_seconds()
    assert elapsed < 1.0, f"Too slow: {elapsed:.3f}s"


def test_response_time_under_500ms(api_client):
    response = api_client.get("/users/1")
    elapsed_ms = response.elapsed.total_seconds() * 1000
    assert elapsed_ms < 500, f"Expected < 500ms, got {elapsed_ms:.0f}ms"


# Декоратор для проверки производительности
import functools
import time


def assert_response_time(max_seconds: float):
    """Декоратор: проверяет время выполнения теста."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            assert elapsed < max_seconds, f"Test took {elapsed:.3f}s > {max_seconds}s"
            return result
        return wrapper
    return decorator


@assert_response_time(2.0)
def test_search_performance(api_client):
    response = api_client.get("/products/search", params={"q": "laptop"})
    assert response.status_code == 200
```

---

## 7. Вспомогательные функции-ассерты

```python
# helpers/assertions.py
import requests
import jsonschema


def assert_status(response: requests.Response, expected: int) -> None:
    assert response.status_code == expected, (
        f"Expected {expected}, got {response.status_code}.\n"
        f"URL: {response.url}\n"
        f"Body: {response.text[:500]}"
    )


def assert_json_schema(response: requests.Response, schema: dict) -> None:
    assert_status(response, 200)
    try:
        jsonschema.validate(response.json(), schema)
    except jsonschema.ValidationError as e:
        raise AssertionError(f"JSON schema validation failed: {e.message}")


def assert_response_time(response: requests.Response, max_seconds: float = 2.0) -> None:
    elapsed = response.elapsed.total_seconds()
    assert elapsed < max_seconds, (
        f"Response too slow: {elapsed:.3f}s > {max_seconds}s. URL: {response.url}"
    )


def assert_pagination(data: dict, expected_page: int, expected_limit: int) -> None:
    assert data["page"] == expected_page
    assert data["limit"] == expected_limit
    assert "total" in data
    assert len(data["items"]) <= expected_limit
```

---

## Полный тест с несколькими уровнями проверок

```python
import pytest
import requests
import jsonschema


ORDER_SCHEMA = {
    "type": "object",
    "required": ["id", "status", "total", "items", "created_at"],
    "properties": {
        "id": {"type": "integer"},
        "status": {"type": "string", "enum": ["pending", "paid", "shipped", "delivered", "cancelled"]},
        "total": {"type": "number", "minimum": 0},
        "items": {"type": "array", "minItems": 1},
        "created_at": {"type": "string"},
    },
}


def test_create_order_full_validation(api_client: requests.Session):
    payload = {"product_id": 1, "quantity": 2}

    response = api_client.post("https://api.example.com/orders", json=payload)

    # 1. Статус-код
    assert response.status_code == 201, f"Body: {response.text}"

    # 2. Content-Type
    assert "application/json" in response.headers["Content-Type"]

    # 3. Время ответа
    assert response.elapsed.total_seconds() < 2.0

    # 4. JSON-схема
    jsonschema.validate(response.json(), ORDER_SCHEMA)

    # 5. Бизнес-логика
    order = response.json()
    assert order["status"] == "pending"
    assert order["total"] > 0
    assert len(order["items"]) == 1
    assert order["items"][0]["quantity"] == 2
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| `response.json()` перед проверкой статуса | `JSONDecodeError` при HTML-ошибке от прокси | Сначала проверяй `status_code`, потом `.json()` |
| Слишком общая схема | `"type": "object"` без properties — любой объект пройдёт | Указывай `required` и `properties` |
| Проверка float == float | `0.1 + 0.2 != 0.3` | Используй `pytest.approx()` или округляй |
| Нет сообщения в assert | Непонятно что упало | Всегда добавляй f-string с деталями |

---

## Вопрос на собесе

**Q: Что нужно проверять в API-ответе помимо статус-кода?**

> Минимум: статус-код, Content-Type, структуру тела (наличие обязательных полей, типы данных), бизнес-логику (корректность значений). Дополнительно: время ответа, JSON-схему, заголовки безопасности.

**Q: jsonschema vs Pydantic — что выбрать для валидации?**

> `jsonschema` — стандарт, подходит для любого языка, схема описывается в JSON, удобно для проверки контракта API. `Pydantic` — Python-специфичный, позволяет описывать схему в коде с type hints, удобно для сложных моделей с валидацией. В командах часто используют оба: Pydantic для модели, jsonschema для контракт-тестов.
