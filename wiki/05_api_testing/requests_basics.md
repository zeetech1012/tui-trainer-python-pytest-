# API-тестирование: библиотека requests

> **Зачем автотестеру:** `requests` — стандартная библиотека для HTTP-запросов в Python. Именно её используют в большинстве QA-команд на WB, Ozon, X5. Знание GET/POST/PUT/DELETE, сессий, заголовков и обработки ошибок — базовое требование.

---

## Установка

```bash
pip install requests
```

---

## Базовые HTTP-методы

### GET — получение данных

```python
import requests

# Простой GET
response = requests.get("https://api.example.com/users")

# С параметрами запроса (?page=1&limit=10)
response = requests.get(
    "https://api.example.com/users",
    params={"page": 1, "limit": 10, "status": "active"},
)

# С заголовками
response = requests.get(
    "https://api.example.com/users/1",
    headers={"Authorization": "Bearer token123"},
)

print(response.status_code)    # 200
print(response.json())         # словарь из JSON-ответа
print(response.text)           # строка
print(response.headers)        # заголовки ответа
print(response.elapsed)        # время ответа
```

### POST — создание ресурса

```python
# JSON-тело (автоматически Content-Type: application/json)
response = requests.post(
    "https://api.example.com/users",
    json={"name": "Alice", "email": "alice@example.com"},
    headers={"Authorization": "Bearer token123"},
)

# Form data (application/x-www-form-urlencoded)
response = requests.post(
    "https://api.example.com/auth/login",
    data={"username": "admin", "password": "secret"},
)

# Multipart (загрузка файла)
with open("report.csv", "rb") as f:
    response = requests.post(
        "https://api.example.com/upload",
        files={"file": ("report.csv", f, "text/csv")},
    )
```

### PUT и PATCH — обновление

```python
# PUT — полное обновление ресурса
response = requests.put(
    "https://api.example.com/users/1",
    json={"name": "Alice Updated", "email": "alice@example.com", "age": 31},
    headers={"Authorization": "Bearer token123"},
)

# PATCH — частичное обновление
response = requests.patch(
    "https://api.example.com/users/1",
    json={"name": "Alice Updated"},
    headers={"Authorization": "Bearer token123"},
)
```

### DELETE — удаление

```python
response = requests.delete(
    "https://api.example.com/users/1",
    headers={"Authorization": "Bearer token123"},
)

print(response.status_code)   # 204 No Content
```

---

## Session — сессия с общими настройками

`Session` сохраняет заголовки, куки и настройки между запросами. Эффективнее для множества запросов (одно TCP-соединение).

```python
import requests


session = requests.Session()

# Настроить общие заголовки один раз
session.headers.update({
    "Authorization": "Bearer token123",
    "Content-Type": "application/json",
    "X-Client-Version": "2.0",
})

# Настроить общий базовый URL (через адаптер) или просто prefix
BASE_URL = "https://api.example.com"

# Использование
users = session.get(f"{BASE_URL}/users").json()
order = session.post(f"{BASE_URL}/orders", json={"product_id": 5}).json()

# Всегда закрывай сессию
session.close()

# Лучше через контекстный менеджер
with requests.Session() as session:
    session.headers["Authorization"] = "Bearer token"
    response = session.get(f"{BASE_URL}/users")
```

---

## Обработка ответов

```python
response = requests.get("https://api.example.com/users/1")

# Статус-код
response.status_code          # 200
response.ok                   # True если 200-299

# Автоматически поднять исключение при 4xx/5xx
response.raise_for_status()   # HTTPError если ошибка

# Тело ответа
response.json()               # dict/list (если Content-Type: application/json)
response.text                 # строка
response.content              # bytes

# Заголовки
response.headers["Content-Type"]
response.headers.get("X-RateLimit-Remaining", "unknown")

# Время ответа
response.elapsed.total_seconds()   # float (секунды)

# URL после редиректов
response.url
response.history   # список редиректов
```

---

## Обработка ошибок

