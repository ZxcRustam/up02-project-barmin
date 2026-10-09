"""Тестирование подсветки."""
from catalog import _get_card_color
from styles import COLOR_HIGHLIGHT, COLOR_MAIN_BG


def test_color():
    """
    Прогон тестов для подсветки.
    """
    test_cases = [
        (10, COLOR_MAIN_BG, "10 > 3"),
        (5, COLOR_MAIN_BG, "5 > 3"),
        (4, COLOR_MAIN_BG, "4 > 3"),
        (3, COLOR_HIGHLIGHT, "3 ≤ 3 (граница!)"),
        (2, COLOR_HIGHLIGHT, "2 ≤ 3"),
        (0, COLOR_HIGHLIGHT, "0 ≤ 3"),
        # Дополнительные 2 теста по заданию 5.6
        (100, COLOR_MAIN_BG, "большое число"),
        (-1, COLOR_HIGHLIGHT, "отрицательное"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ПОДСВЕТКИ")
    print("=" * 60)

    passed = 0
    for qty, expected, comment in test_cases:
        result = _get_card_color(qty)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} qty={qty}: {result} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    test_color()
