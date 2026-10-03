class Product:
    def __init__(self, name: str, price: float, qty: int):
        self.name = name
        self.price = price
        self.qty = qty

    def total(self) -> float:
        """Возвращает общую стоимость товара."""
        return self.price * self.qty

    def info(self) -> str:
        """Возвращает форматированную строку с информацией о товаре."""
        total_cost = int(self.total())
        price_int = int(self.price)
        return f"{self.name}: {price_int} × {self.qty} = {total_cost} руб."


def main():
    p1 = Product("Кроссовки", 8500, 3)
    p2 = Product("Ботинки", 15000, 1)
    p3 = Product("Туфли", 12000, 5)

    print(p1.info())
    print(p2.info())
    print(p3.info())


if __name__ == "__main__":
    main()
