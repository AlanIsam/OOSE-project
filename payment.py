import uuid


class Payment:
    def __init__(self, payment_method, amount):
        self.payment_id = str(uuid.uuid4())
        self.payment_method = payment_method  # "cash", "card", "check"
        self.amount = amount
        self.payment_status = "PENDING"

    def process(self, total_amount):
        if self.payment_method == "cash":
            if self.amount < total_amount:
                self.payment_status = "FAILED"
                return False
            self.payment_status = "SUCCESS"
            return True

        elif self.payment_method in ["card", "check"]:
            # Assume always successful for simplicity
            self.payment_status = "SUCCESS"
            return True

        else:
            self.payment_status = "FAILED"
            return False
