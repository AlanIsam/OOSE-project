# sale.py
from datetime import datetime
import uuid
from payment import CashPayment, CardPayment, CheckPayment


class Sale:
    def __init__(self):
        self.sale_id = str(uuid.uuid4())
        self.date = datetime.now()
        self.items = []
        self.total_amount = 0.0
        self.status = "OPEN"
        self.payment = None
        self.coupon = None

    def add_item(self, name, price, quantity=1):
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })
        self.calculate_total()

    def calculate_total(self):
        self.total_amount = sum(
            item["price"] * item["quantity"] for item in self.items
        )
        return self.total_amount

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
