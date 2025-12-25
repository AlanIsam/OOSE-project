from sale import Sale
from coupon import Coupon
from customer import Customer
from user import User, Cashier, Administrator


def main():
    print("=== POS SYSTEM LOGIN ===")
    user = None

    # Login loop
    while user is None:
        username = input("👤 Enter username: ").strip()
        password = input("🔒 Enter password: ").strip()
        user = User.login(username, password)

        if user is None:
            print("❌ Login failed. Try again.\n")

    print(f"\n✅ Welcome, {user}!\n")

    # Create sale
    sale = Sale()
    customer = Customer(0, "Walk-in Customer")
    sale.cashier = user
    sale.customer = customer

    print(f"Staff on duty: {user}")
    print(f"Customer: {customer.name}\n")

    # Add items
    while True:
        name = input("Enter item name (or 'done'): ").strip()
        if name.lower() == "done":
            break

        try:
            price = float(input("Enter item price: RM "))
            qty = int(input("Enter quantity: "))
        except ValueError:
            print("❌ Invalid input.\n")
            continue

        sale.add_item(name, price, qty)
        print(f"Item added. Current total: RM {sale.total_amount:.2f}\n")

    if not sale.items:
        print("❌ No items added. Sale cancelled.")
        return

    print(f"\n🧾 Subtotal: RM {sale.total_amount:.2f}")

    # Load coupons from file
    coupons = Coupon.load_coupons_from_file()

    use_coupon = input("Apply coupon? (yes/no): ").lower().strip()
    if use_coupon == "yes":
        code = input("Enter coupon code: ").strip().upper()
        coupon = coupons.get(code)

        if coupon:
            sale.apply_coupon(coupon)
        else:
            print("❌ Invalid coupon code.")

    # Payment loop
    while True:
        payment_method = input("\nPayment method (cash/card/check) or 'cancel': ").lower()

        if payment_method == "cancel":
            print("❌ Sale cancelled.")
            sale.status = "CANCELLED"
            return

        try:
            amount = float(input("Enter payment amount: RM "))
        except ValueError:
            print("❌ Invalid amount.")
            continue

        if sale.checkout(payment_method, amount):
            print("\n✅ Payment successful!")
            print(f"Sale ID: {sale.sale_id}")
            print(f"Status: {sale.status}")
            break
        else:
            print("❌ Payment failed. Try again.")


if __name__ == "__main__":
    main()
