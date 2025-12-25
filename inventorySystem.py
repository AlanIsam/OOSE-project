from catalogueSystem import BackendCatalogueSystem


class InventorySystem:
    def __init__(self, catalogue):
        self.catalogue = catalogue

    def checkstock(self, barcode):
        item = self.catalogue.get_item(barcode)
        return item.stock_quantity if item else None

    def updatestock(self, barcode, quantity_change):
        item = self.catalogue.get_item(barcode)
        if item:
            item.updateStock(quantity_change)
            self.save_inventory()

    def restockitem(self, barcode, quantity):
        self.updatestock(barcode, quantity)

    def save_inventory(self):
        try:
            with open('product_list.txt', 'w') as f:
                for item in self.catalogue.items.values():
                    f.write(f"{item.barcode}:{item.name}:{item.price}:{item.stock_quantity}\n")
        except Exception as e:
            print(f"Error saving inventory: {e}")
