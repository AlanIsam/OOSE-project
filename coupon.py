# coupon.py
from datetime import date, datetime


class Coupon:
    def __init__(self, coupon_code, discount_rate, valid_until):
        self.coupon_code = coupon_code
        self.discount_rate = discount_rate
        self.valid_until = valid_until
        self.used = False

    def isValid(self):
        if self.used:
            print("Coupon has already been used.")
            return False

        if date.today() > self.valid_until:
            print("Coupon has expired.")
            return False

        return True

    def calculateDiscount(self, amount):
        return amount * self.discount_rate

    def markAsUsed(self):
        self.used = True

    @classmethod
    def load_coupons_from_file(cls, filename="coupons.txt"):
        coupons = {}

        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    code, rate, expiry = line.split(",")
                    valid_until = datetime.strptime(expiry, "%Y-%m-%d").date()

                    coupons[code.upper()] = cls(
                        coupon_code=code.upper(),
                        discount_rate=float(rate),
                        valid_until=valid_until
                    )
        except FileNotFoundError:
            print("Coupon file not found.")

        return coupons
