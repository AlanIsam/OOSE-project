import customer
from sale import Sale
from user import User, Cashier, Administrator
from customer import Customer

#login function
def login(users):
    print("\n=== LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")

    for user in users:
        if user.authenticate(username, password):
            print(f"\nLogin successful! Welcome {user.role}.")
            return user

    print("\nInvalid username or password.")
    return None


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

    #choose function before proceed as cashier
    if role == "Cashier":
        print(f"\n--- Cashier Menu ({logged_in_user.username}) ---")
        print("1. Start Sale")
        print("2. Return Item")
        choice = input("Select an option (1-2): ")

        if choice == "1":
            print("\nInitializing new sale...")
            sale = Sale()

            # --- Search for Customer ---
            customer_id_input = input("Enter Customer ID: ")
            selected_customer = None
            
            # Loop through the list to find the matching ID
            for c in customers:
                if str(c.customer_id) == customer_id_input:
                    selected_customer = c
                    break
            
            # If not found, create a temporary "Walk-in" customer
            if selected_customer is None:
                print("Customer not found. Proceeding as Walk-in.")
                selected_customer = Customer(0, "Walk-in", "N/A")

            sale.cashier = logged_in_user
            sale.customer = selected_customer # Assign the object, not just a name

            print(f"\nCashier on duty: {logged_in_user}")
            print(f"Customer: {selected_customer.name}\n")

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

        elif choice == "2":
            print("\nInitializing return process...")
            # Logic for returns

    elif role == "Administrator":
        print(f"\n--- Admin Menu ({logged_in_user.username}) ---")
        print("1. User Management")
        print("2. Security Configuration")
        choice = input("Select an option (1-2): ")

        if choice == "1":
            print("\nOpening User Management...")
        elif choice == "2":
            print("\nOpening Security Configuration...")

    else:
        print("Unknown role. Access denied.")



if __name__ == "__main__":
    main()
