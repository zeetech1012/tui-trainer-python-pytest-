# Наследование (Inheritance)

> **Зачем автотестеру:** Наследование — основа Page Object Model. `BasePage` содержит общие методы (открыть страницу, ждать элемент), а `LoginPage`, `CartPage` наследуют их. В pytest фреймворках базовые классы тестов задают `setUp`/`tearDown` логику.

---

## Концепция

Наследование позволяет дочернему классу получить все атрибуты и методы родительского класса и расширить или переопределить их.

```
BasePage          ← родительский класс (parent / superclass)
    ├── LoginPage ← дочерний класс (child / subclass)
    ├── CartPage
    └── ProductPage
```

---

## Базовый синтаксис

```python
class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        return f"{self.name} makes a sound"


class Dog(Animal):   # Dog наследует от Animal
    def speak(self) -> str:
        return f"{self.name} says: Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says: Meow!"


dog = Dog("Rex")
cat = Cat("Whiskers")

dog.speak()   # "Rex says: Woof!"
cat.speak()   # "Whiskers says: Meow!"
dog.name      # "Rex" — унаследован от Animal
```

---

## `super()` — вызов родительского метода

```python
class Vehicle:
    def __init__(self, brand: str, speed: int) -> None:
        self.brand = brand
        self.speed = speed

    def describe(self) -> str:
        return f"{self.brand}, max speed: {self.speed} km/h"


class ElectricCar(Vehicle):
    def __init__(self, brand: str, speed: int, battery_kwh: int) -> None:
        super().__init__(brand, speed)      # вызываем __init__ родителя
        self.battery_kwh = battery_kwh      # добавляем своё

    def describe(self) -> str:
        base = super().describe()           # берём текст от родителя
        return f"{base}, battery: {self.battery_kwh} kWh"


tesla = ElectricCar("Tesla", 250, 100)
tesla.describe()
# "Tesla, max speed: 250 km/h, battery: 100 kWh"
```

---

## Проверка типов

```python
class Animal: pass
class Dog(Animal): pass

dog = Dog()

isinstance(dog, Dog)      # True — dog является Dog
isinstance(dog, Animal)   # True — dog является и Animal (через наследование)
isinstance(dog, str)      # False

issubclass(Dog, Animal)   # True — Dog наследует от Animal
issubclass(Animal, Dog)   # False
```

---

## MRO — Method Resolution Order

Python определяет порядок поиска методов при множественном наследовании по алгоритму C3 linearization.

```python
class A:
    def method(self): return "A"

class B(A):
    def method(self): return "B"

class C(A):
    def method(self): return "C"

class D(B, C):   # множественное наследование
    pass


d = D()
d.method()   # "B" — B идёт первым в D(B, C)

# Посмотреть порядок поиска
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

---

## Page Object Model — реальный пример

```python
import requests


class BasePage:
    """Базовый Page Object с общими методами для API-тестов."""

    def __init__(self, base_url: str, token: str | None = None) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.session.get(f"{self.base_url}{path}", **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.session.post(f"{self.base_url}{path}", **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.session.put(f"{self.base_url}{path}", **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.session.delete(f"{self.base_url}{path}", **kwargs)


class UserService(BasePage):
    """Сервис для работы с пользователями."""

    def get_user(self, user_id: int) -> dict:
        response = self.get(f"/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def create_user(self, name: str, email: str) -> dict:
        response = self.post("/users", json={"name": name, "email": email})
        response.raise_for_status()
        return response.json()

    def delete_user(self, user_id: int) -> None:
        self.delete(f"/users/{user_id}").raise_for_status()


class OrderService(BasePage):
    """Сервис для работы с заказами."""

    def get_orders(self, user_id: int) -> list[dict]:
        response = self.get(f"/users/{user_id}/orders")
        response.raise_for_status()
        return response.json()["items"]

    def create_order(self, user_id: int, product_id: int, qty: int) -> dict:
        response = self.post("/orders", json={
            "user_id": user_id,
            "product_id": product_id,
            "quantity": qty,
        })
        response.raise_for_status()
        return response.json()
```

---

## Как это выглядит в pytest

```python
import pytest


BASE_URL = "https://api.example.com"


@pytest.fixture
def user_service() -> UserService:
    return UserService(base_url=BASE_URL)


@pytest.fixture
def order_service() -> OrderService:
    return OrderService(base_url=BASE_URL)


@pytest.fixture
def auth_user_service(auth_token: str) -> UserService:
    return UserService(base_url=BASE_URL, token=auth_token)


def test_get_user_returns_correct_id(user_service):
    user = user_service.get_user(1)
    assert user["id"] == 1


def test_create_and_delete_user(user_service):
    created = user_service.create_user("Test User", "test@example.com")
    user_id = created["id"]

    user_service.delete_user(user_id)

    with pytest.raises(Exception):
        user_service.get_user(user_id)


def test_user_service_inherits_session(user_service):
    # Проверяем что UserService наследует метод get от BasePage
    assert hasattr(user_service, "get")
    assert isinstance(user_service, BasePage)


def test_order_service_is_base_page():
    service = OrderService(base_url=BASE_URL)
    assert isinstance(service, BasePage)
    assert issubclass(OrderService, BasePage)
```

### Базовый класс тестов (unittest-стиль)

```python
import pytest


class BaseAPITest:
    """Базовый класс для всех API-тестов."""

    BASE_URL = "https://api.example.com"

    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Настройка сессии перед каждым тестом."""
        self.client = requests.Session()
        self.client.headers["Content-Type"] = "application/json"
        yield
        self.client.close()


class TestUserAPI(BaseAPITest):
    def test_get_users_list(self):
        response = self.client.get(f"{self.BASE_URL}/users")
        assert response.status_code == 200

    def test_users_list_not_empty(self):
        response = self.client.get(f"{self.BASE_URL}/users")
        assert len(response.json()["items"]) > 0


class TestOrderAPI(BaseAPITest):
    def test_get_orders(self):
        response = self.client.get(f"{self.BASE_URL}/orders")
        assert response.status_code == 200
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| Забыть `super().__init__()` | Атрибуты родителя не инициализированы | Всегда вызывай `super().__init__()` первым |
| Ромбовидное наследование | Метод вызывается дважды без `super()` | Используй `super()` — C3 MRO решит порядок |
| Переопределение метода без `super()` | Теряется поведение родителя | Осознанно: либо заменяешь, либо расширяешь через `super()` |

---

## Вопрос на собесе

**Q: Зачем использовать `super()` вместо явного вызова родительского класса?**

> `super()` правильно работает при множественном наследовании — следует MRO и не вызывает метод дважды. Явный вызов `ParentClass.__init__(self)` нарушит порядок MRO.

**Q: Как проверить, является ли объект экземпляром класса или его подкласса?**

> `isinstance(obj, ClassName)` — возвращает `True` для самого класса и всех его подклассов. `type(obj) is ClassName` — возвращает `True` только для точного класса, не подклассов.
