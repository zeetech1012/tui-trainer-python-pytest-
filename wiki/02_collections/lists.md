# Списки (list)

> **Зачем автотестеру:** Списки хранят тестовые данные, параметры для параметризации, коллекции ответов API. Умение быстро фильтровать, сортировать и трансформировать списки — ключевой навык на собесе.

---

## Концепция

`list` — изменяемая упорядоченная последовательность произвольных объектов. Индексируется с нуля. Поддерживает дубликаты.

```python
items: list[str] = ["apple", "banana", "cherry"]
mixed: list = [1, "two", 3.0, None, True]
empty: list = []
```

---

## Создание списков

```python
# Литерал
fruits = ["apple", "banana", "cherry"]

# Из другой коллекции
numbers = list(range(1, 6))      # [1, 2, 3, 4, 5]
chars = list("hello")            # ["h", "e", "l", "l", "o"]

# Повторение
zeros = [0] * 5                  # [0, 0, 0, 0, 0]
```

---

## Индексация и срезы

```python
lst = [10, 20, 30, 40, 50]

lst[0]       # 10  — первый
lst[-1]      # 50  — последний
lst[1:3]     # [20, 30]  — с 1 по 2 включительно
lst[:2]      # [10, 20]  — первые 2
lst[2:]      # [30, 40, 50]  — с 3-го до конца
lst[::2]     # [10, 30, 50]  — каждый второй
lst[::-1]    # [50, 40, 30, 20, 10]  — реверс
```

---

## Основные методы

| Метод | Описание | Пример |
|-------|----------|--------|
| `append(x)` | Добавить в конец | `lst.append(6)` |
| `insert(i, x)` | Вставить на позицию `i` | `lst.insert(0, 0)` |
| `extend(iterable)` | Добавить все элементы | `lst.extend([7, 8])` |
| `remove(x)` | Удалить первый x | `lst.remove(3)` |
| `pop(i=-1)` | Удалить и вернуть по индексу | `lst.pop()` |
| `index(x)` | Индекс первого x | `lst.index(30)` |
| `count(x)` | Число вхождений x | `lst.count(2)` |
| `sort()` | Сортировка на месте | `lst.sort()` |
| `reverse()` | Реверс на месте | `lst.reverse()` |
| `copy()` | Поверхностная копия | `new = lst.copy()` |
| `clear()` | Очистить список | `lst.clear()` |
| `len(lst)` | Длина | `len(lst)` |

---

## `sort()` vs `sorted()`

```python
lst = [3, 1, 4, 1, 5, 9, 2]

# sort() — изменяет оригинал, возвращает None
lst.sort()              # [1, 1, 2, 3, 4, 5, 9]
lst.sort(reverse=True)  # [9, 5, 4, 3, 2, 1, 1]

# sorted() — возвращает новый список, оригинал не трогает
original = [3, 1, 4]
new_lst = sorted(original)         # [1, 3, 4]
print(original)                    # [3, 1, 4] — не изменился

# Сортировка по ключу
users = [
    {"name": "Charlie", "age": 30},
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 35},
]
by_age = sorted(users, key=lambda u: u["age"])
by_name = sorted(users, key=lambda u: u["name"])
```

---

## Копирование: поверхностное vs глубокое

```python
import copy

original = [[1, 2], [3, 4]]

# Поверхностная копия — вложенные объекты общие
shallow = original.copy()
shallow[0].append(99)   # меняет и original[0]!

# Глубокая копия — полностью независимая
deep = copy.deepcopy(original)
deep[0].append(99)      # original[0] не изменился
```

---

## Полезные функции для списков

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

min(numbers)        # 1
max(numbers)        # 9
sum(numbers)        # 31
len(numbers)        # 8

any(n > 8 for n in numbers)   # True — есть ли хоть одно > 8
all(n > 0 for n in numbers)   # True — все ли > 0

# zip — объединение двух списков
keys = ["id", "name", "status"]
values = [1, "Alice", "active"]
combined = dict(zip(keys, values))
# {"id": 1, "name": "Alice", "status": "active"}

# enumerate
for i, item in enumerate(["a", "b", "c"], start=1):
    print(f"{i}. {item}")
# 1. a
# 2. b
# 3. c
```

---

## Как это выглядит в pytest

### Проверка списка из API-ответа

```python
import pytest


def get_active_users(users: list[dict]) -> list[dict]:
    """Возвращает только активных пользователей."""
    return [u for u in users if u.get("is_active")]


@pytest.fixture
def sample_users() -> list[dict]:
    return [
        {"id": 1, "name": "Alice", "is_active": True},
        {"id": 2, "name": "Bob", "is_active": False},
        {"id": 3, "name": "Charlie", "is_active": True},
    ]


def test_get_active_users_count(sample_users):
    result = get_active_users(sample_users)
    assert len(result) == 2


def test_get_active_users_names(sample_users):
    result = get_active_users(sample_users)
    names = [u["name"] for u in result]
    assert names == ["Alice", "Charlie"]


def test_get_active_users_empty_list():
    assert get_active_users([]) == []


def test_get_active_users_all_inactive():
    users = [{"id": 1, "name": "Bob", "is_active": False}]
    assert get_active_users(users) == []
```

### Тест сортировки результатов API

```python
def test_orders_sorted_by_date(api_client):
    response = api_client.get("/orders?sort=created_at")
    orders = response.json()["items"]

    dates = [o["created_at"] for o in orders]
    assert dates == sorted(dates), "Orders should be sorted by created_at"


def test_products_contain_expected_ids(api_client):
    response = api_client.get("/products")
    product_ids = [p["id"] for p in response.json()["items"]]

    expected_ids = [1, 2, 3]
    assert all(pid in product_ids for pid in expected_ids)
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| `lst[5]` при `len(lst) == 3` | `IndexError` | Проверяй `len()` или используй `get` паттерн |
| `lst.remove(x)` при отсутствии x | `ValueError` | Проверяй `if x in lst` перед удалением |
| Изменение списка во время итерации | Пропуск элементов | Итерируйся по копии: `for x in lst.copy()` |
| `a = b = []` | Один объект — две переменные | Используй `a, b = [], []` |
| `[None] * 3` vs `[[]] * 3` | `[[]] * 3` — три ссылки на один список | Используй comprehension: `[[] for _ in range(3)]` |

---

## Вопрос на собесе

**Q: В чём разница между `append()` и `extend()`?**

> `append(x)` добавляет один элемент (даже если это список — он добавится как вложенный). `extend(iterable)` разворачивает итерабельный объект и добавляет каждый его элемент.

```python
lst = [1, 2]
lst.append([3, 4])   # [1, 2, [3, 4]]
lst.extend([3, 4])   # [1, 2, 3, 4]
```

**Q: Как удалить дубликаты из списка сохранив порядок?**

```python
def deduplicate(lst: list) -> list:
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]
```
