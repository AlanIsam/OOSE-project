# sale_line_item.py

class SaleLineItem:
    def __init__(self, item_name, price, quantity):
        self.item_name = item_name
        self.price = price
        self.quantity = quantity
        self.sub_total = self.calculateSubTotal()

    def calculateSubTotal(self):
        self.sub_total = self.price * self.quantity
        return self.sub_total

    def updateQuantity(self, quantity):
        self.quantity = quantity
        self.calculateSubTotal()

    def getItemName(self):
        return self.item_name
