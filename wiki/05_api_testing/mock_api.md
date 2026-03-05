# Моки для API

> **Зачем автотестеру:** Реальные HTTP-запросы в юнит-тестах делают их медленными, нестабильными и зависимыми от внешних сервисов. Моки API позволяют тестировать обработку ответов без сети — быстро, надёжно, воспроизводимо.

---

## Обзор инструментов

| Инструмент | Для чего | Установка |
|------------|----------|-----------|
| `unittest.mock.patch` | Мок любого объекта, включая `requests` | встроен |
| `responses` | Мок HTTP-запросов через `requests` | `pip install responses` |
| `httpretty` | Перехват на уровне сокета | `pip install httpretty` |
| `respx` | Мок для `httpx` (async) | `pip install respx` |
| `pytest-mock` | Удобная обёртка над `unittest.mock` | `pip install pytest-mock` |

---

## `unittest.mock.patch` — базовый подход

```python
from unittest.mock import patch, MagicMock
import pytest
import requests


class NotificationService:
    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    def send(self, user_id: int, message: str) -> bool:
        response = requests.post(f"{self.api_url}/notify", json={
            "user_id": user_id,
            "message": message,
        })
        return response.status_code == 200


@pytest.fixture
def service() -> NotificationService:
    return NotificationService("https://notify.example.com")


def test_send_success(service):
    with patch("requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = service.send(user_id=1, message="Hello!")

        assert result is True
        mock_post.assert_called_once_with(
            "https://notify.example.com/notify",
            json={"user_id": 1, "message": "Hello!"},
        )


def test_send_failure(service):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 500

        result = service.send(user_id=1, message="Hello!")
        assert result is False
```

---

## `responses` — декларативный мок для requests

Библиотека `responses` перехватывает реальные запросы requests и возвращает заданные ответы.

```bash
pip install responses
```

### Декоратором

```python
import responses as rsps
import requests


@rsps.activate
def test_get_user():
    rsps.add(
        method=rsps.GET,
        url="https://api.example.com/users/1",
        json={"id": 1, "name": "Alice", "email": "alice@example.com"},
        status=200,
    )

    response = requests.get("https://api.example.com/users/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


@rsps.activate
def test_create_user():
    rsps.add(
        method=rsps.POST,
        url="https://api.example.com/users",
        json={"id": 42, "name": "Bob", "email": "bob@example.com"},
        status=201,
    )

    payload = {"name": "Bob", "email": "bob@example.com"}
    response = requests.post("https://api.example.com/users", json=payload)

    assert response.status_code == 201
    assert response.json()["id"] == 42
```

### Контекстным менеджером (в pytest)

```python
import responses as rsps
import requests
import pytest


@pytest.fixture
def mocked_api():
    """Фикстура с настроенными моками."""
    with rsps.RequestsMock() as mock:
        mock.add(rsps.GET, "https://api.example.com/users", json={
            "items": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
            ],
            "total": 2,
        })
        mock.add(rsps.GET, "https://api.example.com/users/1", json={
            "id": 1, "name": "Alice", "email": "alice@example.com",
        })
        mock.add(rsps.POST, "https://api.example.com/users", json={
            "id": 3, "name": "Charlie",
        }, status=201)
        mock.add(rsps.DELETE, "https://api.example.com/users/1", status=204)
        yield mock


def test_get_users_list(mocked_api):
    response = requests.get("https://api.example.com/users")
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_get_single_user(mocked_api):
    response = requests.get("https://api.example.com/users/1")
    assert response.json()["name"] == "Alice"


def test_create_user(mocked_api):
    response = requests.post("https://api.example.com/users", json={"name": "Charlie"})
    assert response.status_code == 201
    assert response.json()["id"] == 3
```

### Мок с ошибкой и проверкой запроса

```python
import responses as rsps
import requests
import pytest


@rsps.activate
def test_get_nonexistent_user():
    rsps.add(
        method=rsps.GET,
        url="https://api.example.com/users/999",
        json={"error": "User not found"},
        status=404,
    )

    response = requests.get("https://api.example.com/users/999")
    assert response.status_code == 404
    assert "error" in response.json()


@rsps.activate
def test_server_error_handling():
    rsps.add(
        method=rsps.POST,
        url="https://api.example.com/orders",
        json={"error": "Internal Server Error"},
        status=500,
    )

    with pytest.raises(requests.HTTPError):
        response = requests.post("https://api.example.com/orders", json={})
        response.raise_for_status()
```

---

## `respx` — мок для httpx (async API)

```bash
pip install respx httpx
```

