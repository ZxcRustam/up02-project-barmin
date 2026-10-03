def main():
    catalog = [
        {"name": "Кроссовки", "price": 8500, "qty": 3},
        {"name": "Ботинки", "price": 15000, "qty": 1},
        {"name": "Туфли", "price": 12000, "qty": 5},
        {"name": "Сандалии", "price": 4500, "qty": 8},
        {"name": "Кеды", "price": 6000, "qty": 2},
    ]

    total_sum = 0

    print("Каталог товаров:")

    for i, item in enumerate(catalog, start=1):
        name = item["name"]
        price = item["price"]
        qty = item["qty"]

        item_total = price * qty
        total_sum += item_total

        # Используем форматирование строк с выравниванием по левому краю для имени (до 10 символов),
        # чтобы прочерки и цены стояли ровно, как в примере
        print(f"{i}. {name:<10} — {price} × {qty} = {item_total} руб.")

    print("-" * 30)
    print(f"Итого: {total_sum} руб.")


if __name__ == "__main__":
    main()
