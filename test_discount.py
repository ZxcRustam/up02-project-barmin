"""Тестирование алгоритма скидки — Расширенное ДЗ (Вариант 22: Автомобили)."""

from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    """Прогон расширенного набора тестов (10 тест-кейсов)."""
    print("=" * 75)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ (ВАР 22: АВТОСАЛОН)")
    print("=" * 75)

    passed = 0
    
    # НАБОР ТЕСТОВ 1: Проверка в октябре 2026 (анализ заказов за сентябрь)
    date_october = datetime(2026, 10, 15)
    test_cases_october = [
        (1, 1800000, 1800000, "Honda Civic — есть заказы в сентябре (без скидки)"),
        (2, 2800000, 2800000, "Mazda CX-5 — есть заказы в сентябре (без скидки)"),
        (3, 2000000, 2000000, "Nissan Qashqai — есть заказы в сентябре (без скидки)"),
        (4, 3500000, 2625000, "VW Tiguan — нет заказов в сентябре → скидка 25%"),
        (5, 1500000, 1125000, "Skoda Octavia — нет заказов в сентябре → скидка 25%"),
    ]

    # НАБОР ТЕСТОВ 2 (НОВЫЕ ДЛЯ ДЗ): Проверка в ноябре 2026 (анализ за октябрь)
    # В октябре заказов в БД нет, поэтому все эти машины должны получить скидку 25%
    date_november = datetime(2026, 11, 5)
    test_cases_november = [
        (1, 1800000, 1350000, "Honda Civic — нет заказов в октябре → скидка 25%"),
        (3, 2000000, 1500000, "Nissan Qashqai — нет заказов в октябре → скидка 25%"),
        (6, 1700000, 1275000, "Renault Duster — нет заказов в октябре → скидка 25%"),
        (7, 3000000, 2250000, "Kia Sportage — нет заказов в октябре → скидка 25%"),
        (4, 3500000, 2625000, "VW Tiguan — нет заказов в октябре → скидка 25%"),
    ]

    # Запуск первой группы тестов (Октябрь)
    print(f"\n📅 Дата проверки: {date_october.strftime('%d.%m.%Y')} (Анализ за сентябрь):")
    for car_id, price, expected, comment in test_cases_october:
        result = calculate_price_with_discount(car_id, price, date_october)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Авто ID {car_id}: {price} -> {int(result)} (ожидалось {expected}) — {comment}")

    # Запуск второй группы тестов (Ноябрь)
    print(f"\n📅 Дата проверки: {date_november.strftime('%d.%m.%Y')} (Анализ за октябрь):")
    for car_id, price, expected, comment in test_cases_november:
        result = calculate_price_with_discount(car_id, price, date_november)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Авто ID {car_id}: {price} -> {int(result)} (ожидалось {expected}) — {comment}")

    print("=" * 75)
    print(f"ИТОГ ДЗ: Пройдено тестов: {passed} / 10")
    print("=" * 75)


if __name__ == "__main__":
    run_tests()
