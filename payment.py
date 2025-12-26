# payment.py
#Implemented by Alan Isam anak Recky
#103166
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


from datetime import datetime

class CardPayment(Payment):
    def __init__(self, amount):
        super().__init__(amount)
        self.card_number = None
        self.cvv = None
        self.expiry = None

    def validate(self):
        self.card_number = input("Enter card number (16 digits): ").strip()
        self.cvv = input("Enter CVV (3 digits): ").strip()
        self.expiry = input("Enter expiry date (YYYY-MM): ").strip()

        # Basic format checks
        if not (self.card_number.isdigit() and len(self.card_number) == 16):
            print(" Invalid card number format.")
            return False

        if not (self.cvv.isdigit() and len(self.cvv) == 3):
            print(" Invalid CVV format.")
            return False

        try:
            entered_expiry = datetime.strptime(self.expiry, "%Y-%m")
        except ValueError:
            print(" Invalid expiry date format.")
            return False

        # Load mock card database
        try:
            with open("cards.txt", "r") as file:
                for line in file:
                    card_no, file_cvv, file_expiry = line.strip().split(",")

                    if card_no == self.card_number:
                        # CVV check
                        if file_cvv != self.cvv:
                            print("CVV mismatch.")
                            return False

                        # Expiry check
                        card_expiry = datetime.strptime(file_expiry, "%Y-%m")
                        if card_expiry < datetime.now():
                            print("Card expired.")
                            return False

                        print(" Card authorized.")
                        return True

            print("Card not found.")
            return False

        except FileNotFoundError:
            print(" Card database not found.")
            return False


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
