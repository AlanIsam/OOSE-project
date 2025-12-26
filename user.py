class User:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    def get_role(self):
        return self.role

    def __str__(self):
        return f"{self.role}({self.username})"

    @classmethod
    def authenticateUser(cls, username, password):
        # Authenticate user and return appropriate user object based on role
        try:
            with open("employee_list.txt", "r") as file:
                users = file.readlines()

            for user in users:
                user = user.strip()
                if user:
                    parts = user.split(":")
                    if len(parts) == 4:
                        user_id, file_username, file_password, role = parts
                        if file_username == username and file_password == password:
                            # Import here to avoid circular imports
                            if role == "Cashier":
                                from cashier import Cashier
                                print(f"Login successful! Welcome, {username} (Cashier)")
                                return Cashier(int(user_id), username, password)
                            elif role == "Administrator":
                                from administrator import Administrator
                                print(f"Login successful! Welcome, {username} (Administrator)")
                                return Administrator(int(user_id), username, password)

            print("Login failed! Invalid username or password.")
            return None
        except FileNotFoundError:
            print("Employee list file not found.")
            return None
    @classmethod
    def login_loop(cls):
        """Handle user login"""
        print("=== POS SYSTEM LOGIN ===")
        while True:
            username = input(" Enter username: ").strip()
            password = input(" Enter password: ").strip()
            user = cls.authenticateUser(username, password)

            if user:
                print(f"\n Welcome, {user}!\n")
                return user
            else:
                print("Login failed. Try again.\n")

    def logout(self):
        """Handle user logout"""
        print(f"\n Logging out {self.username}...\n")
        return "logout"



