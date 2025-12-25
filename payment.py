# payment.py
import uuid
from datetime import datetime


class Payment:
    def __init__(self, amount):
        self.payment_id = str(uuid.uuid4())
        self.amount = amount
        self.payment_date = datetime.now()
        self.status = "PENDING"

    def validate(self):
        return True

    def process_payment(self, total_amount):
        if self.amount < total_amount:
            self.status = "FAILED"
            return False

        if not self.validate():
            self.status = "FAILED"
            return False

        self.status = "SUCCESS"
        return True


class CashPayment(Payment):
    def __init__(self, amount):
        super().__init__(amount)

    def validate(self):
        return True


class CardPayment(Payment):
    def __init__(self, amount):
        super().__init__(amount)
        self.card_number = None

    def validate(self):
        self.card_number = input("Enter credit card number (16 digits): ").strip()

        if len(self.card_number) != 16 or not self.card_number.isdigit():
            print("Invalid card number.")
            return False

        print("Authorizing card...")
        return True


class CheckPayment(Payment):
    def __init__(self, amount):
        super().__init__(amount)
        self.check_number = None
        self.bank_name = None

    def validate(self):
        self.check_number = input("Enter check number: ").strip()
        self.bank_name = input("Enter bank name: ").strip()

        if not self.check_number or not self.bank_name:
            print("Invalid check details.")
            return False

        print("Verifying check with bank...")
        return True
