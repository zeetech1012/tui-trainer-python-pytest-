# Управление потоком выполнения

> **Зачем автотестеру:** Условия и циклы определяют логику тестовых хелперов, а `try/except` — основа надёжной работы с API и файлами. Понимание этих конструкций нужно для написания устойчивых тестов.

---

## Условные операторы: `if / elif / else`

```python
def classify_status_code(code: int) -> str:
    if 200 <= code < 300:
        return "success"
    elif 400 <= code < 500:
        return "client_error"
    elif 500 <= code < 600:
        return "server_error"
    else:
        return "unknown"
```

### Тернарный оператор (inline if)

```python
# value_if_true if condition else value_if_false
status = "active" if user["is_active"] else "inactive"

# В тестах удобно для сообщений
label = "passed" if result == expected else "failed"
```

### Операторы сравнения и логические

```python
# Сравнение
x == y    # равно
x != y    # не равно
x > y     # больше
x >= y    # больше или равно
x in lst  # вхождение в коллекцию
x not in lst
x is None # проверка на None (не x == None!)
x is not None

# Логические
and   # оба условия True
or    # хотя бы одно True
not   # инверсия

# Пример
if response and response.get("status") == "ok":
    ...
```

---

## Циклы

### `for` — итерация по последовательности

```python
# Итерация по списку
for item in items:
    process(item)

# С индексом — enumerate
for index, item in enumerate(items):
    print(f"{index}: {item}")

# По словарю
for key, value in data.items():
    print(f"{key} = {value}")

# По диапазону
for i in range(10):         # 0..9
    ...
for i in range(1, 11):      # 1..10
    ...
for i in range(10, 0, -1):  # 10..1 (обратный)
    ...
```

### `while` — выполнять пока условие истинно

```python
attempts = 0
max_retries = 3

while attempts < max_retries:
    response = send_request()
    if response.status_code == 200:
        break
    attempts += 1
else:
    # Выполняется если цикл завершился без break
    raise RuntimeError("Max retries exceeded")
```

### `break`, `continue`, `else`

```python
# break — прервать цикл
for item in items:
    if item == target:
        break

# continue — пропустить итерацию
for item in items:
    if item is None:
        continue
    process(item)

# else в for — выполняется если не было break
for item in items:
    if item["status"] == "error":
        break
else:
    print("No errors found")
```

---

## Обработка исключений: `try / except / finally`

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"Value error: {e}")
except (TypeError, KeyError) as e:
    print(f"Type or Key error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    raise   # перебросить исключение дальше
else:
    # Выполняется только если исключений НЕ было
    print("Success!")
finally:
    # Выполняется ВСЕГДА (cleanup)
    cleanup()
```

### Создание своих исключений

```python
class APIError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")


class NotFoundError(APIError):
    pass


def get_user(user_id: int) -> dict:
    response = requests.get(f"/users/{user_id}")
    if response.status_code == 404:
        raise NotFoundError(404, f"User {user_id} not found")
    if not response.ok:
        raise APIError(response.status_code, response.text)
    return response.json()
```

---

## Как это выглядит в pytest

### Тест управляющих конструкций

```python
import pytest


def classify_status_code(code: int) -> str:
    if 200 <= code < 300:
        return "success"
    elif 400 <= code < 500:
        return "client_error"
    elif 500 <= code < 600:
        return "server_error"
    else:
        return "unknown"


@pytest.mark.parametrize("code,expected", [
    (200, "success"),
    (201, "success"),
    (400, "client_error"),
    (404, "client_error"),
    (500, "server_error"),
    (503, "server_error"),
    (100, "unknown"),
    (999, "unknown"),
])
def test_classify_status_code(code: int, expected: str):
    assert classify_status_code(code) == expected
```

### Тест обработки исключений через `pytest.raises`

```python
class APIError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(message)


def fetch_order(order_id: int) -> dict:
    if order_id <= 0:
        raise ValueError(f"Invalid order_id: {order_id}")
    if order_id > 9999:
        raise APIError(404, f"Order {order_id} not found")
    return {"id": order_id, "status": "pending"}


def test_fetch_order_success():
    order = fetch_order(42)
    assert order["id"] == 42


def test_fetch_order_invalid_id():
    with pytest.raises(ValueError, match="Invalid order_id"):
        fetch_order(-1)


def test_fetch_order_not_found():
    with pytest.raises(APIError) as exc_info:
        fetch_order(99999)
    assert exc_info.value.status_code == 404


def test_fetch_order_zero_id():
    with pytest.raises(ValueError):
        fetch_order(0)
```

### Retry-логика в тесте

```python
import time


def wait_for_status(get_status_fn, target: str, retries: int = 5) -> bool:
    """Ждёт пока статус не станет target, иначе False."""
    for attempt in range(retries):
        status = get_status_fn()
        if status == target:
            return True
        time.sleep(0.1)
    return False


def test_wait_for_status_success():
    call_count = 0

    def mock_status():
        nonlocal call_count
        call_count += 1
        return "completed" if call_count >= 3 else "pending"

    assert wait_for_status(mock_status, "completed") is True


def test_wait_for_status_timeout():
    def always_pending():
        return "pending"

    assert wait_for_status(always_pending, "completed", retries=3) is False
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| `except Exception` без `raise` | Скрывает реальную ошибку | Логируй или перебрасывай |
| Голый `except:` | Поймает даже `KeyboardInterrupt` | Используй `except Exception` |
| `is` вместо `==` | `1 is 1` — True, но `1000 is 1000` — может быть False | Используй `==` для сравнения значений, `is` только для `None` |
| Бесконечный `while` | Нет условия выхода | Всегда добавляй счётчик или timeout |
| `for i in range(len(lst))` | Непитонично | Используй `for item in lst` или `enumerate` |

---

## Вопрос на собесе

**Q: В чём разница между `is` и `==`?**

> `==` сравнивает **значения** объектов. `is` проверяет **идентичность** — являются ли они одним и тем же объектом в памяти. `None` всегда сравнивается через `is None`, потому что `None` — синглтон.

**Q: Когда выполняется блок `else` в `try/except`?**

> Блок `else` выполняется только если в блоке `try` **не было исключений**. Это позволяет отделить основную логику от обработки ошибок.

**Q: Как в pytest проверить, что функция бросает исключение?**

> Используй контекстный менеджер `pytest.raises(ExceptionType)`. Можно добавить `match="pattern"` для проверки текста исключения через regex.
