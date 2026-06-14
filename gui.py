import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from logic import SystemManager, User, Admin, Treasurer, FinanceOfficer


class ClubCashSystemApp:
    
    #--------------LOGIN/LOGOUT_LOAD_DATA-------------
    def __init__(self, root):

        self.root = root
        self.root.title("Club Cash System")
        self.root.geometry("500x300")

        self.load_data()

        self.open_login_window()
         
    # load data
    def load_data(self):
        try:
            self.users = SystemManager.load_users("users.csv")
        except FileNotFoundError:
            with open("users.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password", "Role"])
                writer.writerow(["admin", "admin", "admin"])

            self.users = SystemManager.load_users("users.csv")

        try:
            self.accounts = SystemManager.load_accounts("accounts.csv")
        except FileNotFoundError:
            with open("accounts.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Balance"])

            self.accounts = SystemManager.load_accounts("accounts.csv")

        if not os.path.exists("transactions.csv"):
            with open("transactions.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date","Type","Amount","Source","Target","Balance"])

    # login window
    def open_login_window(self):

        self.frame_login = tk.Frame(self.root)
        self.frame_login.pack()
        self.frame_login.pack(expand=True)

        tk.Label(self.frame_login,text="Club Cash System",font=("Arial", 16, "bold")).grid(column=0, row=0, columnspan=2, pady=15)
        
        tk.Label(self.frame_login, text="Username: ", font=('Arial', 10)).grid(column=0, row=1)
        self.entry_username = tk.Entry(self.frame_login)
        self.entry_username.grid(column=1, row=1)
        
        tk.Label(self.frame_login, text="Password: ", font=('Arial', 10)).grid(column=0, row=2)
        self.entry_password = tk.Entry(self.frame_login, show='*')
        self.entry_password.grid(column=1, row=2)
        

        self.login_button = tk.Button(
            self.frame_login, text="Login", font=('Arial', 10), activebackground="#ADD8E6", command=self.login
        )
        self.login_button.grid(column=1, row=3)

    # login
    def login(self):
        
        username = self.entry_username.get()
        password = self.entry_password.get()

        user = self.users.get(username)
        if user and user.password == password:
            messagebox.showinfo("Login Successful", f"Welcome, {user.role.capitalize()}!")
            self.current_user = self.users[username]  # Save current user's data
            self.open_dashboard(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # logout
    def logout(self):

        self.current_user = None

        self.clear_window()

        self.open_login_window()

    # clear window
    def clear_window(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

    # open window due to role
    def open_dashboard(self, user):

        self.clear_window()

        if user.role == 'admin':
            self.admin_dashboard()
        elif user.role == 'treasurer':
            self.treasurer_dashboard()
        elif user.role == 'finance_officer':
            self.finance_dashboard()

    #----------------------ADMIN----------------------
    def admin_dashboard(self):

        frame_admin = tk.Frame(self.root)
        frame_admin.pack()
        frame_admin.pack(expand=True)

        tk.Label(frame_admin, text=f"Admin Panel ({self.current_user.username})", font=('Arial', 14, 'bold')).pack(pady=10)
        tk.Button(frame_admin, text="Create new user", font=('Arial', 10), activebackground="#ADD8E6", command=self.open_create_user_window).pack(fill="x", padx=20, pady=5)
        tk.Button(frame_admin, text="Create new account", font=('Arial', 10), activebackground="#ADD8E6", command=self.open_create_account_window).pack(fill="x", padx=20, pady=5)

        tk.Button(frame_admin, text="Logout", font=('Arial', 10), activebackground="#ffcccc", command=self.logout).pack(fill="x", padx=20, pady=15)

    # create user
    def open_create_user_window(self):

        user_window = tk.Toplevel(self.root)
        user_window.title("Create New User")
        user_window.grab_set()

        frame = tk.Frame(user_window, padx=15, pady=15)
        frame.pack()

        tk.Label(frame,text="Create new user",font=('Arial', 14, 'bold')).grid(column=0, row=0, columnspan=2, pady=10)
        
        tk.Label(frame, text="Username:", font=('Arial', 10)).grid(column=0, row=1, sticky="w", pady=5)
        entry_new_username = tk.Entry(frame, width=25)
        entry_new_username.grid(column=1, row=1, pady=5)

        tk.Label(frame, text="Password:", font=('Arial', 10)).grid(column=0, row=2)
        entry_new_password = tk.Entry(frame, width=25, show="*")
        entry_new_password.grid(column=1, row=2, pady=5)

        tk.Label(frame, text="Role:", font=('Arial', 10)).grid(column=0, row=3, sticky="w", pady=5)
        role_var = tk.StringVar(value="treasurer")
        tk.OptionMenu(frame, role_var, "treasurer", "finance_officer").grid(column=1, row=3, pady=5, sticky="ew")


        def create_user():
            
            new_username = entry_new_username.get()
            new_password = entry_new_password.get()
            new_role = role_var.get()

            if new_username in self.users:
                messagebox.showerror("Error", "User already exists")
                return
            elif new_username == '' or new_password == '':
                messagebox.showerror("Error", "Enter new Username and Password")
                return

            new_user = self.current_user.create_user(new_username, new_password, new_role)
            self.users[new_username] = new_user
            SystemManager.save_users(self.users, "users.csv")
            messagebox.showinfo("Success", f"User {new_username} created successfully")
            frame.destroy()

        tk.Button(frame, text="Create", command=create_user).grid(column=0,row=4,columnspan=2,pady=10,sticky="ew")

    # create account
    def open_create_account_window(self):

        account_window = tk.Toplevel(self.root)
        account_window.title("Create New Account")
        account_window.grab_set()

        frame = tk.Frame(account_window, padx=15, pady=15)
        frame.pack()

        tk.Label(frame, text="Create new account", font=('Arial', 14, 'bold')).grid(column=0, row=0, columnspan=2, pady=10)
    
        tk.Label(frame, text="Name:", font=('Arial', 10)).grid(column=0, row=1, sticky="w", pady=5)
        entry_new_accountname = tk.Entry(frame, width=25)
        entry_new_accountname.grid(column=1, row=1, pady=5)
    
    
        def create_account():

            new_accountname = entry_new_accountname.get()
    
            if any(account.name == new_accountname for account in self.accounts):
                messagebox.showerror("Error", "Account already exists")
                return
            elif new_accountname == '' or ' ' in new_accountname:
                messagebox.showerror("Error", "Enter account's name and don't use space")
                return
            
            new_account = self.current_user.create_account(new_accountname)
            self.accounts.append(new_account)
            SystemManager.save_accounts(self.accounts, "accounts.csv")
            messagebox.showinfo("Success", f"Account {new_accountname} created successfully")
            frame.destroy()
    
        tk.Button(frame, text="Create", font=('Arial', 10), activebackground="#ADD8E6", command=create_account).grid(column=0,row=3,columnspan=2,sticky="ew",pady=10)

    #--------------------TREASURER--------------------
    def treasurer_dashboard(self):
        
        frame_treasurer = tk.Frame(self.root)
        frame_treasurer.pack(expand=True, padx=20, pady=20)

        tk.Label(frame_treasurer, text=f"Treasurer ({self.current_user.username})", font=('Arial', 14, 'bold')).grid(column=0, row=0, columnspan=2, pady=10)

        tk.Button(frame_treasurer, text="Deposit", font=('Arial', 10), activebackground="#ADD8E6", command=self.open_deposit_window).grid(column=0, row=1, columnspan=2, sticky="ew", pady=5)
        tk.Button(frame_treasurer, text="Withdraw", font=('Arial', 10), activebackground="#ADD8E6", command=self.open_withdraw_window).grid(column=0, row=2, columnspan=2, sticky="ew", pady=5)
        tk.Button(frame_treasurer, text="Transfer", font=('Arial', 10), activebackground="#ADD8E6", command=self.open_transfer_window).grid(column=0, row=3, columnspan=2, sticky="ew", pady=5)
        tk.Button(frame_treasurer, text="Transactions History", font=('Arial', 10), activebackground="#ADD8E6", command=self.open_transactions_history_window).grid(column=0, row=4, columnspan=2, sticky="ew", pady=5)
        tk.Button(frame_treasurer, text="Logout", font=('Arial', 10), activebackground="#ffcccc", command=self.logout).grid(column=0, row=5, columnspan=2, sticky="ew", pady=15)

    # deposit
    def open_deposit_window(self):

        accounts = SystemManager.load_accounts("accounts.csv")
        account_names = [account.name for account in accounts]

        if not account_names:
            messagebox.showerror("Error", "No accounts available!")
            return
        
        deposit_window = tk.Toplevel(self.root)
        deposit_window.title("Deposit transaction")
        deposit_window.grab_set()

        frame = tk.Frame(deposit_window, padx=15, pady=15)
        frame.pack()

        tk.Label(frame, text="Select Account: ").grid(column=0, row=0, sticky="w", pady=5)
        selected_account = tk.StringVar(value=account_names[0])
        tk.OptionMenu(frame, selected_account, *account_names).grid(column=1, row=0, sticky="ew", pady=5)

        tk.Label(frame, text="Deposit Amount: ").grid(column=0, row=1, sticky="w", pady=5)
        entry_amount = tk.Entry(frame)
        entry_amount.grid(column=1, row=1, pady=5)

        tk.Label(frame, text="From: ").grid(column=0, row=2, sticky="w", pady=5)
        entry_source = tk.Entry(frame)
        entry_source.grid(column=1, row=2, pady=5)


        def make_deposit():
            
            account_name = selected_account.get()
            source = entry_source.get()
            try:
                amount = float(entry_amount.get())
                
                if amount < 0:
                    messagebox.showerror("Error", "Amount should be positive")
                    return
                
                account = next((acc for acc in accounts if acc.name == account_name), None)

                account.transactions = SystemManager.load_transactions("transactions.csv")
                account.deposit(amount, source)

                messagebox.showinfo("Success", f"Deposited {amount} to {account_name}")
                frame.destroy()

                SystemManager.save_accounts(accounts, "accounts.csv")
                SystemManager.save_transactions(account, "transactions.csv")

            except ValueError as e:
                messagebox.showerror("Error", "Enter amount using digits")

        tk.Button(frame, text="Enter", font=('Arial', 10), activebackground="#ADD8E6", command=make_deposit).grid(column=0, row=3, columnspan=2, sticky="ew", pady=10)

    # withdraw
    def open_withdraw_window(self):

        accounts = SystemManager.load_accounts("accounts.csv")
        account_names = [account.name for account in accounts]

        if not account_names:
            messagebox.showerror("Error", "No accounts available!")
            return
        
        withdraw_window = tk.Toplevel(self.root)
        withdraw_window.title("Withdraw transaction")
        withdraw_window.grab_set()

        frame = tk.Frame(withdraw_window, padx=15, pady=15)
        frame.pack()

        tk.Label(frame, text="Select Account: ").grid(column=0, row=0, sticky="w", pady=5)
        selected_account = tk.StringVar(value=account_names[0])
        tk.OptionMenu(frame, selected_account, *account_names).grid(column=1, row=0, sticky="ew",pady=5)

        tk.Label(frame, text="Withdraw Amount: ").grid(column=0, row=1, sticky="w",pady=5)
        entry_amount = tk.Entry(frame)
        entry_amount.grid(column=1, row=1, pady=5)


        def make_withdraw():
            
            account_name = selected_account.get()
            try:
                amount = float(entry_amount.get())
                
                account = next((acc for acc in accounts if acc.name == account_name), None)
                
                if amount < 0:
                    messagebox.showerror("Error", "Amount should be positive")
                    return
                elif amount > account.balance:
                    messagebox.showerror("Error", "Insufficient funds in the account")
                    return

                account.transactions = SystemManager.load_transactions("transactions.csv")
                account.withdraw(amount, "Treasurer")

                messagebox.showinfo("Success", f"Withdrew {amount} from {account_name}")
                frame.destroy()

                SystemManager.save_accounts(accounts, "accounts.csv")
                SystemManager.save_transactions(account, "transactions.csv")
                
            except ValueError as e:
                messagebox.showerror("Error", "Enter amount using digits")

        tk.Button(frame, text="Enter", font=('Arial', 10), activebackground="#ADD8E6", command=make_withdraw).grid(column=0, row=2, columnspan=2, sticky="ew", pady=10)

    # transfer
    def open_transfer_window(self):
        
        accounts = SystemManager.load_accounts("accounts.csv")
        account_names = [account.name for account in accounts]

        if not account_names:
            messagebox.showerror("Error", "No accounts available!")
            return
        elif len(account_names) < 2:
            messagebox.showerror("Error", "Only one account exists. Transfer is not posible")
            return
        
        transfer_window = tk.Toplevel(self.root)
        transfer_window.title("Transfer transaction")
        transfer_window.grab_set()

        frame = tk.Frame(transfer_window, padx=15, pady=15)
        frame.pack()

        tk.Label(frame, text="From: ").grid(column=0, row=0, sticky="w", pady=5)
        selected_source = tk.StringVar(value=account_names[0])
        tk.OptionMenu(frame, selected_source, *account_names).grid(column=1, row=0, sticky="ew", pady=5)

        tk.Label(frame, text="To: ").grid(column=0, row=1, sticky="w", pady=5)
        selected_target = tk.StringVar(value=account_names[0])
        tk.OptionMenu(frame, selected_target, *account_names).grid(column=1, row=1, sticky="ew", pady=5)

        tk.Label(frame, text="Transfer Amount: ").grid(column=0, row=2, sticky="w", pady=5)
        entry_amount = tk.Entry(frame)
        entry_amount.grid(column=1, row=2, pady=5)


        def make_transfer():
            
            target_account_name = selected_target.get()
            source_account_name = selected_source.get()
            try:
                amount = float(entry_amount.get())
                if amount < 0:
                    messagebox.showerror("Error", "Amount should be positive")
                    return
                
                target_account = next((acc for acc in accounts if acc.name == target_account_name), None)
                source_account = next((acc for acc in accounts if acc.name == source_account_name), None)
                
                source_account.transactions = SystemManager.load_transactions("transactions.csv")
                source_account.transfer(amount, target_account)

                messagebox.showinfo("Success", f"Transferred {amount} from {source_account_name} to {target_account_name}")
                frame.destroy()
                
                SystemManager.save_accounts(accounts, "accounts.csv")
                SystemManager.save_transactions(source_account, "transactions.csv")
            except ValueError as e:
                messagebox.showerror("Error", "Enter amount using digits")

        tk.Button(frame, text="Enter", font=('Arial', 10), activebackground="#ADD8E6", command=make_transfer).grid(column=0, row=3, columnspan=2, sticky="ew", pady=10)

    # transactions history (for treasurer and finance)
    def open_transactions_history_window(self):
        
        transactions_history_window = tk.Toplevel(self.root)
        transactions_history_window.title("Transactions History")
        transactions_history_window.grab_set()
        transactions_history_window.geometry("800x400")

        frame = tk.Frame(transactions_history_window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)


        transactions = SystemManager.load_transactions("transactions.csv")
        if not transactions:
            tk.Label(frame, text="No transactions found").pack()
            return

        columns = list(transactions[0].keys())

        
        table = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=120, anchor="center")

        for row in transactions:
            values = [row[col] for col in columns]
            table.insert("", tk.END, values=values)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)

        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    #-----------------FINANCE_OFFICER-----------------
    def finance_dashboard(self):
        
        frame_finance = tk.Frame(self.root)
        frame_finance.pack(expand=True)

        tk.Label(frame_finance, text=f"Finance Officer ({self.current_user.username})", font=('Arial', 14, 'bold')).grid(column=0, row=0, columnspan=2, pady=10)

        tk.Button(frame_finance, text="Transactions History", font=('Arial', 10), activebackground="#ADD8E6", command=self.open_transactions_history_window).grid(column=0, row=2, columnspan=2, sticky="ew", padx=20, pady=5)
        tk.Button(frame_finance, text="Show accounts info", font=('Arial', 10), activebackground="#ADD8E6", command=self.show_accounts_info).grid(column=0, row=3, columnspan=2, sticky="ew", padx=20, pady=5)
        tk.Button(frame_finance, text="Logout", font=('Arial', 10), activebackground="#ffcccc", command=self.logout).grid(column=0, row=4, columnspan=2, sticky="ew", padx=20, pady=15)
        
        total_balance = sum(account.balance for account in SystemManager.load_accounts("accounts.csv"))

        tk.Label(frame_finance, text=f"Total Balance: {total_balance}", font=('Arial', 12)).grid(column=0, row=1, columnspan=2, pady=5)

    # acconnts info
    def show_accounts_info(self):
        
        accounts_info_window = tk.Toplevel(self.root)
        accounts_info_window.title("Accounts Info")
        accounts_info_window.grab_set()
        accounts_info_window.geometry("350x300")

        frame = tk.Frame(accounts_info_window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        accounts = SystemManager.load_accounts("accounts.csv")
        if not accounts:
            tk.Label(frame, text="No accounts found").pack()
            return

        columns = ("Name", "Balance")
        table = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        table.heading("Name", text="Account Name")
        table.heading("Balance", text="Balance")

        table.column("Name", anchor="center", width=180)
        table.column("Balance", anchor="center", width=120)

        for account in accounts:
            table.insert("", tk.END, values=(account.name, account.balance))

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)

        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")