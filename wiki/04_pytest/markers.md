# Маркеры pytest

> **Зачем автотестеру:** Маркеры позволяют группировать и фильтровать тесты — запускать только smoke-тесты перед деплоем, пропускать тесты с известными багами, помечать медленные тесты. Это обязательный инструмент в реальном проекте.

---

## Концепция

Маркер — метка, которую можно повесить на тест. Маркеры используются для:
- Фильтрации: `pytest -m smoke`
- Пропуска: `@pytest.mark.skip`
- Ожидаемого падения: `@pytest.mark.xfail`
- Кастомной логики: `@pytest.mark.slow`

---

## Встроенные маркеры

### `@pytest.mark.skip` — пропустить тест

```python
import pytest


@pytest.mark.skip(reason="Фича в разработке, тест временно отключён")
def test_new_payment_flow():
    ...


# Условный пропуск
import sys

@pytest.mark.skipif(sys.platform == "win32", reason="Тест не работает на Windows")
def test_unix_file_permissions():
    ...


@pytest.mark.skipif(
    condition=not is_service_available("https://api.example.com"),
    reason="Сервис недоступен в этом окружении",
)
def test_external_api():
    ...
```

### `@pytest.mark.xfail` — ожидаемое падение

```python
@pytest.mark.xfail(reason="Известный баг BUG-1234, ожидаем фикс в v2.5")
def test_discount_calculation_edge_case():
    # Если тест упадёт — xfail (ожидаемо), пройдёт — xpass (неожиданный успех)
    result = calculate_discount(price=0, discount=0.5)
    assert result == 0.0


@pytest.mark.xfail(strict=True, reason="Должен падать пока не реализовано")
def test_unimplemented_feature():
    # strict=True: если тест ПРОШЁЛ — это ошибка (xpass становится FAIL)
    ...


@pytest.mark.xfail(raises=ValueError, reason="Ожидаем ValueError")
def test_raises_value_error():
    parse_negative_count(-1)
```

### `@pytest.mark.parametrize` — параметризация

> Подробнее в [статье о параметризации](parametrize.md).

---

## Кастомные маркеры

### 1. Регистрация в `pytest.ini`

```ini
# pytest.ini
[pytest]
markers =
    smoke: Быстрые проверки основной функциональности (запускать перед деплоем)
    regression: Полная регрессия
    slow: Тесты выполняющиеся дольше 5 секунд
    integration: Тесты, требующие внешних сервисов
    unit: Изолированные юнит-тесты без внешних зависимостей
    critical: Критические бизнес-сценарии
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "smoke: быстрые проверки основной функциональности",
    "regression: полная регрессия",
    "slow: тесты > 5 сек",
    "integration: требуют внешних сервисов",
]
```

### 2. Применение маркеров

```python
import pytest


@pytest.mark.smoke
def test_health_check(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200


@pytest.mark.smoke
@pytest.mark.critical
def test_user_login(api_client):
    response = api_client.post("/auth/login", json={"username": "admin", "password": "pass"})
    assert response.status_code == 200
    assert "token" in response.json()


@pytest.mark.regression
def test_full_order_flow(api_client):
    # Долгий e2e тест
    ...


@pytest.mark.slow
@pytest.mark.integration
def test_bulk_import(api_client):
    # Загрузка 10000 записей
    ...
```

### 3. Запуск по маркеру

```bash
# Только smoke
pytest -m smoke

# Только smoke И critical
pytest -m "smoke and critical"

# smoke ИЛИ critical
pytest -m "smoke or critical"

# Всё кроме slow
pytest -m "not slow"

# Не integration и не slow
pytest -m "not (integration or slow)"
```

---

## Маркеры на уровне класса и модуля

