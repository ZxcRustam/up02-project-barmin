"""Тестирование индикатора «много/мало» с учетом ДЗ."""
from catalog import _indicator


def test_indicator():
    """Прогон тестов для индикатора (расширенная версия)."""
    test_cases = [
        # (qty, expected, comment)
        (10, "много", "10 > 5"),
        (6, "много", "6 > 5 (граница)"),
        (5, "мало", "5 ≤ 5 (граница)"),
        (4, "мало", "4 ≤ 5"),
        (1, "мало", "1 ≤ 5"),
        (0, "мало", "0 ≤ 5"),
        (100, "много", "большое число"),
        # Домашнее задание: 5 новых тестов
        (1000, "много", "ДЗ: большое число 1000"),
        (50, "много", "ДЗ: среднее значение 50"),
        (5, "мало", "ДЗ: повтор границы 5"),
        (6, "много", "ДЗ: повтор границы 6"),
        (-1, "мало", "ДЗ: крайний случай -1"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ИНДИКАТОРА (РАСШИРЕННОЕ)")
    print("=" * 60)

    passed = 0
    for qty, expected, comment in test_cases:
        result = _indicator(qty)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} qty={qty}: {result} (ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    test_indicator()
