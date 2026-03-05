# Comprehensions и генераторы

> **Зачем автотестеру:** Comprehensions — это быстрый и питонический способ трансформировать данные. В тестах они используются для подготовки тестовых данных, фильтрации ответов API, создания параметров. На собесе это один из самых частых топиков.

---

## List Comprehension

### Базовый синтаксис

```python
# Обычный цикл
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension — то же самое, в одну строку
squares = [x ** 2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### С условием фильтрации

```python
# [выражение for элемент in итерабл if условие]
evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

### С условием в выражении (тернарный оператор)

```python
# [значение_если_true if условие else значение_если_false for ...]
labels = ["even" if x % 2 == 0 else "odd" for x in range(6)]
# ["even", "odd", "even", "odd", "even", "odd"]
```

### Вложенные comprehensions (nested)

```python
# Flatten: список списков → плоский список
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Декартово произведение
colors = ["red", "blue"]
sizes = ["S", "M", "L"]
variants = [(c, s) for c in colors for s in sizes]
# [("red","S"), ("red","M"), ("red","L"), ("blue","S"), ...]
```

---

## Dict Comprehension

```python
# {ключ: значение for элемент in итерабл}
squares_dict = {x: x ** 2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Трансформация словаря — ключи в верхний регистр
raw = {"name": "alice", "role": "admin"}
upper_keys = {k.upper(): v for k, v in raw.items()}
# {"NAME": "alice", "ROLE": "admin"}

# Фильтрация словаря — только пары с непустым значением
data = {"name": "Alice", "email": "", "phone": None, "city": "Moscow"}
clean = {k: v for k, v in data.items() if v}
# {"name": "Alice", "city": "Moscow"}

# Инвертирование словаря (значение → ключ)
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
# {1: "a", 2: "b", 3: "c"}
```

---

## Set Comprehension

```python
# {выражение for элемент in итерабл}
unique_lengths = {len(word) for word in ["cat", "dog", "elephant", "ox"]}
# {2, 3, 8}

# Уникальные домены email
emails = ["alice@example.com", "bob@test.com", "charlie@example.com"]
domains = {email.split("@")[1] for email in emails}
# {"example.com", "test.com"}
```

---

## Генераторы (generator expressions)

### Generator Expression — ленивое вычисление

```python
# Выглядит как list comprehension, но в круглых скобках
# Не создаёт список в памяти — вычисляет элементы по требованию
gen = (x ** 2 for x in range(1_000_000))   # почти не занимает память

# Использование
next(gen)         # 0
next(gen)         # 1
list(gen)         # вычислить все оставшиеся

# Внутри функций — скобки можно опустить
total = sum(x ** 2 for x in range(100))
has_admin = any(u["role"] == "admin" for u in users)
all_active = all(u["is_active"] for u in users)
```

### Функция-генератор с `yield`

```python
def generate_test_users(count: int):
    """Генерирует тестовых пользователей лениво."""
    for i in range(1, count + 1):
        yield {
            "id": i,
            "name": f"User{i}",
            "email": f"user{i}@example.com",
        }

# Использование
for user in generate_test_users(3):
    print(user)
# {"id": 1, "name": "User1", ...}
# {"id": 2, "name": "User2", ...}
# {"id": 3, "name": "User3", ...}

# Конвертация в список
users = list(generate_test_users(5))
```

---

## Как это выглядит в pytest

### Подготовка тестовых данных через comprehension

```python
import pytest


def get_order_totals(orders: list[dict]) -> list[float]:
    """Извлекает итоговые суммы из списка заказов."""
    return [o["total"] for o in orders if o.get("total") is not None]


@pytest.fixture
def sample_orders() -> list[dict]:
    return [
        {"id": i, "total": i * 100.0, "status": "paid"}
        for i in range(1, 6)
    ]


def test_order_totals_count(sample_orders):
    totals = get_order_totals(sample_orders)
    assert len(totals) == 5


def test_order_totals_values(sample_orders):
    totals = get_order_totals(sample_orders)
    assert totals == [100.0, 200.0, 300.0, 400.0, 500.0]


def test_order_totals_skips_null():
    orders = [
        {"id": 1, "total": 100.0},
        {"id": 2},               # нет total
        {"id": 3, "total": None},
        {"id": 4, "total": 300.0},
    ]
    assert get_order_totals(orders) == [100.0, 300.0]
```

### Comprehension для проверки API-ответа

```python
def test_all_products_have_required_fields(api_client):
    response = api_client.get("/products")
    products = response.json()["items"]

    required_fields = {"id", "name", "price", "in_stock"}
    missing = [
        {"product_id": p["id"], "missing": required_fields - set(p.keys())}
        for p in products
        if not required_fields.issubset(p.keys())
    ]
    assert missing == [], f"Products with missing fields: {missing}"


def test_extract_unique_categories(api_client):
    response = api_client.get("/products")
    products = response.json()["items"]

    categories = {p["category"] for p in products}
    assert "electronics" in categories
    assert len(categories) >= 3
```

### Generator в параметризации

```python
def generate_invalid_emails():
    invalids = ["notanemail", "@nodomain", "no@tld", "spaces @example.com"]
    for email in invalids:
        yield pytest.param(email, id=email)


@pytest.mark.parametrize("email", generate_invalid_emails())
def test_invalid_email_rejected(api_client, email: str):
    response = api_client.post("/users", json={"email": email})
    assert response.status_code == 422
```

---

## Производительность

```python
import sys

# List comprehension — весь список в памяти
lst = [x ** 2 for x in range(1_000_000)]
print(sys.getsizeof(lst))        # ~8 MB

# Generator — почти ничего не занимает
gen = (x ** 2 for x in range(1_000_000))
print(sys.getsizeof(gen))        # ~112 bytes

# Когда использовать generator:
# - нужно обработать большой поток данных
# - нужно только один раз пройтись по элементам
# - sum/any/all — им не нужен весь список

# Когда использовать list:
# - нужен случайный доступ по индексу
# - нужно пройтись несколько раз
# - нужно знать длину через len()
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| Вложенный comprehension трудночитаем | `[x for row in m for x in row if x > 0]` | Разбей на 2 строки или используй обычный цикл |
| Generator использован дважды | Второй раз — пустой! | Конвертируй в list если нужно несколько проходов |
| Side effects в comprehension | `[print(x) for x in items]` — плохо | Comprehension для вычислений, цикл `for` для действий |
| Тернарный оператор перепутан | `if cond` в конце vs в выражении | В конце — фильтр. В начале — трансформация |

---

## Вопрос на собесе

**Q: Напишите dict comprehension, который из списка пользователей создаёт словарь `{id: name}`**

```python
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
id_to_name = {u["id"]: u["name"] for u in users}
# {1: "Alice", 2: "Bob"}
```

**Q: В чём разница между list comprehension и generator expression?**

> List comprehension создаёт весь список в памяти сразу. Generator expression создаёт объект-генератор, который вычисляет значения лениво — по одному при запросе. Используй generator когда нужен только один проход и важна экономия памяти.
