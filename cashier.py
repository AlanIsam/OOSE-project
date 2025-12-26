from user import User
from sale import Sale
from customer import Customer
from coupon import Coupon
from catalogueSystem import BackendCatalogueSystem
from return_item import Return


class Cashier(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password, role="Cashier")

    def handleSales(self):
        """Handle sales transaction"""
        sale = Sale()
        customer = Customer(0, "Walk-in Customer")

        sale.cashier = self
        sale.customer = customer

        # -------------------------
        # ADD ITEMS
        # -------------------------
        while True:
            name = input("Enter item name (or 'done'): ").strip()
            if name.lower() == "done":
                break

            try:
                qty = int(input("Enter quantity: "))
            except ValueError:
                print(" Invalid input.\n")
                continue

            if sale.add_item(name, qty):
                print(f"Item added. Current total: RM {sale.total_amount:.2f}\n")
            else:
                print(" Item not found.\n")

        if not sale.items:
            print(" No items added. Sale cancelled.")
            return

        # -------------------------
        # COUPON FLOW
        # -------------------------
        coupons = Coupon.load_coupons_from_file()

        while True:
            print(f"\n Subtotal: RM {sale.total_amount:.2f}")
            use_coupon = input("Apply coupon? (yes/no): ").lower().strip()

            if use_coupon == "no":
                break

            if use_coupon != "yes":
                print(" Please enter 'yes' or 'no'.")
                continue

            code = input("Enter coupon code: ").strip().upper()
            coupon = coupons.get(code)

            if not coupon:
                print(" Invalid coupon code.")
                continue

            if sale.apply_coupon(coupon):
                break
            else:
                print("🔁 Coupon not applied. Returning to subtotal...")

        # -------------------------
        # PAYMENT LOOP
        # -------------------------
        while True:
            payment_method = input("\nPayment method (cash/card/check) or 'cancel': ").lower()

            if payment_method == "cancel":
                print(" Sale cancelled.")
                sale.status = "CANCELLED"
                return

            try:
                amount = float(input("Enter payment amount: RM "))
            except ValueError:
                print(" Invalid amount.")
                continue

            if sale.checkout(payment_method, amount):
                print("\n Payment successful!")
                print(f"Sale ID: {sale.sale_id}")
                print(f"Status: {sale.status}")
                sale.save_receipt()
                break
            else:
                print(" Payment failed. Try again.")

    def handleReturn(self):
        """Handle return transaction"""
        print(" RETURN SYSTEM")
        print(f"Staff on duty: {self}\n")

        receipt_id = input("Enter original receipt ID: ").strip()
        catalogue = BackendCatalogueSystem()
        return_obj = Return(receipt_id, catalogue)

        if not return_obj.verifyoriginalreceipt():
            print(" Receipt not found.")
            return

        print(" Receipt verified.")        
        # Show items from the original receipt
        return_obj.view_receipt_items()
        # -------------------------
        # ADD ITEMS TO RETURN
        # -------------------------
        while True:
            item_name = input("Enter item name to return (or 'done'): ").strip()
            if item_name.lower() == "done":
                break

            try:
                qty = int(input("Enter quantity: "))
            except ValueError:
                print(" Invalid quantity.\n")
                continue

            if return_obj.additemtoreturn(item_name, qty):
                print(f"Item added. Current refund: RM {return_obj.return_total:.2f}\n")
            else:
                print(" Item not found.\n")

        if return_obj.return_items:
            return_obj.process_return()
            print(" Return processed.")
        else:
            print(" No items to return.")
