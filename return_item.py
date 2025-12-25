from catalogueSystem import BackendCatalogueSystem
from inventorySystem import InventorySystem
import uuid
import os


class Return:
    def __init__(self, original_receipt_id, catalogue):
        self.refund_id = str(uuid.uuid4())
        self.originalreceiptID = original_receipt_id
        self.refundtotal = 0.0
        self.return_items = []
        self.catalogue = catalogue
        self.inventory = InventorySystem(catalogue)

    def verifyoriginalreceipt(self):
        # Verify if the original receipt exists by checking the receipt file
        filename = f"receipt_{self.originalreceiptID}.txt"
        return os.path.exists(filename)

    def additemtoreturn(self, item_name, quantity):
        # Add item to return list and update refund total
        item = self.catalogue.get_item_by_name(item_name)
        if item:
            self.return_items.append({"item": item, "quantity": quantity})
            self.refundtotal += item.getPrice() * quantity
            return True
        return False

    def process_return(self):
        # Process the return: update inventory (add back stock)
        for return_item in self.return_items:
            self.inventory.updatestock(return_item["item"].barcode, return_item["quantity"])
        # Optionally, record the return or generate return receipt
        print(f"Return processed. Refund ID: {self.refund_id}, Total Refund: RM {self.refundtotal:.2f}")