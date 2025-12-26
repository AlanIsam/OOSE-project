from user import User


class Administrator(User):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password, role="Administrator")

    # Dashboard interface for administrator CRUD operations
    def admin_dashboard(self):

        print("\n" + "="*50)
        print("        ADMINISTRATOR DASHBOARD")
        print("="*50)
        print(f"Welcome, {self.username}!")
        print("Manage user accounts with CRUD operations")
        print("="*50)

        while True:
            print("\n--- User Management Options ---")
            print("1.  View All Users (READ)")
            print("2.  Create New User (CREATE)")
            print("3.  Update User Information (UPDATE)")
            print("4.  Delete User (DELETE)")
            print("5.  Logout (Return to Login)")
            print("-" * 30)

            try:
                choice = input("Enter your choice (1-5): ").strip()

                if choice == "1":
                    print("\n" + "─" * 40)
                    print("📋 VIEWING ALL USERS")
                    print("─" * 40)
                    self.viewUser()

                elif choice == "2":
                    print("\n" + "─" * 40)
                    print("➕ CREATING NEW USER")
                    print("─" * 40)
                    try:
                        user_id = int(input("Enter User ID: "))
                        username = input("Enter Username: ").strip()
                        password = input("Enter Password: ").strip()
                        role = input("Enter Role (Cashier/Administrator): ").strip()

                        if not username or not password or not role:
                            print(" Error: All fields are required!")
                            continue

                        if role not in ["Cashier", "Administrator"]:
                            print(" Error: Role must be 'Cashier' or 'Administrator'!")
                            continue

                        self.createUser(user_id, username, password, role)

                    except ValueError:
                        print(" Error: User ID must be a number!")

                elif choice == "3":
                    print("\n" + "─" * 40)
                    print("✏️  UPDATING USER INFORMATION")
                    print("─" * 40)
                    try:
                        user_id = int(input("Enter User ID to update: "))

                        print("Leave fields blank to keep current values:")
                        new_username = input("New username: ").strip() or None
                        new_password = input("New password: ").strip() or None
                        new_role = input("New role (Cashier/Administrator): ").strip() or None

                        if new_role and new_role not in ["Cashier", "Administrator"]:
                            print(" Error: Role must be 'Cashier' or 'Administrator'!")
                            continue

                        self.updateUser(user_id, new_username, new_password, new_role)

                    except ValueError:
                        print(" Error: User ID must be a number!")

                elif choice == "4":
                    print("\n" + "─" * 40)
                    print("🗑️  DELETING USER")
                    print("─" * 40)
                    try:
                        user_id = int(input("Enter User ID to delete: "))
                        confirm = input(f"⚠️  Are you sure you want to delete user {user_id}? (yes/no): ").lower().strip()

                        if confirm == "yes":
                            self.deleteUser(user_id)
                        else:
                            print(" Deletion cancelled.")

                    except ValueError:
                        print(" Error: User ID must be a number!")

                elif choice == "5":
                    print("\n" + "─" * 40)
                    print("🚪 LOGGING OUT - RETURNING TO LOGIN")
                    print("─" * 40)
                    print(f"Goodbye, {self.username}!")
                    return "logout"  # Return logout signal

                else:
                    print(" Invalid choice! Please enter a number between 1 and 5.")

            except KeyboardInterrupt:
                print("\n\n⚠️  Operation cancelled by user.")
                return "logout"  # Treat Ctrl+C as logout
            except Exception as e:
                print(f" An error occurred: {e}")

            input("\nPress Enter to continue...")

    # View user list in table form
    def viewUser(self):

        try:
            with open("employee_list.txt", "r") as file:
                users = file.readlines()

            if not users:
                print("No users found.")
                return

            print("User List:")
            print("-" * 60)
            print(f"{'User ID':<12} {'Username':<15} {'Password':<15} {'Role':<10}")
            print("-" * 60)

            for user in users:
                user = user.strip()
                if user:
                    parts = user.split(":")
                    if len(parts) == 4:
                        user_id, username, password, role = parts
                        print(f"{user_id:<12} {username:<15} {password:<15} {role:<10}")
            print("-" * 60)
        except FileNotFoundError:
            print("Employee list file not found.")
        except Exception as e:
            print(f"Error reading user list: {e}")

    # Create a new user
    def createUser(self, user_id, username, password, role):
        try:
            # Check if user_id already exists
            with open("employee_list.txt", "r") as file:
                users = file.readlines()

            for user in users:
                existing_id = user.split(":")[0]
                if existing_id == str(user_id):
                    print(f"User ID {user_id} already exists.")
                    return False

            # Add new user
            with open("employee_list.txt", "a") as file:
                file.write(f"{user_id}:{username}:{password}:{role}\n")

            print(f"User {username} created successfully.")
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    # Update user information
    def updateUser(self, user_id, new_username=None, new_password=None, new_role=None):

        try:
            with open("employee_list.txt", "r") as file:
                users = file.readlines()

            updated = False
            for i, user in enumerate(users):
                parts = user.strip().split(":")
                if len(parts) == 4 and parts[0] == str(user_id):
                    current_username, current_password, current_role = parts[1], parts[2], parts[3]

                    # Update fields if provided
                    if new_username:
                        current_username = new_username
                    if new_password:
                        current_password = new_password
                    if new_role:
                        current_role = new_role

                    users[i] = f"{user_id}:{current_username}:{current_password}:{current_role}\n"
                    updated = True
                    break

            if not updated:
                print(f"User ID {user_id} not found.")
                return False

            # Write back to file
            with open("employee_list.txt", "w") as file:
                file.writelines(users)

            print(f"User {user_id} updated successfully.")
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    # Delete an existing user
    def deleteUser(self, user_id):

        try:
            with open("employee_list.txt", "r") as file:
                users = file.readlines()

            original_count = len(users)
            users = [user for user in users if not user.startswith(str(user_id) + ":")]

            if len(users) == original_count:
                print(f"User ID {user_id} not found.")
                return False

            # Write back to file
            with open("employee_list.txt", "w") as file:
                file.writelines(users)

            print(f"User {user_id} deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
