# Множества и кортежи (set, tuple)

> **Зачем автотестеру:** `set` идеален для поиска дубликатов и уникальных значений в ответах API. `tuple` используется для неизменяемых данных — фикстур, конфигурации, ключей словарей.

---

## Множества (set)

### Концепция

`set` — неупорядоченная коллекция уникальных хэшируемых объектов. Основное преимущество — поиск элемента выполняется за O(1).

```python
# Создание
fruits: set[str] = {"apple", "banana", "cherry"}
empty_set = set()          # не {} — это пустой dict!
from_list = set([1, 2, 2, 3, 3])   # {1, 2, 3}
```

### Операции над множествами

```python
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}

# Объединение (все элементы)
a | b          # {1, 2, 3, 4, 5, 6, 7}
a.union(b)

# Пересечение (общие элементы)
a & b          # {3, 4, 5}
a.intersection(b)

# Разность (в a, но не в b)
a - b          # {1, 2}
a.difference(b)

# Симметричная разность (в одном, но не в обоих)
a ^ b          # {1, 2, 6, 7}
a.symmetric_difference(b)

# Проверки
a.issubset(b)          # a ⊆ b?
a.issuperset(b)        # a ⊇ b?
a.isdisjoint(b)        # нет общих элементов?
```

### Методы set

| Метод | Описание |
|-------|----------|
| `add(x)` | Добавить элемент |
| `remove(x)` | Удалить (KeyError если нет) |
| `discard(x)` | Удалить (без ошибки если нет) |
| `pop()` | Удалить произвольный элемент |
| `clear()` | Очистить |
| `copy()` | Поверхностная копия |
| `len(s)` | Размер |
| `x in s` | Проверка вхождения — O(1) |

### `frozenset` — неизменяемое множество

```python
# Можно использовать как ключ словаря или элемент другого set
immutable = frozenset([1, 2, 3])
d = {frozenset([1, 2]): "pair"}
```

---

## Кортежи (tuple)

### Концепция

`tuple` — неизменяемая упорядоченная последовательность. После создания изменить нельзя. Используется для групп данных, которые не должны меняться.

```python
# Создание
point = (10, 20)
rgb = (255, 128, 0)
single = (42,)         # запятая обязательна для кортежа из 1 элемента!
empty = ()

# Без скобок (tuple packing)
coordinates = 10, 20, 30   # это тоже tuple
```

### Распаковка (unpacking)

```python
x, y = (10, 20)
first, *rest = (1, 2, 3, 4, 5)   # first=1, rest=[2,3,4,5]
*head, last = (1, 2, 3, 4, 5)    # head=[1,2,3,4], last=5

# Swap переменных
a, b = 1, 2
a, b = b, a   # a=2, b=1

# Игнорирование значений
_, y, _ = (10, 20, 30)   # берём только y
```

### Tuple vs List

| | tuple | list |
|--|-------|------|
| Изменяемость | нет | да |
| Скорость | быстрее | медленнее |
| Использование памяти | меньше | больше |
| Как ключ dict | можно | нельзя |
| Назначение | неизменяемые данные | изменяемые коллекции |

---

## Практические паттерны

### Поиск дубликатов в списке

```python
def find_duplicates(items: list) -> list:
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)

find_duplicates([1, 2, 3, 2, 4, 3])   # [2, 3]
```

### Уникальные значения с сохранением порядка

```python
def unique_ordered(items: list) -> list:
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]

unique_ordered([3, 1, 4, 1, 5, 9, 2, 6, 5])   # [3, 1, 4, 5, 9, 2, 6]
```

### Проверка что все элементы уникальны

```python
def all_unique(items: list) -> bool:
    return len(items) == len(set(items))
```

### namedtuple — tuple с именованными полями

```python
from collections import namedtuple
from typing import NamedTuple

# Старый стиль
Point = namedtuple("Point", ["x", "y"])

# Современный стиль (с type hints)
class Coordinate(NamedTuple):
    x: float
    y: float
    label: str = ""

p = Coordinate(10.5, 20.3, "center")
print(p.x)        # 10.5
print(p[0])       # 10.5 — работает и как tuple
x, y, _ = p      # распаковка
```

---

## Как это выглядит в pytest

### Тест поиска дубликатов в API-ответе

```python
import pytest


def find_duplicates(items: list) -> set:
    seen: set = set()
    duplicates: set = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return duplicates


def test_find_duplicates_with_duplicates():
    assert find_duplicates([1, 2, 3, 2, 4, 3]) == {2, 3}


def test_find_duplicates_no_duplicates():
    assert find_duplicates([1, 2, 3]) == set()


def test_find_duplicates_empty():
    assert find_duplicates([]) == set()


def test_find_duplicates_all_same():
    assert find_duplicates([5, 5, 5]) == {5}


def test_api_response_ids_are_unique(api_client):
    response = api_client.get("/products")
    product_ids = [p["id"] for p in response.json()["items"]]
    assert len(product_ids) == len(set(product_ids)), "Duplicate IDs found"
```

### Использование tuple в фикстурах

```python
from collections import namedtuple

Credentials = namedtuple("Credentials", ["username", "password"])


@pytest.fixture
def admin_credentials() -> Credentials:
    return Credentials(username="admin", password="secret123")


@pytest.fixture
def user_credentials() -> Credentials:
    return Credentials(username="alice", password="pass456")


def test_admin_login(api_client, admin_credentials):
    response = api_client.post("/auth/login", json={
        "username": admin_credentials.username,
        "password": admin_credentials.password,
    })
    assert response.status_code == 200
```

### Тест операций над множествами

```python
def test_required_fields_present():
    response_fields = {"id", "name", "email", "created_at", "role"}
    required = {"id", "name", "email"}
    missing = required - response_fields
    assert missing == set(), f"Missing fields: {missing}"


def test_no_unexpected_fields():
    response_fields = {"id", "name", "email"}
    allowed = {"id", "name", "email", "created_at", "role"}
    unexpected = response_fields - allowed
    assert unexpected == set(), f"Unexpected fields: {unexpected}"
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| `set()` vs `{}` | `{}` создаёт пустой dict | Всегда `set()` для пустого множества |
| `(42)` — не кортеж | Это просто `42` в скобках | `(42,)` — обязательна запятая |
| `set` из нехэшируемых | `set([[1,2]])` — TypeError | Конвертируй в tuple: `set(tuple(x) for x in lst)` |
| `tuple` с изменяемыми | `(1, [2, 3])` — можно изменить список внутри | Данные внутри неизменяемого могут быть изменяемы |

---

## Вопрос на собесе

**Q: Как проверить, что два списка содержат одинаковые элементы без учёта порядка?**

```python
def same_elements(a: list, b: list) -> bool:
    return set(a) == set(b)

# Или с учётом дубликатов — через Counter:
from collections import Counter
def same_elements_with_count(a: list, b: list) -> bool:
    return Counter(a) == Counter(b)
```

**Q: В чём разница между `remove()` и `discard()` для set?**

> `remove(x)` бросает `KeyError` если элемент не найден. `discard(x)` ничего не делает если элемента нет. В тестовом коде предпочтительнее `discard()`, если неизвестно наличие элемента.
