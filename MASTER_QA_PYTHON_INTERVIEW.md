# MASTER: Python QA Live Coding — Полный курс подготовки
## Middle | WB / Ozon / X5 / Яндекс | Цель: 295k Москва

> Сгенерировано: 03.03.2026  
> Оригинальный промпт сохранён в конце документа.

---

## НАВИГАЦИЯ

| Раздел | Тема |
|--------|------|
| [1. Исходный промпт](#исходный-промпт) | Промпт для регенерации / расширения |
| [2. .cursorrules](#cursorrules) | Правила Cursor для QA-стиля |
| [3. 14-дневный курс](#14-дневный-курс-python-для-qa-live-coding-собеседований) | Дни 1–14, задачи, тесты |
| [4. Cheat Sheet Python QA](#python-qa-cheat-sheet) | Comprehensions, Set tricks, Pytest |
| [5. Cheat Sheet Pytest + Магические методы](#шпаргалка-магические-методы--pytest) | Декораторы, ООП, хуки |
| [6. Подготовка WB](#подготовка-к-собеседованию-wildberries) | Python Core, SQL, Алгоритмы |
| [7. Подготовка X5Tech](#подготовка-к-собеседованию-x5tech) | ООП, Pytest, Story-кейсы |
| [8. 20 Cursor-промптов](#20-cursor-промптов-для-qa-python-собеседований) | Готовые промпты для генерации задач |

---

# ИСХОДНЫЙ ПРОМПТ

> Сохранён для регенерации курса или расширения через Cursor AI.

```
Создай для меня **интерактивный 14-дневный курс Python для QA live coding собеседований**
(middle уровень, фокус WB/Ozon).

Мой фон: QA с опытом requests/Pytest/pydantic, но слаб в comprehensions, set/list/tuple,
парсинг строк, простые алгоритмы. Уволился 16.02.2026, цель — 295k Москва.

**Структура курса** (генерируй как Jupyter notebook или Markdown с кодом):
1. **День 1–4**: Базовые коллекции (list/set/dict/tuple), split(), try/int() — 10 задач каждая
   с решением + тестами.
2. **День 5–8**: Comprehensions (list/dict/set), generators, sorting/filtering — задачи типа
   "квадраты уникальных чисел из строки" (с отрицательными).
3. **День 9–11**: Функции, O(n), edge-кейсы, Pytest fixtures для API.
4. **День 12–14**: Полные live coding симуляции (15 мин/задача): API парсинг, mock, рефакторинг.

**Для каждой задачи**:
- Описание (как на собесе).
- Шаги мышления (что проговаривать).
- 4 варианта кода (правильный + 3 ошибки).
- Pytest тесты.
- Cursor-промпт для самостоятельного решения.

**Дополнительно**:
- .cursorrules файл для QA-style (Pytest, type hints).
- Ежедневный план: 2ч теория + 2ч практика.
- Cheat sheet (1 страница: comprehensions, set tricks).
- 20 готовых промптов для Cursor на типичные собес-задачи.
```

---

# .CURSORRULES

> Скопируй в файл `.cursorrules` в корне проекта для автоматического применения правил.

```
# QA Python Live Coding Interview — Cursor Rules
# Стиль: middle QA, фокус WB/Ozon, Pytest + type hints

## Роль
Ты — Senior Python QA Engineer, помогаешь готовиться к live coding собеседованиям уровня middle.
Фокус: WB, Ozon, X5, Яндекс.

## Правила генерации задач

### Структура каждой задачи
1. Описание — как звучит на собеседовании (1-2 предложения)
2. Шаги мышления — что проговаривать вслух (bullet list)
3. Edge-кейсы — пустой список, None, отрицательные числа, дубликаты
4. Решение — чистый Python с type hints
5. Альтернативы — 3 варианта с ошибками + объяснение почему ошибка
6. Pytest тесты — минимум 4 теста (happy path, edge, negative, boundary)

### Стандарты кода
- Всегда используй type hints для аргументов и возвращаемых значений
- Предпочитай comprehensions над циклами где уместно
- Используй f-strings вместо .format() или %
- Имена переменных — snake_case, описательные
- Функции — маленькие, одна ответственность
- Комментарии — только для неочевидной логики

### Pytest правила
- Фикстуры для повторяющихся данных
- Параметризация через @pytest.mark.parametrize
- Имена тестов: test_<функция>_<сценарий>
- Один assert на тест (предпочтительно)
- Используй pytest.raises для исключений

## Шаблон промпта для генерации задачи

Сгенерируй задачу для live coding собеседования Python (middle QA, WB/Ozon).
Тема: [ТЕМА]
Уровень сложности: [easy/medium/hard]
Ограничения: type hints, без внешних библиотек (только stdlib)
Формат: описание → шаги мышления → решение → 3 ошибки → pytest тесты

## Быстрые команды

- "Дай задачу на comprehensions" → генерирует задачу по теме
- "Разбери ошибку: [код]" → анализирует и объясняет
- "Напиши тесты для: [функция]" → генерирует pytest suite
- "Оптимизируй: [код]" → улучшает с объяснением O(n)
- "Симулируй собес" → 15-минутная задача с таймером

## Типичные темы WB/Ozon собесов
- Парсинг строк (split, strip, int conversion)
- Работа с коллекциями (list, dict, set, tuple)
- Comprehensions (list/dict/set)
- Сортировка и фильтрация
- API тестирование (requests, mock, fixtures)
- Обработка ошибок (try/except)
- Простые алгоритмы (поиск дубликатов, анаграммы, палиндромы)
```

---

# 14-ДНЕВНЫЙ КУРС PYTHON ДЛЯ QA LIVE CODING СОБЕСЕДОВАНИЙ
## Уровень: Middle | Фокус: WB / Ozon / X5 | Цель: 295k Москва

> **Формула дня**: 2ч теория (утро) + 2ч практика (вечер)  
> **Правило собеса**: всегда проговаривай мысли вслух — interviewer оценивает процесс, не только результат

---

## НЕДЕЛЬНЫЙ ПЛАН

| День | Тема | Ключевые навыки |
|------|------|----------------|
| 1 | List — основы | append, slice, sort, in |
| 2 | Dict — основы | get, items, update, defaultdict |
| 3 | Set + Tuple | разница, когда что, frozenset |
| 4 | Парсинг строк | split, strip, int(), try/except |
| 5 | List comprehensions | условия, вложенные |
| 6 | Dict/Set comprehensions | группировка, инверсия |
| 7 | Generators | yield, memory efficiency |
| 8 | Sorting + Filtering | key=, lambda, filter/map |
| 9 | Функции + edge-кейсы | *args, **kwargs, defaults |
| 10 | O(n) мышление | Big O, оптимизация |
| 11 | Pytest fixtures для API | conftest, parametrize, mock |
| 12 | Live coding симуляция 1 | API парсинг |
| 13 | Live coding симуляция 2 | mock + рефакторинг |
| 14 | Live coding симуляция 3 | Финальный прогон |

---

# ДЕНЬ 1: List — Базовые операции

## Теория (2ч утро)

```python
# Ключевые операции со списками
lst = [3, 1, 4, 1, 5, 9, 2, 6]

# Срезы
lst[1:4]      # [1, 4, 1]
lst[::-1]     # разворот
lst[::2]      # каждый второй

# Мутирующие методы (изменяют на месте, возвращают None!)
lst.append(7)       # добавить в конец
lst.insert(0, 0)    # вставить по индексу
lst.remove(1)       # удалить первое вхождение
lst.pop()           # удалить и вернуть последний
lst.sort()          # сортировка на месте
lst.reverse()       # разворот на месте

# НЕ мутирующие (возвращают новый объект)
sorted(lst)         # новый отсортированный список
lst + [10, 11]      # конкатенация
```

---

## ЗАДАЧА 1.1 — Удаление дубликатов с сохранением порядка

**На собесе звучит так:**
> "Напиши функцию, которая принимает список и возвращает новый список без дубликатов, сохраняя порядок первого появления."

### Шаги мышления (проговаривай вслух)
1. "Мне нужно сохранить порядок — значит нельзя просто set()"
2. "Буду отслеживать уже виденные элементы через set (O(1) lookup)"
3. "Итерируюсь по списку, добавляю в результат если не видел раньше"
4. "Edge-кейсы: пустой список, все дубликаты, один элемент"

### Правильное решение

```python
def remove_duplicates(items: list) -> list:
    """Удаляет дубликаты, сохраняя порядок первого появления."""
    seen: set = set()
    result: list = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

### Вариант 2 — через dict.fromkeys (Python 3.7+)

```python
def remove_duplicates_v2(items: list) -> list:
    return list(dict.fromkeys(items))
```

### ОШИБКА 1 — Потеря порядка

```python
# НЕВЕРНО: set() не сохраняет порядок
def remove_duplicates_wrong1(items: list) -> list:
    return list(set(items))  # ❌ порядок изменится
```

### ОШИБКА 2 — O(n²) сложность

```python
# НЕВЕРНО: проверка "in list" — O(n), весь цикл — O(n²)
def remove_duplicates_wrong2(items: list) -> list:
    result = []
    for item in items:
        if item not in result:  # ❌ O(n) поиск в списке
            result.append(item)
    return result
# Работает правильно, но медленно на больших данных
```

### ОШИБКА 3 — Мутация входного списка

```python
# НЕВЕРНО: меняем входной список
def remove_duplicates_wrong3(items: list) -> list:
    i = 0
    while i < len(items):
        if items.count(items[i]) > 1:
            items.remove(items[i])  # ❌ мутируем аргумент
        else:
            i += 1
    return items
```

### Pytest тесты

```python
import pytest
from solution import remove_duplicates

def test_remove_duplicates_basic():
    assert remove_duplicates([1, 2, 1, 3, 2]) == [1, 2, 3]

def test_remove_duplicates_preserves_order():
    assert remove_duplicates([3, 1, 2, 1, 3]) == [3, 1, 2]

def test_remove_duplicates_empty():
    assert remove_duplicates([]) == []

def test_remove_duplicates_no_duplicates():
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]

def test_remove_duplicates_all_same():
    assert remove_duplicates([5, 5, 5]) == [5]

def test_remove_duplicates_strings():
    assert remove_duplicates(["a", "b", "a"]) == ["a", "b"]

def test_remove_duplicates_does_not_mutate():
    original = [1, 2, 1]
    remove_duplicates(original)
    assert original == [1, 2, 1]
```

### Cursor-промпт

```
Сгенерируй 3 новые задачи на удаление/фильтрацию дубликатов из списка Python,
уровень middle QA собеседование. Условия: type hints, без внешних библиотек,
с edge-кейсами (None, пустой список, отрицательные числа).
Для каждой: описание → шаги мышления → решение → pytest тесты.
```

---

## ЗАДАЧА 1.2 — Второй максимальный элемент

**На собесе звучит так:**
> "Найди второй по величине элемент в списке. Что если все элементы одинаковые?"

### Шаги мышления
1. "Нужен второй уникальный максимум или второй по позиции?"
2. "Уточню у интервьюера — обычно имеют в виду второй уникальный"
3. "Подход 1: sorted(set()) — чисто, O(n log n)"
4. "Подход 2: один проход O(n) — для больших данных"
5. "Edge: список с одним уникальным элементом → нет второго"

```python
def second_max(numbers: list[int]) -> int | None:
    """Возвращает второй по величине уникальный элемент."""
    unique = sorted(set(numbers), reverse=True)
    return unique[1] if len(unique) >= 2 else None

# O(n) вариант для больших данных
def second_max_linear(numbers: list[int]) -> int | None:
    if len(numbers) < 2:
        return None
    first = second = float('-inf')
    for num in numbers:
        if num > first:
            second = first
            first = num
        elif num > second and num != first:
            second = num
    return second if second != float('-inf') else None
```

```python
import pytest
from solution import second_max

@pytest.mark.parametrize("nums, expected", [
    ([3, 1, 4, 1, 5, 9], 5),
    ([1, 2], 1),
    ([5, 5, 5], None),
    ([], None),
    ([1], None),
    ([-1, -3, -2], -2),
])
def test_second_max(nums, expected):
    assert second_max(nums) == expected
```

---

## ЗАДАЧА 1.3 — Разворот списка без reverse()

```python
def reverse_list(items: list) -> list:
    result = []
    for i in range(len(items) - 1, -1, -1):
        result.append(items[i])
    return result

# Через swap (in-place)
def reverse_inplace(items: list) -> list:
    left, right = 0, len(items) - 1
    while left < right:
        items[left], items[right] = items[right], items[left]
        left += 1
        right -= 1
    return items
```

```python
@pytest.mark.parametrize("inp, expected", [
    ([1, 2, 3], [3, 2, 1]),
    ([1], [1]),
    ([], []),
    ([1, 2], [2, 1]),
])
def test_reverse_list(inp, expected):
    assert reverse_list(inp) == expected
```

---

## ЗАДАЧИ 1.4–1.10 (Быстрые)

```python
# 1.4 — Плоский список из вложенного (глубина 1)
def flatten(nested: list[list]) -> list:
    return [item for sublist in nested for item in sublist]

# 1.5 — Чанки по N элементов
def chunks(lst: list, n: int) -> list[list]:
    return [lst[i:i+n] for i in range(0, len(lst), n)]

# 1.6 — Пересечение двух списков (без set)
def intersection(a: list, b: list) -> list:
    b_set = set(b)
    return [x for x in a if x in b_set]

# 1.7 — Rotate left на k позиций
def rotate_left(lst: list, k: int) -> list:
    if not lst:
        return lst
    k = k % len(lst)
    return lst[k:] + lst[:k]

# 1.8 — Сумма соседних пар
def pair_sums(lst: list[int]) -> list[int]:
    return [lst[i] + lst[i+1] for i in range(len(lst)-1)]

# 1.9 — Индексы всех вхождений элемента
def find_all_indices(lst: list, target) -> list[int]:
    return [i for i, x in enumerate(lst) if x == target]

# 1.10 — Удалить все вхождения значения
def remove_value(lst: list, value) -> list:
    return [x for x in lst if x != value]
```

---

# ДЕНЬ 2: Dict — Основы

## ЗАДАЧА 2.1 — Подсчёт частоты символов

**На собесе:** "Напиши функцию подсчёта частоты каждого символа в строке."

### Шаги мышления
1. "Результат — словарь {символ: количество}"
2. "Вариант 1: обычный dict с .get()"
3. "Вариант 2: collections.Counter — идеально для этого"
4. "Что со пробелами и регистром? Уточню у интервьюера"

```python
from collections import Counter, defaultdict

def char_frequency(s: str) -> dict[str, int]:
    """Подсчитывает частоту каждого символа."""
    return dict(Counter(s))

# Без Counter
def char_frequency_manual(s: str) -> dict[str, int]:
    freq: dict[str, int] = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq

# Через defaultdict
def char_frequency_defaultdict(s: str) -> dict[str, int]:
    freq: defaultdict[str, int] = defaultdict(int)
    for char in s:
        freq[char] += 1
    return dict(freq)
```

### ОШИБКА — KeyError без защиты

```python
def char_frequency_wrong(s: str) -> dict[str, int]:
    freq = {}
    for char in s:
        freq[char] += 1  # ❌ KeyError при первом вхождении
    return freq
```

```python
@pytest.mark.parametrize("s, expected", [
    ("hello", {"h": 1, "e": 1, "l": 2, "o": 1}),
    ("", {}),
    ("aaa", {"a": 3}),
    ("ab", {"a": 1, "b": 1}),
])
def test_char_frequency(s, expected):
    assert char_frequency(s) == expected
```

---

## ЗАДАЧА 2.2 — Инверсия словаря

```python
def invert_dict(d: dict) -> dict:
    """Меняет ключи и значения местами."""
    return {v: k for k, v in d.items()}

# С обработкой дубликатов значений
def invert_dict_safe(d: dict) -> dict[any, list]:
    result: dict = {}
    for k, v in d.items():
        result.setdefault(v, []).append(k)
    return result
```

## ЗАДАЧА 2.3 — Группировка по ключу

**На собесе:** "Сгруппируй список товаров по категории."

```python
def group_by_key(items: list[dict], key: str) -> dict[str, list]:
    """Группирует список словарей по значению ключа."""
    result: dict[str, list] = {}
    for item in items:
        group = item.get(key, "unknown")
        result.setdefault(group, []).append(item)
    return result
```

## ЗАДАЧИ 2.4–2.10 (Быстрые)

```python
# 2.4 — Слияние двух словарей (Python 3.9+)
def merge_dicts(d1: dict, d2: dict) -> dict:
    return {**d1, **d2}

# 2.5 — Отфильтровать словарь по значению
def filter_dict(d: dict[str, int], threshold: int) -> dict[str, int]:
    return {k: v for k, v in d.items() if v > threshold}

# 2.6 — Топ-N ключей по значению
def top_n(d: dict[str, int], n: int) -> list[str]:
    return sorted(d, key=d.get, reverse=True)[:n]

# 2.7 — Безопасный nested get
def nested_get(d: dict, *keys, default=None):
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

# 2.8 — Словарь из двух списков
def zip_to_dict(keys: list, values: list) -> dict:
    return dict(zip(keys, values))

# 2.9 — Подсчёт уникальных значений
def count_unique_values(d: dict) -> int:
    return len(set(d.values()))

# 2.10 — Найти ключи с максимальным значением
def keys_with_max_value(d: dict[str, int]) -> list[str]:
    if not d:
        return []
    max_val = max(d.values())
    return [k for k, v in d.items() if v == max_val]
```

---

# ДЕНЬ 3: Set + Tuple

## Теория: когда что использовать

```python
# SET — когда важна уникальность и быстрый поиск O(1)
unique_ids = {1, 2, 3, 4}
"fast_lookup" if 3 in unique_ids else "not found"  # O(1)!

# TUPLE — когда данные неизменяемы, используй как ключ dict
point = (10, 20)
coords_cache = {(0, 0): "origin", (10, 20): "point_a"}

# FROZENSET — неизменяемый set, можно как ключ dict
permissions = frozenset(["read", "write"])
```

## ЗАДАЧА 3.1 — Анаграммы

**На собесе:** "Определи, являются ли две строки анаграммами."

```python
from collections import Counter

def are_anagrams(s1: str, s2: str) -> bool:
    """Проверяет, являются ли строки анаграммами."""
    return Counter(s1.lower()) == Counter(s2.lower())

def are_anagrams_v2(s1: str, s2: str) -> bool:
    return sorted(s1.lower()) == sorted(s2.lower())
```

```python
@pytest.mark.parametrize("s1, s2, expected", [
    ("listen", "silent", True),
    ("hello", "world", False),
    ("", "", True),
    ("a", "a", True),
    ("Abc", "cab", True),
    ("abc", "abcd", False),
])
def test_are_anagrams(s1, s2, expected):
    assert are_anagrams(s1, s2) == expected
```

## ЗАДАЧА 3.2 — Операции над множествами

```python
# На собесе: "Найди пользователей, купивших ОБА продукта A и B"
def bought_both(buyers_a: set[int], buyers_b: set[int]) -> set[int]:
    return buyers_a & buyers_b  # пересечение

def only_a(buyers_a: set[int], buyers_b: set[int]) -> set[int]:
    return buyers_a - buyers_b  # разность

def bought_any(buyers_a: set[int], buyers_b: set[int]) -> set[int]:
    return buyers_a | buyers_b  # объединение

def bought_exactly_one(buyers_a: set[int], buyers_b: set[int]) -> set[int]:
    return buyers_a ^ buyers_b  # симметричная разность
```

---

# ДЕНЬ 4: Парсинг строк

## ЗАДАЧА 4.1 — Парсинг строки с числами

**На собесе:** "Дана строка '1, -2, 3, abc, 4'. Верни список только целых чисел."

### Шаги мышления
1. "Разобью строку по запятой через split(',')"
2. "Каждый токен очищу через strip()"
3. "Попробую int() в try/except — если ValueError, пропущу"
4. "Edge: пустая строка, только буквы, отрицательные числа"

```python
def parse_integers(s: str) -> list[int]:
    """Извлекает целые числа из строки, игнорируя нечисловые значения."""
    result: list[int] = []
    for token in s.split(","):
        try:
            result.append(int(token.strip()))
        except ValueError:
            continue
    return result
```

### ОШИБКА 1 — Потеря отрицательных

```python
def parse_integers_wrong1(s: str) -> list[int]:
    # ❌ isdigit() не работает с отрицательными числами
    return [int(x.strip()) for x in s.split(",") if x.strip().isdigit()]
    # "-2".isdigit() → False !
```

### ОШИБКА 2 — Не очищает пробелы

```python
def parse_integers_wrong2(s: str) -> list[int]:
    result = []
    for token in s.split(","):
        try:
            result.append(int(token))  # ❌ " 3" → ValueError из-за пробела
        except ValueError:
            pass
    return result
```

```python
@pytest.mark.parametrize("s, expected", [
    ("1, -2, 3, abc, 4", [1, -2, 3, 4]),
    ("", []),
    ("abc, def", []),
    ("1,2,3", [1, 2, 3]),
    ("-1, -2, -3", [-1, -2, -3]),
    ("  5  ,  10  ", [5, 10]),
])
def test_parse_integers(s, expected):
    assert parse_integers(s) == expected
```

## ЗАДАЧА 4.2 — Проверка палиндрома

```python
def is_palindrome(s: str) -> bool:
    """Проверяет, является ли строка палиндромом (игнорирует регистр и пробелы)."""
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```

## ЗАДАЧА 4.3 — Подсчёт слов

```python
from collections import Counter

def word_count_v2(text: str) -> dict[str, int]:
    return dict(Counter(text.lower().split()))
```

---

# ДЕНЬ 5: List Comprehensions

## Теория — Синтаксис

```python
result = [выражение for элемент in итерируемое if условие]

squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
flat = [x for row in matrix for x in row]
```

## ЗАДАЧА 5.1 — Квадраты уникальных чисел из строки

**На собесе (типичная для WB/Ozon):**
> "Дана строка '3 1 2 -1 2 3'. Верни отсортированный список квадратов уникальных чисел."

### Шаги мышления
1. "Разобью строку → конвертирую в int → возьму уникальные через set"
2. "Для каждого уникального вычислю квадрат"
3. "Отсортирую результат"
4. "Edge: отрицательные — квадрат положительный, пустая строка"

```python
def unique_squares(s: str) -> list[int]:
    """Возвращает отсортированные квадраты уникальных чисел из строки."""
    numbers = [int(x) for x in s.split()]
    return sorted(x**2 for x in set(numbers))

# Однострочник (читаемый)
def unique_squares_v2(s: str) -> list[int]:
    return sorted({int(x)**2 for x in s.split()})
```

```python
@pytest.mark.parametrize("s, expected", [
    ("3 1 2 -1 2 3", [1, 4, 9]),
    ("", []),
    ("0", [0]),
    ("-3 3", [9]),
    ("1 2 3", [1, 4, 9]),
    ("-1 -2 -3", [1, 4, 9]),
])
def test_unique_squares(s, expected):
    assert unique_squares(s) == expected
```

## ЗАДАЧА 5.2 — FizzBuzz через comprehension

```python
def fizzbuzz(n: int) -> list[str]:
    return [
        "FizzBuzz" if i % 15 == 0
        else "Fizz" if i % 3 == 0
        else "Buzz" if i % 5 == 0
        else str(i)
        for i in range(1, n + 1)
    ]
```

## ЗАДАЧА 5.3 — Матрица транспонирования

```python
def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*matrix)]
```

---

# ДЕНЬ 6: Dict/Set Comprehensions

```python
# Инверсия словаря
def invert(d: dict[str, int]) -> dict[int, str]:
    return {v: k for k, v in d.items()}

# Нормализация данных API: id → название продукта
def build_product_map(products: list[dict]) -> dict[int, str]:
    return {p["id"]: p["name"] for p in products if "id" in p and "name" in p}

# Символы встречающиеся больше n раз
def chars_appearing_more_than_n(s: str, n: int) -> set[str]:
    from collections import Counter
    freq = Counter(s)
    return {char for char, count in freq.items() if count > n}
```

---

# ДЕНЬ 7: Generators

```python
# LIST: все в памяти
squares_list = [x**2 for x in range(1_000_000)]  # ~8MB RAM

# GENERATOR: O(1) память
squares_gen = (x**2 for x in range(1_000_000))

def fibonacci_up_to(n: int):
    """Генератор чисел Фибоначчи <= n."""
    a, b = 0, 1
    while a <= n:
        yield a
        a, b = b, a + b

def parse_log_lines(lines: list[str], keyword: str):
    """Генератор: фильтрует строки по ключевому слову."""
    for line in lines:
        if keyword.lower() in line.lower():
            yield line.strip()
```

---

# ДЕНЬ 8: Sorting + Filtering

```python
# Сортировка по цене по убыванию, при равной — по имени
def sort_products(products: list[dict]) -> list[dict]:
    return sorted(products, key=lambda p: (-p["price"], p["name"]))

# Топ-N покупателей
def top_buyers(orders: list[dict], n: int = 3) -> list[str]:
    from collections import defaultdict
    totals: defaultdict[str, float] = defaultdict(float)
    for order in orders:
        totals[order["user"]] += order["amount"]
    return sorted(totals, key=totals.get, reverse=True)[:n]

# Чётные числа → квадрат (comprehension предпочтительнее map+filter)
def filter_and_transform(numbers: list[int]) -> list[int]:
    return [x**2 for x in numbers if x % 2 == 0]
```

---

# ДЕНЬ 9: Функции + Edge-кейсы

```python
def calculate_discount(
    price: float,
    discount_percent: float = 0,
    max_discount: float | None = None
) -> float:
    """Вычисляет цену со скидкой."""
    if price < 0:
        raise ValueError(f"Цена не может быть отрицательной: {price}")
    if not 0 <= discount_percent <= 100:
        raise ValueError(f"Скидка должна быть 0-100%: {discount_percent}")
    discount = price * discount_percent / 100
    if max_discount is not None:
        discount = min(discount, max_discount)
    return round(price - discount, 2)

def build_query(*conditions: str, operator: str = "AND") -> str:
    """Строит SQL-подобный запрос из условий."""
    if not conditions:
        return "WHERE 1=1"
    joined = f" {operator} ".join(conditions)
    return f"WHERE {joined}"
```

```python
def test_calculate_discount_basic():
    assert calculate_discount(100, 10) == 90.0

def test_calculate_discount_max_cap():
    assert calculate_discount(1000, 50, max_discount=100) == 900.0

def test_calculate_discount_negative_price():
    with pytest.raises(ValueError, match="отрицательной"):
        calculate_discount(-100, 10)
```

---

# ДЕНЬ 10: O(n) мышление

## Памятка по Big O

```python
# O(1)  — dict/set lookup, list index access
5 in {1,2,3,4,5}  # O(1) — хэш таблица!
5 in [1,2,3,4,5]  # O(n) — проверяет каждый элемент

# O(n log n) — сортировка
sorted([3,1,2])

# O(n²) — вложенные циклы — ИЗБЕГАЙ на собесе
for i in lst:
    for j in lst: ...
```

## ЗАДАЧА 10.1 — Two Sum (классика каждого собеса)

```python
# O(n²) — плохо
def two_sum_slow(nums: list[int], target: int) -> tuple[int, int] | None:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None

# O(n) — хорошо
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None
```

```python
@pytest.mark.parametrize("nums, target, expected", [
    ([2, 7, 11, 15], 9, (0, 1)),
    ([3, 2, 4], 6, (1, 2)),
    ([1, 2, 3], 10, None),
    ([], 5, None),
])
def test_two_sum(nums, target, expected):
    assert two_sum(nums, target) == expected
```

## ЗАДАЧА 10.2 — Поиск дубликатов O(n)

```python
def find_duplicates(nums: list[int]) -> list[int]:
    """O(n) через set."""
    seen: set[int] = set()
    duplicates: set[int] = set()
    for num in nums:
        if num in seen:
            duplicates.add(num)
        seen.add(num)
    return sorted(duplicates)
```

---

# ДЕНЬ 11: Pytest Fixtures для API

```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def base_url() -> str:
    return "https://api.example.com/v1"

@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer test-token", "Content-Type": "application/json"}

@pytest.fixture
def sample_product() -> dict:
    return {"id": 1, "name": "Test Product", "price": 999.99, "category": "electronics"}

@pytest.fixture
def mock_response():
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"status": "ok"}
    return response
```

```python
# tests/test_product_api.py
import pytest
from unittest.mock import patch, Mock
import requests

def get_product(product_id: int, base_url: str, headers: dict) -> dict:
    response = requests.get(f"{base_url}/products/{product_id}", headers=headers)
    response.raise_for_status()
    return response.json()

class TestGetProduct:
    def test_get_product_success(self, base_url, auth_headers, sample_product):
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_product
            mock_get.return_value = mock_response
            result = get_product(1, base_url, auth_headers)
            assert result["id"] == 1
            assert result["name"] == "Test Product"

    def test_get_product_not_found(self, base_url, auth_headers):
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.HTTPError("404")
            mock_get.return_value = mock_response
            with pytest.raises(requests.HTTPError):
                get_product(999, base_url, auth_headers)

    @pytest.mark.parametrize("status_code", [500, 503, 429])
    def test_get_product_server_errors(self, base_url, auth_headers, status_code):
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.HTTPError(str(status_code))
            mock_get.return_value = mock_response
            with pytest.raises(requests.HTTPError):
                get_product(1, base_url, auth_headers)
```

---

# ДЕНЬ 12: Live Coding Симуляция 1 — API парсинг

**Интервьюер:** "У тебя есть JSON-ответ от API WB с заказами. Напиши функцию которая:
1. Принимает список заказов
2. Возвращает словарь: `{'total_amount': float, 'avg_amount': float, 'top_product': str, 'orders_by_status': dict}`
3. Обрабатывает некорректные данные"

```python
from collections import Counter, defaultdict
from typing import TypedDict

class OrderStats(TypedDict):
    total_amount: float
    avg_amount: float
    top_product: str | None
    orders_by_status: dict[str, int]

def analyze_orders(orders: list[dict]) -> OrderStats:
    if not orders:
        return {"total_amount": 0.0, "avg_amount": 0.0, "top_product": None, "orders_by_status": {}}

    amounts: list[float] = []
    product_counter: Counter = Counter()
    status_groups: defaultdict[str, int] = defaultdict(int)

    for order in orders:
        amount = order.get("amount")
        if isinstance(amount, (int, float)) and amount >= 0:
            amounts.append(float(amount))
        product = order.get("product")
        if product:
            product_counter[product] += 1
        status = order.get("status", "unknown")
        status_groups[status] += 1

    total = sum(amounts)
    avg = total / len(amounts) if amounts else 0.0
    top_product = product_counter.most_common(1)[0][0] if product_counter else None

    return {
        "total_amount": round(total, 2),
        "avg_amount": round(avg, 2),
        "top_product": top_product,
        "orders_by_status": dict(status_groups)
    }
```

```python
@pytest.fixture
def sample_orders():
    return [
        {"id": 1, "amount": 100.0, "product": "iPhone", "status": "completed"},
        {"id": 2, "amount": 200.0, "product": "MacBook", "status": "completed"},
        {"id": 3, "amount": 50.0,  "product": "iPhone",  "status": "pending"},
    ]

def test_analyze_orders_totals(sample_orders):
    result = analyze_orders(sample_orders)
    assert result["total_amount"] == 350.0
    assert result["avg_amount"] == pytest.approx(116.67, abs=0.01)

def test_analyze_orders_top_product(sample_orders):
    assert analyze_orders(sample_orders)["top_product"] == "iPhone"

def test_analyze_orders_empty():
    result = analyze_orders([])
    assert result["total_amount"] == 0.0
    assert result["top_product"] is None

def test_analyze_orders_negative_amount():
    orders = [{"amount": -100, "product": "X", "status": "error"}]
    assert analyze_orders(orders)["total_amount"] == 0.0
```

---

# ДЕНЬ 13: Live Coding Симуляция 2 — Mock + Рефакторинг

**Интервьюер:** "Вот код. Что в нём плохо? Перепиши."

```python
# ПЛОХОЙ КОД — до рефакторинга
def process(data):
    r = []
    for i in range(len(data)):
        if data[i]['status'] == 'active':
            if data[i]['age'] > 18:
                d = {}
                d['name'] = data[i]['name']
                d['age'] = data[i]['age']
                r.append(d)
    return r
```

```
Что говорить:
1. "Не используются type hints"
2. "range(len()) — anti-pattern, лучше прямая итерация"
3. "Вложенные if можно объединить через and"
4. "Магические строки 'active', 18 — лучше константы или параметры"
5. "Нет обработки отсутствующих ключей"
6. "Можно переписать как comprehension"
```

```python
# ХОРОШИЙ КОД — после рефакторинга
MIN_AGE = 18
ACTIVE_STATUS = "active"

def filter_active_adults(
    users: list[dict],
    min_age: int = MIN_AGE,
    status: str = ACTIVE_STATUS
) -> list[dict]:
    """Фильтрует активных совершеннолетних пользователей."""
    return [
        {"name": user["name"], "age": user["age"]}
        for user in users
        if user.get("status") == status and user.get("age", 0) > min_age
    ]
```

---

# ДЕНЬ 14: Финальный прогон

```python
# A: Наиболее частый элемент
def most_common(lst: list) -> any:
    from collections import Counter
    return Counter(lst).most_common(1)[0][0] if lst else None

# B: Проверить скобки
def valid_brackets(s: str) -> bool:
    stack = []
    pairs = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0

# C: Longest common prefix
def longest_common_prefix(strs: list[str]) -> str:
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

# D: Группировка анаграмм
def group_anagrams(words: list[str]) -> list[list[str]]:
    from collections import defaultdict
    groups: defaultdict[str, list] = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)
    return list(groups.values())
```

---

# СТРАТЕГИЯ СОБЕСЕДОВАНИЯ

## Первые 2 минуты (ОБЯЗАТЕЛЬНО)

```
1. Переспроси входные/выходные данные: "Правильно понимаю: на вход X, на выход Y?"
2. Уточни edge-кейсы: "Как обрабатывать None/пустой список/отрицательные числа?"
3. Уточни ограничения: "Можно использовать collections? itertools?"
4. Озвучь подход: "Я думаю подойти так... Согласны?"
```

## Во время кода

```
- Называй что делаешь: "Создаю set для O(1) поиска"
- Объясняй выборы: "Использую defaultdict, чтобы не проверять ключ"
- Думай вслух про O(n): "Это O(n), потому что один проход"
```

## Если застрял

```
- "Дайте подумаю секунду" (15-20 секунд тишины — норма)
- "Могу начать с brute force O(n²), потом оптимизирую"
- "Можно подсказку на направление?"
```

---

# PYTHON QA CHEAT SHEET
## Comprehensions · Set tricks · Sorting · Парсинг · Pytest

---

## LIST COMPREHENSIONS

```python
[x for x in iterable]
[x for x in iterable if condition]
[expr(x) for x in iterable]

# Вложенный (flatten)
[x for row in matrix for x in row]

# С enumerate
[f"{i}: {v}" for i, v in enumerate(lst)]

# С zip
[a + b for a, b in zip(lst1, lst2)]

squares      = [x**2 for x in range(10)]
evens        = [x for x in nums if x % 2 == 0]
upper_words  = [w.upper() for w in words]
flat         = [x for sub in nested for x in sub]
```

---

## DICT COMPREHENSIONS

```python
{k: v for k, v in items}
{k: v for k, v in items if condition}

{v: k for k, v in d.items()}           # инверсия
{k: v for k, v in zip(keys, values)}   # из двух списков
{k: v for k, v in d.items() if v > 0}  # фильтр по значению
{k.lower(): v for k, v in d.items()}   # нормализация ключей
{item["id"]: item for item in items}   # группировка id → объект
```

---

## SET COMPREHENSIONS + SET TRICKS

```python
{x for x in iterable}
{x**2 for x in nums}

sorted({int(x)**2 for x in s.split()})  # уникальные → квадраты → sorted

a & b   # пересечение — купили оба
a | b   # объединение — хоть что-то
a - b   # разность    — только A
a ^ b   # симм. разность — ровно одно

unique = list(dict.fromkeys(lst))       # дедупликация с сохранением порядка

from collections import Counter
dups = {k for k, v in Counter(lst).items() if v > 1}  # дубликаты O(n)
```

---

## GENERATOR EXPRESSIONS

```python
gen = (x**2 for x in range(1000000))  # O(1) память

total = sum(x**2 for x in range(10))
any_negative = any(x < 0 for x in nums)
all_positive = all(x > 0 for x in nums)
```

---

## SORTING

```python
sorted(lst)
sorted(lst, reverse=True)
sorted(lst, key=len)
sorted(lst, key=lambda x: x["price"])
sorted(lst, key=lambda x: (-x["price"], x["name"]))  # множественная

lst.sort(key=lambda x: x[1])  # in-place
```

---

## ПАРСИНГ СТРОК

```python
nums = [int(x.strip()) for x in s.split(",")]

def safe_int(s: str) -> int | None:
    try:
        return int(s.strip())
    except ValueError:
        return None

nums = [n for x in s.split(",") if (n := safe_int(x)) is not None]

s.split(",")         # разбить
s.strip()            # убрать пробелы
s.replace(",", "")   # заменить
s.startswith("http")
s.endswith(".json")
",".join(lst)        # объединить
```

---

## COLLECTIONS

```python
from collections import Counter, defaultdict, deque

c = Counter("aabbbc")          # {'b': 3, 'a': 2, 'c': 1}
c.most_common(2)               # [('b', 3), ('a', 2)]
c["x"]                         # 0 (не KeyError!)

d = defaultdict(int)           # d[key] += 1 без проверки
d = defaultdict(list)          # d[key].append(val) без проверки

q = deque([1, 2, 3])
q.appendleft(0)                # O(1)
q.popleft()                    # O(1)
```

---

## PYTEST ШПАРГАЛКА

```python
@pytest.mark.parametrize("inp, expected", [
    ([1, 2, 3], 6),
    ([], 0),
    ([-1, 1], 0),
])
def test_sum(inp, expected):
    assert my_sum(inp) == expected

def test_raises():
    with pytest.raises(ValueError, match="отрицательн"):
        my_func(-1)

from unittest.mock import patch, Mock

def test_api():
    with patch("module.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"id": 1}
        mock_get.return_value.status_code = 200
        result = my_api_call()
        assert result["id"] == 1

assert result == pytest.approx(3.14, abs=0.01)
```

---

## TYPE HINTS

```python
def f(x: int) -> str: ...
def f(lst: list[int]) -> dict[str, int]: ...
def f(x: int | None) -> str | None: ...
def f(*args: str, **kwargs: int) -> None: ...

from typing import TypedDict
class User(TypedDict):
    id: int
    name: str
```

---

## EDGE-КЕЙСЫ — ВСЕГДА ПРОВЕРЯЙ

```
□ Пустой список/строка/dict
□ None как аргумент
□ Отрицательные числа
□ Очень большие числа
□ Дубликаты
□ Один элемент
□ Все одинаковые элементы
□ Unicode/спецсимволы в строках
```

---

# ШПАРГАЛКА: МАГИЧЕСКИЕ МЕТОДЫ + PYTEST

---

## Декораторы и фикстуры

### Что такое декоратор?
**Что сказать:** «Декоратор — функция высшего порядка: принимает функцию, возвращает обёртку. Меняет или расширяет поведение без изменения исходного кода. Синтаксис `@decorator` — это `func = decorator(func)`.»

```python
def timer(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Time: {time.time() - start}s")
        return result
    return wrapper

@timer
def say_hi():
    print("Hi")
```

### Декоратор с аргументами (тройная вложенность)

```python
from functools import wraps

def retry(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    continue
            raise
        return wrapper
    return decorator

@retry(max_retries=5)
def unstable_api_call():
    ...
```

### Декоратор vs Фикстура

**Что сказать:** «Фикстура — это не декоратор в классическом смысле. `@pytest.fixture` создаёт функцию, которую Pytest вызывает и внедряет результат (Dependency Injection). `@pytest.mark.usefixtures("name")` — применяет фикстуру как декоратор, если не нужен возвращаемый объект.»

```python
@pytest.fixture(autouse=True)
def measure_time():
    import time
    start = time.time()
    yield
    print(f"Time: {time.time() - start}s")
```

---

## Принципы ООП в тестах

| Принцип | В тестах |
|---------|----------|
| **Инкапсуляция** | Helpers, API-клиенты, Page Object скрывают детали |
| **Наследование** | BasePage, базовые тест-классы |
| **Полиморфизм** | Разные валидаторы (XML/JSON) с одним интерфейсом |
| **Абстракция** | ABC, Pydantic-модели контрактов |

```python
from abc import ABC, abstractmethod

class BaseAPIClient(ABC):
    @abstractmethod
    def send(self, body): ...

class X5SoapClient(BaseAPIClient):
    def send(self, body):
        return requests.post(self.url, data=body)
```

---

## Магические методы — «что сказать» + код

### __init__, __str__, __repr__

```python
class APIClient:
    def __init__(self, url: str, timeout: int = 30):
        self.url = url
        self.timeout = timeout

    def __repr__(self):
        return f"Response(status={self.status}, body_len={len(self.body)})"

    def __str__(self):
        return f"API Response: {self.status}"
```

### __eq__ — для сравнения DTO в тестах

**Что сказать:** «Переопределяю для удобного сравнения DTO в assert. Без этого сравниваются id объектов, а не содержимое.»

```python
class APIResponse:
    def __init__(self, status, body):
        self.status = status
        self.body = body

    def __eq__(self, other):
        if not isinstance(other, APIResponse):
            return NotImplemented
        return self.status == other.status and self.body == other.body
```

### __enter__ / __exit__ (context manager)

```python
class TestContext:
    def __enter__(self):
        import time
        self.start = time.time()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        import allure
        allure.attach(f"Duration: {time.time() - self.start}s")
        return False
```

### __call__ — вызываемый объект

```python
class DataProvider:
    def __call__(self, count: int):
        return [f"ID_{i}" for i in range(count)]

provider = DataProvider()
ids = provider(5)
```

### __len__, __getitem__, __iter__

```python
class TestResults:
    def __init__(self, items): self._items = items
    def __len__(self): return len(self._items)
    def __getitem__(self, i): return self._items[i]
    def __iter__(self): return iter(self._items)
```

---

## Pytest — scope фикстур

**Что сказать:** «function — по умолчанию, для лёгких данных. session — для БД, API client, чтобы не создавать каждый раз. module — для конфига файла.»

```python
@pytest.fixture(scope="session")
def db_client():
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture
def request_factory():
    def _create(amount, device_id="POS01"):
        return {"amount": amount, "device_id": device_id}
    return _create

@pytest.fixture(autouse=True)
def db_cleanup(db_cursor):
    yield
    db_cursor.execute("ROLLBACK")
```

### Маркеры

```bash
pytest -m smoke
pytest -m "not integration"
```

```ini
# pytest.ini
markers =
    smoke: критичные тесты
    integration: интеграция с БД/внешними сервисами
```

### Быстрые ответы «в лоб»

| Вопрос | Короткий ответ |
|--------|----------------|
| list vs tuple | list — mutable, tuple — immutable. Tuple — ключи dict, фиксированные данные. |
| global vs nonlocal | global — модульная переменная, nonlocal — во внешней функции. |
| Зачем __eq__ в тестах? | Чтобы `assert actual == expected` работал по смыслу, а не по id. |
| session vs function scope | Session — один раз за прогон (БД, клиент). Function — каждый тест (свежие данные). |
| Как делить smoke и regress? | Маркеры `@pytest.mark.smoke`, запуск `pytest -m smoke` в CI. |

---

# ПОДГОТОВКА К СОБЕСЕДОВАНИЮ WILDBERRIES
## QA Python: High Load, Async, SQL, Algorithms

> WB — это High Load, микросервисы и огромные объемы данных. Акцент на **глубокое понимание Python (особенно асинхронности), базы данных, алгоритмы и архитектуру**.

---

## 1. Python Core (Углубленно)

### Q: В чем разница между итератором и генератором?
**A:**
- **Итератор** — объект с `__iter__` и `__next__`. Сохраняет состояние.
- **Генератор** — упрощённый итератор через `yield` или `(x for x in ...)`. Ленивый, одноразовый, экономит память.
- Все генераторы — итераторы, но не наоборот.

### Q: GIL — что это и как обходить?
**A:** Мьютекс, разрешающий один поток Python за раз. Ограничивает CPU-bound задачи.
- **Multiprocessing** — отдельные процессы с отдельным GIL.
- **Asyncio** — конкурентность в одном потоке (идеально для I/O: сеть, БД).
- C-расширения (NumPy) отпускают GIL.

### Q: Разница между `__init__` и `__new__`?
**A:**
- `__new__` — создаёт объект (выделяет память), возвращает экземпляр.
- `__init__` — инициализирует созданный объект, ничего не возвращает.
- `__new__` нужен для синглтонов или наследования от неизменяемых типов.

### Q: Mutable vs Immutable и аргументы по умолчанию

```python
# ПЛОХО: один и тот же dict переиспользуется между вызовами
def prepare_request(data={}):
    data["amount"] = 100  # мутирует общий объект!

# ХОРОШО
def prepare_request(data=None):
    data = data or {}
    return {**data, "amount": 100}
```

### Q: Asyncio: `await`, `async def`, Event Loop

- `async def` — объявляет корутину.
- `await` — передаёт управление в Event Loop пока ожидается I/O.
- Нельзя использовать `time.sleep` в async — заблокирует весь Loop. Используй `asyncio.sleep`.

---

## 2. Базы Данных (SQL & NoSQL)

### Типы JOIN

- `INNER JOIN` — только совпадающие в обеих таблицах
- `LEFT JOIN` — все из левой, совпадающие из правой (или NULL)
- `FULL JOIN` — все строки из обеих (где нет совпадений — NULL)
- `CROSS JOIN` — декартово произведение

### ACID

- **A**tomicity — все или ничего
- **C**onsistency — из одного валидного состояния в другое
- **I**solation — транзакции не мешают друг другу
- **D**urability — данные не пропадут после коммита

### Индексы

- **B-Tree** (default) — для диапазонов (`<`, `>`, `=`)
- **Hash** — только точное совпадение (`=`)
- **Composite** — по нескольким полям (важен порядок!)

### NoSQL: Redis и ClickHouse

- **Redis**: Key-Value в памяти. Кеширование, очереди, сессии. O(1).
- **ClickHouse**: Колоночная БД для аналитики. Быстрые агрегации на огромных объёмах.

---

## 3. Алгоритмы (Live Coding)

```python
# Задача 1: Развернуть строку
rev = s[::-1]
res = "".join(reversed(s))

# Задача 2: Найти дубликаты
seen = set()
duplicates = set()
for x in nums:
    if x in seen:
        duplicates.add(x)
    seen.add(x)

# Задача 3: Валидация скобок
def is_valid(s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    return not stack

# Задача 4: Фибоначчи (генератор)
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
```

---

## 4. API & Сети

### HTTP методы и идемпотентность

| Метод | Идемпотентный |
|-------|--------------|
| GET | Да |
| PUT | Да |
| DELETE | Да |
| POST | Нет |
| PATCH | Нет |

### Коды ответов

- **2xx**: 200 OK, 201 Created, 204 No Content
- **4xx**: 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
- **5xx**: 500 Internal Error, 502 Bad Gateway, 503 Unavailable

---

## 5. Вопросы к работодателю

1. Как устроен процесс деплоя и тестирования? (GitLab CI, Jenkins?)
2. Какая архитектура тестов? (Монорепозиторий или микросервисы?)
3. Используются ли моки для внешних сервисов или тестовые контуры?
4. Какой % покрытия тестами считается нормой?
5. Как мониторите продакшн? (Grafana, Kibana, Sentry?)

---

# ПОДГОТОВКА К СОБЕСЕДОВАНИЮ X5TECH
## QA Python: база, ООП, магические методы, pytest

> Материал адаптирован под проект afat (X5 Integration API, CAF Promocheck, Session Proxy)

---

## 0. Возврат в X5Tech — как подать историю

**Что сказать:**
> «После X5Tech я перешёл в Automotive — хотел попробовать другой домен, CAN/LIN, встраиваемые системы. Сейчас возвращаюсь, потому что X5 — это розница, API, большие данные, то, где я чувствую себя сильнее. Python и REST освежил по проекту afat и готов быстро войти в поток.»

---

## 1. Про опыт и роль

### Краткий ответ
QA Python с фокусом на API/backend-тестирование. Автоматизация X5Integration (SOAP XML), CAF Promocheck (JSON), Session Proxy. PostgreSQL (sfd, sfd_cl, EDW).

### Типичный день
> «Утро — прогон smoke в CI, разбор падений. День — написание тестов под новые эндпоинты, валидация через Pydantic, проверка контрактов. Вечер — регресс, анализ логов при флейках.»

---

## 2. База по Python

### Типы данных

| Тип | Особенности | Когда использовать |
|-----|-------------|---------------------|
| **list** | Mutable, ordered | Данные, которые меняются |
| **tuple** | Immutable, ordered | Фиксированные наборы, ключи dict |
| **set** | Mutable, unordered, уникальность | Уникальные значения, быстрый `in` |
| **dict** | Mutable, key-value | JSON-ответы, конфиги |

### LEGB — порядок поиска переменной

1. **L**ocal — внутри функции
2. **E**nclosing — во внешних функциях
3. **G**lobal — на уровне модуля
4. **B**uilt-in — встроенные (`len`, `print`)

```python
counter = 0
def increment():
    global counter  # без этого — UnboundLocalError
    counter += 1

def outer():
    x = 1
    def inner():
        nonlocal x
        x += 1
    inner()
    return x  # 2
```

---

## 3. ООП (на примере afat)

### Структура автотестов

```
tests/api/x5integration/     # тесты по фичам
utils/api/helpers/           # API-клиенты, парсеры, БД
models/                      # Pydantic-модели контрактов
conftest.py                  # фикстуры, фабрики, валидаторы
test_data/                   # TestDataManager
configs/                     # конфиги окружений
```

Слои: тесты → фикстуры → хелперы/клиенты → модели/БД

---

## 4. Магические методы

### Шпаргалка

| Метод | Назначение | Когда вызывается |
|-------|------------|------------------|
| `__init__` | Инициализация | При создании экземпляра |
| `__str__` | Для человека | `print(obj)` |
| `__repr__` | Для отладки | В консоли, логах |
| `__eq__` | Сравнение | `a == b` |
| `__enter__`/`__exit__` | Context manager | `with obj:` |
| `__call__` | Вызов как функция | `obj(args)` |
| `__len__` | Длина | `len(obj)` |
| `__iter__` | Итерация | `for x in obj` |

---

## 5. Pytest: фикстуры, хуки, параметризация

### Уровни фикстур

| Scope | Когда создаётся | Когда подходит |
|-------|-----------------|----------------|
| `function` | Каждый тест | Дефолт, лёгкие данные |
| `class` | Один раз на класс | Общий setup |
| `module` | Один раз на модуль | Конфиг, подключения |
| `session` | Один раз за прогон | БД, API client |

```python
@pytest.fixture
def db_cursor(db_connection):
    cursor = db_connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()

@pytest.fixture(autouse=True)
def db_transaction_cleanup(db_cursor):
    yield
    db_cursor.execute("ROLLBACK")
```

### Хуки pytest

```python
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo:
        logging.error(f"FAILED {item.name}: {call.excinfo.value}")
```

---

## 6. Story-кейсы (готовые ответы)

### Кейс 1: Стабилизация регресса
**SIT:** Регресс падал из-за незакрытых транзакций в PostgreSQL.  
**Action:** Добавил `db_transaction_cleanup` (autouse) с `ROLLBACK` + `BEGIN`.  
**Result:** Устранены фейлы из-за «залипших» транзакций, прогон стабилизирован.

### Кейс 2: Ускорение прогона
**SIT:** Каждый тест создавал новое подключение к БД — долго.  
**Action:** `db_connection_factory` с session scope, переиспользование подключений.  
**Result:** Сокращение времени прогона.

### Кейс 3: Валидация контрактов
**SIT:** Ручная проверка JSON-ответов, легко пропустить поле.  
**Action:** Pydantic-модель `PromoCodeResponse` + `model_validate`.  
**Result:** Автоматическая проверка структуры и типов, меньше регрессий.

---

## 7. Подводные вопросы

| Вопрос | Суть ответа |
|--------|-------------|
| Почему list, а не tuple для parametrize? | parametrize принимает итерируемое; список кортежей — удобный формат. |
| Зачем `yield` в фикстуре? | Код после yield — teardown. Выполнится даже при исключении. |
| Чем `__str__` отличается от `__repr__`? | str — для человека, repr — для разработчика (однозначное представление). |
| Что такое идемпотентность в REST? | Повторный вызов даёт тот же результат. GET/PUT/DELETE — да, POST — нет. |

---

# 20 CURSOR-ПРОМПТОВ ДЛЯ QA PYTHON СОБЕСЕДОВАНИЙ
## Копипасти в Cursor Chat → получай новые задачи мгновенно

---

## ГЕНЕРАЦИЯ ЗАДАЧ

### 1. Задача на список (List)
```
Сгенерируй задачу для Python live coding собеседования (middle QA, WB/Ozon) на работу со списками.
Требования:
- type hints для всех аргументов и возвращаемых значений
- обязательно включи edge-кейс: пустой список, один элемент, отрицательные числа
- 4 варианта кода: правильный + 3 с типичными ошибками (объясни каждую)
- pytest тесты с @pytest.mark.parametrize (минимум 5 тест-кейсов)
- шаги мышления: что говорить на собесе вслух
Формат вывода: описание → шаги → код → ошибки → тесты
```

### 2. Задача на словарь (Dict)
```
Сгенерируй задачу для live coding собеседования на работу с dict в Python.
Контекст: middle QA инженер, компании типа WB/Ozon/X5.
Включи: type hints, edge-кейсы (пустой dict, None значения, вложенные структуры),
4 варианта решения (1 правильный, 3 с ошибками), pytest parametrize тесты.
Добавь: "что проговаривать вслух на собесе" — 5 пунктов.
```

### 3. Задача на comprehensions
```
Сгенерируй задачу на list/dict/set comprehensions для Python собеседования (middle QA).
Задача должна быть из реального мира (заказы, пользователи, товары, API данные).
Обязательно: отрицательные числа в данных, type hints, без внешних библиотек (только stdlib).
Покажи: comprehension вариант VS обычный цикл — объясни разницу читаемости и производительности.
Напиши 4 pytest теста с параметризацией.
```

### 4. Задача на парсинг строк
```
Придумай задачу на парсинг строки для Python собеседования (уровень middle QA).
Строка должна содержать: числа (включая отрицательные), слова, специальные символы.
Нужно: split(), strip(), int(), try/except — всё использовать.
ВАЖНО: покажи ошибку с .isdigit() и отрицательными числами.
Формат: задача → решение с type hints → 3 типичные ошибки → pytest тесты.
```

### 5. Задача Two Sum / поиск пар
```
Сгенерируй вариацию задачи "Two Sum" для Python собеседования.
Требования:
- не банальная версия (например, суммы пар товаров)
- покажи O(n²) решение и затем оптимизируй до O(n)
- объясни разницу в Big O
- type hints, pytest тесты с edge-кейсами (пустой список, нет решения, несколько пар)
```

---

## РАЗБОР ОШИБОК

### 6. Найди баг в коде
```
Найди все баги в этом Python коде и объясни каждый:
[ВСТАВЬ КОД]

Для каждого бага:
1. Что именно неправильно
2. При каком input сломается (приведи конкретный пример)
3. Как исправить
4. Какой pytest тест поймал бы этот баг
```

### 7. Code review как на собесе
```
Сделай code review этого Python кода как senior QA engineer на собеседовании:
[ВСТАВЬ КОД]

Оцени по критериям:
- Читаемость (naming, structure)
- Type hints (полнота)
- Edge-кейсы (обработаны ли)
- Производительность (Big O)
- Тестируемость (можно ли замокать зависимости)
- Pythonic style (comprehensions, идиомы)
Дай переработанную версию кода.
```

### 8. Объяснение через аналогию
```
Объясни разницу между list, tuple, set и dict в Python через аналогию с реальной жизнью.
Потом для каждого приведи типичную задачу с собеседования где именно эта структура — лучший выбор.
Добавь: когда НЕ нужно использовать каждую структуру.
```

---

## PYTEST И API ТЕСТЫ

### 9. Pytest fixtures для API
```
Напиши набор pytest fixtures для тестирования REST API (requests библиотека).
Контекст: e-commerce API (заказы, пользователи, товары).
Нужно:
- conftest.py с base_url, auth_headers, sample_data фикстурами
- мок HTTP ответов через unittest.mock.patch
- параметризованный тест для разных HTTP статус-кодов (200, 400, 404, 500)
- тест с side_effect для нестабильного API (первый запрос падает, второй ок)
Type hints везде.
```

### 10. Тесты для функции рефакторинга
```
Я рефакторю эту функцию:
[ВСТАВЬ СТАРЫЙ КОД]

Напиши pytest тесты которые:
1. Покрывают текущее поведение (регрессия)
2. Проверяют edge-кейсы которые могут сломаться при рефакторинге
3. Используют parametrize для разных входных данных
4. Проверяют что функция НЕ мутирует входные аргументы
Type hints в тестах, имена тестов: test_<функция>_<сценарий>.
```

### 11. Mock сложного API
```
Напиши pytest тест для функции которая:
1. Делает GET запрос к API
2. Парсит JSON ответ
3. Фильтрует данные по условию
4. Делает POST запрос с результатом

Используй unittest.mock.patch для mock обоих запросов.
Покажи как тестировать: success path, HTTP ошибки, невалидный JSON, timeout.
```

---

## АЛГОРИТМЫ

### 12. Оптимизация O(n²) → O(n)
```
У меня есть этот неэффективный Python код:
[ВСТАВЬ КОД]

1. Определи текущую сложность O(?)
2. Объясни почему это медленно
3. Предложи O(n) решение
4. Объясни trade-off (память vs время)
5. Напиши benchmark через timeit для сравнения
6. Напиши pytest тесты подтверждающие одинаковый результат
```

### 13. Задача на рекурсию
```
Сгенерируй задачу на рекурсию для Python собеседования (middle уровень).
Тема: деревья, вложенные структуры или divide & conquer.
Контекст: реальная задача QA (дерево зависимостей тестов, вложенные JSON конфиги).
Покажи: рекурсивное решение + итеративное через stack.
Объясни: когда рекурсия может упасть (RecursionError) и как защититься.
```

### 14. Задача на sliding window
```
Придумай задачу на sliding window / two pointers для Python собеседования.
Уровень: middle. Данные из мира e-commerce (временные ряды продаж, буферы заказов).
Формат: описание → brute force O(n²) → оптимизированное O(n) → объяснение → тесты.
```

---

## СИМУЛЯЦИЯ СОБЕСЕДОВАНИЯ

### 15. Полная симуляция (15 минут)
```
Симулируй live coding собеседование Python. Ты — интервьюер из WB/Ozon.
Правила:
- Дай одну задачу среднего уровня (comprehensions + парсинг + edge-кейсы)
- Жди моего решения
- После решения: задай 2 уточняющих вопроса (как оптимизировать, что если данные другие)
- Дай финальную оценку: что хорошо, что улучшить
НЕ давай подсказки пока я не попрошу.
```

### 16. Разбор провала
```
Я только что прошёл собеседование и не решил эту задачу:
[ОПИСАНИЕ ЗАДАЧИ]
Мой ответ был: [ЧТО СКАЗАЛ]

Разбери:
1. Правильное решение с объяснением
2. Что конкретно я должен был сказать в начале (уточняющие вопросы)
3. Шаги мышления которые стоило проговорить вслух
4. Красные флаги в моём ответе которые снижают оценку
5. Как бы ты оценил мой ответ и почему
```

### 17. Вопрос про сложность
```
Задай мне 5 вопросов о Big O нотации как на Python собеседовании (middle QA).
После каждого моего ответа — дай фидбек: правильно/неправильно/неполно.
Темы: list vs set lookup, dict операции, сортировка, вложенные циклы.
```

---

## ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ

### 18. Тестовые данные для API
```
Сгенерируй реалистичные тестовые данные для e-commerce API тестов (WB/Ozon стиль):
- 10 объектов заказа (orders) с полями: id, user_id, product, amount, status, created_at
- Include edge-кейсы: None значения, нулевая сумма, очень длинное название, спецсимволы
- Как pytest fixture с разными наборами данных (valid, invalid, boundary)
- Type hints через TypedDict
```

### 19. Параметры для parametrize
```
У меня есть эта функция:
[ВСТАВЬ ФУНКЦИЮ]

Сгенерируй исчерпывающий список параметров для @pytest.mark.parametrize:
- Happy path (3-5 случаев)
- Edge кейсы (пустые, None, граничные значения)
- Негативные кейсы (неверный тип, выход за пределы)
- Специфичные для этой функции corner cases
Формат: список кортежей с комментарием почему каждый важен.
```

### 20. Код для самопроверки
```
Дай мне задачу на [ТЕМА], которую я должен решить сам за 10 минут.
Правила:
- Только задание, без подсказок и решения
- Укажи: ожидаемый input/output, ограничения, edge-кейсы для проверки
- После того как я напишу код — проверь его и дай детальный фидбек

[Напиши своё решение здесь, потом попроси проверку]
```

---

## КАК ИСПОЛЬЗОВАТЬ ПРОМПТЫ

1. **Ежедневная разминка**: промпт #15 (симуляция) каждый день
2. **После ошибки**: #6 (найди баг) или #16 (разбор провала)
3. **Новые задачи**: #1–5 для свежих задач по конкретной теме
4. **Перед собесом**: #17 (Big O вопросы) + #15 (симуляция)
5. **Написал код**: #10 (тесты для рефакторинга) + #7 (code review)

## ШАБЛОН ДЛЯ СВОЕЙ ЗАДАЧИ

```
Контекст: [middle QA Python собес, WB/Ozon]
Тема: [comprehensions / dict / парсинг / алгоритм]
Сложность: [easy / medium / hard]
Мои слабые места: [comprehensions с условиями / отрицательные числа / set operations]

Задача: [описание]
Моё решение:
[КОД]

Прошу:
1. Найти ошибки
2. Предложить более pythonic вариант
3. Написать pytest тесты которые я пропустил
4. Оценить по критериям собеседования (1-5)
```
