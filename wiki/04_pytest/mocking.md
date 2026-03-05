# Моки (Mocking)

> **Зачем автотестеру:** Моки позволяют тестировать код в изоляции — без реальных HTTP-запросов, баз данных, внешних сервисов. Это основа юнит-тестирования. На собесе обязательно спросят про `unittest.mock`, `MagicMock` и `monkeypatch`.

---

## Концепция

Мок (mock) — заглушка, которая заменяет реальный объект в тесте. Мок:
- Возвращает заданные значения
- Записывает, как его вызывали
- Позволяет проверить, что код работает с зависимостями правильно

---

## `unittest.mock` — встроенный модуль

### `MagicMock` — универсальная заглушка

```python
from unittest.mock import MagicMock

mock = MagicMock()

# Любые атрибуты и методы работают автоматически
mock.some_method()          # MagicMock()
mock.attribute.value        # MagicMock()

# Настройка возвращаемого значения
mock.get_user.return_value = {"id": 1, "name": "Alice"}
result = mock.get_user(1)
print(result)   # {"id": 1, "name": "Alice"}

# Проверка вызовов
mock.get_user.assert_called_once_with(1)
mock.get_user.assert_called_with(1)
assert mock.get_user.call_count == 1

# Настройка исключения
mock.delete_user.side_effect = PermissionError("Access denied")
```

---

## `patch` — замена объекта в модуле

```python
from unittest.mock import patch


def get_weather(city: str) -> dict:
    import requests
    response = requests.get(f"https://api.weather.com/{city}")
    return response.json()


# Декоратором
from unittest.mock import patch

@patch("requests.get")
def test_get_weather_success(mock_get):
    mock_get.return_value.json.return_value = {"temp": 22, "city": "Moscow"}
    mock_get.return_value.status_code = 200

    result = get_weather("Moscow")
    assert result["temp"] == 22
    mock_get.assert_called_once_with("https://api.weather.com/Moscow")


# Контекстным менеджером
def test_get_weather_with_context():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"temp": 15}
        result = get_weather("London")
        assert result["temp"] == 15
```

---

## `pytest-mock` — плагин для pytest

Предоставляет фикстуру `mocker` — удобную обёртку над `unittest.mock`.

```bash
pip install pytest-mock
```

```python
def test_send_notification(mocker):
    # mocker.patch — удобнее чем @patch декоратор
    mock_send = mocker.patch("mymodule.send_email")
    mock_send.return_value = True

    result = notify_user(user_id=1, message="Hello")

    assert result is True
    mock_send.assert_called_once_with(
        to="user@example.com",
        subject="Notification",
        body="Hello",
    )
```

---

## `monkeypatch` — встроенная фикстура pytest

`monkeypatch` изменяет объекты на время теста и автоматически восстанавливает после.

```python
def test_config_from_env(monkeypatch):
    # Подменить переменную окружения
    monkeypatch.setenv("API_URL", "https://test.example.com")
    monkeypatch.setenv("API_TOKEN", "test-token-123")

    config = load_config()
    assert config.api_url == "https://test.example.com"


def test_home_directory(monkeypatch, tmp_path):
    # Подменить атрибут объекта
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    result = get_config_path()
    assert str(tmp_path) in str(result)


def test_random_choice(monkeypatch):
    # Подменить функцию
    monkeypatch.setattr("random.choice", lambda lst: lst[0])

    result = pick_random_item(["a", "b", "c"])
    assert result == "a"
```

---

## Реальный пример: мок HTTP-запроса

```python
# orders.py
import requests


class OrderService:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_order(self, order_id: int) -> dict:
        response = requests.get(f"{self.base_url}/orders/{order_id}")
        if response.status_code == 404:
            raise ValueError(f"Order {order_id} not found")
        response.raise_for_status()
        return response.json()

    def create_order(self, payload: dict) -> dict:
        response = requests.post(f"{self.base_url}/orders", json=payload)
        response.raise_for_status()
        return response.json()
```

