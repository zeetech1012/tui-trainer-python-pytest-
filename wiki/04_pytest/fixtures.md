# Фикстуры (Fixtures)

> **Зачем автотестеру:** Фикстуры — это механизм подготовки и очистки тестовой среды. Без фикстур каждый тест пишет один и тот же setUp-код. Грамотное использование scope, yield и conftest.py делает тест-сьюит быстрым и поддерживаемым.

---

## Концепция

Фикстура — это функция с декоратором `@pytest.fixture`, которая подготавливает данные или окружение для теста. pytest автоматически передаёт фикстуру в тест, если имя параметра совпадает с именем фикстуры.

---

## Базовый синтаксис

```python
import pytest


@pytest.fixture
def sample_user() -> dict:
    """Тестовый пользователь."""
    return {"id": 1, "name": "Alice", "email": "alice@example.com"}


def test_user_has_name(sample_user: dict):
    # pytest автоматически вызовет sample_user() и передаст результат
    assert sample_user["name"] == "Alice"


def test_user_has_email(sample_user: dict):
    assert "@" in sample_user["email"]
```

---

## yield — setup и teardown

Код до `yield` — это setup (подготовка). Код после `yield` — teardown (очистка). Гарантирует очистку даже при ошибке в тесте.

```python
import pytest
import requests


@pytest.fixture
def api_session() -> requests.Session:
    """Открывает сессию перед тестом, закрывает после."""
    session = requests.Session()
    session.headers["Content-Type"] = "application/json"
    yield session      # ← тест получает session
    session.close()    # ← выполняется после теста


@pytest.fixture
def created_user(api_session: requests.Session) -> dict:
    """Создаёт пользователя и удаляет его после теста."""
    # Setup — создание
    response = api_session.post("https://api.example.com/users", json={
        "name": "Test User",
        "email": "test@example.com",
    })
    user = response.json()

    yield user  # ← тест работает с созданным пользователем

    # Teardown — удаление
    api_session.delete(f"https://api.example.com/users/{user['id']}")


def test_user_was_created(created_user: dict):
    assert "id" in created_user
    assert created_user["name"] == "Test User"
```

---

## Scope — область видимости фикстуры

| Scope | Фикстура создаётся | Использование |
|-------|-------------------|---------------|
| `function` | Для каждого теста (дефолт) | Изолированные данные |
| `class` | Один раз на класс тестов | Общее состояние в классе |
| `module` | Один раз на файл | Общие дорогие операции в файле |
| `session` | Один раз на всю сессию | Аутентификация, БД-соединение |

```python
@pytest.fixture(scope="session")
def auth_token() -> str:
    """Получить токен один раз для всей тестовой сессии."""
    response = requests.post("https://api.example.com/auth/login", json={
        "username": "admin",
        "password": "secret",
    })
    return response.json()["token"]


@pytest.fixture(scope="module")
def user_data(auth_token: str) -> dict:
    """Создать тестового пользователя один раз для всего модуля."""
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {auth_token}"
    response = session.post("https://api.example.com/users", json={
        "name": "Module User",
        "email": "module@example.com",
    })
    user = response.json()
    yield user
    session.delete(f"https://api.example.com/users/{user['id']}")


@pytest.fixture(scope="function")
def fresh_order(auth_token: str) -> dict:
    """Новый заказ для каждого теста."""
    # ...
```

---

## conftest.py — совместные фикстуры

```python
# conftest.py (в корне проекта или папке tests/)
import pytest
import requests


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://api.example.com"


@pytest.fixture(scope="session")
def admin_credentials() -> dict:
    return {"username": "admin", "password": "secret123"}


@pytest.fixture(scope="session")
def auth_token(base_url: str, admin_credentials: dict) -> str:
    response = requests.post(
        f"{base_url}/auth/login",
        json=admin_credentials,
    )
    assert response.status_code == 200, f"Auth failed: {response.text}"
    return response.json()["token"]


@pytest.fixture
def api_client(base_url: str, auth_token: str) -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    })
    yield session
    session.close()
```

---

## Параметризованные фикстуры

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database(request) -> str:
    """Тест будет запущен три раза — для каждой БД."""
    db_type = request.param
    # setup подключения к БД
    connection = create_connection(db_type)
    yield connection
    connection.close()


def test_database_connection(database):
    # Этот тест запустится 3 раза
    assert database.is_connected()
```

---

## `autouse` — автоматическое применение

```python
@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Сбрасывает rate limiter перед каждым тестом."""
    clear_rate_limits()
    yield
    # после теста ничего не нужно


@pytest.fixture(autouse=True, scope="session")
def configure_logging():
    """Настраивает логирование один раз для всей сессии."""
    import logging
    logging.basicConfig(level=logging.DEBUG)
```

---

## Как это выглядит в pytest — реальный пример

```python
# conftest.py
import pytest
import requests

BASE_URL = "https://api.example.com"


@pytest.fixture(scope="session")
def auth_token() -> str:
    resp = requests.post(f"{BASE_URL}/auth/login", json={"username": "admin", "password": "pass"})
    return resp.json()["token"]


@pytest.fixture
def client(auth_token: str) -> requests.Session:
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {auth_token}"
    yield s
    s.close()


@pytest.fixture
def user(client: requests.Session) -> dict:
    resp = client.post(f"{BASE_URL}/users", json={"name": "Temp", "email": "tmp@test.com"})
    data = resp.json()
    yield data
    client.delete(f"{BASE_URL}/users/{data['id']}")


# test_user_crud.py
class TestUserCRUD:
    def test_create_returns_id(self, user: dict):
        assert "id" in user

    def test_read_created_user(self, client: requests.Session, user: dict):
        resp = client.get(f"{BASE_URL}/users/{user['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == user["id"]

    def test_update_user_name(self, client: requests.Session, user: dict):
        resp = client.put(
            f"{BASE_URL}/users/{user['id']}",
            json={"name": "Updated Name"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Name"
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| `scope="session"` с mutable объектом | Состояние протекает между тестами | Используй `scope="function"` для изменяемых данных |
| Фикстура с `yield` при ошибке | teardown всё равно выполнится | Это штатное поведение — `yield` гарантирует cleanup |
| Фикстура не найдена | `fixture 'foo' not found` | Проверь conftest.py на нужном уровне, проверь имя |
| Циклические зависимости | Фикстуры зависят друг от друга по кругу | pytest обнаружит и сообщит об ошибке |

---

## Вопрос на собесе

**Q: Зачем использовать `yield` в фикстуре вместо обычного `return`?**

> `yield` позволяет выполнить код очистки после теста (teardown). Код до `yield` — это setup, после — teardown. При ошибке в тесте teardown **всё равно выполнится**. С `return` нельзя гарантировать очистку.

**Q: Какой scope использовать для фикстуры аутентификации?**

> `scope="session"` — аутентификация дорогостоящая операция, один токен подойдёт для всей сессии тестов. Фикстуры самих тестовых сущностей (создание юзера, заказа) лучше делать `scope="function"` чтобы каждый тест работал с чистыми данными.
