"""Тестирование алгоритма скидки (Вариант 22: Автомобили)."""

from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    """Прогон тестов."""
    date = datetime(2026, 10, 15)

    test_cases = [
        # (id, цена, ожидание, пояснение)
        (1, 1800000, 1800000, "Honda Civic — есть заказы в сентябре"),
        (2, 2800000, 2800000, "Mazda CX-5 — есть заказы в сентябре"),
        (3, 2000000, 2000000, "Nissan Qashqai — есть заказы в сентябре"),
        (4, 3500000, 2625000, "VW Tiguan — нет заказов → 25% скидка"),
        (5, 1500000, 1125000, "Skoda Octavia — нет заказов → 25% скидка"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ (АВТОСАЛОН)")
    print("=" * 60)

    passed = 0
    for car_id, price, expected, comment in test_cases:
        result = calculate_price_with_discount(car_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Авто {car_id}: {price} → {int(result)} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()
