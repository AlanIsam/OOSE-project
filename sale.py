# sale.py
from datetime import datetime
import uuid
from payment import CashPayment, CardPayment, CheckPayment
from sale_line_item import SaleLineItem


class Sale:
    def __init__(self):
        self.sale_id = str(uuid.uuid4())
        self.date = datetime.now()
        self.items = []              # List of SaleLineItem
        self.total_amount = 0.0
        self.status = "OPEN"
        self.payment = None
        self.coupon = None

    # =========================
    # SALE LINE ITEM HANDLING
    # =========================
    def add_item(self, name, price, quantity=1):
        item = SaleLineItem(name, price, quantity)
        self.items.append(item)
        self.calculate_total()

    def calculate_total(self):
        self.total_amount = sum(item.calculateSubTotal() for item in self.items)
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

        print(f"✅ Coupon applied! Discount: RM {discount:.2f}")
        print(f"🧾 New total: RM {self.total_amount:.2f}")
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
            print("❌ Invalid payment method.")
            return False

        if payment.process_payment(self.total_amount):
            self.payment = payment
            self.status = "PAID"
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

        cashier_name = self.cashier.username if hasattr(self, "cashier") else "N/A"
        lines.append(f"Cashier   : {cashier_name}")

        customer_name = self.customer.name if hasattr(self, "customer") else "Walk-in"
        lines.append(f"Customer  : {customer_name}")

        lines.append("-------------------------")

        for item in self.items:
            lines.append(
                f"{item.getItemName()} x{item.quantity} "
                f"= RM {item.calculateSubTotal():.2f}"
            )

        lines.append("-------------------------")

        if self.coupon:
            discount = self.coupon.calculateDiscount(
                self.total_amount / (1 - self.coupon.discount_rate)
            )
            lines.append(f"Coupon ({self.coupon.coupon_code}): -RM {discount:.2f}")

        lines.append(f"TOTAL     : RM {self.total_amount:.2f}")
        lines.append(f"Payment   : {self.payment.__class__.__name__}")
        lines.append("STATUS    : PAID")
        lines.append("=========================")

        return "\n".join(lines)

    def save_receipt(self):
        filename = f"receipt_{self.sale_id}.txt"
        with open(filename, "w") as file:
            file.write(self.generate_receipt())

        print(f"🧾 Receipt generated: {filename}")
