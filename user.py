class User:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    def authenticate(self, username, password):
        return self.username == username and self.password == password

    def get_role(self):
        return self.role

    def __str__(self):
        return f"{self.role}({self.username})"
    
#subclass cashier
class Cashier(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password, role="Cashier")

    def handle_sale(self, sale):
        sale.process_sale()
        print(f"Sale {sale.sale_id} handled by {self.username}")

#subclass admin
class Administrator(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password, role="Administrator")

    def create_role(self, security_config, role_name):
        security_config.add_role(role_name)

    def assign_permissions(self, security_config, role_name, permissions):
        security_config.set_permissions(role_name, permissions)

    def remove_role(self, security_config, role_name):
        security_config.delete_role(role_name)

    def view_security_settings(self, security_config):
        return security_config.get_configuration()
