def main():
    catalog = [
        {"name": "Кроссовки", "price": 8500, "qty": 3},
        {"name": "Ботинки", "price": 15000, "qty": 1},
        {"name": "Туфли", "price": 12000, "qty": 5},
        {"name": "Сандалии", "price": 4500, "qty": 8},
        {"name": "Кеды", "price": 6000, "qty": 2},
    ]

    catalog.sort(key=lambda item: item["qty"], reverse=True)

    print("Каталог с индикатором:")

    for i, item in enumerate(catalog, start=1):
        name = item["name"]
        qty = item["qty"]

        if qty > 5:
            indicator = "много"
        else:
            indicator = "мало"

        # Форматированный вывод с выравниванием названия (до 10 символов)
        print(f"{i}. {name:<10} — {qty} шт. → {indicator}")


if __name__ == "__main__":
    main()
