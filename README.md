# Club Cash System

A simple role-based cash management system written in Python with a GUI (Tkinter).


## About

- The system has three roles: Admin, Treasurer, Finance Officer
- Users and accounts are stored in CSV files
- Admin can create users and accounts
- Treasurer can perform financial operations
- Finance Officer can view accounts and transaction history


## Features

- Login system with role-based access
- Create users (admin only)
- Create accounts (admin only)
- Deposit, withdraw, and transfer money (treasurer)
- View accounts and transactions (finance officer)
- Transaction history tracking


## How to Run

- Make sure all project files are in the same folder
- Run the application: python main.py
- Login using existing credentials (default admin account is createt if no file exists)


## Requirements

- Python 3.13
- Tkinter (standart library)
- CSV module (standart library)


## Data Storage

- The system uses local CSV files:
    - users.csv - user accounts
    - accounts.csv - bank accounts
    - transactions.csv - transaction history


## Notes

- If files are missing, they will be created automatically on first run
- Restart may be required after first launch if files were just created


## Author

Daria Balashova