```python
from requests.exceptions import (
    ConnectionError,
    Timeout,
    HTTPError,
    RequestException,
)


def safe_get_user(user_id: int) -> dict | None:
    try:
        response = requests.get(
            f"https://api.example.com/users/{user_id}",
            timeout=5,  # максимальное время ожидания
        )
        response.raise_for_status()
        return response.json()
    except Timeout:
        print(f"Request timed out for user {user_id}")
        return None
    except HTTPError as e:
        print(f"HTTP Error {e.response.status_code}: {e}")
        return None
    except ConnectionError:
        print("Could not connect to API")
        return None
    except RequestException as e:
        print(f"Unexpected error: {e}")
        return None
```

---

## Аутентификация

```python
# Bearer Token (JWT)
headers = {"Authorization": f"Bearer {token}"}

# Basic Auth
from requests.auth import HTTPBasicAuth
response = requests.get(url, auth=HTTPBasicAuth("user", "pass"))
# или коротко:
response = requests.get(url, auth=("user", "pass"))

# API Key в заголовке
headers = {"X-API-Key": "your-api-key"}

# API Key в параметрах
params = {"api_key": "your-api-key"}
```

---

## Как это выглядит в pytest

```python
# conftest.py
import pytest
import requests


BASE_URL = "https://api.example.com"


@pytest.fixture(scope="session")
def auth_token() -> str:
    """Получить токен один раз для всей сессии тестов."""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "test_admin",
        "password": "Test@123",
    })
    assert response.status_code == 200, f"Auth failed: {response.text}"
    return response.json()["access_token"]


@pytest.fixture
def api(auth_token: str) -> requests.Session:
    """Настроенная сессия для каждого теста."""
    with requests.Session() as session:
        session.headers.update({
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        })
        session.base_url = BASE_URL  # type: ignore
        yield session
```

```python
# test_users_api.py
import pytest
import requests


def test_get_users_list(api: requests.Session):
    response = api.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)


def test_create_user_returns_id(api: requests.Session):
    payload = {"name": "Test User", "email": "test@example.com"}
    response = api.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert "id" in created
    assert created["name"] == payload["name"]


def test_get_nonexistent_user(api: requests.Session):
    response = api.get(f"{BASE_URL}/users/999999")
    assert response.status_code == 404
    assert "error" in response.json() or "message" in response.json()


def test_response_time_acceptable(api: requests.Session):
    response = api.get(f"{BASE_URL}/users")
    elapsed = response.elapsed.total_seconds()
    assert elapsed < 2.0, f"Response too slow: {elapsed:.2f}s"


@pytest.mark.parametrize("method,path", [
    ("GET", "/users"),
    ("POST", "/users"),
    ("GET", "/orders"),
])
def test_requires_auth(method: str, path: str):
    """Без токена должен вернуть 401."""
    response = requests.request(method, f"{BASE_URL}{path}")
    assert response.status_code == 401
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| Нет `timeout` | Тест висит вечно при недоступном сервисе | Всегда указывай `timeout=(connect_timeout, read_timeout)` |
| `response.json()` при ошибке | `JSONDecodeError` если тело не JSON | Проверяй `Content-Type` или оборачивай в try/except |
| Нет `raise_for_status()` | Тест проходит при 500 если не проверять статус | Всегда вызывай или явно проверяй `status_code` |
| Утечка соединений | Сессия не закрыта | Используй `with requests.Session()` |

---

## Вопрос на собесе

**Q: В чём разница между `requests.get()` и `Session.get()`?**

> `requests.get()` создаёт новое соединение при каждом вызове. `Session.get()` переиспользует TCP-соединение и сохраняет куки и заголовки между запросами. В тестах лучше использовать `Session` — быстрее и удобнее для авторизованных запросов.

**Q: Как передать query-параметры в GET-запрос?**

> Через аргумент `params=` — dict автоматически кодируется в URL: `requests.get(url, params={"page": 1, "limit": 10})` → `url?page=1&limit=10`.
