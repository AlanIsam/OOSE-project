from sale import Sale


def main():
    print("=== POS SYSTEM ===")

    sale = Sale()

    # --- Scan items ---
    while True:
        name = input("Enter item name (or 'done' to finish): ").strip()
        if name.lower() == "done":
            break

        try:
            price = float(input("Enter item price: RM "))
            qty = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid input. Try again.\n")
            continue

        sale.add_item(name, price, qty)
        print(f"Item added. Current total: RM {sale.total_amount:.2f}\n")

    if not sale.items:
        print("No items added. Sale cancelled.")
        return

    print("\n--- Checkout ---")
    print(f"Final Total: RM {sale.total_amount:.2f}")

    # --- Payment loop ---
    while True:
        payment_method = input("Payment method (cash/card/check) or 'cancel': ").lower()

        if payment_method == "cancel":
            print("Sale cancelled.")
            sale.status = "CANCELLED"
            return

        try:
            amount = float(input("Enter payment amount: RM "))
        except ValueError:
            print("Invalid amount. Try again.\n")
            continue

        success = sale.checkout(payment_method, amount)

        if success:
            print("\nPayment successful!")
            print(f"Sale ID: {sale.sale_id}")
            print("Status:", sale.status)
            break
        else:
            print("\nPayment failed.")
            print("Please retry or choose another payment method.\n")


if __name__ == "__main__":
    main()
