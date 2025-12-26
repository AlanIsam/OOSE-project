from catalogueSystem import BackendCatalogueSystem
from inventorySystem import InventorySystem
import uuid
import os


class Return:
    def __init__(self, original_receipt_id, catalogue):
        self.return_id = str(uuid.uuid4())
        self.originalreceiptID = original_receipt_id
        self.return_total = 0.0
        self.return_items = []
        self.catalogue = catalogue
        self.inventory = InventorySystem(catalogue)

    def verifyoriginalreceipt(self):
        # Verify if the original receipt exists by checking the receipt file
        filename = f"receipt_record/receipt_{self.originalreceiptID}.txt"
        return os.path.exists(filename)

    def view_receipt_items(self):
        # Display the list of items from the original receipt in table format
        filename = f"receipt_record/receipt_{self.originalreceiptID}.txt"
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
            
            print(f"\n Items from Receipt {self.originalreceiptID}:")
            print("-" * 70)
            print(f"{'Item Name':<15} {'Price':<8} {'Qty':<5} {'Total':<8}")
            print("-" * 70)
            
            grand_total = 0.0
            in_items_section = False
            
            for line in lines:
                line = line.strip()
                if line == "-------------------------":
                    in_items_section = not in_items_section
                    continue
                elif in_items_section and line and not line.startswith("TOTAL"):
                    # Parse the item line: "Apple x5 = RM 7.50"
                    if " x" in line and " = RM " in line:
                        try:
                            # Split by " x" to get item name and rest
                            name_part, rest = line.split(" x", 1)
                            # Split rest by " = RM " to get quantity and total price
                            qty_str, total_str = rest.split(" = RM ", 1)
                            
                            item_name = name_part.strip()
                            quantity = int(qty_str.strip())
                            total_price = float(total_str.strip())
                            item_price = total_price / quantity
                            
                            print(f"{item_name:<15} RM{item_price:<6.2f} {quantity:<5} RM{total_price:<6.2f}")
                            grand_total += total_price
                        except (ValueError, IndexError):
                            # If parsing fails, just print the original line
                            print(f"{line:<15}")
            
            print("-" * 70)
            print(f"{'TOTAL':<15} {'':<8} {'':<5} RM{grand_total:<6.2f}")
            print("-" * 70)
            return True
        except FileNotFoundError:
            print(" Receipt file not found.")
            return False
        except Exception as e:
            print(f" Error reading receipt: {e}")
            return False

    def additemtoreturn(self, item_name, quantity):
        # Add item to return list and update refund total
        item = self.catalogue.get_item_by_name(item_name)
        if item:
            self.return_items.append({"item": item, "quantity": quantity})
            self.return_total += item.getPrice() * quantity
            return True
        return False

    def process_return(self):
        # Process the return: update inventory (add back stock)
        for return_item in self.return_items:
            self.inventory.updatestock(return_item["item"].barcode, return_item["quantity"])
        # Optionally, record the return or generate return receipt
        print(f"Return processed. Refund ID: {self.return_id}, Total Refund: RM {self.return_total:.2f}")