# Классы в Python

> **Зачем автотестеру:** Классы — основа Page Object Model (POM) и любого фреймворка для тестирования. Каждый Page Object, API-клиент, база данных фикстур — это класс. Понимание `__init__`, атрибутов и методов обязательно.

---

## Концепция

Класс — шаблон для создания объектов. Объект (экземпляр) создаётся по этому шаблону и имеет свои данные (атрибуты) и поведение (методы).

---

## Базовый синтаксис

```python
class User:
    """Представляет пользователя системы."""

    # Атрибут класса — общий для всех экземпляров
    default_role: str = "viewer"

    def __init__(self, name: str, email: str, age: int) -> None:
        # Атрибуты экземпляра — уникальны для каждого объекта
        self.name = name
        self.email = email
        self.age = age
        self.is_active: bool = True     # дефолтное значение

    def deactivate(self) -> None:
        """Деактивирует пользователя."""
        self.is_active = False

    def greet(self) -> str:
        return f"Hi, I'm {self.name} ({self.email})"


# Создание экземпляра
alice = User(name="Alice", email="alice@example.com", age=30)
bob = User("Bob", "bob@example.com", 25)

# Доступ к атрибутам
print(alice.name)        # "Alice"
print(alice.is_active)   # True

# Вызов метода
alice.deactivate()
print(alice.is_active)   # False
```

---

## Атрибуты класса vs атрибуты экземпляра

```python
class Counter:
    total_count: int = 0    # атрибут класса — общий

    def __init__(self, name: str) -> None:
        self.name = name    # атрибут экземпляра — уникальный
        Counter.total_count += 1

c1 = Counter("first")
c2 = Counter("second")

print(Counter.total_count)   # 2  — через класс
print(c1.total_count)        # 2  — через экземпляр (читает атрибут класса)
print(c1.name)               # "first"
print(c2.name)               # "second"
```

> **Ловушка:** мутабельный атрибут класса (список, dict) делится между всеми экземплярами!

```python
class BadExample:
    items = []   # ПЛОХО — общий для всех!

class GoodExample:
    def __init__(self) -> None:
        self.items = []   # ХОРОШО — у каждого своё
```

---

## Методы

### Методы экземпляра — `self`

```python
class OrderService:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session = None

    def get_order(self, order_id: int) -> dict:
        # self — ссылка на текущий экземпляр
        return {"id": order_id, "url": f"{self.base_url}/orders/{order_id}"}
```

### Методы класса — `@classmethod` и `cls`

```python
class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Альтернативный конструктор из словаря."""
        return cls(name=data["name"], price=data["price"])

    @classmethod
    def free(cls, name: str) -> "Product":
        """Создать бесплатный продукт."""
        return cls(name=name, price=0.0)


# Использование
product = Product.from_dict({"name": "Widget", "price": 9.99})
free_item = Product.free("Promo item")
```

### Статические методы — `@staticmethod`

```python
class Validator:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        return "@" in email and "." in email.split("@")[-1]

    @staticmethod
    def is_valid_price(price: float) -> bool:
        return isinstance(price, (int, float)) and price >= 0


# Не нужен экземпляр или класс
Validator.is_valid_email("test@example.com")   # True
```

---

## `__repr__` и `__str__`

```python
class Order:
    def __init__(self, order_id: int, total: float) -> None:
        self.order_id = order_id
        self.total = total

    def __repr__(self) -> str:
        # Для разработчиков — точное представление
        return f"Order(order_id={self.order_id!r}, total={self.total!r})"

    def __str__(self) -> str:
        # Для пользователей — читаемое представление
        return f"Order #{self.order_id} — {self.total:.2f} ₽"


order = Order(42, 1500.0)
print(order)          # "Order #42 — 1500.00 ₽"  — использует __str__
print(repr(order))    # "Order(order_id=42, total=1500.0)"  — использует __repr__
```

---

## dataclass — современный способ создания классов данных

```python
from dataclasses import dataclass, field


@dataclass
class UserDTO:
    id: int
    name: str
    email: str
    is_active: bool = True
    tags: list[str] = field(default_factory=list)


# Автоматически создаётся __init__, __repr__, __eq__
user = UserDTO(id=1, name="Alice", email="alice@example.com")
print(user)   # UserDTO(id=1, name='Alice', email='alice@example.com', is_active=True, tags=[])
```

---

## Как это выглядит в pytest

### Page Object с классом

```python
class LoginPage:
    """Page Object для страницы входа."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self._last_response = None

    def login(self, username: str, password: str) -> "LoginPage":
        """Выполняет вход. Возвращает self для chaining."""
        import requests
        self._last_response = requests.post(
            f"{self.base_url}/auth/login",
            json={"username": username, "password": password},
        )
        return self

    @property
    def is_logged_in(self) -> bool:
        return self._last_response is not None and self._last_response.status_code == 200

    @property
    def token(self) -> str | None:
        if self.is_logged_in:
            return self._last_response.json().get("token")
        return None


import pytest


@pytest.fixture
def login_page() -> LoginPage:
    return LoginPage(base_url="https://api.example.com")


def test_successful_login(login_page):
    login_page.login("admin", "secret")
    assert login_page.is_logged_in
    assert login_page.token is not None


def test_failed_login(login_page):
    login_page.login("admin", "wrong_password")
    assert not login_page.is_logged_in
```

### `@classmethod` как фабрика тестовых данных

```python
from dataclasses import dataclass


@dataclass
class OrderPayload:
    product_id: int
    quantity: int
    address: str

    @classmethod
    def default(cls) -> "OrderPayload":
        return cls(product_id=1, quantity=1, address="Moscow, Lenina 1")

    @classmethod
    def bulk(cls, product_id: int) -> "OrderPayload":
        return cls(product_id=product_id, quantity=100, address="Moscow, Lenina 1")


def test_create_default_order(api_client):
    payload = OrderPayload.default()
    response = api_client.post("/orders", json=vars(payload))
    assert response.status_code == 201


def test_create_bulk_order(api_client):
    payload = OrderPayload.bulk(product_id=5)
    response = api_client.post("/orders", json=vars(payload))
    assert response.json()["quantity"] == 100
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| Мутабельный атрибут класса | Все экземпляры делят один список | Инициализируй в `__init__` |
| `self` — забыть | `def method(name)` вместо `def method(self, name)` | `TypeError` при вызове |
| Изменяемый дефолт в `@dataclass` | `field: list = []` — ошибка | Используй `field(default_factory=list)` |

---

## Вопрос на собесе

**Q: В чём разница между атрибутом класса и атрибутом экземпляра?**

> Атрибут класса определяется в теле класса вне методов — он общий для всех экземпляров. Атрибут экземпляра определяется через `self` обычно в `__init__` — он уникален для каждого объекта.

**Q: Когда использовать `@classmethod` vs `@staticmethod`?**

> `@classmethod` получает `cls` и может создавать экземпляры класса — используется для альтернативных конструкторов. `@staticmethod` не получает ни `self` ни `cls` — это обычная функция внутри класса, логически с ним связанная (например, валидатор).
