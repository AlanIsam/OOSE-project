from sale import Sale
from user import User, Cashier, Administrator
from customer import Customer


def main():
    print("=== POS SYSTEM LOGIN ===")

    user = None

    # Main application loop
    while True:
        # Login system (only if not logged in)
        if user is None:
            while True:
                username = input("👤 Enter username: ").strip()
                password = input("🔒 Enter password: ").strip()

                user = User.login(username, password)

                if user is None:
                    print("❌ Login failed. Please try again.\n")
                    continue
                else:
                    print(f"✅ Welcome to the POS System, {user.username}!\n")
                    break

        # Role-based interface selection
        if isinstance(user, Administrator):
            print("🔧 Administrator access granted.")
            choice = input("Choose interface - (admin) Admin Dashboard or (pos) POS System: ").lower().strip()

            if choice == "admin":
                result = user.admin_dashboard()
                if result == "logout":
                    print("\n🔄 Returning to login...\n")
                    user = None  # Reset user to trigger login
                    continue
            elif choice == "pos":
                # Continue to POS system
                pass
            else:
                print("❌ Invalid choice. Continuing to POS system...")

        elif isinstance(user, Cashier):
            print("🛒 Cashier access granted.")
            # Continue to POS system
            pass
        else:
            print("❌ Unknown user role. Access denied.")
            user = None
            continue

        # POS System
        print("\n=== POS SYSTEM ===")
        print(f"Staff on duty: {user}")

        # Optional: walk-in customer
        customer = Customer(
            customer_id=201,
            name="Walk-in Customer"
        )

        # Create a sale handled by the logged-in staff
        sale = Sale()
        sale.cashier = user  # Use the logged-in user
        sale.customer = customer

        print(f"Staff on duty: {user}")
        print(f"Customer: {customer}\n")

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
