# Словари (dict)

> **Зачем автотестеру:** JSON-ответы API — это словари. Почти каждый тест работает со словарями: парсит body ответа, сравнивает поля, формирует payload для запроса. Без уверенного владения словарями на собесе не обойтись.

---

## Концепция

`dict` — изменяемая коллекция пар ключ-значение. Начиная с Python 3.7 сохраняет порядок вставки. Ключи должны быть неизменяемыми (str, int, tuple). Поиск по ключу — O(1).

```python
user: dict[str, int | str] = {
    "id": 1,
    "name": "Alice",
    "age": 30,
}
```

---

## Создание словарей

```python
# Литерал
config = {"host": "localhost", "port": 5432}

# Из списка пар
pairs = [("a", 1), ("b", 2)]
d = dict(pairs)              # {"a": 1, "b": 2}

# Ключевые аргументы
d = dict(host="localhost", port=5432)

# dict.fromkeys — одинаковое значение для всех ключей
keys = ["id", "name", "email"]
template = dict.fromkeys(keys, None)
# {"id": None, "name": None, "email": None}
```

---

## Доступ к данным

```python
user = {"id": 1, "name": "Alice", "role": "admin"}

# По ключу — KeyError если нет
user["name"]         # "Alice"
user["missing"]      # KeyError!

# .get() — безопасный доступ
user.get("name")              # "Alice"
user.get("email")             # None
user.get("email", "n/a")     # "n/a"  — дефолтное значение
```

---

## Основные методы

| Метод | Описание | Пример |
|-------|----------|--------|
| `keys()` | Все ключи | `d.keys()` |
| `values()` | Все значения | `d.values()` |
| `items()` | Пары (ключ, значение) | `d.items()` |
| `get(key, default)` | Безопасный доступ | `d.get("key", 0)` |
| `setdefault(key, default)` | Возвращает значение, если нет — создаёт | `d.setdefault("hits", 0)` |
| `update(other)` | Обновить из другого словаря | `d.update({"x": 1})` |
| `pop(key)` | Удалить и вернуть значение | `d.pop("id")` |
| `pop(key, default)` | Без KeyError | `d.pop("id", None)` |
| `copy()` | Поверхностная копия | `d.copy()` |
| `clear()` | Очистить | `d.clear()` |
| `in` | Проверка ключа | `"id" in d` |

---

## Итерация по словарю

```python
user = {"id": 1, "name": "Alice", "role": "admin"}

# Только ключи (дефолтная итерация)
for key in user:
    print(key)

# Ключи явно
for key in user.keys():
    print(key)

# Значения
for value in user.values():
    print(value)

# Пары
for key, value in user.items():
    print(f"{key}: {value}")
```

---

## Объединение словарей

```python
defaults = {"timeout": 30, "retries": 3, "method": "GET"}
overrides = {"timeout": 60, "url": "/api/users"}

# Python 3.9+: оператор |
merged = defaults | overrides
# {"timeout": 60, "retries": 3, "method": "GET", "url": "/api/users"}

# До Python 3.9: unpacking
merged = {**defaults, **overrides}

# update() — изменяет первый словарь
defaults.update(overrides)
```

---

## Вложенные словари

```python
order = {
    "id": 42,
    "user": {
        "id": 1,
        "name": "Alice",
    },
    "items": [
        {"product_id": 10, "quantity": 2},
        {"product_id": 11, "quantity": 1},
    ],
}

# Доступ к вложенным данным
user_name = order["user"]["name"]                    # "Alice"
first_product = order["items"][0]["product_id"]      # 10

# Безопасный доступ к вложенным
city = order.get("user", {}).get("address", {}).get("city", "unknown")
```

---

## `setdefault` — удобный паттерн группировки

```python
# Группировка заказов по статусу
orders = [
    {"id": 1, "status": "pending"},
    {"id": 2, "status": "shipped"},
    {"id": 3, "status": "pending"},
    {"id": 4, "status": "delivered"},
]

grouped: dict[str, list] = {}
for order in orders:
    grouped.setdefault(order["status"], []).append(order["id"])
# {"pending": [1, 3], "shipped": [2], "delivered": [4]}
```

---

## Как это выглядит в pytest

### Тест работы с JSON-ответом

```python
import pytest


def extract_user_info(response_body: dict) -> dict:
    """Извлекает нужные поля из тела ответа."""
    return {
        "id": response_body["id"],
        "name": response_body.get("name", "Unknown"),
        "email": response_body.get("email", ""),
        "is_active": response_body.get("is_active", False),
    }


def test_extract_user_info_full_data():
    body = {"id": 1, "name": "Alice", "email": "alice@example.com", "is_active": True}
    result = extract_user_info(body)
    assert result == {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "is_active": True,
    }


def test_extract_user_info_missing_optional_fields():
    body = {"id": 2}
    result = extract_user_info(body)
    assert result["name"] == "Unknown"
    assert result["email"] == ""
    assert result["is_active"] is False


def test_extract_user_info_missing_required_field():
    body = {"name": "Bob"}
    with pytest.raises(KeyError, match="id"):
        extract_user_info(body)
```

### Параметризованный тест проверки словаря

```python
@pytest.mark.parametrize("field,value", [
    ("status", "active"),
    ("role", "admin"),
    ("is_verified", True),
])
def test_user_response_fields(api_client, field: str, value):
    response = api_client.get("/users/1")
    data = response.json()
    assert data[field] == value


def test_orders_grouped_by_status():
    orders = [
        {"id": 1, "status": "pending"},
        {"id": 2, "status": "shipped"},
        {"id": 3, "status": "pending"},
    ]
    grouped: dict[str, list] = {}
    for o in orders:
        grouped.setdefault(o["status"], []).append(o["id"])

    assert grouped["pending"] == [1, 3]
    assert grouped["shipped"] == [2]
    assert "delivered" not in grouped
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| `d["missing_key"]` | `KeyError` | Используй `d.get("key")` или проверяй `"key" in d` |
| `d.pop("missing")` | `KeyError` | Используй `d.pop("key", None)` |
| Изменение словаря в цикле | `RuntimeError: dictionary changed size during iteration` | Итерируйся по `list(d.keys())` |
| Вложенный `.copy()` | Поверхностная копия не клонирует вложенные dict | Используй `copy.deepcopy(d)` |
| `{**a, **b}` — порядок | Последний перезаписывает первый | Помни: `{**defaults, **overrides}` — overrides побеждают |

---

## Вопрос на собесе

**Q: Как безопасно получить вложенное значение без цепочки `.get()`?**

```python
# Python 3.8+: оператор walrus + get или используй библиотеку
from functools import reduce

def deep_get(d: dict, *keys, default=None):
    try:
        return reduce(lambda obj, key: obj[key], keys, d)
    except (KeyError, TypeError):
        return default

deep_get(order, "user", "address", "city", default="unknown")
```

**Q: В чём разница между `dict.update()` и оператором `|`?**

> `update()` изменяет исходный словарь на месте и возвращает `None`. Оператор `|` (Python 3.9+) возвращает **новый** словарь, не изменяя оригиналы. `|=` обновляет на месте как `update()`.
