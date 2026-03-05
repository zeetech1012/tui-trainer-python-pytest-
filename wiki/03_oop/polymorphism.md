# Полиморфизм (Polymorphism)

> **Зачем автотестеру:** Полиморфизм позволяет писать общий код, который работает с разными типами объектов. В тестировании это проявляется через абстрактные базовые классы для репортеров, драйверов, клиентов — один интерфейс, разные реализации.

---

## Концепция

Полиморфизм (от греч. "многоформенность") — способность объектов разных классов реагировать на один и тот же метод по-разному. В Python полиморфизм реализуется через:

1. **Duck Typing** — "если ходит как утка и крякает как утка — это утка"
2. **Переопределение методов** — дочерний класс меняет поведение родителя
3. **Абстрактные классы** — обязательный контракт для наследников

---

## Duck Typing

Python не требует явного объявления интерфейсов. Если у объекта есть нужный метод — он подходит.

```python
class Dog:
    def speak(self) -> str:
        return "Woof!"

class Cat:
    def speak(self) -> str:
        return "Meow!"

class Robot:
    def speak(self) -> str:
        return "Beep boop"

def make_noise(creature) -> None:
    # Не важно, какого типа creature — лишь бы был метод speak()
    print(creature.speak())

make_noise(Dog())    # "Woof!"
make_noise(Cat())    # "Meow!"
make_noise(Robot())  # "Beep boop"
```

---

## Переопределение методов

```python
class Notifier:
    def send(self, message: str) -> bool:
        raise NotImplementedError("Subclasses must implement send()")


class EmailNotifier(Notifier):
    def __init__(self, email: str) -> None:
        self.email = email

    def send(self, message: str) -> bool:
        print(f"Email to {self.email}: {message}")
        return True


class SlackNotifier(Notifier):
    def __init__(self, channel: str) -> None:
        self.channel = channel

    def send(self, message: str) -> bool:
        print(f"Slack #{self.channel}: {message}")
        return True


class SMSNotifier(Notifier):
    def __init__(self, phone: str) -> None:
        self.phone = phone

    def send(self, message: str) -> bool:
        print(f"SMS to {self.phone}: {message}")
        return True


# Полиморфное использование — один и тот же код для всех типов
def notify_all(notifiers: list[Notifier], message: str) -> int:
    """Отправляет сообщение через все уведомители. Возвращает число успехов."""
    return sum(1 for n in notifiers if n.send(message))
```

---

## Абстрактные классы через `abc`

`ABC` (Abstract Base Class) обязывает наследников реализовать помеченные методы.

```python
from abc import ABC, abstractmethod


class BaseReporter(ABC):
    """Абстрактный базовый класс для отчётов о тестировании."""

    @abstractmethod
    def start_suite(self, name: str) -> None:
        """Начало тестового набора."""

    @abstractmethod
    def add_result(self, test_name: str, passed: bool, error: str = "") -> None:
        """Добавить результат теста."""

    @abstractmethod
    def finish_suite(self) -> dict:
        """Завершить набор и вернуть итоговую статистику."""

    def report_summary(self) -> str:
        """Обычный метод — доступен всем наследникам."""
        stats = self.finish_suite()
        return f"Total: {stats['total']}, Passed: {stats['passed']}, Failed: {stats['failed']}"


class ConsoleReporter(BaseReporter):
    def __init__(self) -> None:
        self._results: list[dict] = []

    def start_suite(self, name: str) -> None:
        print(f"\n=== Test Suite: {name} ===")

    def add_result(self, test_name: str, passed: bool, error: str = "") -> None:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {test_name}" + (f" — {error}" if error else ""))
        self._results.append({"name": test_name, "passed": passed})

    def finish_suite(self) -> dict:
        passed = sum(1 for r in self._results if r["passed"])
        return {
            "total": len(self._results),
            "passed": passed,
            "failed": len(self._results) - passed,
        }


class JSONReporter(BaseReporter):
    def __init__(self) -> None:
        self._suite_name = ""
        self._results: list[dict] = []

    def start_suite(self, name: str) -> None:
        self._suite_name = name

    def add_result(self, test_name: str, passed: bool, error: str = "") -> None:
        self._results.append({
            "test": test_name,
            "status": "passed" if passed else "failed",
            "error": error,
        })

    def finish_suite(self) -> dict:
        passed = sum(1 for r in self._results if r["status"] == "passed")
        return {
            "suite": self._suite_name,
            "total": len(self._results),
            "passed": passed,
            "failed": len(self._results) - passed,
            "results": self._results,
        }


# Нельзя создать экземпляр абстрактного класса
# BaseReporter()  # TypeError: Can't instantiate abstract class
```

---

