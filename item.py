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

class BackendCatalogueSystem:
    def __init__(self):
        self.items = {}  # barcode to Item
        self.name_to_item = {}  # name to Item
        self.load_items()

    def load_items(self):
        try:
            with open('product_list.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(':')
                    if len(parts) == 4:
                        barcode, name, price, stock = parts
                        item = Item(barcode, name, float(price), int(stock))
                        self.items[barcode] = item
                        self.name_to_item[name] = item
        except FileNotFoundError:
            print("Product list file not found.")

    def get_item(self, barcode):
        return self.items.get(barcode)

    def get_item_by_name(self, name):
        return self.name_to_item.get(name)

    def get_price(self, barcode):
        item = self.get_item(barcode)
        return item.getPrice() if item else None

    def get_details(self, barcode):
        item = self.get_item(barcode)
        return item.getDetails() if item else None


class InventorySystem:
    def __init__(self, catalogue):
        self.catalogue = catalogue

    def update_stock(self, barcode, quantity_change):
        item = self.catalogue.get_item(barcode)
        if item:
            item.updateStock(quantity_change)
            self.save_inventory()

    def save_inventory(self):
        try:
            with open('product_list.txt', 'w') as f:
                for item in self.catalogue.items.values():
                    f.write(f"{item.barcode}:{item.name}:{item.price}:{item.stock_quantity}\n")
        except Exception as e:
            print(f"Error saving inventory: {e}")
