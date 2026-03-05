# Магические методы (Magic / Dunder Methods)

> **Зачем автотестеру:** Магические методы делают кастомные классы "питоническими". `__eq__` позволяет сравнивать объекты в `assert`. `__str__` даёт читаемые сообщения об ошибках. `__len__` и `__contains__` позволяют использовать `len()` и `in` с твоими объектами.

---

## Концепция

Магические методы (dunder-методы, от "double underscore") — специальные методы с именами вида `__method__`. Python вызывает их автоматически при определённых операциях: сравнение, арифметика, вывод, контейнерные операции.

---

## Представление объектов

### `__str__` и `__repr__`

```python
class Order:
    def __init__(self, order_id: int, status: str, total: float) -> None:
        self.order_id = order_id
        self.status = status
        self.total = total

    def __str__(self) -> str:
        # Для пользователей — print(), str()
        return f"Order #{self.order_id} [{self.status}] — {self.total:.2f} ₽"

    def __repr__(self) -> str:
        # Для разработчиков — repr(), в отладчике, в списках
        return f"Order(order_id={self.order_id!r}, status={self.status!r}, total={self.total!r})"


order = Order(42, "pending", 1500.0)

print(order)           # "Order #42 [pending] — 1500.00 ₽"
repr(order)            # "Order(order_id=42, status='pending', total=1500.0)"
str(order)             # "Order #42 [pending] — 1500.00 ₽"

orders = [Order(1, "paid", 100.0), Order(2, "pending", 200.0)]
print(orders)  # использует __repr__ для элементов списка
```

---

## Сравнение объектов

### `__eq__`, `__lt__`, `__gt__`, `__le__`, `__ge__`

```python
from dataclasses import dataclass


@dataclass
class Version:
    major: int
    minor: int
    patch: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other: "Version") -> bool:
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __le__(self, other: "Version") -> bool:
        return self == other or self < other

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


v1 = Version(1, 2, 3)
v2 = Version(1, 2, 4)
v3 = Version(1, 2, 3)

v1 == v3    # True
v1 < v2     # True
v2 > v1     # True
sorted([v2, v1, v3])   # [1.2.3, 1.2.3, 1.2.4]
```

> `@dataclass` автоматически генерирует `__eq__` (и `__lt__` если `order=True`).

---

## Контейнерные методы

### `__len__`, `__contains__`, `__getitem__`, `__iter__`

```python
class TestSuite:
    def __init__(self, name: str) -> None:
        self.name = name
        self._tests: list[str] = []

    def add(self, test_name: str) -> "TestSuite":
        self._tests.append(test_name)
        return self

    def __len__(self) -> int:
        return len(self._tests)

    def __contains__(self, test_name: str) -> bool:
        return test_name in self._tests

    def __getitem__(self, index: int) -> str:
        return self._tests[index]

    def __iter__(self):
        return iter(self._tests)

    def __repr__(self) -> str:
        return f"TestSuite({self.name!r}, tests={len(self)})"


suite = TestSuite("smoke")
suite.add("test_login").add("test_logout").add("test_search")

len(suite)                  # 3
"test_login" in suite       # True
"test_register" in suite    # False
suite[0]                    # "test_login"
list(suite)                 # ["test_login", "test_logout", "test_search"]
for test in suite:
    print(test)
```

---

## Контекстный менеджер: `__enter__` и `__exit__`

Используется в конструкции `with`:

```python
import requests


class APISession:
    """API-сессия как контекстный менеджер."""

    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token
        self._session: requests.Session | None = None

    def __enter__(self) -> "APISession":
        self._session = requests.Session()
        self._session.headers["Authorization"] = f"Bearer {self.token}"
        print(f"Session opened for {self.base_url}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._session:
            self._session.close()
            print("Session closed")
        # Возврат True подавляет исключение, False — пробрасывает дальше
        return False

    def get(self, path: str) -> requests.Response:
        return self._session.get(f"{self.base_url}{path}")


# Использование
with APISession("https://api.example.com", token="abc123") as session:
    response = session.get("/users")
    # При выходе из блока __exit__ вызовется автоматически
```

