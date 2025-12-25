# sale_line_item.py

class SaleLineItem:
    def __init__(self, item, quantity):
        self.item = item            # Item object
        self.quantity = quantity
        self.sub_total = self.calculateSubTotal()

    def calculateSubTotal(self):
        self.sub_total = self.item.price * self.quantity
        return self.sub_total

    def updateQuantity(self, quantity):
        self.quantity = quantity
        self.calculateSubTotal()

    def getItemName(self):
        return self.item.name
