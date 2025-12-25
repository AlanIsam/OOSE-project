# Administrator Dashboard

This POS system includes a comprehensive Administrator Dashboard for managing user accounts.

## Features

The Administrator class provides full CRUD (Create, Read, Update, Delete) operations for user management:

### 🔐 Unified Authentication System
- Single `User.login()` method for all user types
- Automatically returns appropriate user object (Cashier or Administrator) based on role
- Secure credential validation against employee database

### 📋 User Management Operations

1. **View Users (READ)**
   - Display all users in a formatted table
   - Shows User ID, Username, Password, and Role

2. **Create User (CREATE)**
   - Add new users to the system
   - Validates for duplicate User IDs
   - Supports both Cashier and Administrator roles

3. **Update User (UPDATE)**
   - Modify existing user information
   - Update username, password, and/or role
   - Partial updates supported (leave fields blank to keep current values)

4. **Delete User (DELETE)**
   - Remove users from the system
   - Includes confirmation prompt for safety

## Dashboard Interface

The `admin_dashboard()` method provides an interactive menu system with:
- Clear visual formatting with emojis and borders
- Input validation and error handling
- User-friendly prompts and confirmations
- Graceful exit handling

## Usage

```python
from user import User

# Login (works for both Cashier and Administrator)
user = User.login("username", "password")

# Check role and provide appropriate interface
if isinstance(user, Administrator):
    user.admin_dashboard()  # Admin gets dashboard access
else:
    # Cashier continues to POS system
    pass
```

## Test Script

Run `test_admin.py` to test the administrator functionality:

```bash
python test_admin.py
```

Use these credentials for testing:
- **Username:** `admin_user`
- **Password:** `adminpass`

## File Structure

- `user.py` - Base User class, Cashier subclass, and Administrator class with CRUD operations and dashboard
- `employee_list.txt` - User data storage
- `test_admin.py` - Test script for administrator functions

## Security Notes

- Passwords are stored in plain text (for educational purposes)
- In production, implement proper password hashing
- Add additional validation and logging as needed