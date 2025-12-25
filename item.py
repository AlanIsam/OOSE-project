class Item:
    def __init__(self, barcode, name, price, stock_quantity):
        self.barcode = barcode
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity

    def getPrice(self):
        return self.price
    
    def getDetails(self):
        return {
            "barcode": self.barcode,
            "name": self.name,
            "price": self.price,
            "stock_quantity": self.stock_quantity
        }
    
    def updateStock(self, quantity_change):
        self.stock_quantity += quantity_change
