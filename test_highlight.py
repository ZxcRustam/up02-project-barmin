"""Тестирование подсветки товаров."""
from catalog import _get_card_color
from styles import COLOR_HIGHLIGHT, COLOR_MAIN_BG


def test_highlight():
    """Прогон тестов для подсветки."""
    test_cases = [
        # (qty, expected_color, comment)
        (10, COLOR_MAIN_BG, "10 > 3 — нет подсветки"),
        (5, COLOR_MAIN_BG, "5 > 3 — нет подсветки"),
        (4, COLOR_MAIN_BG, "4 > 3 — нет подсветки"),
        (3, COLOR_HIGHLIGHT, "3 ≤ 3 — подсветка (граница)"),
        (2, COLOR_HIGHLIGHT, "2 ≤ 3 — подсветка"),
        (1, COLOR_HIGHLIGHT, "1 ≤ 3 — подсветка"),
        (0, COLOR_HIGHLIGHT, "0 ≤ 3 — подсветка"),
    ]

    print("=" * 70)
    print("ТЕСТИРОВАНИЕ ПОДСВЕТКИ")
    print("=" * 70)

    passed = 0
    for qty, expected, comment in test_cases:
        result = _get_card_color(qty)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} qty={qty}: {result} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    test_highlight()