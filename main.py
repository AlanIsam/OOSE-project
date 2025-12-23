import customer
from sale import Sale
from user import Cashier, Administrator
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
    print("=== POS SYSTEM ===")

    #predefined users
    users = [
        Cashier(101, "Jaz", "Jaz123"),
        Administrator(201, "admin01", "admin123")
    ]

    #predefined customers
    customers = [
        Customer(101, "George", "012-345 6789"),
        Customer(102, "Helen", "013-213 6621")
    ]

    logged_in_user = None
    while logged_in_user is None:
        logged_in_user = login(users)

    # Role-based Menu System
    role = logged_in_user.get_role()

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
