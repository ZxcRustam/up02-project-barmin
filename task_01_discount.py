def main():
    price = float(input("Введите цену: "))
    discount_percentage = float(input("Введите скидку (%): "))

    final_price = price * (1 - discount_percentage / 100)

    print(f"Цена со скидкой: {final_price:.2f} руб.")


if __name__ == "__main__":
    main()