```python
import httpx
import respx
import pytest


class AsyncAPIClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def get_user(self, user_id: int) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/users/{user_id}")
            response.raise_for_status()
            return response.json()


@respx.mock
@pytest.mark.asyncio
async def test_get_user_async():
    respx.get("https://api.example.com/users/1").mock(
        return_value=httpx.Response(200, json={"id": 1, "name": "Alice"})
    )

    client = AsyncAPIClient("https://api.example.com")
    user = await client.get_user(1)

    assert user["id"] == 1
    assert user["name"] == "Alice"
```

---

## `pytest-mock` + requests — полный пример

```python
# user_service.py
import requests


class UserService:
    BASE_URL = "https://api.example.com"

    def get_user(self, user_id: int) -> dict:
        response = requests.get(f"{self.BASE_URL}/users/{user_id}")
        if response.status_code == 404:
            raise ValueError(f"User {user_id} not found")
        response.raise_for_status()
        return response.json()

    def get_active_users(self) -> list[dict]:
        response = requests.get(f"{self.BASE_URL}/users", params={"status": "active"})
        response.raise_for_status()
        return response.json()["items"]

    def update_user(self, user_id: int, data: dict) -> dict:
        response = requests.patch(f"{self.BASE_URL}/users/{user_id}", json=data)
        response.raise_for_status()
        return response.json()
```

```python
# test_user_service.py
import pytest
from unittest.mock import MagicMock
from user_service import UserService


@pytest.fixture
def service() -> UserService:
    return UserService()


def make_mock_response(status_code: int, json_data: dict | list) -> MagicMock:
    """Фабрика для создания мок-ответов."""
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    mock.ok = 200 <= status_code < 300
    mock.raise_for_status = MagicMock(
        side_effect=None if mock.ok else Exception(f"HTTP {status_code}")
    )
    return mock


def test_get_user_success(service, mocker):
    mocker.patch("requests.get", return_value=make_mock_response(200, {
        "id": 1, "name": "Alice", "email": "alice@example.com",
    }))

    user = service.get_user(1)

    assert user["id"] == 1
    assert user["name"] == "Alice"


def test_get_user_not_found(service, mocker):
    mocker.patch("requests.get", return_value=make_mock_response(404, {}))

    with pytest.raises(ValueError, match="User 999 not found"):
        service.get_user(999)


def test_get_active_users(service, mocker):
    mock_get = mocker.patch("requests.get", return_value=make_mock_response(200, {
        "items": [
            {"id": 1, "name": "Alice", "status": "active"},
            {"id": 2, "name": "Bob", "status": "active"},
        ],
    }))

    users = service.get_active_users()

    assert len(users) == 2
    mock_get.assert_called_once_with(
        "https://api.example.com/users",
        params={"status": "active"},
    )


def test_update_user(service, mocker):
    mocker.patch("requests.patch", return_value=make_mock_response(200, {
        "id": 1, "name": "Alice Updated",
    }))

    updated = service.update_user(1, {"name": "Alice Updated"})
    assert updated["name"] == "Alice Updated"
```

---

## Когда что использовать

| Ситуация | Инструмент |
|----------|------------|
| Быстрые юнит-тесты, полный контроль над поведением | `unittest.mock.patch` + `MagicMock` |
| Множество HTTP-моков, читаемый код | `responses` |
| Тест конкретного URL с телом/статусом | `responses` |
| async HTTP через httpx | `respx` |
| Общая логика моков в conftest | фикстура с `responses.RequestsMock()` |

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| Тест делает реальный запрос | Мок не применился — неверный путь к patch | Проверь импорт: патчить где используется |
| `@rsps.activate` забыт | `ConnectionError` — мок не активен | Не забывай декоратор или `with rsps.RequestsMock()` |
| URL не совпадает | `ConnectionError: No match for GET url` | Проверь URL точно, включая слеш в конце |

---

## Вопрос на собесе

**Q: Зачем мокировать HTTP-запросы если можно запустить против реального сервера?**

> Реальные запросы делают тесты медленными, нестабильными (сервис может быть недоступен), зависимыми от состояния данных. Юнит-тесты с моками запускаются за миллисекунды, работают офлайн и воспроизводимы. Реальные запросы нужны в интеграционных и E2E тестах.

**Q: Как проверить, что запрос был отправлен с правильными параметрами?**

```python
# С unittest.mock
mock_post.assert_called_once_with(url, json=expected_payload)

# С responses
with rsps.RequestsMock() as mock:
    mock.add(rsps.POST, url, json={})
    # после вызова:
    assert mock.calls[0].request.body == json.dumps(expected_payload)
```