```python
# test_orders.py
import pytest
from unittest.mock import MagicMock, patch
from orders import OrderService


@pytest.fixture
def service() -> OrderService:
    return OrderService("https://api.example.com")


def test_get_order_success(service: OrderService):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 42, "status": "pending"}
        mock_get.return_value = mock_response

        order = service.get_order(42)

        assert order["id"] == 42
        assert order["status"] == "pending"
        mock_get.assert_called_once_with("https://api.example.com/orders/42")


def test_get_order_not_found(service: OrderService):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Order 999 not found"):
            service.get_order(999)


def test_create_order_success(service: OrderService, mocker):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"id": 1, "status": "new"}
    mock_post.return_value.raise_for_status = MagicMock()

    order = service.create_order({"product_id": 5, "quantity": 2})

    assert order["id"] == 1
    mock_post.assert_called_once_with(
        "https://api.example.com/orders",
        json={"product_id": 5, "quantity": 2},
    )
```

---

## `side_effect` — динамическое поведение

```python
def test_retry_on_failure(mocker):
    call_count = 0

    def flaky_response(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        mock_resp = MagicMock()
        if call_count < 3:
            mock_resp.status_code = 503
        else:
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"ok": True}
        return mock_resp

    mocker.patch("requests.get", side_effect=flaky_response)

    result = fetch_with_retry("https://api.example.com/data", retries=3)
    assert result["ok"] is True
    assert call_count == 3


def test_raises_on_network_error(mocker):
    mocker.patch("requests.get", side_effect=ConnectionError("Network unreachable"))

    with pytest.raises(ConnectionError):
        fetch_data("https://api.example.com/users")
```

---

## `responses` — мок для requests без patch

```bash
pip install responses
```

```python
import responses as responses_lib
import requests
import pytest


@responses_lib.activate
def test_get_users():
    responses_lib.add(
        method=responses_lib.GET,
        url="https://api.example.com/users",
        json={"items": [{"id": 1, "name": "Alice"}]},
        status=200,
    )

    response = requests.get("https://api.example.com/users")
    assert response.status_code == 200
    assert response.json()["items"][0]["name"] == "Alice"


@pytest.fixture
def mocked_api():
    with responses_lib.RequestsMock() as rsps:
        rsps.add(responses_lib.GET, "https://api.example.com/users", json={"items": []})
        yield rsps


def test_empty_users(mocked_api):
    response = requests.get("https://api.example.com/users")
    assert response.json() == {"items": []}
```

---

## Проверка вызовов мока

```python
from unittest.mock import MagicMock, call

mock_notify = MagicMock()

# Вызовем несколько раз
mock_notify("user1@example.com", "Hello")
mock_notify("user2@example.com", "World")

# Проверки
mock_notify.assert_called()                           # вызывался хотя бы раз
mock_notify.assert_called_once()                      # вызывался ровно один раз (упадёт — 2 раза)
mock_notify.assert_called_with("user2@example.com", "World")  # последний вызов
mock_notify.assert_any_call("user1@example.com", "Hello")     # хотя бы раз с этими аргументами
assert mock_notify.call_count == 2

# Порядок вызовов
mock_notify.assert_has_calls([
    call("user1@example.com", "Hello"),
    call("user2@example.com", "World"),
])
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| Неправильный путь к patch | `@patch("requests.get")` вместо `@patch("mymodule.requests.get")` | Патчить там, где используется, не где определяется |
| Мок не сбрасывается | Состояние мока протекает между тестами | Используй `mocker` от pytest-mock — автосброс |
| `assert_called_with` vs `assert_called_once_with` | `assert_called_with` проверяет только последний вызов | Если нужен точно один вызов — используй `assert_called_once_with` |

---

## Вопрос на собесе

**Q: В чём разница между `Mock` и `MagicMock`?**

> `MagicMock` — подкласс `Mock`, который автоматически реализует магические методы (`__len__`, `__iter__`, `__str__` и др.). Для большинства случаев используй `MagicMock`.

**Q: Как правильно указать путь к `patch`?**

> Патчить нужно **там, где используется**, а не там, где определено. Если в файле `mymodule.py` написано `import requests` и вызывается `requests.get()`, то патчить нужно `mymodule.requests.get` или `requests.get` (если requests не переимпортирован).
