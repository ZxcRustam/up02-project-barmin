"""Тестирование каталога."""
import db_products as db


def test_db_available():
    """
    Проверяет, что БД доступна.
    """
    try:
        products = db.get_all_products()
        return isinstance(products, list)
    except Exception as e:
        print(f"❌ БД недоступна: {e}")
        return False


def test_products_count():
    """
    Проверяет, что товары загружены.
    """
    products = db.get_all_products()
    return len(products) > 0


def test_product_fields():
    """
    Проверяет, что у всех товаров есть ключевые атрибуты.
    """
    products = db.get_all_products()
    for p in products:
        if not hasattr(p, 'model') or not hasattr(p, 'price') or not hasattr(p, 'quantity'):
            print(f"❌ Товар id={getattr(p, 'id', 'unknown')}: отсутствуют обязательные поля")
            return False
    return True


def test_prices_are_numbers():
    """
    Проверяет, что все цены — числа или отсутствуют (обработаны).
    """
    products = db.get_all_products()
    for p in products:
        if p.price is not None and not isinstance(p.price, (int, float)):
            print(f"❌ Товар id={getattr(p, 'id', 'unknown')}: цена не число")
            return False
    return True


def test_quantity_not_negative():
    """
    Проверяет, что количество не отрицательное.
    """
    products = db.get_all_products()
    for p in products:
        if p.quantity is not None and p.quantity < 0:
            print(f"❌ Товар id={getattr(p, 'id', 'unknown')}: отрицательное количество")
            return False
    return True


def test_names_not_empty():
    """
    Проверяет, что у всех товаров есть название (модель).
    """
    products = db.get_all_products()
    for p in products:
        if not p.model:
            print(f"❌ Товар id={getattr(p, 'id', 'unknown')}: пустое название")
            return False
    return True


# Домашнее задание 2: тест проверки картинок
def test_at_least_one_image():
    """
    Проверяет, что хотя бы у одного товара есть изображение.
    """
    products = db.get_all_products()
    for p in products:
        if hasattr(p, 'photo') and p.photo and p.photo.strip():
            return True
    print("❌ Ни у одного товара нет изображения")
    return False


def run_all_tests():
    """
    Прогон всех тестов каталога.
    """
    tests = [
        ("БД доступна", test_db_available),
        ("Товары загружены", test_products_count),
        ("У всех товаров нужные поля", test_product_fields),
        ("Все цены — числа", test_prices_are_numbers),
        ("Количество не отрицательное", test_quantity_not_negative),
        ("Названия не пустые", test_names_not_empty),
        ("Хотя бы у одного товара есть фото", test_at_least_one_image),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КАТАЛОГА")
    print("=" * 60)

    passed = 0
    for name, func in tests:
        result = func()
        status = "✅" if result else "❌"
        if result:
            passed += 1
        print(f"{status} {name}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(tests)}")


if __name__ == "__main__":
    run_all_tests()
