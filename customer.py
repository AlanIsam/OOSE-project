class Customer:
    def __init__(self, customer_id, name, phone=None):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone

    def __str__(self):
        return f"Customer({self.name})"
