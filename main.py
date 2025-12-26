# main.py
from user import User
from cashier import Cashier
from administrator import Administrator


def cashier_pos_flow(user):

    """Cashier POS workflow"""
    print("🛒 POS SYSTEM (Cashier Mode)")
    print(f"Staff on duty: {user}\n")

    choice = input("Choose action: (sale/return): ").lower().strip()
    if choice == "sale":
        user.handleSales()
    elif choice == "return":
        user.handleReturn()
    else:
        print(" Invalid choice.")


def admin_flow(user):
    # Administrator dashboard
    print("🔧 Administrator Mode")
    result = user.admin_dashboard()

    if result == "logout":
        user.logout()


def main():
    while True:
        user = User.login_loop()

        # -------------------------
        # ROLE ROUTING
        # -------------------------
        if isinstance(user, Administrator):
            admin_flow(user)

        elif isinstance(user, Cashier):
            cashier_pos_flow(user)

        else:
            print(" Unknown user role.")

        # -------------------------
        # POST SESSION
        # -------------------------
        choice = input("\nReturn to login? (yes/no): ").lower().strip()
        if choice != "yes":
            print("👋 Exiting POS system. Goodbye!")
            break


if __name__ == "__main__":
    main()
