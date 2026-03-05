# Инкапсуляция (Encapsulation)

> **Зачем автотестеру:** Инкапсуляция скрывает внутреннее состояние объекта. В Page Object `_driver` — приватный атрибут, который не должен изменяться снаружи. `@property` позволяет добавить логику при доступе к данным, не меняя интерфейс.

---

## Концепция

Инкапсуляция — принцип, при котором внутреннее состояние объекта скрыто и доступно только через публичный интерфейс. Это защищает данные от случайного изменения и упрощает контроль над состоянием.

---

## Уровни доступа в Python

Python не имеет строгих модификаторов доступа как Java/C#. Вместо этого используются соглашения:

```python
class User:
    def __init__(self, name: str, age: int, password: str) -> None:
        self.name = name           # публичный — доступен везде
        self._age = age            # "защищённый" — соглашение: не трогать снаружи
        self.__password = password # "приватный" — name mangling

    def get_info(self) -> str:
        return f"{self.name}, {self._age}"

user = User("Alice", 30, "secret")

user.name          # "Alice"  — OK
user._age          # 30       — работает, но не рекомендуется
user.__password    # AttributeError! — name mangling
user._User__password   # "secret" — можно обойти, зная технику
```

### Name Mangling

```python
class BankAccount:
    def __init__(self, balance: float) -> None:
        self.__balance = balance    # → _BankAccount__balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.__balance += amount

    def get_balance(self) -> float:
        return self.__balance
```

---

## `@property` — умные геттеры и сеттеры

`@property` позволяет обращаться к методу как к атрибуту и добавлять валидацию.

### Геттер через @property

```python
class Product:
    def __init__(self, name: str, price: float) -> None:
        self._name = name
        self._price = price

    @property
    def price(self) -> float:
        """Возвращает цену с округлением."""
        return round(self._price, 2)

    @property
    def price_with_vat(self) -> float:
        """Вычисляемый атрибут — не хранится, вычисляется каждый раз."""
        return round(self._price * 1.2, 2)


product = Product("Widget", 9.999)
print(product.price)           # 10.0  — как атрибут, не метод!
print(product.price_with_vat)  # 12.0
```

### Геттер + сеттер + делитер

```python
class User:
    def __init__(self, name: str, age: int) -> None:
        self._name = name
        self._age = age

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0 or value > 150:
            raise ValueError(f"Age {value} is out of range")
        self._age = value

    @age.deleter
    def age(self) -> None:
        self._age = None

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value


user = User("Alice", 30)
user.age = 31       # вызывает setter
user.age = -1       # ValueError!
del user.age        # вызывает deleter
```

---

## Реальный пример: API-клиент с инкапсуляцией

```python
import requests


class APIClient:
    """Клиент для работы с REST API."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._session = requests.Session()
        self._token: str | None = None

    @property
    def is_authenticated(self) -> bool:
        return self._token is not None

    @property
    def base_url(self) -> str:
        return self._base_url

    def authenticate(self, username: str, password: str) -> bool:
        """Аутентификация. Возвращает True при успехе."""
        response = self._session.post(
            f"{self._base_url}/auth/login",
            json={"username": username, "password": password},
        )
        if response.status_code == 200:
            self._token = response.json()["token"]
            self._session.headers["Authorization"] = f"Bearer {self._token}"
            return True
        return False

    def _make_request(self, method: str, path: str, **kwargs) -> requests.Response:
        """Приватный метод — детали реализации запроса."""
        if not self.is_authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        response = self._session.request(method, f"{self._base_url}{path}", **kwargs)
        response.raise_for_status()
        return response

    def get_users(self) -> list[dict]:
        return self._make_request("GET", "/users").json()["items"]

    def create_user(self, data: dict) -> dict:
        return self._make_request("POST", "/users", json=data).json()
```

---

## Как это выглядит в pytest

```python
import pytest


class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError(f"Temperature below absolute zero: {value}")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32


def test_temperature_celsius_getter():
    temp = Temperature(100.0)
    assert temp.celsius == 100.0


def test_temperature_fahrenheit_conversion():
    temp = Temperature(0.0)
    assert temp.fahrenheit == 32.0


def test_temperature_setter_valid():
    temp = Temperature(20.0)
    temp.celsius = 37.0
    assert temp.celsius == 37.0


def test_temperature_setter_invalid():
    temp = Temperature(20.0)
    with pytest.raises(ValueError, match="absolute zero"):
        temp.celsius = -300.0


def test_temperature_direct_access_blocked():
    temp = Temperature(20.0)
    # Попытка обойти инкапсуляцию через _celsius — работает, но это нарушение контракта
    # В тестах проверяем публичный интерфейс, не внутренние атрибуты
    assert temp.celsius == 20.0  # не temp._celsius
```

### Тест API-клиента с инкапсуляцией

```python
@pytest.fixture
def api_client() -> APIClient:
    return APIClient(base_url="https://api.example.com")


def test_client_not_authenticated_by_default(api_client):
    assert not api_client.is_authenticated


def test_client_authenticated_after_login(api_client, requests_mock):
    requests_mock.post(
        "https://api.example.com/auth/login",
        json={"token": "test-token-123"},
    )
    result = api_client.authenticate("admin", "password")
    assert result is True
    assert api_client.is_authenticated


def test_client_raises_if_not_authenticated(api_client):
    with pytest.raises(RuntimeError, match="Not authenticated"):
        api_client.get_users()
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| `@property` без сеттера | `user.age = 31` → AttributeError | Добавь `@age.setter` если нужна запись |
| Прямой доступ к `_attr` | Нарушает инкапсуляцию | В тестах проверяй только публичный интерфейс |
| Сеттер без валидации | Смысл теряется | Добавляй проверки типов и диапазонов |
| `__attr` в подклассе | `self.__token` в подклассе будет `_SubClass__token`, не `_Parent__token` | Используй `_attr` (одно подчёркивание) для защищённых |

---

## Вопрос на собесе

**Q: В чём разница между `_attr` и `__attr`?**

> `_attr` — это соглашение. Один знак подчёркивания сигнализирует: "не использовать снаружи", но доступ технически возможен. `__attr` (два знака) задействует name mangling: Python переименует атрибут в `_ClassName__attr`, что делает случайный доступ снаружи невозможным.

**Q: Зачем `@property` если можно просто напрямую обратиться к атрибуту?**

> `@property` позволяет добавить логику (валидацию, вычисление, кэширование) без изменения публичного интерфейса. Сначала `user.age` был просто атрибутом, потом понадобилась валидация — добавил `@property` и всё работает без изменений в коде вызывающей стороны.