```python
# Маркер для всего класса
@pytest.mark.smoke
class TestHealthChecks:
    def test_api_is_up(self, api_client):
        response = api_client.get("/health")
        assert response.status_code == 200

    def test_database_is_up(self, api_client):
        response = api_client.get("/health/db")
        assert response.status_code == 200


# Маркер для всего модуля — через переменную pytestmark
pytestmark = pytest.mark.integration  # применяется ко всем тестам в файле

# Несколько маркеров для модуля
pytestmark = [pytest.mark.integration, pytest.mark.slow]
```

---

## conftest.py — автоматические маркеры

```python
# conftest.py
import pytest


def pytest_collection_modifyitems(items):
    """Автоматически помечает тесты в папке tests/slow/ как @pytest.mark.slow."""
    for item in items:
        if "slow" in str(item.fspath):
            item.add_marker(pytest.mark.slow)
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
```

---

## `pytest.mark.usefixtures` — применить фикстуру без аргумента

```python
@pytest.fixture(autouse=False)
def reset_database():
    """Очищает БД перед тестом."""
    clear_test_data()
    yield
    clear_test_data()


# Применить фикстуру к классу без autouse
@pytest.mark.usefixtures("reset_database")
class TestOrderCreation:
    def test_create_order(self, api_client):
        ...

    def test_create_bulk_orders(self, api_client):
        ...
```

---

## Реальная конфигурация проекта

```ini
# pytest.ini
[pytest]
testpaths = tests
addopts = -v --tb=short -ra
markers =
    smoke: Smoke-тесты, запускать перед каждым деплоем
    regression: Регрессионные тесты, запускать на ночь
    unit: Юнит-тесты без внешних зависимостей
    integration: Интеграционные тесты с реальными сервисами
    slow: Тесты дольше 10 секунд
    critical: Критичные для бизнеса сценарии
    wip: Work in progress — временно пропускать
```

```python
# conftest.py
import pytest


@pytest.fixture(scope="session", autouse=True)
def check_environment():
    """Проверяет окружение перед запуском тестов."""
    import os
    env = os.getenv("TEST_ENV", "local")
    print(f"\nRunning tests in {env} environment")


def pytest_configure(config):
    """Регистрация маркеров программно."""
    config.addinivalue_line("markers", "smoke: smoke tests")
    config.addinivalue_line("markers", "slow: slow tests")
```

---

## Тест с несколькими маркерами — полный пример

```python
import pytest


pytestmark = pytest.mark.integration


@pytest.mark.smoke
@pytest.mark.critical
def test_create_user_flow(api_client):
    # 1. Создать
    create_resp = api_client.post("/users", json={"name": "Alice", "email": "a@a.com"})
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    # 2. Прочитать
    get_resp = api_client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200

    # 3. Удалить
    del_resp = api_client.delete(f"/users/{user_id}")
    assert del_resp.status_code == 204


@pytest.mark.xfail(reason="BUG-2345: скидка не применяется к нулевой цене")
def test_zero_price_with_discount(api_client):
    response = api_client.post("/orders", json={"price": 0, "discount": 0.1})
    assert response.json()["total"] == 0.0


@pytest.mark.skip(reason="Сервис оплаты не подключён в test-окружении")
def test_payment_processing(api_client):
    ...


@pytest.mark.slow
def test_import_large_catalog(api_client):
    # Загрузка 50000 товаров
    ...
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| Незарегистрированный маркер | `PytestUnknownMarkWarning` | Зарегистрируй в `pytest.ini` |
| `xfail` без reason | Нет контекста зачем тест xfail | Всегда добавляй `reason=` с номером задачи |
| Слишком много маркеров | Тяжело поддерживать | Не более 3 маркеров на тест |

---

## Вопрос на собесе

**Q: В чём разница между `skip` и `xfail`?**

> `skip` — тест не запускается вообще. `xfail` — тест запускается, и ожидается что упадёт. Если он упал — `xfail` (нормально). Если прошёл — `xpass` (неожиданно, может быть ошибкой при `strict=True`). `xfail` используют для документирования известных багов.

**Q: Как запустить только критические smoke-тесты?**

```bash
pytest -m "smoke and critical" -v
```