## Абстрактный базовый класс: API Storage

```python
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """Контракт для хранилищ тестовых данных."""

    @abstractmethod
    def save(self, key: str, data: dict) -> None: ...

    @abstractmethod
    def load(self, key: str) -> dict | None: ...

    @abstractmethod
    def delete(self, key: str) -> bool: ...


class InMemoryStorage(BaseStorage):
    """Хранилище в памяти — для тестов."""

    def __init__(self) -> None:
        self._store: dict[str, dict] = {}

    def save(self, key: str, data: dict) -> None:
        self._store[key] = data

    def load(self, key: str) -> dict | None:
        return self._store.get(key)

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False


class FileStorage(BaseStorage):
    """Хранилище в файле — для production."""
    import json
    import pathlib

    def __init__(self, path: str) -> None:
        self._path = pathlib.Path(path)

    def save(self, key: str, data: dict) -> None:
        existing = self._load_all()
        existing[key] = data
        self._path.write_text(self.json.dumps(existing))

    def load(self, key: str) -> dict | None:
        return self._load_all().get(key)

    def delete(self, key: str) -> bool:
        existing = self._load_all()
        if key in existing:
            del existing[key]
            self._path.write_text(self.json.dumps(existing))
            return True
        return False

    def _load_all(self) -> dict:
        if not self._path.exists():
            return {}
        return self.json.loads(self._path.read_text())
```

---

## Как это выглядит в pytest

```python
import pytest
from abc import ABC, abstractmethod


class BaseReporter(ABC):
    @abstractmethod
    def start_suite(self, name: str) -> None: ...
    @abstractmethod
    def add_result(self, test_name: str, passed: bool, error: str = "") -> None: ...
    @abstractmethod
    def finish_suite(self) -> dict: ...


class ConsoleReporter(BaseReporter):
    def __init__(self) -> None:
        self._results: list[dict] = []

    def start_suite(self, name: str) -> None:
        pass

    def add_result(self, test_name: str, passed: bool, error: str = "") -> None:
        self._results.append({"name": test_name, "passed": passed})

    def finish_suite(self) -> dict:
        passed = sum(1 for r in self._results if r["passed"])
        return {"total": len(self._results), "passed": passed, "failed": len(self._results) - passed}


@pytest.fixture
def reporter() -> ConsoleReporter:
    return ConsoleReporter()


def test_reporter_empty_suite(reporter):
    reporter.start_suite("empty")
    stats = reporter.finish_suite()
    assert stats["total"] == 0
    assert stats["passed"] == 0


def test_reporter_counts_passed(reporter):
    reporter.start_suite("suite")
    reporter.add_result("test_one", passed=True)
    reporter.add_result("test_two", passed=True)
    stats = reporter.finish_suite()
    assert stats["passed"] == 2
    assert stats["failed"] == 0


def test_reporter_counts_failed(reporter):
    reporter.start_suite("suite")
    reporter.add_result("test_one", passed=True)
    reporter.add_result("test_two", passed=False, error="AssertionError")
    stats = reporter.finish_suite()
    assert stats["failed"] == 1


def test_abstract_class_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseReporter()


@pytest.mark.parametrize("reporter_class", [ConsoleReporter])
def test_reporter_implements_interface(reporter_class):
    """Проверяет что все реализации соответствуют интерфейсу."""
    assert issubclass(reporter_class, BaseReporter)
    reporter = reporter_class()
    reporter.start_suite("test")
    reporter.add_result("check", passed=True)
    stats = reporter.finish_suite()
    assert "total" in stats
    assert "passed" in stats
    assert "failed" in stats
```

---

## Edge-кейсы

| Ситуация | Проблема | Решение |
|----------|----------|---------|
| Забытый `@abstractmethod` | Можно создать базовый класс без реализации | Добавляй `@abstractmethod` ко всем обязательным методам |
| Duck typing без проверки | `AttributeError` в рантайме | Используй `hasattr()` или `isinstance()` для проверки |
| Переопределение без `super()` | Теряется поведение родителя | Осознанный выбор: замена vs расширение |

---

## Вопрос на собесе

**Q: Что такое duck typing?**

> Duck typing — принцип, при котором тип объекта определяется не его классом, а наличием нужных методов и атрибутов. "Если у объекта есть метод `send()` — он подходит как Notifier, независимо от того, от какого класса он унаследован."

**Q: Зачем абстрактные классы если можно просто поднять NotImplementedError?**

> `ABC` с `@abstractmethod` даёт ошибку **при создании объекта**, не при вызове метода. Это позволяет поймать проблему раньше. Также `isinstance(obj, BaseReporter)` гарантирует, что все абстрактные методы реализованы.