---

## Арифметические методы

```python
from dataclasses import dataclass


@dataclass
class Money:
    amount: float
    currency: str = "RUB"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract different currencies")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: float) -> "Money":
        return Money(self.amount * factor, self.currency)

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"


price = Money(100.0)
tax = Money(20.0)
total = price + tax          # Money(120.0, "RUB")
discounted = total * 0.9     # Money(108.0, "RUB")
```

---

## Хэширование: `__hash__`

```python
class ProductKey:
    """Используется как ключ словаря."""

    def __init__(self, sku: str, warehouse_id: int) -> None:
        self.sku = sku
        self.warehouse_id = warehouse_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProductKey):
            return NotImplemented
        return self.sku == other.sku and self.warehouse_id == other.warehouse_id

    def __hash__(self) -> int:
        return hash((self.sku, self.warehouse_id))


# Теперь можно использовать как ключ
stock = {
    ProductKey("SKU-001", 1): 50,
    ProductKey("SKU-001", 2): 30,
}
```

> Если определяешь `__eq__`, Python автоматически делает объект нехэшируемым. Нужно явно определить `__hash__`.

---

## Как это выглядит в pytest

```python
import pytest


class APIResponse:
    def __init__(self, status_code: int, body: dict) -> None:
        self.status_code = status_code
        self.body = body

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, APIResponse):
            return NotImplemented
        return self.status_code == other.status_code and self.body == other.body

    def __repr__(self) -> str:
        return f"APIResponse(status={self.status_code}, body={self.body})"

    def __bool__(self) -> bool:
        return 200 <= self.status_code < 300


def test_response_equality():
    r1 = APIResponse(200, {"id": 1, "name": "Alice"})
    r2 = APIResponse(200, {"id": 1, "name": "Alice"})
    r3 = APIResponse(404, {"error": "not found"})

    assert r1 == r2
    assert r1 != r3


def test_response_bool_success():
    response = APIResponse(200, {"ok": True})
    assert response   # bool(response) → True


def test_response_bool_failure():
    response = APIResponse(404, {"error": "not found"})
    assert not response   # bool(response) → False


def test_suite_len_and_contains():
    suite = TestSuite("regression")
    suite.add("test_login").add("test_search")

    assert len(suite) == 2
    assert "test_login" in suite
    assert "test_register" not in suite


def test_suite_iteration():
    suite = TestSuite("smoke")
    suite.add("test_a").add("test_b")

    names = [t for t in suite]
    assert names == ["test_a", "test_b"]
```

---

## Таблица магических методов

| Метод | Вызывается при |
|-------|----------------|
| `__init__` | `obj = Class()` |
| `__str__` | `str(obj)`, `print(obj)` |
| `__repr__` | `repr(obj)`, в отладчике |
| `__eq__` | `obj1 == obj2` |
| `__lt__` | `obj1 < obj2` |
| `__len__` | `len(obj)` |
| `__contains__` | `x in obj` |
| `__getitem__` | `obj[key]` |
| `__setitem__` | `obj[key] = value` |
| `__iter__` | `for x in obj`, `list(obj)` |
| `__bool__` | `bool(obj)`, `if obj:` |
| `__hash__` | `hash(obj)`, использование как ключ dict |
| `__enter__` | `with obj as x:` |
| `__exit__` | выход из блока `with` |
| `__add__` | `obj1 + obj2` |
| `__call__` | `obj()` — вызов объекта как функции |

---

## Вопрос на собесе

**Q: Зачем определять `__repr__` если уже есть `__str__`?**

> `__str__` — для вывода пользователю. `__repr__` — для разработчика, отладки. Если `__str__` не определён, Python использует `__repr__`. В списках и словарях Python всегда использует `__repr__`. Поэтому `__repr__` более важен из двух.

**Q: Что произойдёт с `__hash__` если определить `__eq__`?**

> Если определить только `__eq__`, Python автоматически устанавливает `__hash__ = None`, делая объект нехэшируемым (нельзя использовать как ключ dict или элемент set). Чтобы сохранить хэшируемость, нужно явно определить `__hash__`.
