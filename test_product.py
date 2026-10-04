"""Проверка класса Product (Вариант 22: Автомобили)."""
from models import Product

p = Product(
    product_id=1,
    brand="Honda",
    model="Civic",
    year=2020,
    price=1800000,
    quantity=4,
    photo="civic.png"
)

print(p.info())
print(f"Со скидкой 25%: {p.price_with_discount(25):.2f} руб.")
