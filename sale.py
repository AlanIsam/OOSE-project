from datetime import datetime
import uuid


class Sale:
    def __init__(self):
        self.sale_id = str(uuid.uuid4())
        self.date = datetime.now()
        self.items = []
        self.total_amount = 0.0
        self.status = "OPEN"
        self.payment = None

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

    def checkout(self, payment_method, amount):
        from payment import Payment

        payment = Payment(payment_method, amount)

        if payment.process(self.total_amount):
            self.payment = payment
            self.status = "PAID"
            return True
        else:
            return False
