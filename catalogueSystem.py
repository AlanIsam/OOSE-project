from item import Item


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
        # Case-insensitive search
        for item_name, item in self.name_to_item.items():
            if item_name.lower() == name.lower():
                return item
        return None

    def get_price(self, barcode):
        item = self.get_item(barcode)
        return item.getPrice() if item else None

    def get_details(self, barcode):
        return self.getItemDetail(barcode)

    def getItemDetail(self, barcode):
        item = self.get_item(barcode)
        return item.getDetails() if item else None

    def VerifyCoupon(self, coupon_code):
        # Placeholder for coupon verification
        # Assuming coupons are handled elsewhere, return False for now
        return False

    def recordTransaction(self, transaction_data):
        # Placeholder for recording transaction
        # Could log to a file or database
        print(f"Transaction recorded: {transaction_data}")
