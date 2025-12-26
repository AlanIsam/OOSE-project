# sale.py
from datetime import datetime
import uuid
import os
from payment import CashPayment, CardPayment, CheckPayment
from catalogueSystem import BackendCatalogueSystem
from inventorySystem import InventorySystem
from sale_line_item import SaleLineItem


class Sale:
    def __init__(self):
        self.sale_id = str(uuid.uuid4())
        self.date = datetime.now()
        self.items = []              # List[SaleLineItem]
        self.total_amount = 0.0
        self.status = "OPEN"
        self.payment = None
        self.coupon = None
        self.cashier = None
        self.customer = None

        self.catalogue = BackendCatalogueSystem()
        self.inventory = InventorySystem(self.catalogue)

    # =========================
    # SALE LINE ITEM
    # =========================
    def add_item(self, name, quantity):
        item = self.catalogue.get_item_by_name(name)

        if not item:
            print(f"Item '{name}' not found.")
            return False

        # Optional: stock check
        if quantity > item.stock_quantity:
            print(f"Not enough stock. Available: {item.stock_quantity}")
            return False

        sale_item = SaleLineItem(item, quantity)
        self.items.append(sale_item)
        self.calculate_total()
        return True

    def calculate_total(self):
        self.total_amount = sum(
            item.calculateSubTotal() for item in self.items
        )
        return self.total_amount

    # =========================
    # COUPON
    # =========================
    def apply_coupon(self, coupon):
        if not coupon.isValid():
            return False

        discount = coupon.calculateDiscount(self.total_amount)
        self.total_amount -= discount
        coupon.markAsUsed()
        self.coupon = coupon

        print(f"Coupon applied! Discount: RM {discount:.2f}")
        print(f"New total: RM {self.total_amount:.2f}")
        return True

    # =========================
    # PAYMENT
    # =========================
    def checkout(self, payment_type, amount):
        if payment_type == "cash":
            payment = CashPayment(amount)
        elif payment_type == "card":
            payment = CardPayment(amount)
        elif payment_type == "check":
            payment = CheckPayment(amount)
        else:
            print("Invalid payment method.")
            return False

        if payment.process_payment(self.total_amount):
            self.payment = payment
            self.status = "PAID"

            # Update inventory
            for sale_item in self.items:
                self.inventory.updatestock(
                    sale_item.item.barcode,
                    -sale_item.quantity
                )

            return True

        return False

    # =========================
    # RECEIPT
    # =========================
    def generate_receipt(self):
        lines = []
        lines.append("======== RECEIPT ========")
        lines.append(f"Sale ID   : {self.sale_id}")
        lines.append(f"Date      : {self.date.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Cashier   : {self.cashier.username}")
        lines.append(f"Customer  : {self.customer.name}")
        lines.append("-------------------------")

        for item in self.items:
            lines.append(
                f"{item.getItemName()} x{item.quantity} "
                f"= RM {item.calculateSubTotal():.2f}"
            )

        lines.append("-------------------------")

        if self.coupon:
            lines.append(f"Coupon {self.coupon.coupon_code} applied")

        lines.append(f"TOTAL     : RM {self.total_amount:.2f}")
        lines.append(f"Payment   : {self.payment.__class__.__name__}")
        lines.append("STATUS    : PAID")
        lines.append("=========================")

        return "\n".join(lines)

    def record_transaction(self):
        # Store sale record in transaction_record.txt using ":" as tokenizer
        payment_type = self.payment.__class__.__name__ if self.payment else "N/A"
        items_summary = ";".join([f"{item.getItemName()}x{item.quantity}" for item in self.items])
        record = f"{self.sale_id}:{self.date.strftime('%Y-%m-%d %H:%M:%S')}:{self.cashier.username}:{self.customer.name}:{items_summary}:{self.total_amount:.2f}:{payment_type}"
        with open("transaction_record.txt", 'a') as f:
            f.write(record + "\n")

    def save_receipt(self):
        folder = "receipt_record"
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = f"{folder}/receipt_{self.sale_id}.txt"
        with open(filename, "w") as f:
            f.write(self.generate_receipt())
        self.record_transaction()

        print(f"🧾 Receipt generated: {filename}")
