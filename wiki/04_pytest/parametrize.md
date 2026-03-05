# Параметризация тестов

> **Зачем автотестеру:** Параметризация — способ запустить один тест с разными входными данными. Вместо 10 почти одинаковых тест-функций — одна с `@pytest.mark.parametrize`. Это экономит код и улучшает покрытие.

---

## Концепция

`@pytest.mark.parametrize` позволяет передать список значений, для каждого из которых тест будет запущен отдельно. Результат — отдельная строка для каждого набора данных в отчёте.

---

## Базовый синтаксис

```python
import pytest


@pytest.mark.parametrize("input_value,expected", [
    (1, 2),
    (5, 10),
    (0, 0),
    (-3, -6),
])
def test_double(input_value: int, expected: int):
    assert input_value * 2 == expected
```

Запуск: создаст 4 отдельных теста:
```
test_double[1-2]
test_double[5-10]
test_double[0-0]
test_double[-3--6]
```

---

## Один параметр

```python
@pytest.mark.parametrize("status_code", [200, 201, 204])
def test_success_status_codes(status_code: int):
    from http import HTTPStatus
    assert 200 <= status_code < 300


@pytest.mark.parametrize("invalid_email", [
    "notanemail",
    "@nodomain.com",
    "no-at-sign",
    "",
    "spaces in@email.com",
    "double@@email.com",
])
def test_invalid_email_format(api_client, invalid_email: str):
    response = api_client.post("/users", json={"email": invalid_email})
    assert response.status_code == 422
```

---

## Несколько параметров

```python
@pytest.mark.parametrize("username,password,expected_status", [
    ("admin", "correct_pass", 200),
    ("admin", "wrong_pass", 401),
    ("unknown_user", "any_pass", 401),
    ("", "password", 422),
    ("admin", "", 422),
])
def test_login(api_client, username: str, password: str, expected_status: int):
    response = api_client.post("/auth/login", json={
        "username": username,
        "password": password,
    })
    assert response.status_code == expected_status
```

---

## `ids` — понятные имена для параметров

```python
@pytest.mark.parametrize("price,quantity,discount,expected_total", [
    (100.0, 2, 0.0, 200.0),
    (100.0, 2, 0.1, 180.0),
    (50.0, 10, 0.2, 400.0),
    (0.0, 5, 0.0, 0.0),
], ids=[
    "no_discount",
    "10pct_discount",
    "20pct_discount",
    "zero_price",
])
def test_order_total(price: float, quantity: int, discount: float, expected_total: float):
    total = price * quantity * (1 - discount)
    assert total == pytest.approx(expected_total)
```

Запуск покажет:
```
test_order_total[no_discount]
test_order_total[10pct_discount]
test_order_total[20pct_discount]
test_order_total[zero_price]
```

---

## `pytest.param` — параметр с маркером или id

```python
@pytest.mark.parametrize("order_id,expected_status", [
    pytest.param(1, 200, id="valid_order"),
    pytest.param(9999, 404, id="nonexistent_order"),
    pytest.param(-1, 422, id="negative_id"),
    pytest.param(0, 422, id="zero_id"),
    pytest.param(
        99999999,
        404,
        id="very_large_id",
        marks=pytest.mark.slow,
    ),
])
def test_get_order(api_client, order_id: int, expected_status: int):
    response = api_client.get(f"/orders/{order_id}")
    assert response.status_code == expected_status
```

---

## Комбинирование (декартово произведение)

Два `@pytest.mark.parametrize` создают все возможные комбинации:

```python
@pytest.mark.parametrize("method", ["GET", "POST", "PUT", "DELETE"])
@pytest.mark.parametrize("endpoint", ["/users", "/orders", "/products"])
def test_auth_required(api_client_no_auth, method: str, endpoint: str):
    """Каждый метод × каждый endpoint = 12 тестов."""
    response = api_client_no_auth.request(method, f"https://api.example.com{endpoint}")
    assert response.status_code == 401
```

---

## Параметризация с фикстурами

```python
@pytest.fixture
def api_client():
    return create_api_client()


@pytest.mark.parametrize("field,value", [
    ("name", ""),
    ("email", "invalid"),
    ("age", -1),
    ("age", 200),
])
def test_create_user_validation(api_client, field: str, value):
    """api_client — фикстура, field/value — параметры."""
    payload = {"name": "Test", "email": "test@example.com", "age": 25}
    payload[field] = value
    response = api_client.post("/users", json=payload)
    assert response.status_code == 422
```

---

## Реальный тест — полная параметризация HTTP-методов

```python
import pytest
import requests


BASE_URL = "https://api.example.com"


@pytest.mark.parametrize("endpoint,method,payload,expected_status", [
    # CRUD для users
    ("/users", "GET", None, 200),
    ("/users", "POST", {"name": "Test", "email": "t@t.com"}, 201),
    ("/users/1", "GET", None, 200),
    ("/users/1", "PUT", {"name": "Updated"}, 200),
    ("/users/1", "DELETE", None, 204),
    # Несуществующие ресурсы
    ("/users/99999", "GET", None, 404),
    ("/users/99999", "DELETE", None, 404),
], ids=[
    "list_users",
    "create_user",
    "get_user",
    "update_user",
    "delete_user",
    "get_nonexistent",
    "delete_nonexistent",
])
def test_user_api_endpoints(
    api_client: requests.Session,
    endpoint: str,
    method: str,
    payload: dict | None,
    expected_status: int,
):
    response = api_client.request(
        method=method,
        url=f"{BASE_URL}{endpoint}",
        json=payload,
    )
    assert response.status_code == expected_status, (
        f"{method} {endpoint} expected {expected_status}, got {response.status_code}. "
        f"Body: {response.text[:200]}"
    )
```

---

## Генератор параметров

```python
def generate_boundary_values(min_val: int, max_val: int):
    """Генерирует граничные значения для параметризации."""
    return [
        pytest.param(min_val - 1, False, id=f"below_min_{min_val-1}"),
        pytest.param(min_val, True, id=f"min_{min_val}"),
        pytest.param((min_val + max_val) // 2, True, id="middle"),
        pytest.param(max_val, True, id=f"max_{max_val}"),
        pytest.param(max_val + 1, False, id=f"above_max_{max_val+1}"),
    ]


@pytest.mark.parametrize("age,is_valid", generate_boundary_values(0, 150))
def test_user_age_validation(api_client, age: int, is_valid: bool):
    response = api_client.post("/users", json={"name": "Test", "age": age})
    if is_valid:
        assert response.status_code in (200, 201)
    else:
        assert response.status_code == 422
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| Слишком много параметров | Тест тяжело читать | Добавь `ids=` или используй `pytest.param` |
| Параметр — изменяемый объект | Один объект для всех тестов | Используй фикстуру для создания нового объекта |
| Комбинаторный взрыв | 5×5×5 = 125 тестов | Используй pairwise тестирование или разделяй на отдельные тесты |
| Длинный список параметров | Тяжело поддерживать inline | Вынеси в переменную или загрузи из JSON-файла |

---

## Вопрос на собесе

**Q: Как в pytest запустить только определённый параметрический тест?**

> `pytest test_file.py::test_name[param_id]` — указать id параметра в квадратных скобках. Например: `pytest -k "no_discount"` запустит все тесты с "no_discount" в имени.

**Q: В чём разница между `@pytest.mark.parametrize` и параметризованной фикстурой?**

> `@pytest.mark.parametrize` — параметры напрямую в тесте, удобно для простых значений. Параметризованная фикстура (`@pytest.fixture(params=[...])`) — когда нужно выполнить setup/teardown для каждого значения (например, разные типы БД).
