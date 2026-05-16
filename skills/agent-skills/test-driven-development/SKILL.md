---
name: test-driven-development
description: Разработка через тесты (TDD). Используй при реализации логики, фиксе багов, изменении поведения. pytest/unittest вместо Jest. Адаптировано под Python/Bash.
---

# Test-Driven Development (Python/Bash Edition)

## Overview

Напиши падающий тест ДО написания кода. Для фикса багов — воспроизведи баг тестом ДО исправления. Тесты — это доказательство, «кажется правильным» — это не сделано.

## Когда использовать

- Реализация новой логики или поведения
- Фикс любого бага (Prove-It Pattern)
- Изменение существующей функциональности
- Добавление edge case handling

**НЕ использовать:** Чисто конфигурационные изменения, обновления документации, статический контент без поведенческого воздействия.

## TDD Cycle

```
    RED                GREEN              REFACTOR
 Напиши тест  →  Напиши минимальный  →  Почини код  →  (повтори)
 который падает     код чтобы прошёл
```

## Python: pytest

### Структура теста
```python
# tests/test_module.py
import pytest
from mymodule import my_function

def test_basic_case():
    """Тест базового случая"""
    assert my_function(2, 3) == 5

def test_edge_case_zero():
    """Граничный случай — ноль"""
    assert my_function(0, 5) == 5

def test_edge_case_negative():
    """Граничный случай — отрицательные"""
    assert my_function(-1, 1) == 0

def test_invalid_input():
    """Невалидный ввод"""
    with pytest.raises(ValueError):
        my_function("a", "b")
```

### Запуск
```bash
# Все тесты
pytest

# Конкретный тест
pytest tests/test_module.py::test_basic_case -v

# С покрытием
pytest --cov=mymodule --cov-report=term-missing

# Только падающие
pytest --lf
```

### Fixtures
```python
@pytest.fixture
def sample_data():
    """Тестовые данные"""
    return {"name": "test", "value": 42}

def test_with_fixture(sample_data):
    assert sample_data["value"] == 42
```

### Parametrize
```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (0, 0),
    (-1, 1),
])
def test_square(input, expected):
    assert square(input) == expected
```

## Bash: BATS (Bash Automated Testing System)

### Структура
```bash
#!/usr/bin/env bats

@test "basic functionality" {
  run my_function "hello"
  [ "$status" -eq 0 ]
  [ "$output" = "HELLO" ]
}

@test "handles empty input" {
  run my_function ""
  [ "$status" -eq 1 ]
}

@test "handles file not found" {
  run process_file "/nonexistent"
  [ "$status" -eq 2 ]
  [[ "$output" == *"not found"* ]]
}
```

### Запуск
```bash
bats test_script.bats
```

## Для наших проектов

### IoT-проекты
```python
# tests/test_sensor_reader.py
def test_sensor_reading_parsing():
    raw = "temp:23.5,humidity:65"
    result = parse_sensor_data(raw)
    assert result["temperature"] == 23.5
    assert result["humidity"] == 65

def test_sensor_timeout():
    with pytest.raises(TimeoutError):
        read_sensor(timeout=0.001)
```

### Агроаналитика
```python
# tests/test_agronomy.py
def test_gdd_calculation():
    """Тест расчёта сумм активных температур"""
    temps = [15, 18, 22, 12, 25]
    base_temp = 10
    gdd = calculate_gdd(temps, base_temp)
    assert gdd == (5 + 8 + 12 + 2 + 15)

def test_irrigation_threshold():
    """Тест порога полива"""
    assert should_irrigate(swd=0.15, threshold=0.2) == True
    assert should_irrigate(swd=0.25, threshold=0.2) == False
```

### OpenClaw-навыки
```python
# tests/test_skill.py
def test_skill_trigger():
    """Тест что навык активируется по триггеру"""
    assert is_triggered("проверь систему", "quick-check")
    assert not is_triggered("погода в Москве", "quick-check")
```

## Anti-Patterns

| Паттерн | Проблема | Решение |
|---------|----------|---------|
| "Добавлю тесты потом" | Потом никогда не будет | RED → GREEN → REFACTOR |
| Тест проверяет реализацию | Ломается при рефакторинге | Тестируй поведение |
| Один огромный тест | Не понятно что сломалось | Много маленьких тестов |
| Тесты без edge cases | Баги в проде | 0, None, пустые строки, границы |
| Мок всего | Тест не проверяет реальность | Мокай только внешние зависимости |

## Тестовая пирамида

```
        /  E2E  \          ← 5%  (медленные, дорогие)
       / Integration \     ← 15% (API, БД, внешние сервисы)
      /    Unit       \    ← 80% (быстрые, изолированные)
```

## Checklist

- [ ] Тест написан ДО кода (RED)
- [ ] Тест падает по правильной причине
- [ ] Минимальный код чтобы тест прошёл (GREEN)
- [ ] Рефакторинг с зелёными тестами
- [ ] Edge cases покрыты
- [ ] Тесты быстрые (< 1 сек на тест)
- [ ] Имена тестов описывают поведение

## См. также

- `code-review-and-quality` — ревью тестов
- `debugging-and-error-recovery` — когда тесты падают
- `testing-patterns.md` — паттерны тестирования
